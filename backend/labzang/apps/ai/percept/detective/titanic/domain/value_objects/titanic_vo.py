from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Optional


def _strip_opt(value: object) -> Optional[str]:
    if value is None:
        return None
    v = str(value).strip()
    return v if v else None


@dataclass(frozen=True, slots=True)
class PassengerId:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError("PassengerId must be a positive integer.")


@dataclass(frozen=True, slots=True)
class Survived:
    value: int

    def __post_init__(self) -> None:
        if self.value not in (0, 1):
            raise ValueError("Survived must be 0 or 1.")

    @classmethod
    def from_raw(cls, raw: object) -> Optional[Survived]:
        if raw is None or _strip_opt(raw) is None:
            return None
        return cls(int(raw))


@dataclass(frozen=True, slots=True)
class PassengerClass:
    value: int

    def __post_init__(self) -> None:
        if self.value not in (1, 2, 3):
            raise ValueError("Pclass must be 1, 2, or 3.")


@dataclass(frozen=True, slots=True)
class PassengerName:
    _max_len: ClassVar[int] = 255
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Name cannot be empty.")
        if len(v) > self._max_len:
            raise ValueError(f"Name max length is {self._max_len}.")
        object.__setattr__(self, "value", v)


@dataclass(frozen=True, slots=True)
class Gender:
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Gender cannot be empty.")
        normalized = v.lower()
        if normalized not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'.")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class DatasetSplit:
    """행이 train 세트인지 test 세트인지 구분 (리소스 CSV·저장 스키마와 동일)."""

    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("DatasetSplit cannot be empty.")
        normalized = v.lower()
        if normalized not in ("train", "test"):
            raise ValueError("DatasetSplit must be 'train' or 'test'.")
        object.__setattr__(self, "value", normalized)

    @classmethod
    def from_raw(cls, raw: object, default: str = "train") -> DatasetSplit:
        if raw is None or _strip_opt(raw) is None:
            return cls(str(default))
        return cls(str(raw))


@dataclass(frozen=True, slots=True)
class Age:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0 or self.value > 120:
            raise ValueError("Age must be between 0 and 120.")

    @classmethod
    def from_raw(cls, raw: object) -> Optional[Age]:
        if raw is None or _strip_opt(raw) is None:
            return None
        return cls(float(raw))


@dataclass(frozen=True, slots=True)
class SibSp:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("SibSp must be >= 0.")


@dataclass(frozen=True, slots=True)
class Parch:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Parch must be >= 0.")


@dataclass(frozen=True, slots=True)
class Ticket:
    _max_len: ClassVar[int] = 50
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Ticket cannot be empty.")
        if len(v) > self._max_len:
            raise ValueError(f"Ticket max length is {self._max_len}.")
        object.__setattr__(self, "value", v)


@dataclass(frozen=True, slots=True)
class Fare:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Fare must be >= 0.")

    @classmethod
    def from_raw(cls, raw: object) -> Optional[Fare]:
        if raw is None or _strip_opt(raw) is None:
            return None
        return cls(float(raw))


@dataclass(frozen=True, slots=True)
class Cabin:
    _max_len: ClassVar[int] = 50
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Cabin cannot be empty.")
        if len(v) > self._max_len:
            raise ValueError(f"Cabin max length is {self._max_len}.")
        object.__setattr__(self, "value", v)

    @classmethod
    def from_raw(cls, raw: object) -> Optional[Cabin]:
        v = _strip_opt(raw)
        if v is None:
            return None
        return cls(v)


@dataclass(frozen=True, slots=True)
class Embarked:
    value: str

    def __post_init__(self) -> None:
        v = _strip_opt(self.value)
        if not v:
            raise ValueError("Embarked cannot be empty.")
        normalized = v.upper()
        if normalized not in ("C", "Q", "S"):
            raise ValueError("Embarked must be one of C, Q, S.")
        object.__setattr__(self, "value", normalized)

    @classmethod
    def from_raw(cls, raw: object) -> Optional[Embarked]:
        v = _strip_opt(raw)
        if v is None:
            return None
        return cls(v)
