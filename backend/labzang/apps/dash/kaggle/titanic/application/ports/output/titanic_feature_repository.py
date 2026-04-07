from __future__ import annotations

from typing import Protocol, Sequence

from labzang.apps.data.kaggle.titanic.application.dtos.titanic_feature_row_dto import (
    TitanicFeatureRowDTO,
)


class TitanicFeatureRepositoryPort(Protocol):
    """`titanic_passenger_features` upsert."""

    def upsert_features(self, rows: Sequence[TitanicFeatureRowDTO]) -> int:
        ...
