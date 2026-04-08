"""
단일 FastAPI 앱 조립(Composition Root).

도메인·유스케이스·포트는 기존 헥사고날 구조를 유지하고,
여기서는 인바운드 어댑터(라우터)만 한 프로세스에 등록한다.
Application 계층은 이 모듈을 참조하지 않는다.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from labzang.apps.ai.intel.advisor.inquiry.adapter.inbound.api.v1.chat_router import (
    router as chat_router,
)
from labzang.apps.ai.intel.advisor.inquiry.adapter.inbound.api.v1.search_router import (
    router as search_router,
)
from labzang.apps.ai.percept.detective.santander.adapter.inbound.api.v1 import (
    seoul_crime_router,
    titanic_router,
    us_unemployment_router,
    wordcloud_router,
)
from labzang.apps.ext.bridge.crawler.music.adapter.inbound.api.v1.crawler_router import (
    router as crawler_router,
)
from labzang.apps.ext.shield.guard.gateway.adapter.inbound.api.v1.auth_router import (
    router as auth_router,
)
from labzang.apps.ext.shield.guard.gateway.adapter.outbound.orm.user_orm import UserORM  # noqa: F401
from labzang.core.config import ChatbotServiceConfig
from labzang.core.database import engine
from labzang.core.middleware import LoggingMiddleware
from labzang.core.utils.utils import setup_logging


def create_monolith_app() -> FastAPI:
    """헥사고날 라우터를 단일 FastAPI 인스턴스에 등록한다."""
    config = ChatbotServiceConfig()
    logger = setup_logging(config.service_name)

    app = FastAPI(
        title="Labzang API (Monolith)",
        description="FastAPI 단일 프로세스 — 도메인별 헥사고날 패키지 유지",
        version=config.service_version,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)

    app.include_router(auth_router)
    app.include_router(chat_router)
    app.include_router(search_router)
    app.include_router(crawler_router)
    app.include_router(titanic_router)
    app.include_router(seoul_crime_router, prefix="/seoul")
    app.include_router(wordcloud_router, prefix="/wordcloud")
    app.include_router(us_unemployment_router, prefix="/usa")

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": config.service_name}

    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        return {
            "service": "labzang-monolith",
            "version": config.service_version,
            "docs": "/docs",
        }

    @app.on_event("startup")
    async def _startup() -> None:
        try:
            UserORM.__table__.create(bind=engine, checkfirst=True)
            logger.info("ext.guard `users` table ensured")
        except Exception as e:
            logger.warning("ext.guard users table create skipped: %s", e)
        logger.info(
            "%s v%s started (monolith)",
            config.service_name,
            config.service_version,
        )

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        logger.info("%s shutting down", config.service_name)

    return app
