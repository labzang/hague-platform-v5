"""
Chatbot Service - FastAPI 애플리케이션
"""

import sys
from pathlib import Path

# backend 디렉터리를 PYTHONPATH에 추가 (labzang 패키지 로드)
_backend_dir = Path(__file__).resolve().parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from labzang.core.config import ChatbotServiceConfig
from labzang.apps.chat.adapter.input.api import router as chat_router
from labzang.apps.kaggle.adapter.input.api.v1 import (
    titanic_router as hex_titanic_router,
)
from labzang.core.middleware import LoggingMiddleware
from labzang.shared import setup_logging

# 설정 로드
config = ChatbotServiceConfig()

# 로깅 설정
logger = setup_logging(config.service_name)

# FastAPI 앱 생성
app = FastAPI(
    title="Chatbot Service API",
    description="챗봇 서비스 API 문서",
    version=config.service_version,
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
app.add_middleware(LoggingMiddleware)

# 라우터 등록
app.include_router(chat_router)
app.include_router(hex_titanic_router, prefix="/hex")


@app.on_event("startup")
async def startup_event():
    """서비스 시작 시 실행"""
    logger.info(f"{config.service_name} v{config.service_version} started")


@app.on_event("shutdown")
async def shutdown_event():
    """서비스 종료 시 실행"""
    logger.info(f"{config.service_name} shutting down")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=config.port)
