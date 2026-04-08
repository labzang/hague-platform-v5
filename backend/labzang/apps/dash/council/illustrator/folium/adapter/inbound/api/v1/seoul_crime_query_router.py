"""서울 범죄 Query 라우터.

- 조회 성격의 읽기 엔드포인트를 담당한다.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from labzang.shared import create_response

router = APIRouter(tags=["seoul-query"])


@router.get("/")
async def seoul_hex_root() -> JSONResponse:
    body = create_response(
        data={
            "service": "mlservice",
            "module": "seoul-hex",
            "architecture": "hexagonal",
            "status": "running",
        },
        message="Seoul Crime Hexagonal API is running",
    )
    return JSONResponse(content=body)
