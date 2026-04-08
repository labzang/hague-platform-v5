"""Inbound API for external training events (e.g., Vercel button/webhook)."""

import os

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import JSONResponse

from labzang.apps.ai.sentiment.adapter.inbound.api.schemas import (
    TrainingClickEventRequest,
)
from labzang.apps.ai.sentiment.adapter.inbound.dependencies import (
    get_training_event_command,
)
from labzang.apps.ai.sentiment.application.ports.input import TrainingEventCommand

router = APIRouter(prefix="/sentiment/events", tags=["sentiment-training-events"])


def _check_event_key(x_event_key: str | None) -> None:
    required = os.getenv("SENTIMENT_EVENT_KEY")
    if not required:
        return
    if x_event_key != required:
        raise HTTPException(status_code=401, detail="Invalid event key")


@router.post("/train-click")
async def on_train_click(
    request: TrainingClickEventRequest,
    command: TrainingEventCommand = Depends(get_training_event_command),
    x_event_key: str | None = Header(default=None),
):
    _check_event_key(x_event_key)
    payload = request.model_dump()
    result = await command.on_train_click(payload)
    return JSONResponse(status_code=202, content={"success": True, "data": result})


@router.get("/train-status")
async def train_status(
    command: TrainingEventCommand = Depends(get_training_event_command),
    x_event_key: str | None = Header(default=None),
):
    _check_event_key(x_event_key)
    result = await command.get_training_status()
    return JSONResponse(status_code=200, content={"success": True, "data": result})
