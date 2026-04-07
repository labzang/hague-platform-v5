"""서울 자치구 인구 엑셀(raw) → DataFrame (`header=2`, 열 B,D,G,J,N)."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def _read_csv_any_encoding(path: Path) -> pd.DataFrame:
    for enc in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"CSV 인코딩을 판별할 수 없습니다: {path}")


class PopSeoulReader:
    """엑셀 원본 경로(`fname`)를 두고 `xls_to_dframe`으로 표를 읽는다."""

    def __init__(self, fname: str | Path | None = None) -> None:
        self.fname: str | Path | None = fname
        self.df: pd.DataFrame | None = None

    def xls_to_dframe(
        self,
        header: int = 2,
        usecols: str = "B,D,G,J,N",
        *,
        sheet_name: str | int = 0,
    ) -> pd.DataFrame:
        """서울시 인구 통계 엑셀에서 자치구·인구·한국인·외국인·고령자 열만 읽는다."""
        if self.fname is None:
            raise ValueError("fname이 설정되지 않았습니다.")
        path = Path(self.fname)
        if not path.is_file():
            raise FileNotFoundError(str(path))

        suffix = path.suffix.lower()
        if suffix == ".xls":
            engine = "xlrd"
        elif suffix in (".xlsx", ".xlsm"):
            engine = "openpyxl"
        else:
            raise ValueError(
                "xls_to_dframe은 .xls / .xlsx / .xlsm 에만 사용하세요. "
                f"받은 확장자: {suffix!r}"
            )

        self.df = pd.read_excel(
            path,
            sheet_name=sheet_name,
            header=header,
            usecols=usecols,
            engine=engine,
        )
        return self.df


class PopInSeoulImportService:
    """업로드 파일 → `pop_in_seoul.csv` 형식으로 저장."""

    OUTPUT_COLUMNS = ["자치구", "인구수", "한국인", "외국인", "고령자"]

    def __init__(self, reader: PopSeoulReader | None = None) -> None:
        self.reader = reader or PopSeoulReader()

    def load_from_excel(self, path: Path) -> pd.DataFrame:
        self.reader.fname = path
        df = self.reader.xls_to_dframe()
        if df.shape[1] != len(self.OUTPUT_COLUMNS):
            raise ValueError(
                f"열 개수가 기대(5)와 다릅니다: {df.shape[1]} — usecols B,D,G,J,N 확인"
            )
        df = df.copy()
        df.columns = self.OUTPUT_COLUMNS
        return df

    def load_from_csv(self, path: Path) -> pd.DataFrame:
        """이미 정제된 `pop_in_seoul` 형 CSV를 읽는다."""
        return _read_csv_any_encoding(path)

    def ingest_to_dataframe(self, path: Path) -> pd.DataFrame:
        suffix = path.suffix.lower()
        if suffix in (".xls", ".xlsx", ".xlsm"):
            return self.load_from_excel(path)
        if suffix == ".csv":
            return self.load_from_csv(path)
        raise ValueError(f"지원하지 않는 형식입니다: {suffix}")

    def save_processed_csv(self, df: pd.DataFrame, out_path: Path) -> None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=False, encoding="utf-8-sig")

    def ingest_and_save(
        self,
        source_path: Path,
        out_path: Path,
    ) -> dict[str, Any]:
        df = self.ingest_to_dataframe(source_path)
        self.save_processed_csv(df, out_path)
        preview = df.head(5)
        return {
            "path": str(out_path.resolve()),
            "shape": [int(df.shape[0]), int(df.shape[1])],
            "columns": df.columns.tolist(),
            "preview": preview.to_dict(orient="records"),
        }
