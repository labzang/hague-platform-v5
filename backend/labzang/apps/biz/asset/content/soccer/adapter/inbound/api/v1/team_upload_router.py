# -*- coding: utf-8 -*-
"""Team JSONL upload inbound API -> application command -> repository."""

import json
import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from labzang.apps.biz.asset.content.soccer.adapter.outbound.impl.team_repository_impl import (
    TeamRepositoryImpl,
)
from labzang.apps.biz.asset.content.soccer.application.ports.input.team_command import TeamCommand
from labzang.apps.biz.asset.content.soccer.application.use_cases.team_command_impl import (
    TeamCommandImpl,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def get_team_command() -> TeamCommand:
    return TeamCommandImpl(TeamRepositoryImpl())


@router.post("/upload")
async def upload_teams_jsonl(
    file: UploadFile = File(..., description="teams.jsonl (one JSON object per line)"),
    command: TeamCommand = Depends(get_team_command),
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

    result = await command.upload_teams_batch(items)
    logger.info(
        "teams jsonl upload: filename=%s lines=%s result=%s",
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
