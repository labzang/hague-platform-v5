from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from labzang.apps.ai.percept.detective.titanic.domain.entities.titanic import TitanicPassenger


class TitanicRowDTO(BaseModel):
    """Application DTO aligned with train.csv columns (Gender)."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

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

    @classmethod
    def from_entity(cls, entity: TitanicPassenger) -> TitanicRowDTO:
        return cls.model_validate(entity.to_dict())

    def to_entity(self) -> TitanicPassenger:
        from labzang.apps.ai.percept.detective.titanic.domain.entities.titanic import TitanicPassenger

        return TitanicPassenger.from_csv_dict(self.model_dump(mode="python"))


class TitanicPreprocessPipelineResultDTO(BaseModel):
    """배치 업로드 → 전처리(TitanicModel 파이프라인) + DB upsert 결과."""

    persisted_count: int = 0
    persist_note: Optional[str] = None
    features_persisted_count: int = 0
    features_persist_note: Optional[str] = None
    processed_train_rows: int = 0
    processed_test_rows: int = 0
    feature_columns: list[str] = Field(default_factory=list)
    train_preview: list[dict[str, Any]] = Field(default_factory=list)
    test_preview: list[dict[str, Any]] = Field(default_factory=list)
