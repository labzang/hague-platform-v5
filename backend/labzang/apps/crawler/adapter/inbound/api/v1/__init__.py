# 헥사고날: HTTP 라우터는 adapter에만 위치
from labzang.apps.crawler.adapter.inbound.api.v1.crawler_router import (
    router as crawler_router,
)

__all__ = ["crawler_router"]
