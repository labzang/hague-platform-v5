"""CCTV CSV 업로드 → `resources/processed/cctv_in_seoul.csv` 저장 후 행렬 생성."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder

from labzang.apps.geospatial.seoul_crime.application.services.cctv_matrix_service import (
    CctvMatrixService,
)
from labzang.core.paths import LABZANG_ROOT
from labzang.shared import create_response

logger = logging.getLogger(__name__)

router = APIRouter(tags=["seoul-cctv"])

PROCESSED_CCTV_CSV: Path = (
    LABZANG_ROOT
    / "apps"
    / "geospatial"
    / "seoul_crime"
    / "resources"
    / "processed"
    / "cctv_in_seoul.csv"
)


def get_cctv_matrix_service() -> CctvMatrixService:
    return CctvMatrixService()


@router.post("/upload")
async def upload_cctv_csv(
    file: UploadFile = File(..., description="cctv_in_seoul.csv 등 CSV"),
    service: CctvMatrixService = Depends(get_cctv_matrix_service),
):
    """버셀·프론트 등에서 CSV를 보내면 processed 경로에 저장하고 `create_matrix`를 실행한다."""
    name = (file.filename or "").strip()
    if not name.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="CSV 파일(.csv)만 업로드할 수 있습니다.",
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
