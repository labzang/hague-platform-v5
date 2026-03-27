# -*- coding: utf-8 -*-
"""일정 도메인 엔티티 — 식별자(ScheduleId)와 값 객체로 구성."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from labzang.apps.biz.soccer.schedule.domain.value_objects.schedule_vo import (
    MatchScore,
    ScheDate,
    ScheduleGubun,
    ScheduleId,
    ScheduleStadiumCode,
    ScheduleTeamCode,
    StadiumRefId,
    TeamRefId,
)


@dataclass(slots=True)
class Schedule:
    """일정 엔티티. 동등성은 `schedule_id`만 기준으로 한다."""

    schedule_id: ScheduleId
    stadium_id: Optional[StadiumRefId] = None
    hometeam_id: Optional[TeamRefId] = None
    awayteam_id: Optional[TeamRefId] = None
    stadium_code: Optional[ScheduleStadiumCode] = None
    sche_date: Optional[ScheDate] = None
    gubun: Optional[ScheduleGubun] = None
    hometeam_code: Optional[ScheduleTeamCode] = None
    awayteam_code: Optional[ScheduleTeamCode] = None
    home_score: Optional[MatchScore] = None
    away_score: Optional[MatchScore] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Schedule):
            return NotImplemented
        return self.schedule_id == other.schedule_id

    def __hash__(self) -> int:
        return hash(self.schedule_id)

    @classmethod
    def from_json_dict(cls, row: Mapping[str, Any]) -> Schedule:
        return cls(
            schedule_id=ScheduleId.from_json(row.get("id")),
            stadium_id=StadiumRefId.from_json(row.get("stadium_id")),
            hometeam_id=TeamRefId.from_json(row.get("hometeam_id")),
            awayteam_id=TeamRefId.from_json(row.get("awayteam_id")),
            stadium_code=ScheduleStadiumCode.from_json(row.get("stadium_code")),
            sche_date=ScheDate.from_json(row.get("sche_date")),
            gubun=ScheduleGubun.from_json(row.get("gubun")),
            hometeam_code=ScheduleTeamCode.from_json(row.get("hometeam_code")),
            awayteam_code=ScheduleTeamCode.from_json(row.get("awayteam_code")),
            home_score=MatchScore.from_json(row.get("home_score")),
            away_score=MatchScore.from_json(row.get("away_score")),
        )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "id": self.schedule_id.value,
            "stadium_id": None if self.stadium_id is None else self.stadium_id.value,
            "hometeam_id": None if self.hometeam_id is None else self.hometeam_id.value,
            "awayteam_id": None if self.awayteam_id is None else self.awayteam_id.value,
            "stadium_code": None
            if self.stadium_code is None
            else self.stadium_code.value,
            "sche_date": None if self.sche_date is None else self.sche_date.value,
            "gubun": None if self.gubun is None else self.gubun.value,
            "hometeam_code": None
            if self.hometeam_code is None
            else self.hometeam_code.value,
            "awayteam_code": None
            if self.awayteam_code is None
            else self.awayteam_code.value,
            "home_score": None if self.home_score is None else self.home_score.value,
            "away_score": None if self.away_score is None else self.away_score.value,
        }
