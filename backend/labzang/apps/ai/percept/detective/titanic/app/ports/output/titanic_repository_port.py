from __future__ import annotations

from typing import Protocol, Sequence

from labzang.apps.ai.percept.detective.titanic.app.dtos.titanic_feature_row_dto import (
    TitanicFeatureRowDTO,
)
from labzang.apps.ai.percept.detective.titanic.app.dtos.titanic_row_dto import (
    TitanicRowDTO,
)


class TitanicPassengerRepositoryPort(Protocol):
    """원시 승객 행(Postgres/Neon `titanic_passengers`) upsert."""

    def upsert_passengers(self, rows: Sequence[TitanicRowDTO]) -> int:
        """저장(merge)된 행 수. 연결 실패 시 예외를 던질 수 있음."""
        ...


class TitanicFeatureRepositoryPort(Protocol):
    """`titanic_passenger_features` upsert."""

    def upsert_features(self, rows: Sequence[TitanicFeatureRowDTO]) -> int:
        ...
