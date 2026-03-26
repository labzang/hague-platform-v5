"""CCTV CSV 로드 및 수치 열 상관 행렬(매트릭스) 산출."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def _read_csv(path: Path) -> pd.DataFrame:
    for enc in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"CSV 인코딩을 판별할 수 없습니다: {path}")


class CctvCsvReader:
    """업로드·저장된 경로의 CSV를 DataFrame으로 읽는다."""

    def __init__(self, fname: str | Path | None = None) -> None:
        self.fname: str | Path | None = fname
        self.df: pd.DataFrame | None = None

    def csv_to_dframe(self) -> pd.DataFrame:
        if self.fname is None:
            raise ValueError("fname이 설정되지 않았습니다.")
        path = Path(self.fname)
        if not path.is_file():
            raise FileNotFoundError(str(path))
        self.df = _read_csv(path)
        return self.df


class CctvMatrixService:
    """``reader.fname`` → ``csv_to_dframe()`` → 수치 열 상관계수 행렬."""

    def __init__(self, reader: CctvCsvReader | None = None) -> None:
        self.reader = reader or CctvCsvReader()

    def create_matrix(self, fname: str | Path) -> dict[str, Any]:
        fname = Path(fname)
        logger.info("cctv csv file: %s", fname)
        self.reader.fname = fname
        df = self.reader.csv_to_dframe()

        numeric = df.select_dtypes(include=["number"])
        correlation: dict[str, dict[str, float | None]] | None = None
        if numeric.shape[1] >= 2:
            corr = numeric.corr().round(8)
            correlation = {
                str(idx): {
                    str(c): (None if pd.isna(v) else float(v))
                    for c, v in row.items()
                }
                for idx, row in corr.iterrows()
            }

        preview = df.head(5)
        return {
            "path": str(fname.resolve()),
            "shape": [int(df.shape[0]), int(df.shape[1])],
            "columns": df.columns.tolist(),
            "preview": preview.to_dict(orient="records"),
            "numeric_columns": numeric.columns.tolist(),
            "correlation_matrix": correlation,
        }
