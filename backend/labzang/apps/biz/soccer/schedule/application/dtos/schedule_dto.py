# -*- coding: utf-8 -*-
"""애플리케이션 계층 일정 DTO — 도메인 `Schedule` 엔티티와 동일 정보를 원시 타입으로 표현."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from labzang.apps.biz.soccer.schedule.domain.entities.schedule import Schedule


class ScheduleDTO(BaseModel):
    """`domain.entities.schedule.Schedule` / schedules.jsonl 키와 호환되는 Pydantic 모델."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    id: int = Field(..., gt=0, description="일정 PK")
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

    @classmethod
    def from_entity(cls, entity: Schedule) -> ScheduleDTO:
        return cls.model_validate(entity.to_json_dict())

    def to_entity(self) -> Schedule:
        from labzang.apps.biz.soccer.schedule.domain.entities.schedule import Schedule

        return Schedule.from_json_dict(self.model_dump(mode="json"))

    @classmethod
    def from_json_dict(cls, row: dict[str, Any]) -> ScheduleDTO:
        return cls.model_validate(row)
