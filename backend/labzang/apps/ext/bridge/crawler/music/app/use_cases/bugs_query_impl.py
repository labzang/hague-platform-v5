"""
벅스 차트 크롤링 유스케이스 (포트만 의존, 비즈니스 오케스트레이션)
"""

from labzang.apps.ext.bridge.crawler.music.app.ports.input.bugs_query_port import (
    BugsCrawlerPort,
    BugsQueryPort,
)
from labzang.apps.ext.bridge.crawler.music.app.services.bugs_query_service import (
    BugsQueryService,
)
from labzang.apps.ext.bridge.crawler.music.domain.entities.bugsmusic import BugsmusicChart


class BugsQueryImpl(BugsQueryPort):
    def __init__(
        self,
        chart_crawl_port: BugsCrawlerPort,
        query_service: BugsQueryService | None = None,
    ):
        self._crawl = chart_crawl_port
        self._service = query_service or BugsQueryService()

    def execute(self) -> BugsmusicChart:
        raw_songs = self._crawl.fetch_chart()
        return self._service.to_chart(raw_songs)

