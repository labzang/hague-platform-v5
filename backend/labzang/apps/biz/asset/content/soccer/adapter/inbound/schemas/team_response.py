# -*- coding: utf-8 -*-
"""Inbound response schemas — JSON for clients from team `find_by_id` / list results."""

from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from labzang.apps.biz.asset.content.soccer.application.dtos.team_dto import TeamDTO as HubTeamDTO


class TeamResponse(BaseModel):
    """단일 팀 페이로드 — 허브 `TeamDTO`(dataclass)와 정렬."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1011,
                "stadium_id": 1011,
                "team_code": "K06",
                "region_name": "부산",
                "team_name": "아이파크",
            }
        }
    )

    id: int = Field(..., gt=0, description="Team primary key")
    stadium_id: Optional[int] = Field(default=None, description="Stadium FK")
    team_code: Optional[str] = Field(default=None, max_length=10)
    region_name: Optional[str] = Field(default=None, max_length=10)
    team_name: Optional[str] = Field(default=None, max_length=40)
    e_team_name: Optional[str] = Field(default=None, max_length=50)
    orig_yyyy: Optional[str] = Field(default=None, max_length=10)
    zip_code1: Optional[str] = Field(default=None, max_length=10)
    zip_code2: Optional[str] = Field(default=None, max_length=10)
    address: Optional[str] = Field(default=None, max_length=80)
    ddd: Optional[str] = Field(default=None, max_length=10)
    tel: Optional[str] = Field(default=None, max_length=20)
    fax: Optional[str] = Field(default=None, max_length=20)
    homepage: Optional[str] = Field(default=None, max_length=100)
    owner: Optional[str] = Field(default=None, max_length=50)
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None
    embedding_created_at: Optional[datetime] = None

    @classmethod
    def from_team_dto(cls, dto: HubTeamDTO) -> TeamResponse:
        return cls(
            id=dto.id,
            stadium_id=dto.stadium_id,
            team_code=dto.team_code,
            region_name=dto.region_name,
            team_name=dto.team_name,
            e_team_name=dto.e_team_name,
            orig_yyyy=dto.orig_yyyy,
            zip_code1=dto.zip_code1,
            zip_code2=dto.zip_code2,
            address=dto.address,
            ddd=dto.ddd,
            tel=dto.tel,
            fax=dto.fax,
            homepage=dto.homepage,
            owner=dto.owner,
            embedding_content=dto.embedding_content,
            embedding=dto.embedding,
            embedding_created_at=dto.embedding_created_at,
        )

    def to_json_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


__all__ = ["TeamResponse"]
