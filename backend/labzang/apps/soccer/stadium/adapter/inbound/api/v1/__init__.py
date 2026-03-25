"""HTTP API v1 — stadium routes (upload + find)."""

from fastapi import APIRouter

from labzang.apps.soccer.stadium.adapter.inbound.api.v1.stadium_find_router import (
    router as find_router,
)
from labzang.apps.soccer.stadium.adapter.inbound.api.v1.stadium_upload_router import (
    router as upload_router,
)

router = APIRouter()
router.include_router(upload_router)
router.include_router(find_router)

__all__ = ["router", "upload_router", "find_router"]
