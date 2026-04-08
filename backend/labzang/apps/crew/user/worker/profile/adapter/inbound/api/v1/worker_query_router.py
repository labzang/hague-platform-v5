"""워커 조회 API 라우터(엔드포인트는 상위 앱에서 등록)."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/workers", tags=["worker-queries"])
