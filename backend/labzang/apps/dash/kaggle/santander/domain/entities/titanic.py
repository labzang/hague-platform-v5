"""
타이타닉 도메인 엔티티 (순수 파이썬)
- TitanicTrain ORM 컬럼과 1:1 대응. 식별자: passenger_id.
"""
from dataclasses import dataclass
from typing import Optional

from labzang.apps.data.kaggle.santander.domain.value_objects.titanic_vo import (
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


