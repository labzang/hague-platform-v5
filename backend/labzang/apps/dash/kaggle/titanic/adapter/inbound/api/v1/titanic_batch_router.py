"""train.csv / test.csv 업로드 → CSV 파싱 후 스키마 검증, 라우트별 DatasetSplit 고정."""

from __future__ import annotations

import csv
import logging
from io import StringIO
from typing import Any, Literal

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from labzang.apps.data.kaggle.titanic.adapter.inbound.dependencies import get_titanic_command_impl
from labzang.apps.data.kaggle.titanic.adapter.inbound.schemas.titanic_request import (
    TitanicBatchUpsertRequest,
    TitanicUpsertRequest,
)
from labzang.apps.data.kaggle.titanic.application.dtos.titanic_row_dto import TitanicRowDTO
from labzang.apps.data.kaggle.titanic.application.ports.input.titanic_command import (
    TitanicCommandPort,
)
from labzang.shared import create_response

logger = logging.getLogger(__name__)

router = APIRouter(tags=["titanic-batch"])

_MAX_ROWS = 5000
_MAX_ERROR_DETAIL = 30


def _normalize_row_keys(row: dict[str | None, str | None]) -> dict[str, str]:
    return {
        (k or "").strip().lstrip("\ufeff"): (v or "").strip()
        for k, v in row.items()
        if k is not None
    }


def _build_upsert_payload(
    r: dict[str, str],
    forced_split: Literal["train", "test"] | None = None,
) -> dict[str, Any]:
    if "Gender" not in r and "Sex" in r:
        r = {**r, "Gender": r["Sex"]}

    def req_str(name: str) -> str:
        v = r.get(name, "").strip()
        if not v:
            raise ValueError(f"필수 문자열 누락: {name}")
        return v

    def opt_str(name: str) -> str | None:
        v = r.get(name, "").strip()
        return None if v == "" else v

    def opt_int(name: str) -> int | None:
        v = r.get(name, "").strip()
        if v == "":
            return None
        return int(float(v))

    def req_int(name: str) -> int:
        v = r.get(name, "").strip()
        if v == "":
            raise ValueError(f"필수 정수 누락: {name}")
        return int(float(v))

    def opt_float(name: str) -> float | None:
        v = r.get(name, "").strip()
        if v == "":
            return None
        return float(v)

    if forced_split is not None:
        ds = forced_split
    else:
        ds = opt_str("DatasetSplit") or opt_str("split") or "train"
        if ds.lower() not in ("train", "test"):
            raise ValueError("DatasetSplit은 train 또는 test 여야 합니다.")
        ds = ds.lower()

    return {
        "PassengerId": req_int("PassengerId"),
        "DatasetSplit": ds,
        "Survived": opt_int("Survived"),
        "Pclass": req_int("Pclass"),
        "Name": req_str("Name"),
        "Gender": req_str("Gender").lower(),
        "Age": opt_float("Age"),
        "SibSp": req_int("SibSp"),
        "Parch": req_int("Parch"),
        "Ticket": req_str("Ticket"),
        "Fare": opt_float("Fare"),
        "Cabin": opt_str("Cabin"),
        "Embarked": opt_str("Embarked"),
    }


def _parse_csv_to_validated_rows(
    text: str,
    *,
    forced_split: Literal["train", "test"],
) -> list[TitanicUpsertRequest]:
    reader = csv.DictReader(StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV에 헤더 행이 없습니다.")

    validated_rows: list[TitanicUpsertRequest] = []
    errors: list[dict[str, Any]] = []

    for line_no, raw_row in enumerate(reader, start=2):
        if line_no - 2 >= _MAX_ROWS:
            errors.append(
                {
                    "row": line_no,
                    "detail": f"최대 {_MAX_ROWS}행까지만 처리합니다.",
                }
            )
            break

        try:
            norm = _normalize_row_keys(raw_row)
            payload = _build_upsert_payload(norm, forced_split=forced_split)
            validated_rows.append(TitanicUpsertRequest.model_validate(payload))
        except ValueError as e:
            errors.append({"row": line_no, "detail": str(e)})
        except ValidationError as e:
            errors.append({"row": line_no, "detail": e.errors()})
            if len(errors) >= _MAX_ERROR_DETAIL:
                break

    if errors:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "CSV 행 검증 실패",
                "errors": errors,
                "parsed_ok_count": len(validated_rows),
            },
        )

    if not validated_rows:
        raise HTTPException(
            status_code=400,
            detail="데이터 행이 없습니다. 헤더만 있는 CSV는 허용되지 않습니다.",
        )

    return validated_rows


async def _read_upload_as_utf8(file: UploadFile) -> tuple[str, str]:
    name = (file.filename or "").strip()
    if not name.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="CSV 파일(.csv)만 업로드할 수 있습니다.",
        )
    try:
        raw = await file.read()
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"UTF-8로 디코딩할 수 없습니다: {e}",
        ) from e
    return name, text


@router.post("/train/upload")
async def upload_train_csv(
    file: UploadFile = File(..., description="Kaggle-style train.csv (헤더에 Gender 또는 Sex)"),
    command: TitanicCommandPort = Depends(get_titanic_command_impl),
):
    """train.csv 업로드: DatasetSplit은 항상 train으로 고정, Survived 필수."""
    name, text = await _read_upload_as_utf8(file)
    validated_rows = _parse_csv_to_validated_rows(text, forced_split="train")

    if any(r.Survived is None for r in validated_rows):
        raise HTTPException(
            status_code=422,
            detail="train.csv의 모든 데이터 행에 Survived 값이 있어야 합니다.",
        )

    batch = TitanicBatchUpsertRequest(rows=validated_rows)
    dtos = [TitanicRowDTO.model_validate(r.model_dump()) for r in batch.rows]

    try:
        pipeline = command.ingest_train_batch(dtos, test_rows=None)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return create_response(
        data=jsonable_encoder(
            {
                "upload_filename": name,
                "row_count": len(batch.rows),
                "batch": batch.model_dump(mode="python"),
                "preview": [r.model_dump(mode="python") for r in batch.rows[:5]],
                "pipeline": pipeline.model_dump(mode="python"),
            }
        ),
        message=(
            f"train.csv {len(batch.rows)}건 검증·전처리 완료 "
            f"(원본 저장: {pipeline.persisted_count}건, 특성: {pipeline.features_persisted_count}건)."
        ),
    )


@router.post("/test/upload")
async def upload_test_csv(
    file: UploadFile = File(..., description="Kaggle-style test.csv (Survived 컬럼 없음 가능)"),
    command: TitanicCommandPort = Depends(get_titanic_command_impl),
):
    """test.csv 업로드: DatasetSplit은 항상 test로 고정."""
    name, text = await _read_upload_as_utf8(file)
    validated_rows = _parse_csv_to_validated_rows(text, forced_split="test")
    batch = TitanicBatchUpsertRequest(rows=validated_rows)
    dtos = [TitanicRowDTO.model_validate(r.model_dump()) for r in batch.rows]

    try:
        pipeline = command.ingest_test_batch(dtos)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return create_response(
        data=jsonable_encoder(
            {
                "upload_filename": name,
                "row_count": len(batch.rows),
                "batch": batch.model_dump(mode="python"),
                "preview": [r.model_dump(mode="python") for r in batch.rows[:5]],
                "pipeline": pipeline.model_dump(mode="python"),
            }
        ),
        message=(
            f"test.csv {len(batch.rows)}건 검증·전처리 완료 "
            f"(원본 저장: {pipeline.persisted_count}건, 특성: {pipeline.features_persisted_count}건)."
        ),
    )
