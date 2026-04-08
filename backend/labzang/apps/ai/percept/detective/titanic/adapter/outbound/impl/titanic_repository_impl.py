from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from labzang.apps.ai.percept.detective.titanic.adapter.outbound.orm.titanic_feature_orm import (
    TitanicFeatureORM,
)
from labzang.apps.ai.percept.detective.titanic.adapter.outbound.orm.titanic_orm import TitanicORM
from labzang.apps.ai.percept.detective.titanic.app.dtos.titanic_feature_row_dto import (
    TitanicFeatureRowDTO,
)
from labzang.apps.ai.percept.detective.titanic.app.dtos.titanic_row_dto import TitanicRowDTO
from labzang.apps.ai.percept.detective.titanic.app.ports.output.titanic_repository_port import (
    TitanicFeatureRepositoryPort,
    TitanicPassengerRepositoryPort,
)

logger = logging.getLogger(__name__)


class TitanicPassengerRepositoryImpl(TitanicPassengerRepositoryPort):
    """`titanic_passengers` 테이블에 승객 행 merge upsert (Neon = Postgres `DATABASE_URL`)."""

    def __init__(
        self,
        session_factory: Callable[[], Session] | None = None,
    ) -> None:
        if session_factory is None:
            from labzang.core.database import SessionLocal

            self._session_factory: Callable[[], Session] = SessionLocal
        else:
            self._session_factory = session_factory

    def upsert_passengers(self, rows: Sequence[TitanicRowDTO]) -> int:
        session = self._session_factory()
        n = 0
        try:
            for row in rows:
                orm = TitanicORM(
                    passenger_id=row.PassengerId,
                    dataset_split=row.DatasetSplit,
                    survived=row.Survived,
                    pclass=row.Pclass,
                    name=row.Name,
                    gender=row.Gender,
                    age=row.Age,
                    sibsp=row.SibSp,
                    parch=row.Parch,
                    ticket=row.Ticket,
                    fare=row.Fare,
                    cabin=row.Cabin,
                    embarked=row.Embarked,
                )
                session.merge(orm)
                n += 1
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.warning("Titanic ORM upsert 실패: %s", e)
            raise RuntimeError(
                "데이터베이스에 저장하지 못했습니다. DATABASE_URL(Neon)과 테이블 생성 여부를 확인하세요."
            ) from e
        finally:
            session.close()
        return n


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
