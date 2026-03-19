"""
타이타닉 도메인 엔티티 (순수 파이썬)
- TitanicTrain ORM 컬럼과 1:1 대응. 식별자: passenger_id.
"""
from dataclasses import dataclass
from typing import Optional

from ..value_objects.titanic import (
    Age,
    Embarked,
    Fare,
    Gender,
    Parch,
    Pclass,
    SibSp,
    Survived,
)


@dataclass
class Passenger:
    """승객 엔티티. passenger_id로 식별. ORM TitanicTrain과 컬럼 일치."""

    passenger_id: int
    survived: Optional[Survived] = None
    pclass: Optional[Pclass] = None
    name: Optional[str] = None
    gender: Optional[Gender] = None
    age: Optional[Age] = None
    sib_sp: Optional[SibSp] = None
    parch: Optional[Parch] = None
    ticket: Optional[str] = None
    fare: Optional[Fare] = None
    cabin: Optional[str] = None
    embarked: Optional[Embarked] = None


@dataclass
class TitanicModels:
    """타이타닉 모델 실험 Run — 어떤 모델로 평가/제출했는지 등 메타."""

    best_model: Optional[str] = None
    run_id: str = ""
