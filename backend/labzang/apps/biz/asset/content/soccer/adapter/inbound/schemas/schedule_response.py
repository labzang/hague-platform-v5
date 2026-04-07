# -*- coding: utf-8 -*-
"""Inbound response schemas — JSON for clients from schedule `find_by_id` / list results."""

from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from labzang.apps.biz.asset.content.soccer.application.dtos.schedule_dto import ScheduleDTO


class ScheduleResponse(BaseModel):
    """단일 일정 페이로드 — 허브 `ScheduleDTO`(dataclass)와 정렬."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1000,
                "stadium_id": 1011,
                "hometeam_id": 1011,
                "awayteam_id": 1008,
                "stadium_code": "C02",
                "sche_date": "20120501",
                "gubun": "Y",
                "hometeam_code": "K06",
                "awayteam_code": "K10",
                "home_score": 2,
                "away_score": 0,
            }
        }
    )

    id: int = Field(..., gt=0, description="Schedule primary key")
    stadium_id: Optional[int] = Field(default=None, gt=0)
    hometeam_id: Optional[int] = Field(default=None, gt=0)
    awayteam_id: Optional[int] = Field(default=None, gt=0)
    stadium_code: Optional[str] = Field(default=None, max_length=10)
    sche_date: Optional[str] = Field(default=None, max_length=10)
    gubun: Optional[str] = Field(default=None, max_length=5)
    hometeam_code: Optional[str] = Field(default=None, max_length=10)
    awayteam_code: Optional[str] = Field(default=None, max_length=10)
    home_score: Optional[int] = Field(default=None, ge=0)
    away_score: Optional[int] = Field(default=None, ge=0)
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None
    embedding_created_at: Optional[datetime] = None

    @classmethod
    def from_schedule_dto(cls, dto: ScheduleDTO) -> ScheduleResponse:
        return cls(
            id=dto.id,
            stadium_id=dto.stadium_id,
            hometeam_id=dto.hometeam_id,
            awayteam_id=dto.awayteam_id,
            stadium_code=dto.stadium_code,
            sche_date=dto.sche_date,
            gubun=dto.gubun,
            hometeam_code=dto.hometeam_code,
            awayteam_code=dto.awayteam_code,
            home_score=dto.home_score,
            away_score=dto.away_score,
            embedding_content=dto.embedding_content,
            embedding=dto.embedding,
            embedding_created_at=dto.embedding_created_at,
        )

    def to_json_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


__all__ = ["ScheduleResponse"]
