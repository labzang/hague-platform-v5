"""
TitanicModel 전처리 파이프라인 (pandas).
성별은 컬럼명 `Gender`(male/female) 기준이며, 레거시 `Sex` 컬럼은 ingest 시 `Gender`로 통일한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import pandas as pd

from labzang.apps.data.kaggle.titanic.application.dtos.titanic_feature_row_dto import (
    TitanicFeatureRowDTO,
)


@dataclass
class _Ctx:
    train: pd.DataFrame
    test: pd.DataFrame
    id: pd.Series | None = None
    label: pd.Series | None = None


class TitanicPreprocessService:
    """
    DataFrame 입력 → 특성 공학 후 (train, test) 반환.

    - 헬퍼는 **인스턴스 메서드**로 두어, 나중에 `self`에 설정값(구간 bin 등)을 두거나
      서브클래스로 확장하기 쉽게 한다. (`@staticmethod`만 가능한 것은 아님.)
    - **입력** `train_df` / `test_df`는 내부에서 `copy()` 하므로 호출자 쪽 원본은 바뀌지 않는다.
    - **출력**은 `run()` 반환값과 동일한 객체를 `last_processed_train` / `last_processed_test`에
      보관한다(DB 적재·후속 파이프라인에서 재사용 가능).
    """

    def __init__(self) -> None:
        self.last_processed_train: pd.DataFrame | None = None
        self.last_processed_test: pd.DataFrame | None = None
        self.last_train_label: pd.Series | None = None
        self.last_test_passenger_ids: pd.Series | None = None

    def run(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        this = _Ctx(train=train_df.copy(), test=test_df.copy())
        this.id = this.test["PassengerId"] if "PassengerId" in this.test.columns else None
        self.last_test_passenger_ids = this.id.copy() if this.id is not None else None
        if "Survived" not in this.train.columns:
            raise ValueError("train에는 Survived 컬럼이 필요합니다.")
        this.label = this.train["Survived"]
        self.last_train_label = this.label.copy()
        this.train = this.train.drop("Survived", axis=1)
        if "Survived" in this.test.columns:
            this.test = this.test.drop("Survived", axis=1)

        self._apply_feature_pipeline(this)

        train_out = this.train.copy()
        test_out = this.test.copy()
        self.last_processed_train = train_out
        self.last_processed_test = test_out
        return train_out, test_out

    def run_single_split(
        self,
        df: pd.DataFrame,
        *,
        split: Literal["train", "test"],
    ) -> pd.DataFrame:
        """단일 CSV(train만 또는 test만)를 train/test 슬롯에 동일 복제해 파이프라인을 돌린 뒤 해당 split 결과만 반환."""
        this = _Ctx(train=df.copy(), test=df.copy())
        self.last_test_passenger_ids = (
            this.test["PassengerId"].copy() if "PassengerId" in this.test.columns else None
        )
        if split == "train":
            if "Survived" not in this.train.columns:
                raise ValueError("train 배치에는 Survived 컬럼이 필요합니다.")
            this.label = this.train["Survived"]
            self.last_train_label = this.label.copy()
            this.train = this.train.drop("Survived", axis=1)
            this.test = this.test.drop("Survived", axis=1)
        else:
            self.last_train_label = None
            if "Survived" in this.train.columns:
                this.train = this.train.drop("Survived", axis=1)
                this.test = this.test.drop("Survived", axis=1)

        self._apply_feature_pipeline(this)
        train_out = this.train.copy()
        test_out = this.test.copy()
        self.last_processed_train = train_out
        self.last_processed_test = test_out
        return train_out if split == "train" else test_out

    def _apply_feature_pipeline(self, this: _Ctx) -> None:
        self._drop_feature(this, "SibSp", "Parch", "Cabin", "Ticket")
        self._extract_title_from_name(this)
        title_mapping = self._remove_duplicate_title()
        self._title_nominal(this, title_mapping)
        self._drop_feature(this, "Name")
        self._gender_nominal(this)
        self._embarked_nominal(this)
        self._age_ratio(this)
        self._pclass_ordinal(this)
        self._fare_ratio(this)
        self._drop_feature(this, "Fare")

    def _drop_feature(self, this: _Ctx, *feature: str) -> None:
        for df in (this.train, this.test):
            for col in feature:
                if col in df.columns:
                    df.drop(col, axis=1, inplace=True)

    def _extract_title_from_name(self, this: _Ctx) -> None:
        for these in (this.train, this.test):
            these["Title"] = these["Name"].str.extract(r"([A-Za-z]+)\.", expand=False)

    def _remove_duplicate_title(self) -> dict[str, int]:
        return {"Mr": 1, "Ms": 2, "Mrs": 3, "Master": 4, "Royal": 5, "Rare": 6}

    def _title_nominal(self, this: _Ctx, title_mapping: dict[str, int]) -> None:
        for these in (this.train, this.test):
            these["Title"] = these["Title"].replace(
                ["Countess", "Lady", "Sir"],
                "Royal",
            )
            these["Title"] = these["Title"].replace(
                [
                    "Capt",
                    "Col",
                    "Don",
                    "Dr",
                    "Major",
                    "Rev",
                    "Jonkheer",
                    "Dona",
                    "Mme",
                ],
                "Rare",
            )
            these["Title"] = these["Title"].replace(["Mlle"], "Mr")
            these["Title"] = these["Title"].replace(["Miss"], "Ms")
            these["Title"] = these["Title"].fillna("Rare")
            these["Title"] = these["Title"].map(title_mapping)
            these["Title"] = (
                pd.to_numeric(these["Title"], errors="coerce").fillna(0).astype(int)
            )

    def _gender_nominal(self, this: _Ctx) -> None:
        """문자열 Gender(male/female) → 이진(0/1). 컬럼명은 `Gender` 유지."""
        gender_mapping = {"male": 0, "female": 1}
        for these in (this.train, this.test):
            g = these["Gender"].astype(str).str.strip().str.lower()
            these["Gender"] = g.map(gender_mapping)

    def _embarked_nominal(self, this: _Ctx) -> None:
        embarked_mapping = {"S": 1, "C": 2, "Q": 3}
        for these in (this.train, this.test):
            these["Embarked"] = these["Embarked"].fillna("S").map(embarked_mapping)

    def _age_ratio(self, this: _Ctx) -> None:
        """연속형 Age → 구간(pd.cut) → AgeGroup(0~7). 원본 Age 컬럼은 제거한다."""
        age_mapping = {
            "Unknown": 0,
            "Baby": 1,
            "Child": 2,
            "Teenager": 3,
            "Student": 4,
            "Young Adult": 5,
            "Adult": 6,
            "Senior": 7,
        }
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        labels = [
            "Unknown",
            "Baby",
            "Child",
            "Teenager",
            "Student",
            "Young Adult",
            "Adult",
            "Senior",
        ]
        for these in (this.train, this.test):
            age_for_cut = these["Age"].fillna(-0.5)
            age_cat = pd.cut(age_for_cut, bins, labels=labels)
            these["AgeGroup"] = age_cat.map(age_mapping)
            these["AgeGroup"] = these["AgeGroup"].fillna(0).astype(int)
            if "Age" in these.columns:
                these.drop(columns=["Age"], inplace=True)

    def _pclass_ordinal(self, this: _Ctx) -> None:
        mapping = {1: 1, 2: 2, 3: 3}
        for these in (this.train, this.test):
            orig = these["Pclass"]
            these["Pclass"] = these["Pclass"].map(mapping).fillna(orig)

    def _fare_ratio(self, this: _Ctx) -> None:
        bins = [-1, 8, 15, 31, np.inf]
        labels = ["Unknown", "Low", "Mid", "High"]
        fare_mapping = {"Unknown": 0, "Low": 1, "Mid": 2, "High": 3}
        for these in (this.train, this.test):
            these["Fare"] = these["Fare"].fillna(0)
            fare_cat = pd.cut(these["Fare"], bins, labels=labels)
            these["FareBand"] = fare_cat.map(fare_mapping)
            these["FareBand"] = these["FareBand"].fillna(0).astype(int)


def _ensure_gender_column(df: pd.DataFrame) -> pd.DataFrame:
    """레거시 `Sex` 컬럼이 있으면 `Gender`로 이름만 맞춘다."""
    if "Sex" in df.columns and "Gender" not in df.columns:
        return df.rename(columns={"Sex": "Gender"})
    return df


def _drop_dataset_split_meta(df: pd.DataFrame) -> pd.DataFrame:
    """전처리 특성 공학에는 `DatasetSplit` 메타 컬럼이 필요 없다."""
    if "DatasetSplit" in df.columns:
        return df.drop(columns=["DatasetSplit"])
    return df


def dataframe_from_dto_rows(rows: list[Any]) -> pd.DataFrame:
    """단일 split DTO 리스트 → DataFrame (DatasetSplit 메타는 전처리 전에 제거)."""
    df = _ensure_gender_column(pd.DataFrame([r.model_dump() for r in rows]))
    return _drop_dataset_split_meta(df)


def train_test_from_dtos(
    train_rows: list[Any],
    test_rows: list[Any] | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """TitanicRowDTO 리스트 → DataFrame. 성별 컬럼은 `Gender`(레거시 `Sex`는 `Gender`로 통일)."""
    train_records = [r.model_dump() for r in train_rows]
    train_df = _ensure_gender_column(pd.DataFrame(train_records))

    if test_rows:
        test_df = pd.DataFrame([r.model_dump() for r in test_rows])
        test_df = _ensure_gender_column(test_df)
        if "Survived" in test_df.columns:
            test_df = test_df.drop(columns=["Survived"])
    else:
        cols = [c for c in train_df.columns if c != "Survived"]
        test_df = pd.DataFrame(columns=cols)
    train_df = _drop_dataset_split_meta(train_df)
    test_df = _drop_dataset_split_meta(test_df)
    return train_df, test_df


_FEATURE_FRAME_COLUMNS = (
    "PassengerId",
    "Pclass",
    "Embarked",
    "Title",
    "Gender",
    "AgeGroup",
    "FareBand",
)


def dataframe_to_feature_dtos(
    df: pd.DataFrame,
    dataset_split: str,
) -> list[TitanicFeatureRowDTO]:
    """전처리 결과 DataFrame → 특성 테이블용 DTO (지정 split 메타 부여)."""
    if df.empty:
        return []
    missing = [c for c in _FEATURE_FRAME_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"전처리 결과에 필요한 컬럼이 없습니다: {missing}")
    out: list[TitanicFeatureRowDTO] = []
    for rec in df.replace({np.nan: None}).to_dict(orient="records"):
        out.append(
            TitanicFeatureRowDTO(
                PassengerId=int(rec["PassengerId"]),
                DatasetSplit=dataset_split,
                Pclass=int(rec["Pclass"]),
                Embarked=int(rec["Embarked"]),
                Title=int(rec["Title"]),
                Gender=int(rec["Gender"]),
                AgeGroup=int(rec["AgeGroup"]),
                FareBand=int(rec["FareBand"]),
            )
        )
    return out


def dataframe_preview_records(df: pd.DataFrame, limit: int = 5) -> list[dict[str, Any]]:
    if df.empty or limit <= 0:
        return []
    out: list[dict[str, Any]] = []
    for row in df.head(limit).replace({np.nan: None}).to_dict(orient="records"):
        clean: dict[str, Any] = {}
        for k, v in row.items():
            if hasattr(v, "item"):
                try:
                    clean[k] = v.item()
                except Exception:
                    clean[k] = v
            else:
                clean[k] = v
        out.append(clean)
    return out
