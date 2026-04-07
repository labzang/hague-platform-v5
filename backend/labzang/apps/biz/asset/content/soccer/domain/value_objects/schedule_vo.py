# -*- coding: utf-8 -*-
"""schedules.jsonl / DB `schedules` 컬럼 단위 값 객체."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Optional


def _strip_opt(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    t = str(s).strip()
    return t if t else None


@dataclass(frozen=True, slots=True)
class ScheduleId:
    """일정 PK (`id`)."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError("ScheduleId는 양의 정수여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> ScheduleId:
        if raw is None:
            raise ValueError("ScheduleId는 필수입니다.")
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class StadiumRefId:
    """`stadium_id` — `stadiums.id` FK."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError("StadiumRefId는 양의 정수여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> Optional[StadiumRefId]:
        if raw is None:
            return None
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class TeamRefId:
    """`hometeam_id` / `awayteam_id` — `teams.id` FK."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError("TeamRefId는 양의 정수여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> Optional[TeamRefId]:
        if raw is None:
            return None
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class ScheduleStadiumCode:
    """경기장 코드 (`stadium_code`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("ScheduleStadiumCode는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"ScheduleStadiumCode는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[ScheduleStadiumCode]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class ScheDate:
    """일정 날짜 (`sche_date`), YYYYMMDD 8자리 문자열."""

    _len: ClassVar[int] = 8
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("ScheDate는 비어 있을 수 없습니다.")
        if len(v) != self._len or not v.isdigit():
            raise ValueError("ScheDate는 8자리 숫자(YYYYMMDD)여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[ScheDate]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class ScheduleGubun:
    """구분 (`gubun`), 예: Y/N. 최대 5자."""

    _max_len: ClassVar[int] = 5
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("ScheduleGubun은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"ScheduleGubun은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[ScheduleGubun]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class ScheduleTeamCode:
    """팀 코드 (`hometeam_code`, `awayteam_code`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("ScheduleTeamCode는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"ScheduleTeamCode는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[ScheduleTeamCode]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class MatchScore:
    """득점 (`home_score`, `away_score`), 0 이상 정수."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value < 0:
            raise ValueError("MatchScore는 0 이상 정수여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> Optional[MatchScore]:
        if raw is None:
            return None
        return cls(int(raw))
