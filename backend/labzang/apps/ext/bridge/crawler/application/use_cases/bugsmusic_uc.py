"""
벅스 차트 크롤링 유스케이스 (포트만 의존, 비즈니스 오케스트레이션)
"""

from labzang.apps.ext.crawler.application.ports.output.crawler_port import CrawlerPort
from labzang.apps.ext.crawler.domain.entities.bugsmusic import BugsmusicChart, ChartEntry
from labzang.apps.ext.crawler.domain.value_objects.bugsmusic_vo import (
    ArtistName,
    ChartRank,
    SongTitle,
)


def _chart_entry_from_raw(s: dict) -> ChartEntry | None:
    """원시 dict → ChartEntry. 순위 불가 시 None."""
    try:
        rank = ChartRank(int(s.get("rank", 0)))
    except (TypeError, ValueError):
        return None
    artist_raw = str(s.get("artist", "")).strip()
    title_raw = str(s.get("title", "")).strip()
    artist = ArtistName(artist_raw) if artist_raw else None
    title = SongTitle(title_raw) if title_raw else None
    return ChartEntry(rank=rank, artist=artist, title=title)


class BugsmusicUC:
    def __init__(self, chart_crawl_port: CrawlerPort):
        self._crawl = chart_crawl_port

    def execute(self) -> BugsmusicChart:
        raw_songs = self._crawl.fetch_chart()
        entries: list[ChartEntry] = []
        for s in raw_songs:
            if not isinstance(s, dict):
                continue
            row = _chart_entry_from_raw(s)
            if row is not None:
                entries.append(row)
        return BugsmusicChart(chart_date="", entries=entries)
