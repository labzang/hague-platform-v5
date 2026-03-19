"""
벅스 차트 크롤링 유스케이스 (포트만 의존, 비즈니스 오케스트레이션)
"""

from labzang.apps.crawler.application.ports.output.crawler_port import CrawlerPort
from labzang.apps.crawler.domain.entities.bugsmusic import BugsmusicChart
from labzang.apps.crawler.domain.value_objects.bugsmusic_vo import BugsmusicChartRow


class BugsmusicUC:
    def __init__(self, chart_crawl_port: CrawlerPort):
        self._crawl = chart_crawl_port

    def execute(self) -> BugsmusicChart:
        raw_songs = self._crawl.fetch_chart()
        entries = [
            BugsmusicChartRow(
                rank=int(s.get("rank", 0)),
                artist=str(s.get("artist", "")).strip(),
                title=str(s.get("title", "")).strip(),
            )
            for s in raw_songs
            if isinstance(s, dict)
        ]
        return BugsmusicChart(chart_date="", entries=entries)
