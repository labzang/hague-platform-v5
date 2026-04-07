from __future__ import annotations

import logging

from labzang.apps.dash.kaggle.titanic.application.dtos.titanic_row_dto import (
    TitanicPreprocessPipelineResultDTO,
    TitanicRowDTO,
)
from labzang.apps.dash.kaggle.titanic.application.ports.output.titanic_feature_repository import (
    TitanicFeatureRepositoryPort,
)
from labzang.apps.dash.kaggle.titanic.application.ports.output.titanic_repository import (
    TitanicPassengerRepositoryPort,
)
from labzang.apps.dash.kaggle.titanic.application.services.titanic_preprocess_service import (
    TitanicPreprocessService,
    dataframe_from_dto_rows,
    dataframe_preview_records,
    dataframe_to_feature_dtos,
    train_test_from_dtos,
)

logger = logging.getLogger(__name__)


class TitanicCommandImpl:
    """배치 DTO 수신 → 전처리 → 원본·특성 테이블 upsert."""

    def __init__(
        self,
        repository: TitanicPassengerRepositoryPort,
        feature_repository: TitanicFeatureRepositoryPort,
        preprocess_service: TitanicPreprocessService | None = None,
    ) -> None:
        self._repository = repository
        self._feature_repository = feature_repository
        self._preprocess = preprocess_service or TitanicPreprocessService()

    def ingest_train_batch(
        self,
        train_rows: list[TitanicRowDTO],
        test_rows: list[TitanicRowDTO] | None = None,
    ) -> TitanicPreprocessPipelineResultDTO:
        if not train_rows:
            raise ValueError("train_rows가 비어 있습니다.")

        train_fixed = [r.model_copy(update={"DatasetSplit": "train"}) for r in train_rows]
        if any(r.Survived is None for r in train_fixed):
            raise ValueError("train 배치의 모든 행에 Survived가 필요합니다.")

        test_fixed: list[TitanicRowDTO] | None = None
        if test_rows:
            test_fixed = [r.model_copy(update={"DatasetSplit": "test"}) for r in test_rows]

        train_df, test_df = train_test_from_dtos(train_fixed, test_fixed)
        train_out, test_out = self._preprocess.run(train_df, test_df)

        raw_to_store = list(train_fixed)
        if test_fixed:
            raw_to_store.extend(test_fixed)

        persisted = 0
        persist_note: str | None = None
        try:
            persisted = self._repository.upsert_passengers(raw_to_store)
        except Exception as e:
            logger.warning("titanic_passengers upsert 생략/실패: %s", e)
            persist_note = str(e)

        feature_rows = dataframe_to_feature_dtos(train_out, "train")
        feature_rows.extend(dataframe_to_feature_dtos(test_out, "test"))

        features_persisted = 0
        features_persist_note: str | None = None
        try:
            features_persisted = self._feature_repository.upsert_features(feature_rows)
        except Exception as e:
            logger.warning("titanic_passenger_features upsert 생략/실패: %s", e)
            features_persist_note = str(e)

        return TitanicPreprocessPipelineResultDTO(
            persisted_count=persisted,
            persist_note=persist_note,
            features_persisted_count=features_persisted,
            features_persist_note=features_persist_note,
            processed_train_rows=len(train_out),
            processed_test_rows=len(test_out),
            feature_columns=list(train_out.columns),
            train_preview=dataframe_preview_records(train_out, 5),
            test_preview=dataframe_preview_records(test_out, 5),
        )

    def ingest_test_batch(self, test_rows: list[TitanicRowDTO]) -> TitanicPreprocessPipelineResultDTO:
        if not test_rows:
            raise ValueError("test_rows가 비어 있습니다.")

        test_fixed = [r.model_copy(update={"DatasetSplit": "test"}) for r in test_rows]
        test_df = dataframe_from_dto_rows(test_fixed)
        test_out = self._preprocess.run_single_split(test_df, split="test")

        persisted = 0
        persist_note: str | None = None
        try:
            persisted = self._repository.upsert_passengers(test_fixed)
        except Exception as e:
            logger.warning("titanic_passengers upsert 생략/실패: %s", e)
            persist_note = str(e)

        feature_rows = dataframe_to_feature_dtos(test_out, "test")
        features_persisted = 0
        features_persist_note: str | None = None
        try:
            features_persisted = self._feature_repository.upsert_features(feature_rows)
        except Exception as e:
            logger.warning("titanic_passenger_features upsert 생략/실패: %s", e)
            features_persist_note = str(e)

        return TitanicPreprocessPipelineResultDTO(
            persisted_count=persisted,
            persist_note=persist_note,
            features_persisted_count=features_persisted,
            features_persist_note=features_persist_note,
            processed_train_rows=0,
            processed_test_rows=len(test_out),
            feature_columns=list(test_out.columns),
            train_preview=[],
            test_preview=dataframe_preview_records(test_out, 5),
        )
