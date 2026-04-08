"""인바운드 요청 스키마 스켈레톤."""

from __future__ import annotations

from pydantic import BaseModel, Field


class WorkerUpsertBody(BaseModel):
    name: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
