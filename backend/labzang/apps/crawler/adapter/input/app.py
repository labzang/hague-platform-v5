"""
Crawler 서비스 FastAPI 앱 조립(Composition Root).
- 앱 생성·라우터 등록은 어댑터 계층에서만 수행. Application은 어댑터를 참조하지 않음.
"""
import sys
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 절대경로 (진입점 호환)
_labzang_root = Path(__file__).resolve().parent.parent.parent.parent
_crawler_root = _labzang_root / "apps" / "crawler"
for _p in (_labzang_root, _crawler_root):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)
if os.path.exists("/app") and "/app" not in sys.path:
    sys.path.insert(0, "/app")

# 설정 (Application 계층 제공)
try:
    from labzang.apps.crawler.application.config import CrawlerServiceConfig
    config = CrawlerServiceConfig()
except Exception:
    class CrawlerServiceConfig:
        service_name = "crawlerservice"
        service_version = "1.0.0"
        port = 9001
    config = CrawlerServiceConfig()

try:
    from labzang.core.middleware import LoggingMiddleware
    from labzang.shared import setup_logging
    logger = setup_logging(config.service_name)
except ImportError:
    import logging
    logger = logging.getLogger("crawler")
    LoggingMiddleware = None

from labzang.apps.crawler.adapter.input.api.v1 import crawler_router

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


def run():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.port)


if __name__ == "__main__":
    run()
