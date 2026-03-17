"""
Learning 앱 - 헥사고날 아키텍처 전용 진입점
- PYTHONPATH를 learning 루트로 두고 실행: python main_hex.py 또는 -m main_hex
"""
import sys
from pathlib import Path

# learning 루트를 path 최상단에 추가 (domain, application, adapter 패키지 인식)
_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from application.config import TitanicServiceConfig
    config = TitanicServiceConfig()
except Exception:
    class TitanicServiceConfig:
        service_name = "mlservice"
        service_version = "1.0.0"
        port = 9010
    config = TitanicServiceConfig()

try:
    from common.middleware import LoggingMiddleware
    from common.utils import setup_logging
except ImportError:
    import logging
    LoggingMiddleware = None
    def setup_logging(name):
        return logging.getLogger(name)

logger = setup_logging(config.service_name)

app = FastAPI(
    title="Learning API (Hexagonal)",
    description="헥사고날 아키텍처 샘플 - Titanic 유스케이스",
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

from adapter.input.api.v1 import titanic_router
app.include_router(titanic_router, prefix="/hex")

@app.get("/")
async def root():
    return {
        "service": config.service_name,
        "version": config.service_version,
        "architecture": "hexagonal",
        "message": "Learning API (Hexagonal sample)",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.port)
