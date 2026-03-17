"""
Titanic Service - FastAPI 애플리케이션
"""

import sys
import csv
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

try:
    from labzang.apps.kaggle.adapter.input.api.v1 import (
        seoul_crime_router as seoul_router,
    )
except ImportError:
    seoul_router = None

try:
    from labzang.apps.kaggle.application.us_unemployment.router import (
        router as usa_router,
    )
except ImportError:
    usa_router = None

try:
    from labzang.apps.kaggle.application.nlp.nlp_router import router as nlp_router
except ImportError:
    nlp_router = None

# 절대경로: backend( labzang 상위 ) → labzang.apps.kaggle.* import 가능
_labzang_root = Path(__file__).resolve().parent.parent.parent.parent
_learning_root = _labzang_root / "apps" / "learning"
_backend_root = _labzang_root.parent
for _p in (_backend_root, _labzang_root, _learning_root):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)
if os.path.exists("/app") and "/app" not in sys.path:
    sys.path.insert(0, "/app")

# 설정 로드 (경로 설정 후)
try:
    from labzang.apps.kaggle.application.config import TitanicServiceConfig

    config = TitanicServiceConfig()
except Exception:
    # config.py를 찾을 수 없는 경우 기본값 사용
    class Config:
        service_name = "mlservice"
        service_version = "1.0.0"
        port = 9010

    config = Config()

# 라우터 및 공통 모듈 import (헥사고날: HTTP 라우터는 adapter에만 둠)
LoggingMiddleware = None
try:
    from labzang.apps.kaggle.adapter.input.api.v1.legacy_titanic_router import (
        router as titanic_router,
    )
    from labzang.core.middleware import LoggingMiddleware
    from labzang.shared import setup_logging
except ImportError:
    from fastapi import APIRouter

    titanic_router = APIRouter()

    def setup_logging(name):
        import logging

        return logging.getLogger(name)


# 로깅 설정
logger = setup_logging(config.service_name)

# FastAPI 앱 생성
app = FastAPI(
    title="Titanic Service API",
    description="""
    ## 타이타닉 데이터 서비스 API
    
    머신러닝을 활용한 타이타닉 승객 데이터 분석 및 생존 예측 서비스입니다.
    
    ### 주요 기능
    - 승객 데이터 조회 및 통계 분석
    - 머신러닝 모델 훈련 (Random Forest)
    - 승객 생존 예측
    - 배치 예측 지원
    
    ### 기술 스택
    - **Framework**: FastAPI
    - **ML Library**: scikit-learn, pandas, numpy
    - **Model**: Random Forest Classifier
    
    ### API 문서
    - Swagger UI: `/docs`
    - ReDoc: `/redoc`
    - OpenAPI Schema: `/openapi.json`
    """,
    version=config.service_version,
    contact={
        "name": "ML Service Team",
        "email": "support@labzang.com",
    },
    license_info={
        "name": "MIT",
    },
    tags_metadata=[
        {
            "name": "titanic",
            "description": "타이타닉 승객 데이터 관련 API",
        },
    ],
    openapi_tags=[
        {
            "name": "titanic",
            "description": "타이타닉 승객 데이터 및 머신러닝 예측 기능",
        },
    ],
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 미들웨어 추가
if LoggingMiddleware is not None:
    app.add_middleware(LoggingMiddleware)

# /titanic: adapter에서 Use Case(application.use_cases) + Output Adapter 호출
app.include_router(titanic_router, prefix="/titanic")
# /hex: 헥사고날 유스케이스 API (adapter에서 use_cases + ports 호출)
try:
    from labzang.apps.kaggle.adapter.input.api.v1 import (
        titanic_router as hex_titanic_router,
    )

    app.include_router(hex_titanic_router, prefix="/hex")
except ImportError:
    hex_titanic_router = None

if seoul_router is not None:
    app.include_router(seoul_router, prefix="/seoul")
if usa_router is not None:
    app.include_router(usa_router, prefix="/usa")
if nlp_router is not None:
    app.include_router(nlp_router, prefix="/nlp")


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
    """서비스 시작 시 실행"""
    logger.info(f"{config.service_name} v{config.service_version} started")
    # 시작 시 상위 10명 출력


@app.on_event("shutdown")
async def shutdown_event():
    """서비스 종료 시 실행"""
    logger.info(f"{config.service_name} shutting down")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=config.port)
