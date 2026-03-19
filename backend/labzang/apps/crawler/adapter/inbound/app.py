"""
Crawler 서비스 FastAPI 앱 조립(Composition Root).
- 앱 생성·라우터 등록은 어댑터 계층에서만 수행. Application은 어댑터를 참조하지 않음.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Crawler Service API",
    description="Crawler 서비스 API 문서 (헥사고날 구조)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
