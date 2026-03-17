"""
Crawler Service - FastAPI 애플리케이션 (learning 구조 정렬)
- HTTP 라우터는 adapter/input 에만, 설정·진입점은 application/
"""
import sys
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 절대경로: labzang 루트 및 crawler 앱 루트
_labzang_root = Path(__file__).resolve().parent.parent.parent.parent
_crawler_root = _labzang_root / "apps" / "crawler"
for _p in (_labzang_root, _crawler_root):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)
if os.path.exists("/app") and "/app" not in sys.path:
    sys.path.insert(0, "/app")

# 설정
try:
    from labzang.apps.crawler.application.config import CrawlerServiceConfig
    config = CrawlerServiceConfig()
except Exception:
    class CrawlerServiceConfig:
        service_name = "crawlerservice"
        service_version = "1.0.0"
        port = 9001
    config = CrawlerServiceConfig()

# 로깅
try:
    from labzang.core.middleware import LoggingMiddleware
    from labzang.shared import setup_logging
    logger = setup_logging(config.service_name)
except ImportError:
    import logging
    logger = logging.getLogger("crawler")
    LoggingMiddleware = None

# 라우터 (adapter에서만)
try:
    from labzang.apps.crawler.adapter.input.api.v1 import crawler_router
except ImportError:
    from fastapi import APIRouter
    crawler_router = APIRouter(prefix="/crawler", tags=["crawler"])

app = FastAPI(
    title="Crawler Service API",
    description="Crawler 서비스 API 문서 (헥사고날 구조)",
    version=config.service_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if LoggingMiddleware is not None:
    app.add_middleware(LoggingMiddleware)

app.include_router(crawler_router)


@app.on_event("startup")
async def startup_event():
    logger.info("%s v%s started", config.service_name, config.service_version)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("%s shutting down", config.service_name)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.port)
