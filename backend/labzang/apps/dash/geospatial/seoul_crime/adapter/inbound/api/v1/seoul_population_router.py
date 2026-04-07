"""인구 엑셀/CSV 업로드 → `resources/processed/pop_in_seoul.csv` 로 저장."""

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder

from labzang.apps.data.geospatial.seoul_crime.application.services.pop_seoul_reader_service import (
    PopInSeoulImportService,
)
from labzang.core.paths import LABZANG_ROOT
from labzang.shared import create_response

logger = logging.getLogger(__name__)

router = APIRouter(tags=["seoul-population"])

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


def get_pop_import_service() -> PopInSeoulImportService:
    return PopInSeoulImportService()


@router.post("/upload")
async def upload_population_file(
    file: UploadFile = File(..., description="pop 원본 .xls/.xlsx 또는 정제 .csv"),
    service: PopInSeoulImportService = Depends(get_pop_import_service),
):
    """엑셀은 `xls_to_dframe(header=2, usecols='B,D,G,J,N')` 경로로, CSV는 그대로 읽어 저장한다."""
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
