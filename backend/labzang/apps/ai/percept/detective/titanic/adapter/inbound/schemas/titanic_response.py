from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from labzang.apps.dash.kaggle.titanic.application.dtos.titanic_row_dto import TitanicRowDTO


class TitanicRowResponse(BaseModel):
    model_config = ConfigDict()

    PassengerId: int = Field(..., gt=0)
    DatasetSplit: str = Field(default="train", pattern="^(train|test)$")
    Survived: Optional[int] = Field(default=None, ge=0, le=1)
    Pclass: int = Field(..., ge=1, le=3)
    Name: str
    Gender: str
    Age: Optional[float] = None
    SibSp: int
    Parch: int
    Ticket: str
    Fare: Optional[float] = None
    Cabin: Optional[str] = None
    Embarked: Optional[str] = None

    @classmethod
    def from_dto(cls, dto: TitanicRowDTO) -> TitanicRowResponse:
        return cls.model_validate(dto.model_dump(mode="python"))

    def to_json_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class TitanicBatchUpsertResponse(BaseModel):
    inserted_count: int = 0
    updated_count: int = 0
    error_count: int = 0


class TitanicListResponse(BaseModel):
    total: int
    items: List[TitanicRowResponse]
