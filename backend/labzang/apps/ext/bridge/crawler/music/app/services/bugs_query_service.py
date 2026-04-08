"""
벅스 차트 애플리케이션 서비스.
- 어댑터/포트와 분리된 순수 변환 책임만 가진다.
- UseCase는 오케스트레이션만 수행한다.
"""

from __future__ import annotations

from labzang.apps.ext.bridge.crawler.music.domain.entities.bugsmusic import (
    BugsmusicChart,
    ChartEntry,
)
from labzang.apps.ext.bridge.crawler.music.domain.value_objects.bugsmusic_vo import (
    ArtistName,
    ChartRank,
    SongTitle,
)


class BugsQueryService:
    """원시 크롤링 결과(dict 목록)를 도메인 엔티티로 조립하는 서비스."""

    def chart_entry_from_raw(self, s: dict) -> ChartEntry | None:
        """원시 dict -> ChartEntry. 순위 파싱 불가 시 None."""
        try:
            rank = ChartRank(int(s.get("rank", 0)))
        except (TypeError, ValueError):
            return None
        artist_raw = str(s.get("artist", "")).strip()
        title_raw = str(s.get("title", "")).strip()
        artist = ArtistName(artist_raw) if artist_raw else None
        title = SongTitle(title_raw) if title_raw else None
        return ChartEntry(rank=rank, artist=artist, title=title)

    def to_chart(self, raw_songs: list[dict]) -> BugsmusicChart:
        """원시 차트 목록을 BugsmusicChart로 변환."""
        entries: list[ChartEntry] = []
        for s in raw_songs:
            if not isinstance(s, dict):
                continue
            row = self.chart_entry_from_raw(s)
            if row is not None:
                entries.append(row)
        return BugsmusicChart(chart_date="", entries=entries)
