"""
크롤러 헥사고날 API (인바운드 어댑터)
- 유스케이스는 조립 루트(dependencies)에서 주입받음. 출력 어댑터 직접 참조 없음.
"""

from fastapi import APIRouter, Depends

from labzang.apps.ext.crawler.application.use_cases import BugsmusicUC
from labzang.apps.ext.crawler.adapter.inbound.dependencies import get_bugsmusic_uc
from labzang.shared import create_response, create_error_response, ServiceException

router = APIRouter(prefix="/crawler", tags=["crawler"])


@router.get("/")
async def crawler_root():
    """크롤러 서비스 루트."""
    return create_response(
        data={"service": "crawlerservice", "status": "running"},
        message="Crawler Service is running",
    )


@router.get("/bugsmusic")
async def get_bugs_music_chart(
    use_case: BugsmusicUC = Depends(get_bugsmusic_uc),
):
    """벅스뮤직 실시간 차트 크롤링."""
    try:
        result = use_case.execute()
        if not result.songs:
            raise ServiceException("차트 데이터를 가져올 수 없습니다.")
        return create_response(
            data={
                "chart_type": result.chart_type,
                "total_count": result.total_count,
                "songs": result.songs,
            },
            message="벅스뮤직 차트 조회 성공",
        )
    except ServiceException as e:
        return create_error_response(
            message=str(e),
            error_code="CRAWL_ERROR",
        )
    except Exception as e:
        return create_error_response(
            message=f"크롤링 중 오류 발생: {str(e)}",
            error_code="CRAWL_ERROR",
        )
