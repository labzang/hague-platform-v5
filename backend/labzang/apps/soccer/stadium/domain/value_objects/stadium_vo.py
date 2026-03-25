# -*- coding: utf-8 -*-
"""stadiums.jsonl / DB `stadiums` 컬럼 단위 값 객체."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Optional


def _strip_opt(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    t = str(s).strip()
    return t if t else None


@dataclass(frozen=True, slots=True)
class StadiumId:
    """경기장 PK (`id`)."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError("StadiumId는 양의 정수여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> StadiumId:
        if raw is None:
            raise ValueError("StadiumId는 필수입니다.")
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class StadiumCode:
    """경기장 코드 (`stadium_code`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("StadiumCode는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"StadiumCode는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[StadiumCode]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class StadiumName:
    """경기장명 (`stadium_name` / JSONL 오타 `statdium_name`), 최대 60자."""

    _max_len: ClassVar[int] = 60
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("StadiumName은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"StadiumName은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[StadiumName]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class HometeamCode:
    """홈팀 코드 (`hometeam_code`), 최대 10자. 빈 문자열은 None."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("HometeamCode는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"HometeamCode는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[HometeamCode]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class SeatCount:
    """좌석 수 (`seat_count`), 0 이상 정수."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value < 0:
            raise ValueError("SeatCount는 0 이상 정수여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> Optional[SeatCount]:
        if raw is None:
            return None
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class StadiumAddress:
    """주소 (`address`), 최대 80자."""

    _max_len: ClassVar[int] = 80
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("StadiumAddress는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"StadiumAddress는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[StadiumAddress]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class StadiumDdd:
    """지역번호 (`ddd`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("StadiumDdd는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"StadiumDdd는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[StadiumDdd]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class StadiumTel:
    """전화 (`tel`), 최대 20자. 빈 문자열은 None."""

    _max_len: ClassVar[int] = 20
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("StadiumTel은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"StadiumTel은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[StadiumTel]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)
