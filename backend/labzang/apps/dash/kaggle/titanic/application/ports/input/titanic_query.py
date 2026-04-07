from __future__ import annotations

from typing import Protocol

from labzang.apps.data.kaggle.titanic.application.dtos.titanic_eda_dto import (
    TitanicEdaDashboardDTO,
)


class TitanicQueryPort(Protocol):
    """타이타닉 EDA·조회 유스케이스."""

    def get_eda_dashboard(self) -> TitanicEdaDashboardDTO:
        """대시보드 차트용 집계 JSON (DB 우선, 실패 시 번들 train.csv)."""
        ...
