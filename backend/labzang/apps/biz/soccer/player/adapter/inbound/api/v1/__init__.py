"""HTTP API v1 — player routes (batch upload + query)."""

from fastapi import APIRouter

from labzang.apps.biz.soccer.player.adapter.inbound.api.v1.player_batch_router import (
    router as batch_router,
)
from labzang.apps.biz.soccer.player.adapter.inbound.api.v1.player_query_router import (
    router as query_router,
)

router = APIRouter()
router.include_router(batch_router)
router.include_router(query_router)

__all__ = ["router", "batch_router", "query_router"]
