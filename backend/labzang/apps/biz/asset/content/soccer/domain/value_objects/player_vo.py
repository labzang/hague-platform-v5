# -*- coding: utf-8 -*-
"""players.jsonl / DB `players` 컬럼 단위 값 객체."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import ClassVar, Optional


def _strip_opt(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    t = str(s).strip()
    return t if t else None


@dataclass(frozen=True, slots=True)
class PlayerId:
    """선수 PK (`id`)."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError("PlayerId는 양의 정수여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> PlayerId:
        if raw is None:
            raise ValueError("PlayerId는 필수입니다.")
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class TeamId:
    """소속 팀 FK (`team_id`)."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError("TeamId는 양의 정수여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> Optional[TeamId]:
        if raw is None:
            return None
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class PlayerName:
    """선수명 (`player_name`), 최대 20자."""

    _max_len: ClassVar[int] = 20
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("PlayerName은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"PlayerName은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[PlayerName]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class EPlayerName:
    """영문 선수명 (`e_player_name`), 최대 40자."""

    _max_len: ClassVar[int] = 40
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("EPlayerName은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"EPlayerName은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[EPlayerName]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class Nickname:
    """닉네임 (`nickname`), 최대 30자."""

    _max_len: ClassVar[int] = 30
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Nickname은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"Nickname은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[Nickname]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class JoinYear:
    """입단 연도 문자열 (`join_yyyy`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("JoinYear는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"JoinYear는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[JoinYear]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class PlayerPosition:
    """포지션 (`position`), 최대 10자 (예: DF, MF)."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("PlayerPosition은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"PlayerPosition은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[PlayerPosition]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class BackNumber:
    """등번호 (`back_no`)."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError("BackNumber는 정수여야 합니다.")
        if not (0 <= self.value <= 99):
            raise ValueError("BackNumber는 0~99 범위여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> Optional[BackNumber]:
        if raw is None:
            return None
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class Nation:
    """국적 (`nation`), 최대 20자."""

    _max_len: ClassVar[int] = 20
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Nation은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"Nation은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[Nation]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class BirthDate:
    """생년월일 (`birth_date`). JSON 문자열 YYYY-MM-DD 또는 date."""

    value: date

    def __post_init__(self) -> None:
        if not isinstance(self.value, date):
            raise ValueError("BirthDate.value는 date여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> Optional[BirthDate]:
        if raw is None:
            return None
        if isinstance(raw, date) and not isinstance(raw, datetime):
            return cls(raw)
        s = _strip_opt(str(raw))
        if s is None:
            return None
        try:
            return cls(datetime.strptime(s, "%Y-%m-%d").date())
        except ValueError as e:
            raise ValueError(f"birth_date 형식은 YYYY-MM-DD 여야 합니다: {raw!r}") from e


@dataclass(frozen=True, slots=True)
class SolarCalendar:
    """양력/음력 구분 (`solar`), 스키마상 최대 10자. 샘플: '1', '2'."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("SolarCalendar는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"SolarCalendar는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[SolarCalendar]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class HeightCm:
    """키 cm (`height`)."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError("HeightCm는 정수여야 합니다.")
        if not (50 <= self.value <= 280):
            raise ValueError("HeightCm는 50~280(cm) 범위를 벗어났습니다.")

    @classmethod
    def from_json(cls, raw: object) -> Optional[HeightCm]:
        if raw is None:
            return None
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class WeightKg:
    """몸무게 kg (`weight`)."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError("WeightKg는 정수여야 합니다.")
        if not (20 <= self.value <= 200):
            raise ValueError("WeightKg는 20~200(kg) 범위를 벗어났습니다.")

    @classmethod
    def from_json(cls, raw: object) -> Optional[WeightKg]:
        if raw is None:
            return None
        return cls(int(raw))
