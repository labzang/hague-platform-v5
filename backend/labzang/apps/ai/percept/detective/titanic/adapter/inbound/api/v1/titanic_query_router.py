"""타이타닉 EDA 대시보드용 JSON API (프론트에서 차트 렌더링)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from labzang.apps.dash.kaggle.titanic.adapter.inbound.dependencies import (
    get_titanic_query_impl,
)
from labzang.apps.dash.kaggle.titanic.application.ports.input.titanic_query import (
    TitanicQueryPort,
)
from labzang.shared import create_response

router = APIRouter(tags=["titanic-query"])


@router.get(
    "/eda/dashboard",
    summary="EDA 대시보드 집계 JSON",
)
async def get_eda_dashboard(
    query: TitanicQueryPort = Depends(get_titanic_query_impl),
):
    """
    결측·생존비·성별·객실등급·나이·가족·승선항·요금 등 차트용 집계.
    DB(`titanic_passengers`, `titanic_passenger_features`)가 비어 있거나 연결 실패 시
    번들 `resources/train.csv`로 대체한다.
    """
    dto = query.get_eda_dashboard()
    return create_response(
        data=jsonable_encoder(dto.model_dump(mode="python")),
        message="EDA dashboard data",
    )
