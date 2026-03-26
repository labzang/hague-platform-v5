"""HTTP API v1 — player routes (upload + find)."""

from fastapi import APIRouter

from labzang.apps.soccer.player.adapter.inbound.api.v1.player_find_router import (
    router as find_router,
)
from labzang.apps.soccer.player.adapter.inbound.api.v1.player_upload_router import (
    router as upload_router,
)

router = APIRouter()
router.include_router(upload_router)
router.include_router(find_router)

__all__ = ["router", "upload_router", "find_router"]
