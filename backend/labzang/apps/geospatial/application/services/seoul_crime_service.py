"""
서울시 범죄 현황 분석 — 노트북 스크립트를 SeoulCrimeService OOP로 구성.
- 데이터 경로·HTML 출력·Google Maps API 키는 생성자/환경에서 주입 (하드코딩 금지).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import googlemaps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import font_manager, rc
from sklearn import preprocessing

import folium


@dataclass
class SeoulCrimePipelineResult:
    """전처리·정규화까지의 주요 산출물."""

    crime_by_station: pd.DataFrame
    police_by_gu: pd.DataFrame
    police_norm: pd.DataFrame
    police_norm_sort_arrest: pd.DataFrame
    police_norm_sort_crime: pd.DataFrame
    police_position: pd.DataFrame
    intermediate_csv: Optional[Path] = None


class SeoulCrimeService:
    """
    서울 경찰서 단위 범죄 CSV → 지오코딩·구 단위 집계 → 정규화·CCTV/인구 머지 → (선택) 시각화/HTML 저장.
    """

    _CRIME_OCC_COLS = ["강간", "강도", "절도", "살인", "폭력"]
    _ARREST_RATE_COLS = [
        "강간검거율",
        "강도검거율",
        "절도검거율",
        "살인검거율",
        "폭력검거율",
    ]

    def __init__(
        self,
        data_dir: str | Path,
        html_dir: str | Path | None = None,
        *,
        gmaps_api_key: str | None = None,
        gmaps_client: Any | None = None,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.html_dir = Path(html_dir) if html_dir else self.data_dir.parent / "html"
        key = gmaps_api_key or os.environ.get("GOOGLE_MAPS_API_KEY")
        self._gmaps_client = gmaps_client or (
            googlemaps.Client(key=key) if key else None
        )
        self.station_lat: list[float] = []
        self.station_lng: list[float] = []
        self.station_address: list[str] = []

    def _require_gmaps(self) -> googlemaps.Client:
        if self._gmaps_client is None:
            raise ValueError(
                "Google Maps 클라이언트가 없습니다. gmaps_api_key 또는 gmaps_client를 넘기거나 "
                "환경변수 GOOGLE_MAPS_API_KEY를 설정하세요."
            )
        return self._gmaps_client

    @staticmethod
    def _extract_gu_from_address(formatted_address: str) -> str:
        if not formatted_address:
            return ""
        for token in formatted_address.split():
            if len(token) > 0 and token[-1] == "구":
                return token
        return ""

    def _configure_korean_font(self) -> None:
        """Windows 맑은 고딕 우선, 실패 시 seaborn 기본."""
        try:
            path = "C:/Windows/Fonts/malgun.ttf"
            if Path(path).is_file():
                name = font_manager.FontProperties(fname=path).get_name()
                rc("font", family=name)
        except OSError:
            pass
        plt.rcParams["axes.unicode_minus"] = False

    def load_crime_in_seoul(self, filename: str = "crime_in_seoul.csv") -> pd.DataFrame:
        path = self.data_dir / filename
        return pd.read_csv(path, thousands=",", encoding="euc-kr")

    def build_station_queries(self, crime_df: pd.DataFrame) -> list[str]:
        names: list[str] = []
        for raw in crime_df["관서명"]:
            names.append("서울" + str(raw[:-1]) + "경찰서")
        return names

    def geocode_stations(self, station_names: list[str]) -> None:
        """경찰서명 지오코딩 결과를 인스턴스에 저장."""
        gmaps = self._require_gmaps()
        self.station_address = []
        self.station_lat = []
        self.station_lng = []
        for name in station_names:
            tmp = gmaps.geocode(name, language="ko")
            if not tmp:
                self.station_address.append("")
                self.station_lat.append(float("nan"))
                self.station_lng.append(float("nan"))
                continue
            first = tmp[0]
            self.station_address.append(first.get("formatted_address") or "")
            loc = first.get("geometry", {}).get("location", {})
            self.station_lat.append(float(loc.get("lat", float("nan"))))
            self.station_lng.append(float(loc.get("lng", float("nan"))))

    def attach_gu_column(self, crime_df: pd.DataFrame) -> pd.DataFrame:
        out = crime_df.copy()
        gu_name = [
            self._extract_gu_from_address(addr) for addr in self.station_address
        ]
        out["구별"] = gu_name
        return out

    @staticmethod
    def apply_geumcheon_exception(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out.loc[out["관서명"] == "금천서", ["구별"]] = "금천구"
        return out

    def save_crime_anal_police(
        self, df: pd.DataFrame, filename: str = "crime_anal_police2.csv"
    ) -> Path:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        path = self.data_dir / filename
        df.to_csv(path, index=False)
        return path

    def load_crime_anal_police(self, filename: str = "crime_anal_police2.csv") -> pd.DataFrame:
        return pd.read_csv(self.data_dir / filename)

    def pivot_by_gu(self, crime_df: pd.DataFrame) -> pd.DataFrame:
        return pd.pivot_table(crime_df, index="구별", aggfunc=np.sum)

    def compute_police_metrics(self, police: pd.DataFrame) -> pd.DataFrame:
        p = police.copy()
        p["강간검거율"] = p["강간 검거"] / p["강간 발생"] * 100
        p["강도검거율"] = p["강도 검거"] / p["강도 발생"] * 100
        p["절도검거율"] = p["절도 검거"] / p["절도 발생"] * 100
        p["살인검거율"] = p["살인 검거"] / p["살인 발생"] * 100
        p["폭력검거율"] = p["폭력 검거"] / p["폭력 발생"] * 100
        for col in [
            "강간 검거",
            "강도 검거",
            "절도 검거",
            "살인 검거",
            "폭력 검거",
        ]:
            del p[col]
        for col in self._ARREST_RATE_COLS:
            p.loc[p[col] > 100, col] = 100
        p.rename(
            columns={
                "강간 발생": "강간",
                "강도 발생": "강도",
                "절도 발생": "절도",
                "살인 발생": "살인",
                "폭력 발생": "폭력",
            },
            inplace=True,
        )
        return p

    def normalize_crime_counts(self, police: pd.DataFrame) -> pd.DataFrame:
        col = self._CRIME_OCC_COLS
        scaler = preprocessing.MinMaxScaler()
        x_scaled = scaler.fit_transform(police[col].values.astype(float))
        police_norm = pd.DataFrame(
            x_scaled, columns=col, index=police.index.copy()
        )
        for c in self._ARREST_RATE_COLS:
            police_norm[c] = police[c]
        return police_norm

    def load_cctv_merge_pop(self, filename: str = "cctv_merge_pop.csv") -> pd.DataFrame:
        return pd.read_csv(self.data_dir / filename, index_col="구별")

    def merge_cctv_into_police_norm(
        self, police_norm: pd.DataFrame, cctv_merge_pop: pd.DataFrame
    ) -> pd.DataFrame:
        out = police_norm.copy()
        out["범죄"] = np.sum(out[self._CRIME_OCC_COLS], axis=1)
        out["검거"] = np.sum(out[self._ARREST_RATE_COLS], axis=1)
        out[["인구수", "CCTV"]] = cctv_merge_pop[["인구수", "소계"]]
        return out

    def normalize_arrest_total_score(self, police_norm: pd.DataFrame) -> pd.DataFrame:
        out = police_norm.copy()
        m = out["검거"].max()
        if m and m > 0:
            out["검거"] = out["검거"] / m * 100
        return out

    def sort_by_column(
        self, df: pd.DataFrame, col: str, *, ascending: bool = False
    ) -> pd.DataFrame:
        return df.sort_values(by=col, ascending=ascending)

    def load_police_position(self, filename: str = "police_position.csv") -> pd.DataFrame:
        return pd.read_csv(self.data_dir / filename)

    def attach_station_coords(self, police_position: pd.DataFrame) -> pd.DataFrame:
        out = police_position.copy()
        out["lat"] = self.station_lat
        out["lng"] = self.station_lng
        return out

    def compute_police_position_score(self, police_position: pd.DataFrame) -> pd.DataFrame:
        out = police_position.copy()
        col = ["살인 검거", "강도 검거", "강간 검거", "절도 검거", "폭력 검거"]
        tmp = out[col] / out[col].max()
        out["검거"] = np.sum(tmp, axis=1)
        return out

    def load_geo_json(self, filename: str = "geo_simple.json") -> dict[str, Any]:
        path = self.data_dir / filename
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    # --- 시각화 / HTML (선택 실행) ---

    def save_pairplot_crime_triplet(
        self,
        police_norm: pd.DataFrame,
        filename: str = "pairplot_crime_triplet.png",
        *,
        show: bool = False,
    ) -> Path:
        self._configure_korean_font()
        self.html_dir.mkdir(parents=True, exist_ok=True)
        out = self.html_dir.parent / "plots" / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        sns.pairplot(
            police_norm,
            vars=["강도", "살인", "폭력"],
            kind="reg",
            height=3,
        )
        plt.tight_layout()
        plt.savefig(out, dpi=150, bbox_inches="tight")
        if show:
            plt.show()
        plt.close()
        return out

    def save_pairplot_pop_cctv_vs_crime(
        self,
        police_norm: pd.DataFrame,
        filename: str = "pairplot_pop_cctv_crime.png",
        *,
        show: bool = False,
    ) -> Path:
        self._configure_korean_font()
        out = self.html_dir.parent / "plots" / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        sns.pairplot(
            police_norm,
            x_vars=["인구수", "CCTV"],
            y_vars=["살인", "강도"],
            kind="reg",
            height=3,
        )
        plt.tight_layout()
        plt.savefig(out, dpi=150, bbox_inches="tight")
        if show:
            plt.show()
        plt.close()
        return out

    def save_pairplot_pop_cctv_vs_arrest(
        self,
        police_norm: pd.DataFrame,
        filename: str = "pairplot_pop_cctv_arrest.png",
        *,
        show: bool = False,
    ) -> Path:
        self._configure_korean_font()
        out = self.html_dir.parent / "plots" / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        sns.pairplot(
            police_norm,
            x_vars=["인구수", "CCTV"],
            y_vars=["강간검거율", "폭력검거율"],
            kind="reg",
            height=3,
        )
        plt.tight_layout()
        plt.savefig(out, dpi=150, bbox_inches="tight")
        if show:
            plt.show()
        plt.close()
        return out

    def save_heatmap_arrest_rates(
        self,
        police_norm_sort: pd.DataFrame,
        filename: str = "heatmap_arrest.png",
        *,
        show: bool = False,
    ) -> Path:
        self._configure_korean_font()
        out = self.html_dir.parent / "plots" / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        target_col = self._ARREST_RATE_COLS
        plt.figure(figsize=(10, 10))
        sns.heatmap(
            police_norm_sort[target_col], annot=True, fmt="f", linewidths=0.5
        )
        plt.title("범죄 검거 비율(정규화된 검거의 합으로 정렬)")
        plt.tight_layout()
        plt.savefig(out, dpi=150, bbox_inches="tight")
        if show:
            plt.show()
        plt.close()
        return out

    def save_heatmap_crime_rates(
        self,
        police_norm: pd.DataFrame,
        filename: str = "heatmap_crime.png",
        *,
        show: bool = False,
    ) -> Path:
        self._configure_korean_font()
        df = police_norm.copy()
        df["범죄"] = df["범죄"] / 5
        df_sort = df.sort_values(by="범죄", ascending=False)
        target_col = [*self._CRIME_OCC_COLS, "범죄"]
        out = self.html_dir.parent / "plots" / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        plt.figure(figsize=(10, 10))
        sns.heatmap(df_sort[target_col], annot=True, fmt="f", linewidths=0.5)
        plt.title("범죄 비율(정규화된 발생건수로 정렬)")
        plt.tight_layout()
        plt.savefig(out, dpi=150, bbox_inches="tight")
        if show:
            plt.show()
        plt.close()
        return out

    def save_folium_base_map(
        self,
        filename: str = "seoul_area.html",
        *,
        location: tuple[float, float] = (37.5502, 126.982),
        zoom_start: int = 12,
    ) -> Path:
        self.html_dir.mkdir(parents=True, exist_ok=True)
        path = self.html_dir / filename
        m = folium.Map(location=list(location), zoom_start=zoom_start)
        m.save(str(path))
        return path

    def _choropleth_map(
        self,
        geo_data: dict[str, Any],
        series: pd.Series,
        *,
        fill_color: str = "PuRd",
        tiles: str = "Stamen Toner",
    ) -> folium.Map:
        m = folium.Map(
            location=[37.5502, 126.982], zoom_start=12, tiles=tiles
        )
        if series.index.name is None:
            series = series.copy()
            series.index.name = "구별"
        data_df = series.reset_index()
        # pivot 인덱스 이름이 없으면 첫 컬럼이 구명
        cols = list(data_df.columns)
        if len(cols) < 2:
            raise ValueError("choropleth용 Series는 구별 인덱스가 필요합니다.")
        folium.Choropleth(
            geo_data=geo_data,
            data=data_df,
            columns=[cols[0], cols[1]],
            key_on="feature.id",
            fill_color=fill_color,
            fill_opacity=0.7,
            line_opacity=0.2,
        ).add_to(m)
        return m

    def save_folium_toner_blank(self) -> Path:
        """서울 시청 중심 Stamen Toner 베이스맵 (원본 노트북 toner1.html)."""
        self.html_dir.mkdir(parents=True, exist_ok=True)
        path = self.html_dir / "toner1.html"
        m = folium.Map(
            location=[37.5502, 126.982], zoom_start=12, tiles="Stamen Toner"
        )
        m.save(str(path))
        return path

    def save_folium_crime_choropleth(
        self,
        geo_str: dict[str, Any],
        police_norm: pd.DataFrame,
        filename: str,
        *,
        value_column: str = "범죄",
        per_capita_million: bool = False,
    ) -> Path:
        self.html_dir.mkdir(parents=True, exist_ok=True)
        path = self.html_dir / filename
        s = police_norm[value_column]
        if per_capita_million:
            s = s / police_norm["인구수"] * 1_000_000
        m = self._choropleth_map(geo_str, s)
        m.save(str(path))
        return path

    def save_folium_police_markers(
        self,
        police_position_scored: pd.DataFrame,
        filename: str = "police_position.html",
    ) -> Path:
        """경찰서 CircleMarker만 올린 지도 (원본 스크립트의 seoul_map 미정의 버그 수정)."""
        self.html_dir.mkdir(parents=True, exist_ok=True)
        path = self.html_dir / filename
        base = folium.Map(location=[37.5502, 126.982], zoom_start=12)
        for i in police_position_scored.index:
            folium.CircleMarker(
                location=[
                    police_position_scored["lat"][i],
                    police_position_scored["lng"][i],
                ],
                radius=float(police_position_scored["검거"][i]) * 10,
                color="#3186cc",
                fill_color="#3186cc",
            ).add_to(base)
        base.save(str(path))
        return path

    def save_folium_choropleth_with_markers(
        self,
        geo_str: dict[str, Any],
        police_norm: pd.DataFrame,
        police_position_scored: pd.DataFrame,
        filename: str = "result.html",
    ) -> Path:
        self.html_dir.mkdir(parents=True, exist_ok=True)
        path = self.html_dir / filename
        m = self._choropleth_map(geo_str, police_norm["범죄"])
        for i in police_position_scored.index:
            folium.CircleMarker(
                location=[
                    police_position_scored["lat"][i],
                    police_position_scored["lng"][i],
                ],
                radius=float(police_position_scored["검거"][i]) * 10,
                color="#3186cc",
                fill_color="#3186cc",
            ).add_to(m)
        m.save(str(path))
        return path

    def run_full_pipeline(
        self,
        *,
        crime_csv: str = "crime_in_seoul.csv",
        save_intermediate: bool = True,
        intermediate_name: str = "crime_anal_police2.csv",
        skip_geocode: bool = False,
        intermediate_csv: str | None = None,
    ) -> SeoulCrimePipelineResult:
        """
        전체 흐름: 원본 CSV → (지오코딩) → 구 피벗 → 검거율·정규화 → CCTV/인구 머지 → 정렬용 프레임.
        skip_geocode=True이면 intermediate_csv(기본 crime_anal_police2.csv)에서 이어서 진행.
        """
        if skip_geocode:
            if intermediate_csv:
                crime_gu = self.load_crime_anal_police(intermediate_csv)
            else:
                crime_gu = self.load_crime_anal_police(intermediate_name)
        else:
            raw = self.load_crime_in_seoul(crime_csv)
            stations = self.build_station_queries(raw)
            self.geocode_stations(stations)
            crime_gu = self.apply_geumcheon_exception(self.attach_gu_column(raw))
            if save_intermediate:
                self.save_crime_anal_police(crime_gu, intermediate_name)

        police = self.pivot_by_gu(crime_gu)
        police = self.compute_police_metrics(police)
        police_norm = self.normalize_crime_counts(police)
        cctv_pop = self.load_cctv_merge_pop()
        police_norm = self.merge_cctv_into_police_norm(police_norm, cctv_pop)

        police_norm_arrest = self.normalize_arrest_total_score(police_norm.copy())
        sort_arrest = self.sort_by_column(police_norm_arrest, "검거", ascending=False)

        pos = self.load_police_position()
        pos = self.compute_police_position_score(pos)
        if "lat" in pos.columns and "lng" in pos.columns:
            pass
        else:
            pos = self.attach_station_coords(pos)

        saved_path: Optional[Path] = None
        if save_intermediate and not skip_geocode:
            saved_path = self.data_dir / intermediate_name

        crime_sort = police_norm.copy()
        crime_sort["범죄"] = crime_sort["범죄"] / 5
        sort_crime = self.sort_by_column(crime_sort, "범죄", ascending=False)

        return SeoulCrimePipelineResult(
            crime_by_station=crime_gu,
            police_by_gu=police,
            police_norm=police_norm,
            police_norm_sort_arrest=sort_arrest,
            police_norm_sort_crime=sort_crime,
            police_position=pos,
            intermediate_csv=saved_path,
        )

    def run_all_visualizations(
        self,
        result: SeoulCrimePipelineResult,
        geo_filename: str = "geo_simple.json",
        *,
        show_plots: bool = False,
    ) -> dict[str, Path]:
        """노트북에 있던 plot·folium HTML을 파일로 저장."""
        pn = result.police_norm
        paths: dict[str, Path] = {}
        paths["pair_triplet"] = self.save_pairplot_crime_triplet(
            pn, show=show_plots
        )
        paths["pair_pop_cctv"] = self.save_pairplot_pop_cctv_vs_crime(
            pn, show=show_plots
        )
        paths["pair_pop_arrest"] = self.save_pairplot_pop_cctv_vs_arrest(
            pn, show=show_plots
        )
        paths["heatmap_arrest"] = self.save_heatmap_arrest_rates(
            result.police_norm_sort_arrest, show=show_plots
        )
        paths["heatmap_crime"] = self.save_heatmap_crime_rates(pn, show=show_plots)
        paths["folium_base"] = self.save_folium_base_map()
        geo = self.load_geo_json(geo_filename)
        paths["toner1"] = self.save_folium_toner_blank()
        paths["toner2"] = self.save_folium_crime_choropleth(
            geo, pn, "toner2.html", value_column="범죄"
        )
        paths["toner3"] = self.save_folium_crime_choropleth(
            geo,
            pn,
            "toner3.html",
            value_column="범죄",
            per_capita_million=True,
        )
        paths["police_markers"] = self.save_folium_police_markers(
            result.police_position
        )
        paths["result"] = self.save_folium_choropleth_with_markers(
            geo, pn, result.police_position
        )
        return paths
