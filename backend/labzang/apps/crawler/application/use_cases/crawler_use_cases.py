"""
크롤러 유스케이스 (포트만 의존, 비즈니스 오케스트레이션)
"""
from labzang.apps.crawler.domain.ports import IChartCrawlPort
from labzang.apps.crawler.domain.value_objects import ChartResult


class CrawlBugsChartUseCase:
    def __init__(self, chart_crawl_port: IChartCrawlPort):
        self._crawl = chart_crawl_port

    def execute(self) -> ChartResult:
        songs = self._crawl.fetch_chart()
        return ChartResult(
            chart_type="bugs_realtime",
            total_count=len(songs),
            songs=songs,
        )
