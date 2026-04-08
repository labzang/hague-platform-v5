"""
미국 실업률 Query 라우터 (인바운드 어댑터)
- 조회/시각화(GET) 전용 엔드포인트를 담당.
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException

from labzang.apps.biz.desk.clerk.bill.app.use_cases.us_unemployment_uc import (
    USUnemploymentService,
)
from labzang.shared import create_response
from labzang.shared.common.font_utils import (
    get_available_korean_fonts,
    test_korean_font,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["usa-query"])

_service_instance: Optional[USUnemploymentService] = None


def get_service() -> USUnemploymentService:
    """USUnemploymentService 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = USUnemploymentService()
    return _service_instance


@router.get("/")
async def usa_root():
    """미국 실업률 서비스 루트"""
    return create_response(
        data={"service": "mlservice", "module": "usa", "status": "running"},
        message="USA Unemployment Service is running",
    )


@router.get("/stats")
async def get_unemployment_stats():
    """
    미국 실업률 통계 정보 조회
    - 전체 주 수, 평균/최대/최소 실업률, 최고/최저 실업률 주 정보
    """
    try:
        service = get_service()
        service.load_unemployment_data()
        stats = service.get_unemployment_stats()
        if stats is None:
            raise HTTPException(status_code=404, detail="실업률 데이터를 찾을 수 없습니다")
        return create_response(
            data=stats, message="미국 실업률 통계 조회가 완료되었습니다"
        )
    except Exception as e:
        logger.error(f"실업률 통계 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"통계 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/data")
async def get_unemployment_data():
    """
    미국 실업률 원본 데이터 조회
    - 모든 주의 실업률 데이터를 JSON 형태로 반환
    """
    try:
        service = get_service()
        unemployment_data = service.load_unemployment_data()
        data_dict = unemployment_data.to_dict(orient="records")
        return create_response(
            data={"total_states": len(data_dict), "unemployment_data": data_dict},
            message="미국 실업률 데이터 조회가 완료되었습니다",
        )
    except Exception as e:
        logger.error(f"데이터 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"데이터 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/geo")
async def get_geo_data():
    """
    미국 주 경계 GeoJSON 데이터 조회
    - 지도 시각화에 사용되는 지리 정보 반환
    """
    try:
        service = get_service()
        geo_data = service.load_geo_data()
        return create_response(
            data={
                "type": geo_data.get("type"),
                "features_count": len(geo_data.get("features", [])),
                "geo_data": geo_data,
            },
            message="미국 주 경계 GeoJSON 데이터 조회가 완료되었습니다",
        )
    except Exception as e:
        logger.error(f"GeoJSON 데이터 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"GeoJSON 데이터 조회 중 오류가 발생했습니다: {str(e)}",
        )


@router.get("/font-test")
async def test_font():
    """
    한글 폰트 테스트
    - matplotlib에서 한글이 제대로 표시되는지 확인
    - 사용 가능한 한글 폰트 목록 반환
    """
    try:
        test_result = test_korean_font()
        available_fonts = get_available_korean_fonts()
        return create_response(
            data={
                "test_result": test_result,
                "available_korean_fonts": available_fonts,
                "total_korean_fonts": len(available_fonts),
            },
            message="한글 폰트 테스트가 완료되었습니다",
        )
    except Exception as e:
        logger.error(f"폰트 테스트 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"폰트 테스트 중 오류가 발생했습니다: {str(e)}"
        )
