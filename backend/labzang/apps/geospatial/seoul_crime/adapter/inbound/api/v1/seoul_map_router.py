from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse

from labzang.apps.geospatial.seoul_crime.adapter.outbound.geocoding import (
    GoogleMapsGeocoder,
)
from labzang.apps.geospatial.seoul_crime.application.use_cases.seoul_crime_map_uc import (
    SeoulCrimeMapUseCase,
)
from labzang.core.paths import LABZANG_ROOT

router = APIRouter(tags=["seoul-map"])


def _build_use_case(with_geocoder: bool) -> SeoulCrimeMapUseCase:
    processed = (
        LABZANG_ROOT
        / "apps"
        / "geospatial"
        / "seoul_crime"
        / "resources"
        / "processed"
    )
    raw = (
        LABZANG_ROOT
        / "apps"
        / "geospatial"
        / "seoul_crime"
        / "resources"
        / "raw"
    )

    geocoder = None
    if with_geocoder:
        try:
            geocoder = GoogleMapsGeocoder()
        except Exception:
            geocoder = None

    return SeoulCrimeMapUseCase(
        processed_dir=Path(processed),
        raw_dir=Path(raw),
        geocoder=geocoder,
    )


@router.get("/render", response_class=HTMLResponse)
async def render_seoul_map(
    force_geocode: bool = Query(False, description="true면 관서명→자치구 지오코딩 강제 실행"),
):
    """processed 데이터를 갱신하고 Folium HTML 지도를 반환한다(버셀 iframe/srcdoc 용)."""
    try:
        uc = _build_use_case(with_geocoder=force_geocode)
        result = uc.execute(force_geocode=force_geocode)
        return HTMLResponse(
            content=result.map_html,
            status_code=200,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "X-Seoul-Crime-Gu-Count": str(result.summary["gu_count"]),
                "X-Seoul-Crime-Rows": str(result.summary["police_norm_rows"]),
            },
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
