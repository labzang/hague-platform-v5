from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from labzang.apps.kaggle.titanic.domain.value_objects.titanic_vo import (
    Age,
    Cabin,
    Embarked,
    Fare,
    Parch,
    PassengerClass,
    PassengerId,
    PassengerName,
    Sex,
    SibSp,
    Survived,
    Ticket,
)


@dataclass(slots=True)
class TitanicPassenger:
    """Titanic row entity preserving train.csv column semantics."""

    passenger_id: PassengerId
    survived: Optional[Survived]
    pclass: PassengerClass
    name: PassengerName
    sex: Sex
    age: Optional[Age]
    sibsp: SibSp
    parch: Parch
    ticket: Ticket
    fare: Optional[Fare]
    cabin: Optional[Cabin]
    embarked: Optional[Embarked]

    @classmethod
    def from_csv_dict(cls, row: Mapping[str, Any]) -> TitanicPassenger:
        return cls(
            passenger_id=PassengerId(int(row.get("PassengerId"))),
            survived=Survived.from_raw(row.get("Survived")),
            pclass=PassengerClass(int(row.get("Pclass"))),
            name=PassengerName(str(row.get("Name"))),
            sex=Sex(str(row.get("Sex"))),
            age=Age.from_raw(row.get("Age")),
            sibsp=SibSp(int(row.get("SibSp"))),
            parch=Parch(int(row.get("Parch"))),
            ticket=Ticket(str(row.get("Ticket"))),
            fare=Fare.from_raw(row.get("Fare")),
            cabin=Cabin.from_raw(row.get("Cabin")),
            embarked=Embarked.from_raw(row.get("Embarked")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "PassengerId": self.passenger_id.value,
            "Survived": None if self.survived is None else self.survived.value,
            "Pclass": self.pclass.value,
            "Name": self.name.value,
            "Sex": self.sex.value,
            "Age": None if self.age is None else self.age.value,
            "SibSp": self.sibsp.value,
            "Parch": self.parch.value,
            "Ticket": self.ticket.value,
            "Fare": None if self.fare is None else self.fare.value,
            "Cabin": None if self.cabin is None else self.cabin.value,
            "Embarked": None if self.embarked is None else self.embarked.value,
        }
