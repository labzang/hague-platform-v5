"""
조립 루트(Composition Root): 포트 구현체 생성 후 유스케이스 주입.
- 인바운드 어댑터(라우터)는 이 모듈의 의존성만 사용하며, output 어댑터를 직접 import하지 않음.
"""
from labzang.apps.crawler.application.use_cases import CrawlBugsChartUseCase
from labzang.apps.crawler.adapter.output.crawler_adapters import BugsCrawlAdapter


def get_crawl_use_case() -> CrawlBugsChartUseCase:
    """벅스 차트 크롤링 유스케이스 (포트 구현체는 여기서만 조립)."""
    port = BugsCrawlAdapter()
    return CrawlBugsChartUseCase(port)
