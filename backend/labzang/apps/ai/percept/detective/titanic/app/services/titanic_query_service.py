"""Titanic query helper service (EDA 집계 보조 함수 모음)."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from labzang.apps.ai.percept.detective.titanic.adapter.outbound.orm.titanic_feature_orm import (
    TitanicFeatureORM,
)
from labzang.apps.ai.percept.detective.titanic.adapter.outbound.orm.titanic_orm import TitanicORM

logger = logging.getLogger(__name__)


class TitanicQueryService:
    _TRAIN_CSV = Path(__file__).resolve().parents[2] / "resources" / "train.csv"

    @staticmethod
    def json_safe_number(v: Any) -> float | int | None:
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return None
        if hasattr(v, "item"):
            try:
                v = v.item()
            except Exception:
                pass
        if isinstance(v, (np.integer, int)):
            return int(v)
        if isinstance(v, (np.floating, float)):
            return float(v)
        return v

    @classmethod
    def describe_series(cls, s: pd.Series) -> dict[str, float | int | None]:
        d = s.describe().to_dict()
        out: dict[str, float | int | None] = {}
        for k, v in d.items():
            out[str(k)] = cls.json_safe_number(v)
        return out

    @staticmethod
    def histogram_counts(
        values: np.ndarray,
        *,
        bins: int = 20,
        range_: tuple[float, float] | None = None,
    ) -> dict[str, list[float]]:
        counts, edges = np.histogram(values, bins=bins, range=range_)
        return {
            "bin_edges": [float(x) for x in edges],
            "counts": [int(x) for x in counts],
        }

    @staticmethod
    def crosstab_to_records(ct: pd.DataFrame) -> dict[str, dict[str, int]]:
        ct = ct.fillna(0).astype(int)
        out: dict[str, dict[str, int]] = {}
        for idx in ct.index:
            out[str(idx)] = {str(c): int(ct.loc[idx, c]) for c in ct.columns}
        return out

    @staticmethod
    def load_train_from_db(session_factory: Callable[[], Session]) -> pd.DataFrame | None:
        session = session_factory()
        try:
            rows = session.query(TitanicORM).filter(TitanicORM.dataset_split == "train").all()
            if not rows:
                return None
            records = []
            for r in rows:
                records.append(
                    {
                        "PassengerId": r.passenger_id,
                        "Survived": r.survived,
                        "Pclass": r.pclass,
                        "Name": r.name,
                        "Sex": r.gender,
                        "Age": r.age,
                        "SibSp": r.sibsp,
                        "Parch": r.parch,
                        "Ticket": r.ticket,
                        "Fare": r.fare,
                        "Cabin": r.cabin,
                        "Embarked": r.embarked,
                    }
                )
            return pd.DataFrame.from_records(records)
        except Exception as e:
            logger.warning("titanic_passengers 조회 실패, CSV로 대체: %s", e)
            return None
        finally:
            session.close()

    @classmethod
    def load_train_from_csv(cls) -> pd.DataFrame:
        df = pd.read_csv(cls._TRAIN_CSV)
        if "Gender" in df.columns and "Sex" not in df.columns:
            df = df.rename(columns={"Gender": "Sex"})
        return df

    @staticmethod
    def feature_summary_from_db(
        session_factory: Callable[[], Session],
    ) -> dict[str, Any] | None:
        session = session_factory()
        try:
            rows = (
                session.query(TitanicFeatureORM)
                .filter(TitanicFeatureORM.dataset_split == "train")
                .all()
            )
            if not rows:
                return None
            df = pd.DataFrame(
                [
                    {
                        "pclass": r.pclass,
                        "embarked": r.embarked,
                        "title": r.title,
                        "gender": r.gender,
                        "age_group": r.age_group,
                        "fare_band": r.fare_band,
                    }
                    for r in rows
                ]
            )

            def _vc(s: pd.Series) -> dict[str, int]:
                return {str(k): int(v) for k, v in s.value_counts().sort_index().items()}

            return {
                "row_count": len(df),
                "value_counts": {
                    "pclass": _vc(df["pclass"]),
                    "embarked_encoded": _vc(df["embarked"]),
                    "title": _vc(df["title"]),
                    "gender": _vc(df["gender"]),
                    "age_group": _vc(df["age_group"]),
                    "fare_band": _vc(df["fare_band"]),
                },
            }
        except Exception as e:
            logger.warning("titanic_passenger_features 조회 실패: %s", e)
            return None
        finally:
            session.close()
