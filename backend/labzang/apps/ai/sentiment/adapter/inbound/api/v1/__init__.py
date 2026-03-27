from fastapi import APIRouter

from labzang.apps.ai.sentiment.adapter.inbound.api.v1.sentiment_router import (
    router as sentiment_router,
)
from labzang.apps.ai.sentiment.adapter.inbound.api.v1.training_event_router import (
    router as training_event_router,
)

router = APIRouter()
router.include_router(sentiment_router)
router.include_router(training_event_router)

__all__ = ["router", "sentiment_router", "training_event_router"]
