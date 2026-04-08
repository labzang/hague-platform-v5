from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import folium
import numpy as np
import pandas as pd
from sklearn import preprocessing

from labzang.apps.dash.council.illustrator.folium.app.ports.input.seoul_crime_command_port import (
    SeoulCrimeCommandPort,
)


@dataclass
class SeoulCrimeMapResult:
    map_html: str
    saved_files: dict[str, str]
    summary: dict[str, Any]


class SeoulCrimeCommandImpl(SeoulCrimeCommandPort):
    """서울 범죄 Command 유스케이스 구현체."""

    def __init__(
        self,
        *,
        processed_dir: Path,
        raw_dir: Path,
        geocoder: Any | None = None,
    ) -> None:
        self.processed_dir = processed_dir
        self.raw_dir = raw_dir
        self.geocoder = geocoder

        self.cctv: pd.DataFrame | None = None
        self.crime: pd.DataFrame | None = None
        self.pop: pd.DataFrame | None = None
        self.police: pd.DataFrame | None = None
        self.police_norm: pd.DataFrame | None = None

    @staticmethod
    def _read_csv_flexible(path: Path) -> pd.DataFrame:
        for enc in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
            try:
                return pd.read_csv(path, encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError(f"CSV 인코딩 판별 실패: {path}")

    def _load_inputs(self) -> None:
        self.cctv = self._read_csv_flexible(self.processed_dir / "cctv_in_seoul.csv")
        self.crime = self._read_csv_flexible(self.processed_dir / "crime_in_seoul.csv")
        self.pop = self._read_csv_flexible(self.processed_dir / "pop_in_seoul.csv")

    def update_cctv(self) -> "SeoulCrimeMapUseCase":
        if self.cctv is None:
            raise ValueError("cctv 데이터가 없습니다")
        cctv = self.cctv.copy()
        cctv = cctv.drop(
            columns=["2013년도 이전", "2014년", "2015년", "2016년"],
            errors="ignore",
        )
        if "기관명" in cctv.columns:
            cctv = cctv.rename(columns={"기관명": "자치구"})
        cctv.to_csv(
            self.processed_dir / "cctv_in_seoul.csv", index=False, encoding="utf-8-sig"
        )
        self.cctv = cctv
        return self

    @staticmethod
    def _extract_gu(addr: str) -> str:
        for token in str(addr).split():
            if token.endswith("구"):
                return token
        return ""

    def update_crime(self, *, force_geocode: bool = False) -> "SeoulCrimeMapUseCase":
        if self.crime is None:
            raise ValueError("crime 데이터가 없습니다")

        crime = self.crime.copy()
        has_gu = "자치구" in crime.columns and crime["자치구"].notna().any()

        if (
            (not has_gu or force_geocode)
            and self.geocoder is not None
            and "관서명" in crime.columns
        ):
            station_names = [f"서울{str(name)[:-1]}경찰서" for name in crime["관서명"]]
            gu_names: list[str] = []
            for name in station_names:
                results = self.geocoder.geocode(name, language="ko")
                addr = ""
                if results:
                    addr = str(results[0].get("formatted_address", ""))
                gu_names.append(self._extract_gu(addr))
            crime["자치구"] = gu_names

        if "관서명" in crime.columns and "자치구" in crime.columns:
            # 원본 코드의 '==' 오타를 '=' 대입으로 보정
            crime.loc[crime["관서명"] == "혜화서", "자치구"] = "종로구"
            crime.loc[crime["관서명"] == "서부서", "자치구"] = "은평구"
            crime.loc[crime["관서명"] == "강서서", "자치구"] = "양천구"
            crime.loc[crime["관서명"] == "종암서", "자치구"] = "성북구"
            crime.loc[crime["관서명"] == "방배서", "자치구"] = "서초구"
            crime.loc[crime["관서명"] == "수서서", "자치구"] = "강남구"

        crime.to_csv(
            self.processed_dir / "crime_in_seoul.csv", index=False, encoding="utf-8-sig"
        )
        self.crime = crime
        return self

    def update_pop(self) -> "SeoulCrimeMapUseCase":
        if self.pop is None:
            raise ValueError("pop 데이터가 없습니다")
        pop = self.pop.copy()
        if "자치구" in pop.columns:
            pop = pop[pop["자치구"] != "합계"].reset_index(drop=True)
        expected = ["자치구", "인구수", "한국인", "외국인", "고령자"]
        if len(pop.columns) >= 5:
            col_map = {pop.columns[i]: expected[i] for i in range(5)}
            pop = pop.rename(columns=col_map)
        pop.to_csv(
            self.processed_dir / "pop_in_seoul.csv", index=False, encoding="utf-8-sig"
        )
        self.pop = pop
        return self

    @staticmethod
    def _safe_ratio(num: pd.Series, den: pd.Series) -> pd.Series:
        den = den.replace(0, np.nan)
        out = (num.astype(float) / den.astype(float)) * 100
        return out.fillna(0)

    def update_police(self) -> "SeoulCrimeMapUseCase":
        if self.crime is None:
            raise ValueError("crime 데이터가 없습니다")
        if self.cctv is None:
            raise ValueError("cctv 데이터가 없습니다")
        if self.pop is None:
            raise ValueError("pop 데이터가 없습니다")

        crime = self.crime.copy()
        if "자치구" not in crime.columns:
            raise ValueError("crime_in_seoul.csv에 자치구 컬럼이 필요합니다")

        grouped = crime.groupby("자치구", as_index=False).sum(numeric_only=True)

        police = grouped.copy()
        police["살인검거율"] = self._safe_ratio(police["살인 검거"], police["살인 발생"])
        police["강도검거율"] = self._safe_ratio(police["강도 검거"], police["강도 발생"])
        police["강간검거율"] = self._safe_ratio(police["강간 검거"], police["강간 발생"])
        police["절도검거율"] = self._safe_ratio(police["절도 검거"], police["절도 발생"])
        police["폭력검거율"] = self._safe_ratio(police["폭력 검거"], police["폭력 발생"])
        police = police.drop(
            columns=["살인 검거", "강도 검거", "강간 검거", "절도 검거", "폭력 검거"],
            errors="ignore",
        )
        for c in ["살인검거율", "강도검거율", "강간검거율", "절도검거율", "폭력검거율"]:
            police.loc[police[c] > 100, c] = 100

        police = police.rename(
            columns={
                "살인 발생": "살인",
                "강도 발생": "강도",
                "강간 발생": "강간",
                "절도 발생": "절도",
                "폭력 발생": "폭력",
            }
        )

        crime_cols = ["살인", "강도", "강간", "절도", "폭력"]
        scaler = preprocessing.MinMaxScaler()
        x_scaled = scaler.fit_transform(police[crime_cols].astype(float).values)
        police_norm = pd.DataFrame(x_scaled, columns=crime_cols)
        police_norm.insert(0, "자치구", police["자치구"].values)

        rate_cols = ["살인검거율", "강도검거율", "강간검거율", "절도검거율", "폭력검거율"]
        for c in rate_cols:
            police_norm[c] = police[c].values

        police_norm["범죄"] = police_norm[crime_cols].sum(axis=1)
        police_norm["검거"] = police_norm[rate_cols].sum(axis=1)

        merged = police_norm.merge(self.pop[["자치구", "인구수"]], on="자치구", how="left")
        merged = merged.merge(
            self.cctv[["자치구", "소계"]].rename(columns={"소계": "CCTV"}),
            on="자치구",
            how="left",
        )

        police.to_csv(
            self.processed_dir / "police_in_seoul.csv", index=False, encoding="utf-8-sig"
        )
        merged.to_csv(
            self.processed_dir / "police_norm_in_seoul.csv",
            index=False,
            encoding="utf-8-sig",
        )

        self.police = police
        self.police_norm = merged
        return self

    def _load_geo(self) -> dict[str, Any]:
        with (self.raw_dir / "geo_simple.json").open("r", encoding="utf-8") as f:
            return json.load(f)

    def render_map_html(self) -> str:
        if self.police_norm is None:
            raise ValueError("police_norm 데이터가 없습니다")

        m = folium.Map(
            location=[37.5502, 126.982], zoom_start=11, tiles="cartodbpositron"
        )
        folium.Choropleth(
            geo_data=self._load_geo(),
            data=self.police_norm,
            columns=["자치구", "범죄"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Seoul Crime Score",
        ).add_to(m)
        return m._repr_html_()

    # ---- SeoulCrimeCommandPort 구현 ----
    def ingest_raw_files(self) -> dict[str, str]:
        """
        현재 raw/processed 입력 파일의 존재 여부를 점검해 반환한다.
        (실제 업로드/저장은 인바운드 라우터에서 수행)
        """
        files = {
            "cctv": str((self.processed_dir / "cctv_in_seoul.csv").resolve()),
            "crime": str((self.processed_dir / "crime_in_seoul.csv").resolve()),
            "pop": str((self.processed_dir / "pop_in_seoul.csv").resolve()),
        }
        missing = [name for name, path in files.items() if not Path(path).exists()]
        if missing:
            raise FileNotFoundError(f"입력 파일이 없습니다: {', '.join(missing)}")
        return files

    def preprocess(self, *, force_geocode: bool = False) -> dict[str, Any]:
        self._load_inputs()
        self.update_cctv().update_pop().update_crime(
            force_geocode=force_geocode
        ).update_police()
        if self.crime is None or self.police_norm is None:
            raise ValueError("전처리 결과가 비어 있습니다")
        return {
            "crime_rows": int(len(self.crime)),
            "police_norm_rows": int(len(self.police_norm)),
            "gu_count": int(self.police_norm["자치구"].nunique()),
            "saved_files": {
                "cctv": str((self.processed_dir / "cctv_in_seoul.csv").resolve()),
                "crime": str((self.processed_dir / "crime_in_seoul.csv").resolve()),
                "pop": str((self.processed_dir / "pop_in_seoul.csv").resolve()),
                "police": str((self.processed_dir / "police_in_seoul.csv").resolve()),
                "police_norm": str(
                    (self.processed_dir / "police_norm_in_seoul.csv").resolve()
                ),
            },
        }

    def rebuild_police_norm(self) -> dict[str, Any]:
        self._load_inputs()
        self.update_police()
        if self.police_norm is None:
            raise ValueError("police_norm 데이터가 없습니다")
        return {
            "police_norm_rows": int(len(self.police_norm)),
            "gu_count": int(self.police_norm["자치구"].nunique()),
            "saved_to": str((self.processed_dir / "police_norm_in_seoul.csv").resolve()),
        }

    def generate_map(self) -> dict[str, Any]:
        # preprocess가 아직 수행되지 않았다면 안전하게 실행
        if self.police_norm is None:
            self.preprocess(force_geocode=False)
        html = self.render_map_html()
        if self.police_norm is None:
            raise ValueError("지도 생성을 위한 데이터가 없습니다")
        return {
            "map_html": html,
            "police_norm_rows": int(len(self.police_norm)),
            "gu_count": int(self.police_norm["자치구"].nunique()),
        }

    def execute(self, *, force_geocode: bool = False) -> SeoulCrimeMapResult:
        pre = self.preprocess(force_geocode=force_geocode)
        gen = self.generate_map()
        if self.police_norm is None or self.crime is None:
            raise ValueError("지도 생성을 위한 데이터가 없습니다")

        return SeoulCrimeMapResult(
            map_html=str(gen["map_html"]),
            saved_files=dict(pre["saved_files"]),
            summary={
                "crime_rows": int(len(self.crime)),
                "police_norm_rows": int(len(self.police_norm)),
                "gu_count": int(self.police_norm["자치구"].nunique()),
            },
        )


# 하위 호환 이름 유지 (기존 라우터 import 경로 대응)
SeoulCrimeMapUseCase = SeoulCrimeCommandImpl
