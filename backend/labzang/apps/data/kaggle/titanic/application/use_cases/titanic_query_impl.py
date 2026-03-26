"""DB(`titanic_passengers`, `titanic_passenger_features`) 또는 번들 CSV로 EDA 집계."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable, Literal

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from labzang.apps.data.kaggle.titanic.adapter.outbound.orm.titanic_feature_orm import (
    TitanicFeatureORM,
)
from labzang.apps.data.kaggle.titanic.adapter.outbound.orm.titanic_orm import TitanicORM
from labzang.apps.data.kaggle.titanic.application.dtos.titanic_eda_dto import (
    TitanicEdaDashboardDTO,
)
from labzang.apps.data.kaggle.titanic.application.ports.input.titanic_query import (
    TitanicQueryPort,
)

logger = logging.getLogger(__name__)

_TRAIN_CSV = (
    Path(__file__).resolve().parents[2] / "resources" / "train.csv"
)


def _json_safe_number(v: Any) -> float | int | None:
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


def _describe_series(s: pd.Series) -> dict[str, float | int | None]:
    d = s.describe().to_dict()
    out: dict[str, float | int | None] = {}
    for k, v in d.items():
        out[str(k)] = _json_safe_number(v)
    return out


def _histogram_counts(
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


def _crosstab_to_records(
    ct: pd.DataFrame,
) -> dict[str, dict[str, int]]:
    ct = ct.fillna(0).astype(int)
    out: dict[str, dict[str, int]] = {}
    for idx in ct.index:
        out[str(idx)] = {str(c): int(ct.loc[idx, c]) for c in ct.columns}
    return out


def _load_train_from_db(session_factory: Callable[[], Session]) -> pd.DataFrame | None:
    session = session_factory()
    try:
        rows = (
            session.query(TitanicORM)
            .filter(TitanicORM.dataset_split == "train")
            .all()
        )
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


def _load_train_from_csv() -> pd.DataFrame:
    df = pd.read_csv(_TRAIN_CSV)
    if "Gender" in df.columns and "Sex" not in df.columns:
        df = df.rename(columns={"Gender": "Sex"})
    return df


def _feature_summary_from_db(
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


class TitanicQueryImpl(TitanicQueryPort):
    def __init__(
        self,
        session_factory: Callable[[], Session] | None = None,
    ) -> None:
        if session_factory is None:
            from labzang.core.database import SessionLocal

            self._session_factory: Callable[[], Session] = SessionLocal
        else:
            self._session_factory = session_factory

    def get_eda_dashboard(self) -> TitanicEdaDashboardDTO:
        source: Literal["database", "fallback_csv"] = "database"
        df = _load_train_from_db(self._session_factory)
        if df is None or df.empty:
            df = _load_train_from_csv()
            source = "fallback_csv"

        for col in (
            "PassengerId",
            "Survived",
            "Pclass",
            "Sex",
            "Age",
            "SibSp",
            "Parch",
            "Fare",
            "Cabin",
            "Embarked",
        ):
            if col not in df.columns:
                df[col] = np.nan

        df = df.copy()
        df["Survived"] = pd.to_numeric(df["Survived"], errors="coerce")

        missing = {}
        for col in df.columns:
            missing[str(col)] = int(df[col].isna().sum())

        surv = df["Survived"].dropna()
        vc = surv.value_counts()
        survival_ratio = {
            "dead": int(vc.get(0)),
            "survived": int(vc.get(1)),
        }

        sex_analysis = self._sex_block(df)
        pclass_analysis = self._pclass_block(df)
        age_stats = self._age_block(df)
        family_stats = self._family_block(df)
        embarked_stats = self._embarked_block(df)
        fare_stats = self._fare_block(df)

        feature_summary = _feature_summary_from_db(self._session_factory)

        return TitanicEdaDashboardDTO(
            source=source,
            row_count=len(df),
            missing_values=missing,
            survival_ratio=survival_ratio,
            sex_analysis=sex_analysis,
            pclass_analysis=pclass_analysis,
            age_stats=age_stats,
            family_stats=family_stats,
            embarked_stats=embarked_stats,
            fare_stats=fare_stats,
            feature_table_summary=feature_summary,
        )

    def _sex_block(self, df: pd.DataFrame) -> dict[str, Any]:
        sub = df.dropna(subset=["Sex", "Survived"])
        counts = sub["Sex"].astype(str).str.lower().value_counts().to_dict()
        counts = {str(k): int(v) for k, v in counts.items()}
        ct = pd.crosstab(sub["Sex"].astype(str).str.lower(), sub["Survived"])
        for col in (0, 1):
            if col not in ct.columns:
                ct[col] = 0
        rate = (
            sub.groupby(sub["Sex"].astype(str).str.lower(), as_index=True)["Survived"]
            .mean()
            .to_dict()
        )
        rate = {str(k): float(v) for k, v in rate.items()}
        return {
            "counts_by_sex": counts,
            "crosstab_sex_survived": _crosstab_to_records(ct),
            "survival_rate_by_sex": rate,
        }

    def _pclass_block(self, df: pd.DataFrame) -> dict[str, Any]:
        sub = df.dropna(subset=["Pclass", "Survived"])
        labels = sorted(sub["Pclass"].astype(int).unique().tolist())
        counts = [int((sub["Pclass"] == p).sum()) for p in labels]
        ct = pd.crosstab(sub["Pclass"], sub["Survived"])
        for col in (0, 1):
            if col not in ct.columns:
                ct[col] = 0
        mean_rate = (
            sub.groupby("Pclass", as_index=True)["Survived"].mean().to_dict()
        )
        mean_rate = {int(k): float(v) for k, v in mean_rate.items()}
        survived_row = ct.loc[:, 1].to_dict()
        dead_row = ct.loc[:, 0].to_dict()
        return {
            "labels": labels,
            "counts_per_class": counts,
            "survival_breakdown": {
                "survived": {int(k): int(survived_row.get(k, 0)) for k in labels},
                "dead": {int(k): int(dead_row.get(k, 0)) for k in labels},
            },
            "mean_survival_rate_by_pclass": mean_rate,
        }

    def _age_block(self, df: pd.DataFrame) -> dict[str, Any]:
        ages = df["Age"].dropna()
        if ages.empty:
            return {
                "describe": {},
                "histogram": {"bin_edges": [], "counts": []},
                "by_survival": {},
            }
        desc = _describe_series(ages)
        mx = float(np.nanmax(ages.to_numpy()))
        rng = (0.0, max(80.0, mx))
        hist_all = _histogram_counts(ages.to_numpy(), bins=20, range_=rng)

        out_surv: dict[str, Any] = {}
        for label, val in (("survived", 1), ("dead", 0)):
            sub = df.loc[df["Survived"] == val, "Age"].dropna()
            if sub.empty:
                out_surv[label] = {"bin_edges": [], "counts": []}
            else:
                out_surv[label] = _histogram_counts(
                    sub.to_numpy(),
                    bins=20,
                    range_=rng,
                )
        return {
            "describe": desc,
            "histogram": hist_all,
            "by_survival": out_surv,
        }

    def _family_block(self, df: pd.DataFrame) -> dict[str, Any]:
        sub = df.dropna(subset=["Survived"])
        sib_ct = pd.crosstab(sub["SibSp"], sub["Survived"])
        par_ct = pd.crosstab(sub["Parch"], sub["Survived"])
        sib_rate = (
            sub.groupby("SibSp", as_index=True)["Survived"].mean().to_dict()
        )
        par_rate = (
            sub.groupby("Parch", as_index=True)["Survived"].mean().to_dict()
        )
        return {
            "sibsp_counts": sub["SibSp"].value_counts().sort_index().to_dict(),
            "parch_counts": sub["Parch"].value_counts().sort_index().to_dict(),
            "crosstab_sibsp_survived": _crosstab_to_records(sib_ct),
            "crosstab_parch_survived": _crosstab_to_records(par_ct),
            "mean_survival_by_sibsp": {int(k): float(v) for k, v in sib_rate.items()},
            "mean_survival_by_parch": {int(k): float(v) for k, v in par_rate.items()},
        }

    def _embarked_block(self, df: pd.DataFrame) -> dict[str, Any]:
        sub = df.dropna(subset=["Embarked", "Survived"])
        counts = sub["Embarked"].astype(str).value_counts().to_dict()
        counts = {str(k): int(v) for k, v in counts.items()}
        rate = (
            sub.groupby("Embarked", as_index=True)["Survived"].mean().to_dict()
        )
        rate = {str(k): float(v) for k, v in rate.items()}
        pclass_ct = pd.crosstab(sub["Embarked"], sub["Pclass"])
        pclass_nested: dict[str, dict[str, int]] = {}
        for idx in pclass_ct.index:
            pclass_nested[str(idx)] = {
                str(int(c)): int(pclass_ct.loc[idx, c]) for c in pclass_ct.columns
            }

        sibsp_by_port: dict[str, dict[str, int]] = {}
        parch_by_port: dict[str, dict[str, int]] = {}
        for port in sub["Embarked"].unique():
            ps = str(port)
            part = sub[sub["Embarked"] == port]
            sibsp_by_port[ps] = {
                str(int(k)): int(v)
                for k, v in part["SibSp"].value_counts().sort_index().items()
            }
            parch_by_port[ps] = {
                str(int(k)): int(v)
                for k, v in part["Parch"].value_counts().sort_index().items()
            }

        return {
            "counts_by_port": counts,
            "survival_rates_by_port": rate,
            "pclass_by_port": pclass_nested,
            "sibsp_distribution_by_port": sibsp_by_port,
            "parch_distribution_by_port": parch_by_port,
        }

    def _fare_block(self, df: pd.DataFrame) -> dict[str, Any]:
        sub = df.dropna(subset=["Fare", "Survived"])
        fares = sub["Fare"].to_numpy(dtype=float)
        mx = float(np.nanmax(fares)) if np.size(fares) else 100.0
        rng = (0.0, min(max(mx, 1.0), 600.0))
        hist_all = _histogram_counts(fares, bins=40, range_=rng)
        out: dict[str, Any] = {"histogram": hist_all}
        for label, val in (("survived", 1), ("dead", 0)):
            fv = sub.loc[sub["Survived"] == val, "Fare"].dropna().to_numpy()
            if fv.size == 0:
                out[label] = {"bin_edges": [], "counts": []}
            else:
                out[label] = _histogram_counts(fv, bins=40, range_=rng)
        out["sample_fares_by_survival"] = {
            "survived": sub.loc[sub["Survived"] == 1, "Fare"]
            .dropna()
            .head(500)
            .tolist(),
            "dead": sub.loc[sub["Survived"] == 0, "Fare"]
            .dropna()
            .head(500)
            .tolist(),
        }
        return out
