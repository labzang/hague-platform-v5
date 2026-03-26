"""
벅스 차트 도메인 엔티티 (Titanic 패턴 정렬)
- 한 줄 엔티티 + 실행 메타 엔티티로 분리.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from labzang.apps.ext.crawler.domain.value_objects.bugsmusic_vo import (
    ArtistName,
    ChartRank,
    SongTitle,
)


@dataclass
class ChartEntry:
    """차트 한 건 엔티티 (Titanic의 Passenger와 동일 역할)."""

    rank: Optional[ChartRank] = None
    artist: Optional[ArtistName] = None
    title: Optional[SongTitle] = None

    def to_dict(self) -> Dict[str, Any]:
        """JSON 저장용 딕셔너리."""
        return {
            "rank": self.rank.value if self.rank else None,
            "artist": self.artist.value if self.artist else "",
            "title": self.title.value if self.title else "",
        }

    def to_table_row(self) -> List[Any]:
        """테이블(CSV 등) 저장용 [순위, 아티스트, 제목]."""
        return [
            self.rank.value if self.rank else None,
            self.artist.value if self.artist else "",
            self.title.value if self.title else "",
        ]


@dataclass
class BugsmusicChart:
    """벅스 차트 결과 집계 엔티티."""

    chart_date: str
    entries: List[ChartEntry] = field(default_factory=list)
    chart_type: str = "bugs_realtime"

    @property
    def songs(self) -> List[Dict[str, Any]]:
        """라우터/API 호환용. entries를 dict 리스트로."""
        return [row.to_dict() for row in self.entries]

    @property
    def total_count(self) -> int:
        return len(self.entries)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chart_date": self.chart_date,
            "entries": [row.to_dict() for row in self.entries],
            "total_count": len(self.entries),
        }

    def to_table(self) -> List[List[Any]]:
        header = ["rank", "artist", "title"]
        rows = [row.to_table_row() for row in self.entries]
        return [header] + rows

    def to_table_as_dicts(self) -> List[Dict[str, Any]]:
        return [row.to_dict() for row in self.entries]


@dataclass
class BugsmusicModels:
    """크롤링 실행 메타 엔티티 (TitanicModels 대응)."""

    id: Optional[int] = None
    run_date: Optional[str] = None
    source: Optional[str] = None
    item_count: Optional[int] = None
    artifact_path: Optional[str] = None
    notes: Optional[str] = None


# 하위 호환 이름 유지
BugsmusicChartRow = ChartEntry
