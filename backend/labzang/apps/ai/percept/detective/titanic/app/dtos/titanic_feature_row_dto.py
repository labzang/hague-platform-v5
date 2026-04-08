from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TitanicFeatureRowDTO(BaseModel):
    """전처리 파이프라인 산출 컬럼만 보관 (drop·라벨 제외)."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    PassengerId: int = Field(..., gt=0)
    DatasetSplit: str = Field(..., pattern="^(train|test)$")
    Pclass: int = Field(..., ge=1, le=3)
    Embarked: int = Field(..., ge=0)
    Title: int = Field(..., ge=0)
    Gender: int = Field(..., ge=0, le=1)
    AgeGroup: int = Field(..., ge=0)
    FareBand: int = Field(..., ge=0)
