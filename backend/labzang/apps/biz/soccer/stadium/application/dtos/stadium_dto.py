# -*- coding: utf-8 -*-
"""애플리케이션 계층 경기장 DTO — 도메인 `Stadium` 엔티티와 동일 정보를 원시 타입으로 표현."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from labzang.apps.soccer.stadium.domain.entities.stadium import Stadium


def _normalize_stadium_jsonl_keys(row: dict[str, Any]) -> dict[str, Any]:
    """`stadiums.jsonl`의 `statdium_name` 오타를 `stadium_name`으로 맞춘다."""
    out = dict(row)
    if "stadium_name" not in out and "statdium_name" in out:
        out["stadium_name"] = out.get("statdium_name")
    return out


class StadiumDTO(BaseModel):
    """`domain.entities.stadium.Stadium` / stadiums.jsonl 키와 호환되는 Pydantic 모델."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    id: int = Field(..., gt=0, description="경기장 PK")
    stadium_code: Optional[str] = Field(default=None, max_length=10)
    stadium_name: Optional[str] = Field(default=None, max_length=60)
    hometeam_code: Optional[str] = Field(default=None, max_length=10)
    seat_count: Optional[int] = Field(default=None, ge=0)
    address: Optional[str] = Field(default=None, max_length=80)
    ddd: Optional[str] = Field(default=None, max_length=10)
    tel: Optional[str] = Field(default=None, max_length=20)

    @classmethod
    def from_entity(cls, entity: Stadium) -> StadiumDTO:
        return cls.model_validate(entity.to_json_dict())

    def to_entity(self) -> Stadium:
        from labzang.apps.soccer.stadium.domain.entities.stadium import Stadium

        return Stadium.from_json_dict(self.model_dump(mode="json"))

    @classmethod
    def from_json_dict(cls, row: dict[str, Any]) -> StadiumDTO:
        return cls.model_validate(_normalize_stadium_jsonl_keys(row))
