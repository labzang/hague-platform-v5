"""
서울 범죄 아웃바운드 어댑터 (ISeoulDataPort, ISeoulPreprocessorPort, IGeocodePort 구현)
"""
import io
import logging
import os
from pathlib import Path
from typing import Any, List

import pandas as pd

from domain.ports import (
    ISeoulDataPort,
    ISeoulPreprocessorPort,
    IGeocodePort,
)

logger = logging.getLogger(__name__)


# --- ISeoulDataPort ---
class SeoulDataAdapter(ISeoulDataPort):
    def __init__(self, data_dir: Path, save_dir: Path):
        self._data_dir = Path(data_dir)
        self._save_dir = Path(save_dir)

    def get_data_dir(self) -> str:
        return str(self._data_dir)

    def get_save_dir(self) -> str:
        return str(self._save_dir)

    def load_cctv(self) -> Any:
        path = self._data_dir / "cctv.csv"
        if not path.exists():
            raise FileNotFoundError(f"cctv.csv 없음: {path}")
        return pd.read_csv(path, encoding="utf-8")

    def load_crime(self) -> Any:
        path = self._data_dir / "crime.csv"
        if not path.exists():
            raise FileNotFoundError(f"crime.csv 없음: {path}")
        return pd.read_csv(path, encoding="utf-8")

    def load_pop(self) -> Any:
        path = self._data_dir / "pop.xls"
        if not path.exists():
            raise FileNotFoundError(f"pop.xls 없음: {path}")
        return pd.read_excel(path)

    def save_crime(self, crime_df: Any) -> str:
        self._save_dir.mkdir(parents=True, exist_ok=True)
        out_file = self._save_dir / "crime.csv"
        csv_buffer = io.StringIO()
        crime_df.to_csv(csv_buffer, index=False, encoding=None)
        csv_content = csv_buffer.getvalue()
        with open(out_file, "w", encoding="utf-8-sig") as f:
            f.write(csv_content)
        logger.info("crime 저장 완료 (UTF-8 BOM): %s", out_file)
        return str(out_file)


# --- ISeoulPreprocessorPort ---
class SeoulPreprocessorAdapter(ISeoulPreprocessorPort):
    def csv_to_df(self, path: str) -> Any:
        return pd.read_csv(path, encoding="utf-8")

    def xlsx_to_df(self, path: str) -> Any:
        return pd.read_excel(path)

    def df_merge(
        self,
        left: Any,
        right: Any,
        left_on: str,
        right_on: str,
        how: str = "inner",
    ) -> Any:
        merged = pd.merge(
            left, right, left_on=left_on, right_on=right_on, how=how, suffixes=("", "_y")
        )
        duplicate_cols = [c for c in merged.columns if c.endswith("_y")]
        for col in duplicate_cols:
            if col[:-2] in merged.columns:
                merged = merged.drop(columns=[col])
        return merged

    def drop_columns(self, df: Any, columns: List[str]) -> Any:
        return df.drop(columns=[c for c in columns if c in df.columns], errors="ignore")

    def drop_cctv_columns(self, cctv_df: Any, columns: List[str]) -> Any:
        return self.drop_columns(cctv_df, columns)

    def filter_pop_columns_and_rows(self, pop_df: Any) -> Any:
        if len(pop_df.columns) < 4:
            raise ValueError(f"pop 컬럼 부족: {len(pop_df.columns)}")
        cols = [pop_df.columns[1], pop_df.columns[3]]
        pop_df = pop_df[cols].copy()
        if len(pop_df) >= 4:
            pop_df = pop_df.drop(pop_df.index[1:4]).reset_index(drop=True)
        return pop_df

    def get_station_names_from_crime(self, crime_df: Any) -> List[str]:
        result = []
        if "관서명" not in crime_df.columns:
            return result
        for name in crime_df["관서명"]:
            result.append("서울" + str(name)[:-1] + "경찰서")
        return result

    def add_gu_to_crime(self, crime_df: Any, gu_list: List[str]) -> Any:
        out = crime_df.copy()
        n = len(out)
        if len(gu_list) == n:
            out["자치구"] = gu_list
        elif len(gu_list) > n:
            out["자치구"] = gu_list[:n]
        else:
            out["자치구"] = gu_list + [""] * (n - len(gu_list))
        return out

    def order_crime_columns(self, crime_df: Any, desired_cols: List[str]) -> Any:
        ordered = [c for c in desired_cols if c in crime_df.columns]
        rest = [c for c in crime_df.columns if c not in ordered]
        return crime_df[ordered + rest]

    def head_to_dict(self, df: Any, n: int = 3) -> List[dict]:
        return df.head(n).to_dict(orient="records")


# --- IGeocodePort (카카오맵) ---
class KakaoGeocodeAdapter(IGeocodePort):
    def __init__(self, api_key: str | None = None):
        self._api_key = api_key or self._retrieve_api_key()
        self._base_url = "https://dapi.kakao.com/v2/local"

    def _retrieve_api_key(self) -> str:
        key = os.getenv("KAKAO_REST_API_KEY") or os.getenv("KAKAO_API_KEY")
        if key:
            return key
        try:
            from dotenv import load_dotenv
            base = Path(__file__).resolve().parent.parent.parent.parent
            for p in [base / ".env", base.parent / ".env", Path(".env")]:
                if p.exists():
                    load_dotenv(p)
                    break
            else:
                load_dotenv()
        except ImportError:
            pass
        key = os.getenv("KAKAO_REST_API_KEY") or os.getenv("KAKAO_API_KEY")
        if not key:
            raise ValueError(
                "KAKAO_REST_API_KEY 또는 KAKAO_API_KEY 환경 변수를 설정해주세요."
            )
        return key

    def geocode(self, query: str, language: str = "ko") -> List[dict]:
        try:
            import requests
        except ImportError:
            logger.warning("requests 미설치로 카카오 지오코딩 스킵")
            return []
        url = f"{self._base_url}/search/keyword.json"
        headers = {"Authorization": f"KakaoAK {self._api_key}"}
        params = {"query": query}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            docs = data.get("documents", [])
            if not docs:
                return []
            result: List[dict] = []
            for doc in docs:
                addr = (
                    doc.get("address_name")
                    or doc.get("road_address_name")
                    or doc.get("place_name")
                    or ""
                )
                y, x = float(doc.get("y", 0)), float(doc.get("x", 0))
                result.append({
                    "formatted_address": addr,
                    "lat": y,
                    "lng": x,
                })
            return result
        except Exception as e:
            logger.warning("카카오 지오코딩 실패 %s: %s", query, e)
            return []
