# -*- coding: utf-8 -*-
"""Schedule JSONL upload inbound API -> application command -> repository."""

import json
import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from labzang.apps.biz.soccer.schedule.adapter.outbound.impl.schedule_repository_impl import (
    ScheduleRepositoryImpl,
)
from labzang.apps.biz.soccer.schedule.application.ports.input.schedule_command import (
    ScheduleCommand,
)
from labzang.apps.biz.soccer.schedule.application.use_cases.schedule_command_impl import (
    ScheduleCommandImpl,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def get_schedule_command() -> ScheduleCommand:
    return ScheduleCommandImpl(ScheduleRepositoryImpl())


@router.post("/upload")
async def upload_schedules_jsonl(
    file: UploadFile = File(
        ..., description="schedules.jsonl (one JSON object per line)"
    ),
    command: ScheduleCommand = Depends(get_schedule_command),
) -> JSONResponse:
    """Accept multipart JSONL and delegate persistence to the application layer."""
    if not file.filename or not file.filename.lower().endswith(".jsonl"):
        raise HTTPException(
            status_code=400,
            detail="Expected a .jsonl file.",
        )
    try:
        raw = await file.read()
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise HTTPException(status_code=400, detail="File must be UTF-8.") from e

    items: List[Dict[str, Any]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Line {line_no}: invalid JSON ({e})",
            ) from e

    if not items:
        raise HTTPException(status_code=400, detail="No JSON lines found in file.")

    result = await command.upload_schedules_batch(items)
    logger.info(
        "schedules jsonl upload: filename=%s lines=%s result=%s",
        file.filename,
        len(items),
        result,
    )
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "filename": file.filename,
            "parsed_count": len(items),
            **result,
        },
    )
