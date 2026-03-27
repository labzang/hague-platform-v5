# -*- coding: utf-8 -*-
"""애플리케이션 계층 선수 DTO — 도메인 `Player` 엔티티와 동일 정보를 원시 타입으로 표현."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from labzang.apps.biz.soccer.player.domain.entities.player import Player


class PlayerDTO(BaseModel):
    """`domain.entities.player.Player` / JSONL 키와 필드명을 맞춘 Pydantic 모델."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    id: int = Field(..., gt=0, description="선수 PK")
    team_id: Optional[int] = Field(default=None, gt=0)
    player_name: Optional[str] = Field(default=None, max_length=20)
    e_player_name: Optional[str] = Field(default=None, max_length=40)
    nickname: Optional[str] = Field(default=None, max_length=30)
    join_yyyy: Optional[str] = Field(default=None, max_length=10)
    position: Optional[str] = Field(default=None, max_length=10)
    back_no: Optional[int] = Field(default=None, ge=0, le=99)
    nation: Optional[str] = Field(default=None, max_length=20)
    birth_date: Optional[date] = None
    solar: Optional[str] = Field(default=None, max_length=10)
    height: Optional[int] = Field(default=None, ge=50, le=280)
    weight: Optional[int] = Field(default=None, ge=20, le=200)

    @classmethod
    def from_entity(cls, entity: Player) -> PlayerDTO:
        return cls.model_validate(entity.to_json_dict())

    def to_entity(self) -> Player:
        from labzang.apps.biz.soccer.player.domain.entities.player import Player

        return Player.from_json_dict(self.model_dump(mode="json"))

    @classmethod
    def from_json_dict(cls, row: dict[str, Any]) -> PlayerDTO:
        """JSONL 한 줄 등 원시 딕셔너리에서 생성."""
        return cls.model_validate(row)
