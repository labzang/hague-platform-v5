from __future__ import annotations

from typing import Protocol

from labzang.apps.data.kaggle.titanic.application.dtos.titanic_row_dto import (
    TitanicPreprocessPipelineResultDTO,
    TitanicRowDTO,
)


class TitanicCommandPort(Protocol):
    """train/test 배치 수신 → DTO 정합 → 전처리 → (Neon/Postgres) 저장."""

    def ingest_train_batch(
        self,
        train_rows: list[TitanicRowDTO],
        test_rows: list[TitanicRowDTO] | None = None,
    ) -> TitanicPreprocessPipelineResultDTO:
        ...

    def ingest_test_batch(self, test_rows: list[TitanicRowDTO]) -> TitanicPreprocessPipelineResultDTO:
        ...
