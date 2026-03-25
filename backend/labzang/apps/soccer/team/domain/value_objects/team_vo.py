# -*- coding: utf-8 -*-
"""teams.jsonl / DB `teams` 컬럼 단위 값 객체."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Optional


def _strip_opt(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    t = str(s).strip()
    return t if t else None


@dataclass(frozen=True, slots=True)
class TeamId:
    """팀 PK (`id`)."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError("TeamId는 양의 정수여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> TeamId:
        if raw is None:
            raise ValueError("TeamId는 필수입니다.")
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class StadiumId:
    """경기장 FK (`stadium_id`)."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError("StadiumId는 양의 정수여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> Optional[StadiumId]:
        if raw is None:
            return None
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class TeamCode:
    """팀 코드 (`team_code`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("TeamCode는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"TeamCode는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[TeamCode]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class RegionName:
    """지역명 (`region_name`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("RegionName은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"RegionName은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[RegionName]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class TeamName:
    """팀명 (`team_name`), 최대 40자."""

    _max_len: ClassVar[int] = 40
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("TeamName은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"TeamName은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[TeamName]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class ETeamName:
    """영문 팀명 (`e_team_name`), 최대 50자."""

    _max_len: ClassVar[int] = 50
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("ETeamName은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"ETeamName은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[ETeamName]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class OrigYyyy:
    """창단 연도 문자열 (`orig_yyyy`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("OrigYyyy는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"OrigYyyy는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[OrigYyyy]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class ZipCode1:
    """우편번호 앞 (`zip_code1`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("ZipCode1은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"ZipCode1은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[ZipCode1]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class ZipCode2:
    """우편번호 뒤 (`zip_code2`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("ZipCode2는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"ZipCode2는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[ZipCode2]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class Address:
    """주소 (`address`), 최대 80자."""

    _max_len: ClassVar[int] = 80
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Address는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"Address는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[Address]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class Ddd:
    """지역번호 (`ddd`), 최대 10자."""

    _max_len: ClassVar[int] = 10
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Ddd는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"Ddd는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[Ddd]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class Tel:
    """전화 (`tel`), 최대 20자."""

    _max_len: ClassVar[int] = 20
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Tel은 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"Tel은 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[Tel]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class Fax:
    """팩스 (`fax`), 최대 20자."""

    _max_len: ClassVar[int] = 20
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Fax는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"Fax는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[Fax]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class Homepage:
    """홈페이지 URL (`homepage`), 최대 100자."""

    _max_len: ClassVar[int] = 100
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Homepage는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"Homepage는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[Homepage]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class Owner:
    """오너 (`owner`), 최대 50자."""

    _max_len: ClassVar[int] = 50
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Owner는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"Owner는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> Optional[Owner]:
        v = _strip_opt(None if raw is None else str(raw))
        if v is None:
            return None
        return cls(v)
