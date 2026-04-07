from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from labzang.apps.dash.kaggle.titanic.domain.value_objects.titanic_vo import (
    Age,
    Cabin,
    DatasetSplit,
    Embarked,
    Fare,
    Gender,
    Parch,
    PassengerClass,
    PassengerId,
    PassengerName,
    SibSp,
    Survived,
    Ticket,
)


@dataclass(slots=True)
class TitanicPassenger:
    """Titanic passenger row; Gender in dict/CSV, Sex still accepted when ingesting."""

    passenger_id: PassengerId
    dataset_split: DatasetSplit
    survived: Optional[Survived]
    pclass: PassengerClass
    name: PassengerName
    gender: Gender
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
            dataset_split=DatasetSplit.from_raw(
                row.get("DatasetSplit") or row.get("split"),
                default="train",
            ),
            survived=Survived.from_raw(row.get("Survived")),
            pclass=PassengerClass(int(row.get("Pclass"))),
            name=PassengerName(str(row.get("Name"))),
            gender=Gender(str(row.get("Gender") or row.get("Sex"))),
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
            "DatasetSplit": self.dataset_split.value,
            "Survived": None if self.survived is None else self.survived.value,
            "Pclass": self.pclass.value,
            "Name": self.name.value,
            "Gender": self.gender.value,
            "Age": None if self.age is None else self.age.value,
            "SibSp": self.sibsp.value,
            "Parch": self.parch.value,
            "Ticket": self.ticket.value,
            "Fare": None if self.fare is None else self.fare.value,
            "Cabin": None if self.cabin is None else self.cabin.value,
            "Embarked": None if self.embarked is None else self.embarked.value,
        }
