"""
미국 실업률 Command 라우터 (인바운드 어댑터)
- 생성/갱신/삭제 등 상태 변경 엔드포인트 전용.
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse

from labzang.apps.biz.desk.clerk.bill.app.use_cases.us_unemployment_uc import (
    USUnemploymentService,
)

router = APIRouter(tags=["usa-command"])

logger = logging.getLogger(__name__)

_service_instance: Optional[USUnemploymentService] = None


def get_service() -> USUnemploymentService:
    """USUnemploymentService 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = USUnemploymentService()
    return _service_instance


@router.get("/map")
async def generate_unemployment_map(
    location_lat: float = Query(48, description="지도 중심 위도"),
    location_lng: float = Query(-102, description="지도 중심 경도"),
    zoom_start: int = Query(3, description="초기 줌 레벨"),
    fill_color: str = Query("YlGn", description="색상 팔레트 (YlGn, Blues, Reds 등)"),
    fill_opacity: float = Query(0.7, description="채우기 투명도 (0.0-1.0)"),
    line_opacity: float = Query(0.2, description="경계선 투명도 (0.0-1.0)"),
    legend_name: str = Query("Unemployment Rate (%)", description="범례 이름"),
):
    """
    미국 실업률 지도 생성
    - 코로플레스(단계구분도) 방식으로 실업률을 시각화
    - 다양한 커스터마이징 옵션 제공
    """
    try:
        service = get_service()
        folium_map = service.generate_map(
            location=[location_lat, location_lng],
            zoom_start=zoom_start,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            line_opacity=line_opacity,
            legend_name=legend_name,
        )
        map_html = folium_map._repr_html_()
        return HTMLResponse(
            content=map_html,
            status_code=200,
            headers={"Content-Type": "text/html; charset=utf-8"},
        )
    except Exception as e:
        logger.error(f"지도 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"지도 생성 중 오류가 발생했습니다: {str(e)}"
        )
