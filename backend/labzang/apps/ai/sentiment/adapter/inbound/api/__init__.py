from fastapi import APIRouter

from labzang.apps.ai.sentiment.adapter.inbound.api.v1 import router as sentiment_v1_router

router = APIRouter()
router.include_router(sentiment_v1_router)

__all__ = ["router", "sentiment_v1_router"]