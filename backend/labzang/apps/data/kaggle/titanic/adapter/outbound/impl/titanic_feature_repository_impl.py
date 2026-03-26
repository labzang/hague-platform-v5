from __future__ import annotations

import logging
from collections.abc import Callable, Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from labzang.apps.data.kaggle.titanic.adapter.outbound.orm.titanic_feature_orm import (
    TitanicFeatureORM,
)
from labzang.apps.data.kaggle.titanic.application.dtos.titanic_feature_row_dto import (
    TitanicFeatureRowDTO,
)
from labzang.apps.data.kaggle.titanic.application.ports.output.titanic_feature_repository import (
    TitanicFeatureRepositoryPort,
)

logger = logging.getLogger(__name__)


class TitanicFeatureRepositoryImpl(TitanicFeatureRepositoryPort):
    def __init__(
        self,
        session_factory: Callable[[], Session] | None = None,
    ) -> None:
        if session_factory is None:
            from labzang.core.database import SessionLocal

            self._session_factory: Callable[[], Session] = SessionLocal
        else:
            self._session_factory = session_factory

    def upsert_features(self, rows: Sequence[TitanicFeatureRowDTO]) -> int:
        session = self._session_factory()
        n = 0
        try:
            for row in rows:
                orm = TitanicFeatureORM(
                    passenger_id=row.PassengerId,
                    dataset_split=row.DatasetSplit,
                    pclass=row.Pclass,
                    embarked=row.Embarked,
                    title=row.Title,
                    gender=row.Gender,
                    age_group=row.AgeGroup,
                    fare_band=row.FareBand,
                )
                session.merge(orm)
                n += 1
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.warning("Titanic feature ORM upsert 실패: %s", e)
            raise RuntimeError(
                "특성 테이블에 저장하지 못했습니다. DATABASE_URL과 마이그레이션을 확인하세요."
            ) from e
        finally:
            session.close()
        return n
