"""Value objects for sentiment review domain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar


def _strip(raw: object) -> str:
    return str(raw).strip()


@dataclass(frozen=True, slots=True)
class ReviewId:
    value: str
    _max_len: ClassVar[int] = 30

    def __post_init__(self) -> None:
        v = _strip(self.value)
        if not v:
            raise ValueError("ReviewId는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"ReviewId는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> "ReviewId":
        return cls(raw)


@dataclass(frozen=True, slots=True)
class MovieId:
    value: str
    _max_len: ClassVar[int] = 20

    def __post_init__(self) -> None:
        v = _strip(self.value)
        if not v:
            raise ValueError("MovieId는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"MovieId는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> "MovieId":
        return cls(raw)


@dataclass(frozen=True, slots=True)
class Author:
    value: str
    _max_len: ClassVar[int] = 50

    def __post_init__(self) -> None:
        v = _strip(self.value)
        if len(v) > self._max_len:
            raise ValueError(f"Author는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> "Author":
        if raw is None:
            return cls("")
        return cls(raw)


@dataclass(frozen=True, slots=True)
class ReviewText:
    value: str
    _max_len: ClassVar[int] = 5000

    def __post_init__(self) -> None:
        v = _strip(self.value)
        if not v:
            raise ValueError("ReviewText는 비어 있을 수 없습니다.")
        if len(v) > self._max_len:
            raise ValueError(f"ReviewText는 {self._max_len}자 이하여야 합니다.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_json(cls, raw: object) -> "ReviewText":
        return cls(raw)


@dataclass(frozen=True, slots=True)
class Rating:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError("Rating은 정수여야 합니다.")
        if not (0 <= self.value <= 10):
            raise ValueError("Rating은 0~10 범위여야 합니다.")

    @classmethod
    def from_json(cls, raw: object) -> "Rating | None":
        if raw is None:
            return None
        s = _strip(raw)
        if not s:
            return None
        if not s.isdigit():
            return None
        return cls(int(s))

    @property
    def sentiment_label(self) -> str:
        return "positive" if self.value >= 6 else "negative"


@dataclass(frozen=True, slots=True)
class ReviewDate:
    value: datetime

    @classmethod
    def from_json(cls, raw: object) -> "ReviewDate | None":
        if raw is None:
            return None
        s = _strip(raw)
        if not s:
            return None
        for fmt in ("%y.%m.%d", "%Y-%m-%d"):
            try:
                return cls(datetime.strptime(s, fmt))
            except ValueError:
                continue
        return None
