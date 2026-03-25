from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from labzang.apps.kaggle.titanic.domain.entities.titanic import TitanicPassenger


class TitanicRowDTO(BaseModel):
    """Application DTO aligned with train.csv columns."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    PassengerId: int = Field(..., gt=0)
    Survived: Optional[int] = Field(default=None, ge=0, le=1)
    Pclass: int = Field(..., ge=1, le=3)
    Name: str = Field(..., min_length=1, max_length=255)
    Sex: str = Field(..., pattern="^(male|female)$")
    Age: Optional[float] = Field(default=None, ge=0, le=120)
    SibSp: int = Field(..., ge=0)
    Parch: int = Field(..., ge=0)
    Ticket: str = Field(..., min_length=1, max_length=50)
    Fare: Optional[float] = Field(default=None, ge=0)
    Cabin: Optional[str] = Field(default=None, max_length=50)
    Embarked: Optional[str] = Field(default=None, pattern="^(C|Q|S)$")

    @classmethod
    def from_entity(cls, entity: TitanicPassenger) -> TitanicRowDTO:
        return cls.model_validate(entity.to_dict())

    def to_entity(self) -> TitanicPassenger:
        from labzang.apps.kaggle.titanic.domain.entities.titanic import TitanicPassenger

        return TitanicPassenger.from_csv_dict(self.model_dump(mode="python"))
