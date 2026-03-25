# -*- coding: utf-8 -*-
"""애플리케이션 계층 팀 DTO — 도메인 `Team` 엔티티와 동일 정보를 원시 타입으로 표현."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from labzang.apps.soccer.team.domain.entities.team import Team


class TeamDTO(BaseModel):
    """`domain.entities.team.Team` / teams.jsonl 키와 필드명을 맞춘 Pydantic 모델."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    id: int = Field(..., gt=0, description="팀 PK")
    stadium_id: Optional[int] = Field(default=None, gt=0)
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

    @classmethod
    def from_entity(cls, entity: Team) -> TeamDTO:
        return cls.model_validate(entity.to_json_dict())

    def to_entity(self) -> Team:
        from labzang.apps.soccer.team.domain.entities.team import Team

        return Team.from_json_dict(self.model_dump(mode="json"))

    @classmethod
    def from_json_dict(cls, row: dict[str, Any]) -> TeamDTO:
        return cls.model_validate(row)
