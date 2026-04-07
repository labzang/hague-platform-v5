"""Application DTOs — 유스케이스/포트 간 데이터 전달. 도메인 VO와 분리."""

from labzang.apps.dash.kaggle.santander.application.dtos.titanic_dto import (
    EvaluationResult,
    PreprocessResult,
    TitanicDatasetDTO,
    TitanicRowDTO,
)

__all__ = [
    "EvaluationResult",
    "PreprocessResult",
    "TitanicDatasetDTO",
    "TitanicRowDTO",
]
