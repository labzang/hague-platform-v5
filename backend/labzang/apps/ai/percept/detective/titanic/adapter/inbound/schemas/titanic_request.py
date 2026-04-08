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


class TitanicRowRequest(BaseModel):
    """JSONL 한 줄에 해당하는 요청 모델 (legacy ingest 호환)."""

    model_config = ConfigDict(str_strip_whitespace=True, populate_by_name=True)

    PassengerId: Optional[int] = Field(None, gt=0, description="승객 ID")
    Survived: Optional[int] = Field(None, ge=0, le=1, description="0=사망, 1=생존")
    Pclass: Optional[int] = Field(None, ge=1, le=3, description="좌석 등급 1/2/3")
    Name: Optional[str] = Field(None, max_length=256)
    Gender: Optional[str] = Field(None, max_length=16, alias="Sex")
    Age: Optional[float] = Field(None, ge=0, le=120)
    SibSp: Optional[int] = Field(None, ge=0, description="형제/배우자 동반 수")
    Parch: Optional[int] = Field(None, ge=0, description="부모/자녀 동반 수")
    Ticket: Optional[str] = Field(None, max_length=64)
    Fare: Optional[float] = Field(None, ge=0)
    Cabin: Optional[str] = Field(None, max_length=32)
    Embarked: Optional[str] = Field(None, max_length=1, description="S/C/Q")

    def to_orm_kwargs(self) -> dict:
        return {
            "passenger_id": self.PassengerId,
            "survived": self.Survived,
            "pclass": self.Pclass,
            "name": self.Name,
            "gender": self.Gender,
            "age": self.Age,
            "sib_sp": self.SibSp,
            "parch": self.Parch,
            "ticket": self.Ticket,
            "fare": self.Fare,
            "cabin": self.Cabin,
            "embarked": self.Embarked,
        }


class TitanicJsonlBody(BaseModel):
    rows: List[TitanicRowRequest] = Field(default_factory=list)


def parse_jsonl_to_rows(jsonl_text: str) -> List[TitanicRowRequest]:
    rows: List[TitanicRowRequest] = []
    for line in jsonl_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(TitanicRowRequest.model_validate_json(line))
    return rows


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
