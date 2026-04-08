"""
Kaggle(Titanic) 서비스 FastAPI 앱 조립(Composition Root).
- 앱 생성·라우터 등록은 어댑터 계층에서만 수행. Application은 어댑터를 참조하지 않음.
"""

import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from labzang.core.paths import BACKEND_ROOT, LABZANG_ROOT, LEARNING_ROOT

# 절대경로 (진입점 호환)
for _p in (BACKEND_ROOT, LABZANG_ROOT, LEARNING_ROOT):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)
if os.path.exists("/app") and "/app" not in sys.path:
    sys.path.insert(0, "/app")

# 설정 (Application 계층 제공)
try:
    from labzang.apps.ai.percept.detective.santander.application.config import TitanicServiceConfig

    config = TitanicServiceConfig()
except Exception:

    class Config:
        service_name = "mlservice"
        service_version = "1.0.0"
        port = 9010

    config = Config()

LoggingMiddleware = None
try:
    from labzang.core.middleware import LoggingMiddleware
    from labzang.core.utils.utils import setup_logging
except ImportError:

    def setup_logging(name):
        import logging

        return logging.getLogger(name)


logger = setup_logging(config.service_name)

# 타이타닉 전용 — command/query 라우터 로드
from labzang.apps.ai.percept.detective.titanic.adapter.inbound.api.v1.titanic_command_router import (  # noqa: E402
    router as titanic_command_router,
)
from labzang.apps.ai.percept.detective.titanic.adapter.inbound.api.v1.titanic_query_router import (  # noqa: E402
    router as titanic_query_router,
)

app = FastAPI(
    title="Titanic Service API",
    description="""
    ## 타이타닉 데이터 서비스 API
    머신러닝을 활용한 타이타닉 승객 데이터 분석 및 생존 예측 서비스입니다.
    ### 기술 스택: FastAPI, scikit-learn, pandas, numpy
    """,
    version=config.service_version,
    contact={"name": "ML Service Team", "email": "support@labzang.com"},
    license_info={"name": "MIT"},
    tags_metadata=[{"name": "titanic", "description": "타이타닉 승객 데이터 관련 API"}],
    openapi_tags=[
        {"name": "titanic", "description": "타이타닉 데이터 및 머신러닝 예측 기능"}
    ],
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

# 타이타닉 라우터 등록
app.include_router(titanic_command_router, prefix="/titanic")
app.include_router(titanic_query_router, prefix="/titanic/query")


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": config.service_name,
        "version": config.service_version,
        "message": "Titanic Service API",
    }


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
