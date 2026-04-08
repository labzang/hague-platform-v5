from __future__ import annotations

from fastapi import APIRouter

from labzang.apps.crew.user.worker.profile.adapter.inbound.api.v1.worker_command_router import (
    router as worker_command_router,
)
from labzang.apps.crew.user.worker.profile.adapter.inbound.api.v1.worker_query_router import (
    router as worker_query_router,
)

router = APIRouter()
router.include_router(worker_command_router)
router.include_router(worker_query_router)

__all__ = ["router", "worker_command_router", "worker_query_router"]
