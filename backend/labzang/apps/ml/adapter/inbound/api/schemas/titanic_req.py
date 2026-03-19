"""
타이타닉 JSONL 요청 스키마 — train.csv 한 행 = JSON 한 줄.
API에서 JSONL(한 줄당 하나의 JSON 객체)로 수신할 때 매핑용.
"""
from typing import List, Optional

from pydantic import BaseModel, Field


class TitanicRowRequest(BaseModel):
    """train.csv 한 행에 대응하는 요청 모델. JSONL 한 줄 = 이 스키마 한 건."""

    PassengerId: Optional[int] = Field(None, description="승객 ID")
    Survived: Optional[int] = Field(None, ge=0, le=1, description="0=사망, 1=생존")
    Pclass: Optional[int] = Field(None, ge=1, le=3, description="좌석 등급 1/2/3")
    Name: Optional[str] = Field(None, max_length=256)
    # 원본 키 "Sex" 수신 → 도입 시점에서 Gender로 순화 (alias로 수신)
    Gender: Optional[str] = Field(None, max_length=16, alias="Sex")
    Age: Optional[float] = Field(None, ge=0, le=120)
    SibSp: Optional[int] = Field(None, ge=0, description="형제/배우자 동반 수")
    Parch: Optional[int] = Field(None, ge=0, description="부모/자녀 동반 수")
    Ticket: Optional[str] = Field(None, max_length=64)
    Fare: Optional[float] = Field(None, ge=0)
    Cabin: Optional[str] = Field(None, max_length=32)
    Embarked: Optional[str] = Field(None, max_length=1, description="S/C/Q")

    class Config:
        populate_by_name = True
        str_strip_whitespace = True

    def to_orm_kwargs(self) -> dict:
        """ORM(TitanicTrain) 생성 시 넣을 kwargs로 변환."""
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
    """JSONL 본문 파싱 결과 — 여러 행을 리스트로 담을 때."""

    rows: List[TitanicRowRequest] = Field(
        default_factory=list, description="한 줄당 TitanicRowRequest 한 건"
    )


def parse_jsonl_to_rows(jsonl_text: str) -> List[TitanicRowRequest]:
    """JSONL 문자열(한 줄당 JSON 객체)을 TitanicRowRequest 리스트로 파싱."""
    rows: List[TitanicRowRequest] = []
    for line in jsonl_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(TitanicRowRequest.model_validate_json(line))
    return rows


__all__ = [
    "TitanicRowRequest",
    "TitanicJsonlBody",
    "parse_jsonl_to_rows",
]
