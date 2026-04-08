"""타이타닉 EDA 대시보드용 JSON API (프론트에서 차트 렌더링)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from labzang.apps.ai.percept.detective.santander.application.dtos.titanic_dto import (
    EvaluationResult,
)
from labzang.apps.ai.percept.detective.titanic.app.ports.input.titanic_query import (
    TitanicEvaluatePort,
)
from labzang.apps.ai.percept.detective.titanic.adapter.inbound.dependencies import (
    get_evaluate_titanic_use_case,
    get_titanic_query_impl,
)
from labzang.shared import create_response

router = APIRouter(tags=["titanic-query"])


@router.get("/")
async def titanic_hex_root():
    """헥사고날 타이타닉 서비스 루트."""
    return create_response(
        data={
            "service": "mlservice",
            "module": "titanic-hex",
            "architecture": "hexagonal",
            "status": "running",
        },
        message="Titanic Hexagonal API is running",
    )


@router.get("/evaluate")
async def evaluate(
    use_case: TitanicEvaluatePort = Depends(get_evaluate_titanic_use_case),
):
    """모델 평가 실행 (유스케이스)."""
    try:
        result = use_case.execute()
        if not isinstance(result, EvaluationResult):
            raise HTTPException(
                status_code=500,
                detail=f"평가 결과 타입 오류: {type(result).__name__}",
            )
        return create_response(
            data={
                "best_model": result.best_model,
                "results": result.results,
            },
            message="모델 평가가 완료되었습니다",
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/eda/dashboard",
    summary="EDA 대시보드 집계 JSON",
)
async def get_eda_dashboard(
    query: Any = Depends(get_titanic_query_impl),
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
