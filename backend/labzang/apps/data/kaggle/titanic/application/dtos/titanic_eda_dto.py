"""EDA 대시보드용 집계 결과 (프론트에서 차트만 그리면 되도록 JSON 직렬화 가능한 구조)."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class TitanicEdaDashboardDTO(BaseModel):
    """원본 승객(train) 기준 탐색적 분석 데이터."""

    source: Literal["database", "fallback_csv"] = Field(
        ...,
        description="집계에 사용한 데이터 출처",
    )
    row_count: int = Field(..., ge=0)
    missing_values: dict[str, int] = Field(
        default_factory=dict,
        description="컬럼별 결측 개수",
    )
    survival_ratio: dict[str, int] = Field(
        default_factory=dict,
        description="생존·사망 건수 (예: survived, dead)",
    )
    sex_analysis: dict[str, Any] = Field(default_factory=dict)
    pclass_analysis: dict[str, Any] = Field(default_factory=dict)
    age_stats: dict[str, Any] = Field(default_factory=dict)
    family_stats: dict[str, Any] = Field(default_factory=dict)
    embarked_stats: dict[str, Any] = Field(default_factory=dict)
    fare_stats: dict[str, Any] = Field(default_factory=dict)
    feature_table_summary: dict[str, Any] | None = Field(
        default=None,
        description="titanic_passenger_features(train) 요약 (DB 연결 시)",
    )
