"""
크롤러 헥사고날 API (인바운드 어댑터)
- 포트 구현체 조립 → 유스케이스 호출 → HTTP
"""
from fastapi import APIRouter, HTTPException

from labzang.apps.crawler.domain.ports import IChartCrawlPort
from labzang.apps.crawler.application.use_cases import CrawlBugsChartUseCase
from labzang.apps.crawler.adapter.output.crawler_adapters import BugsCrawlAdapter
from labzang.shared import create_response, create_error_response, ServiceException

router = APIRouter(prefix="/crawler", tags=["crawler"])


def _create_chart_crawl_port() -> IChartCrawlPort:
    return BugsCrawlAdapter()


@router.get("/")
async def crawler_root():
    """크롤러 서비스 루트."""
    return create_response(
        data={"service": "crawlerservice", "status": "running"},
        message="Crawler Service is running",
    )


@router.get("/bugsmusic")
async def get_bugs_music_chart():
    """벅스뮤직 실시간 차트 크롤링."""
    try:
        port = _create_chart_crawl_port()
        use_case = CrawlBugsChartUseCase(port)
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
