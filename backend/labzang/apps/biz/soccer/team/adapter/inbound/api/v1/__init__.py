"""HTTP API v1 — team routes (upload + find)."""

from fastapi import APIRouter

from labzang.apps.biz.soccer.team.adapter.inbound.api.v1.team_find_router import (
    router as find_router,
)
from labzang.apps.biz.soccer.team.adapter.inbound.api.v1.team_upload_router import (
    router as upload_router,
)

router = APIRouter()
router.include_router(upload_router)
router.include_router(find_router)

__all__ = ["router", "upload_router", "find_router"]
