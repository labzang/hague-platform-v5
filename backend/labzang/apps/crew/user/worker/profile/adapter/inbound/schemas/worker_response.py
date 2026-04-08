"""인바운드 응답 스키마 스켈레톤."""

from __future__ import annotations

from pydantic import BaseModel, Field


class WorkerResponse(BaseModel):
    user_id: str
    name: str
    role: str
