"""
타이타닉 도메인 값 객체 (순수: 외부 라이브러리 미참조)
- TitanicTrain ORM 컬럼 기준: survived, pclass, name, gender, age, sib_sp, parch, ticket, fare, cabin, embarked
- 도메인 의미·검증이 있는 값만 VO로 정의. name/ticket/cabin은 엔티티에서 Optional[str].
"""
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Survived:
    """생존 여부. 0=사망, 1=생존. ORM: survived (Integer)."""
    value: Literal[0, 1]

    def __post_init__(self) -> None:
        if self.value not in (0, 1):
            raise ValueError("Survived must be 0 or 1")

    @property
    def is_alive(self) -> bool:
        return self.value == 1


@dataclass(frozen=True)
class Pclass:
    """좌석 등급. 1=1등급, 2=2등급, 3=3등급. ORM: pclass (Integer)."""
    value: Literal[1, 2, 3]

    def __post_init__(self) -> None:
        if self.value not in (1, 2, 3):
            raise ValueError("Pclass must be 1, 2, or 3")


@dataclass(frozen=True)
class Gender:
    """성별. ORM: sex 컬럼, Python에서는 gender로 사용."""
    value: Literal["male", "female"]

    def __post_init__(self) -> None:
        if self.value not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'")


@dataclass(frozen=True)
class Age:
    """승객 나이. 0~120 범위 (미기록은 엔티티에서 None). ORM: age (Float)."""
    value: float

    def __post_init__(self) -> None:
        if not (0 <= self.value <= 120):
            raise ValueError("Age must be between 0 and 120")


@dataclass(frozen=True)
class SibSp:
    """형제/배우자 동반 수. 비음수. ORM: sib_sp (Integer)."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("SibSp must be non-negative")


@dataclass(frozen=True)
class Parch:
    """부모/자녀 동반 수. 비음수. ORM: parch (Integer)."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Parch must be non-negative")


@dataclass(frozen=True)
class Fare:
    """티켓 요금. 비음수. ORM: fare (Float)."""
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Fare must be non-negative")


@dataclass(frozen=True)
class Embarked:
    """탑승 항구. C=Cherbourg, Q=Queenstown, S=Southampton. ORM: embarked (String(1))."""
    value: Literal["C", "Q", "S"]

    def __post_init__(self) -> None:
        if self.value not in ("C", "Q", "S"):
            raise ValueError("Embarked must be C, Q, or S")
