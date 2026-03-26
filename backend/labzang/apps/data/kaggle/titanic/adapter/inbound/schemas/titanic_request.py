from __future__ import annotations

from typing import Annotated, List, Optional

from fastapi import Depends, Query
from pydantic import BaseModel, ConfigDict, Field


class TitanicUpsertRequest(BaseModel):
    """Single row payload that mirrors train.csv-style columns (Gender)."""

    model_config = ConfigDict(str_strip_whitespace=True)

    PassengerId: int = Field(..., gt=0)
    DatasetSplit: str = Field(default="train", pattern="^(train|test)$")
    Survived: Optional[int] = Field(default=None, ge=0, le=1)
    Pclass: int = Field(..., ge=1, le=3)
    Name: str = Field(..., min_length=1, max_length=255)
    Gender: str = Field(..., pattern="^(male|female)$")
    Age: Optional[float] = Field(default=None, ge=0, le=120)
    SibSp: int = Field(..., ge=0)
    Parch: int = Field(..., ge=0)
    Ticket: str = Field(..., min_length=1, max_length=50)
    Fare: Optional[float] = Field(default=None, ge=0)
    Cabin: Optional[str] = Field(default=None, max_length=50)
    Embarked: Optional[str] = Field(default=None, pattern="^(C|Q|S)$")


class TitanicBatchUpsertRequest(BaseModel):
    rows: List[TitanicUpsertRequest] = Field(default_factory=list, min_length=1)


class TitanicSearchRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    passenger_id: Optional[int] = Field(default=None, gt=0)
    survived: Optional[int] = Field(default=None, ge=0, le=1)
    pclass: Optional[int] = Field(default=None, ge=1, le=3)
    gender: Optional[str] = Field(default=None, pattern="^(male|female)$")
    embarked: Optional[str] = Field(default=None, pattern="^(C|Q|S)$")
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


def get_titanic_search_params(
    passenger_id: Optional[int] = Query(None, gt=0),
    survived: Optional[int] = Query(None, ge=0, le=1),
    pclass: Optional[int] = Query(None, ge=1, le=3),
    gender: Optional[str] = Query(None, pattern="^(male|female)$"),
    embarked: Optional[str] = Query(None, pattern="^(C|Q|S)$"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> TitanicSearchRequest:
    return TitanicSearchRequest(
        passenger_id=passenger_id,
        survived=survived,
        pclass=pclass,
        gender=gender,
        embarked=embarked,
        limit=limit,
        offset=offset,
    )


TitanicSearchQuery = Annotated[TitanicSearchRequest, Depends(get_titanic_search_params)]
