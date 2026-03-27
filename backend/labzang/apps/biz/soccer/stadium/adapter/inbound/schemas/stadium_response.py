# -*- coding: utf-8 -*-
"""Inbound response schemas — JSON for clients from stadium `find_by_id` / list results."""

from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from labzang.apps.biz.soccer.stadium.application.dtos.stadium_dto import StadiumDTO as HubStadiumDTO


class StadiumResponse(BaseModel):
    """단일 경기장 페이로드 — 허브 `StadiumDTO`(dataclass)와 정렬."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1011,
                "stadium_code": "C02",
                "stadium_name": "부산아시아드경기장",
                "hometeam_code": "K06",
                "seat_count": 30000,
            }
        }
    )

    id: int = Field(..., gt=0, description="Stadium primary key")
    stadium_code: Optional[str] = Field(default=None, max_length=10)
    stadium_name: Optional[str] = Field(default=None, max_length=60)
    hometeam_code: Optional[str] = Field(default=None, max_length=10)
    seat_count: Optional[int] = Field(default=None, ge=0)
    address: Optional[str] = Field(default=None, max_length=80)
    ddd: Optional[str] = Field(default=None, max_length=10)
    tel: Optional[str] = Field(default=None, max_length=20)
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None
    embedding_created_at: Optional[datetime] = None

    @classmethod
    def from_stadium_dto(cls, dto: HubStadiumDTO) -> StadiumResponse:
        return cls(
            id=dto.id,
            stadium_code=dto.stadium_code,
            stadium_name=dto.stadium_name,
            hometeam_code=dto.hometeam_code,
            seat_count=dto.seat_count,
            address=dto.address,
            ddd=dto.ddd,
            tel=dto.tel,
            embedding_content=dto.embedding_content,
            embedding=dto.embedding,
            embedding_created_at=dto.embedding_created_at,
        )

    def to_json_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


__all__ = ["StadiumResponse"]
