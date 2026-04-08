# -*- coding: utf-8 -*-
"""선수 도메인 엔티티 — 식별자(PlayerId)와 값 객체로 구성."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from labzang.apps.biz.field.provider.soccer.domain.value_objects.player_vo import (
    BackNumber,
    BirthDate,
    EPlayerName,
    HeightCm,
    JoinYear,
    Nation,
    Nickname,
    PlayerId,
    PlayerName,
    PlayerPosition,
    SolarCalendar,
    TeamId,
    WeightKg,
)


@dataclass(slots=True)
class Player:
    """선수 엔티티. 동등성은 `player_id`만 기준으로 한다."""

    player_id: PlayerId
    team_id: Optional[TeamId] = None
    player_name: Optional[PlayerName] = None
    e_player_name: Optional[EPlayerName] = None
    nickname: Optional[Nickname] = None
    join_year: Optional[JoinYear] = None
    position: Optional[PlayerPosition] = None
    back_number: Optional[BackNumber] = None
    nation: Optional[Nation] = None
    birth_date: Optional[BirthDate] = None
    solar: Optional[SolarCalendar] = None
    height: Optional[HeightCm] = None
    weight: Optional[WeightKg] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.player_id == other.player_id

    def __hash__(self) -> int:
        return hash(self.player_id)

    @classmethod
    def from_json_dict(cls, row: Mapping[str, Any]) -> Player:
        """JSONL 한 줄 또는 동일 키를 가진 매핑에서 엔티티를 구성한다."""
        return cls(
            player_id=PlayerId.from_json(row.get("id")),
            team_id=TeamId.from_json(row.get("team_id")),
            player_name=PlayerName.from_json(row.get("player_name")),
            e_player_name=EPlayerName.from_json(row.get("e_player_name")),
            nickname=Nickname.from_json(row.get("nickname")),
            join_year=JoinYear.from_json(row.get("join_yyyy")),
            position=PlayerPosition.from_json(row.get("position")),
            back_number=BackNumber.from_json(row.get("back_no")),
            nation=Nation.from_json(row.get("nation")),
            birth_date=BirthDate.from_json(row.get("birth_date")),
            solar=SolarCalendar.from_json(row.get("solar")),
            height=HeightCm.from_json(row.get("height")),
            weight=WeightKg.from_json(row.get("weight")),
        )

    def to_json_dict(self) -> dict[str, Any]:
        """JSONL/DB 어댑터용 원시 딕셔너리 (None은 그대로 유지)."""
        return {
            "id": self.player_id.value,
            "team_id": None if self.team_id is None else self.team_id.value,
            "player_name": None if self.player_name is None else self.player_name.value,
            "e_player_name": None
            if self.e_player_name is None
            else self.e_player_name.value,
            "nickname": None if self.nickname is None else self.nickname.value,
            "join_yyyy": None if self.join_year is None else self.join_year.value,
            "position": None if self.position is None else self.position.value,
            "back_no": None if self.back_number is None else self.back_number.value,
            "nation": None if self.nation is None else self.nation.value,
            "birth_date": None
            if self.birth_date is None
            else self.birth_date.value.isoformat(),
            "solar": None if self.solar is None else self.solar.value,
            "height": None if self.height is None else self.height.value,
            "weight": None if self.weight is None else self.weight.value,
        }
