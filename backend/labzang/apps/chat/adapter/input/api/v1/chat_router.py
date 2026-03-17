"""챗봇 API 라우터 (main.py include_router용)."""
# 챗봇 API 진입점 (FastAPI Router)
# Hub → Spoke 라우팅 후 RAG/타이타닉 등 응답 반환 (필요 시 구현)

from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/")
async def chat_root():
    """챗봇 서비스 루트."""
    return {"service": "chat", "status": "ok"}
