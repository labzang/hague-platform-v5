"""서울 범죄 Command 라우터.

- 상태를 변경하거나 산출물을 생성하는 엔드포인트를 담당한다.
"""

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse

from labzang.core.dash.council.illustrator.folium.google_maps_geocoder import (
    GoogleMapsGeocoder,
)
from labzang.apps.dash.council.illustrator.folium.app.services.cctv_matrix_service import (
    CctvMatrixService,
)
from labzang.apps.dash.council.illustrator.folium.app.services.pop_seoul_reader_service import (
    PopInSeoulImportService,
)
from labzang.apps.dash.council.illustrator.folium.app.use_cases.seoul_crime_command_impl import (
    SeoulCrimeMapUseCase,
)
from labzang.apps.dash.council.illustrator.folium.adapter.inbound.deps import (
    get_preprocess_seoul_use_case,
)
from labzang.apps.biz.desk.clerk.bill.app.use_cases.seoul_crime_uc import (
    PreprocessSeoulCrimeUC,
)
from labzang.core.paths import LABZANG_ROOT
from labzang.shared import create_response

logger = logging.getLogger(__name__)
router = APIRouter(tags=["seoul-command"])

PROCESSED_CCTV_CSV: Path = (
    LABZANG_ROOT
    / "apps"
    / "geospatial"
    / "seoul_crime"
    / "resources"
    / "processed"
    / "cctv_in_seoul.csv"
)
PROCESSED_POP_CSV: Path = (
    LABZANG_ROOT
    / "apps"
    / "geospatial"
    / "seoul_crime"
    / "resources"
    / "processed"
    / "pop_in_seoul.csv"
)
_ALLOWED_SUFFIXES = frozenset({".xls", ".xlsx", ".xlsm", ".csv"})


def get_cctv_matrix_service() -> CctvMatrixService:
    return CctvMatrixService()


def get_pop_import_service() -> PopInSeoulImportService:
    return PopInSeoulImportService()


def _build_seoul_map_use_case(with_geocoder: bool) -> SeoulCrimeMapUseCase:
    processed = (
        LABZANG_ROOT / "apps" / "geospatial" / "seoul_crime" / "resources" / "processed"
    )
    raw = LABZANG_ROOT / "apps" / "geospatial" / "seoul_crime" / "resources" / "raw"
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


@router.post("/cctv/upload")
async def upload_cctv_csv(
    file: UploadFile = File(..., description="cctv_in_seoul.csv 등 CSV"),
    service: CctvMatrixService = Depends(get_cctv_matrix_service),
):
    name = (file.filename or "").strip()
    if not name.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="CSV 파일(.csv)만 업로드할 수 있습니다."
        )

    PROCESSED_CCTV_CSV.parent.mkdir(parents=True, exist_ok=True)
    try:
        body = await file.read()
        PROCESSED_CCTV_CSV.write_bytes(body)
    except OSError as e:
        logger.exception("CCTV CSV 저장 실패")
        raise HTTPException(status_code=500, detail=f"파일 저장 실패: {e}") from e

    try:
        matrix_payload = service.create_matrix(PROCESSED_CCTV_CSV)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("create_matrix 실패")
        raise HTTPException(status_code=500, detail=str(e)) from e

    payload = {
        "upload_filename": name,
        "saved_to": str(PROCESSED_CCTV_CSV.resolve()),
        **matrix_payload,
    }
    return create_response(
        data=jsonable_encoder(payload),
        message="CCTV CSV 저장 및 행렬 생성이 완료되었습니다.",
    )


@router.post("/population/upload")
async def upload_population_file(
    file: UploadFile = File(..., description="pop 원본 .xls/.xlsx 또는 정제 .csv"),
    service: PopInSeoulImportService = Depends(get_pop_import_service),
):
    name = (file.filename or "").strip()
    suffix = Path(name).suffix.lower()
    if suffix not in _ALLOWED_SUFFIXES:
        raise HTTPException(
            status_code=400,
            detail=f"허용 확장자: {sorted(_ALLOWED_SUFFIXES)}",
        )

    PROCESSED_POP_CSV.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(
        suffix=suffix,
        prefix="upload_pop_",
        dir=PROCESSED_POP_CSV.parent,
    )
    staging = Path(tmp)
    try:
        body = await file.read()
        os.write(fd, body)
    except OSError as e:
        logger.exception("인구 파일 스테이징 실패")
        raise HTTPException(status_code=500, detail=f"파일 저장 실패: {e}") from e
    finally:
        os.close(fd)

    try:
        payload = service.ingest_and_save(staging, PROCESSED_POP_CSV)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("인구 ingest 실패")
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        try:
            staging.unlink(missing_ok=True)
        except OSError:
            logger.warning("스테이징 파일 삭제 실패: %s", staging)

    return create_response(
        data=jsonable_encoder(
            {
                "upload_filename": name,
                "saved_to": payload["path"],
                "shape": payload["shape"],
                "columns": payload["columns"],
                "preview": payload["preview"],
            }
        ),
        message="pop_in_seoul.csv 저장이 완료되었습니다.",
    )


@router.post("/preprocess")
async def preprocess(
    use_case: PreprocessSeoulCrimeUC = Depends(get_preprocess_seoul_use_case),
):
    try:
        result = use_case.execute()
        return create_response(
            data={
                "status": result.status,
                "cctv_rows": result.cctv_rows,
                "cctv_columns": result.cctv_columns,
                "crime_rows": result.crime_rows,
                "crime_columns": result.crime_columns,
                "pop_rows": result.pop_rows,
                "pop_columns": result.pop_columns,
                "cctv_pop_rows": result.cctv_pop_rows,
                "cctv_pop_columns": result.cctv_pop_columns,
                "cctv_preview": result.cctv_preview,
                "crime_preview": result.crime_preview,
                "pop_preview": result.pop_preview,
                "cctv_pop_preview": result.cctv_pop_preview,
                "message": result.message,
            },
            message=result.message,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/map/render", response_class=HTMLResponse)
async def render_seoul_map(
    force_geocode: bool = Query(
        False, description="true면 관서명→자치구 지오코딩 강제 실행"
    ),
):
    try:
        uc = _build_seoul_map_use_case(with_geocoder=force_geocode)
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
