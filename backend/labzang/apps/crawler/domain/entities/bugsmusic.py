"""
벅스 차트 크롤링 결과 엔티티.
- JSON 전체 저장 및 테이블(2차원) 저장용.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List

from labzang.apps.crawler.domain.value_objects.bugsmusic_vo import BugsmusicChartRow


@dataclass
class BugsmusicChart:
    """벅스 실시간 차트 한 페이지 결과."""

    chart_date: str
    entries: List[BugsmusicChartRow] = field(default_factory=list)
    chart_type: str = "bugs_realtime"

    @property
    def songs(self) -> List[Dict[str, Any]]:
        """라우터/API 호환용. entries를 dict 리스트로."""
        return [row.to_dict() for row in self.entries]

    @property
    def total_count(self) -> int:
        """항목 수."""
        return len(self.entries)

    def to_dict(self) -> Dict[str, Any]:
        """JSON 저장용 딕셔너리. entries는 리스트[딕셔너리]."""
        return {
            "chart_date": self.chart_date,
            "entries": [row.to_dict() for row in self.entries],
            "total_count": len(self.entries),
        }

    def to_table(self) -> List[List[Any]]:
        """테이블(CSV/DB) 저장용 2차원 리스트. 첫 행은 헤더."""
        header = ["rank", "artist", "title"]
        rows = [row.to_table_row() for row in self.entries]
        return [header] + rows

    def to_table_as_dicts(self) -> List[Dict[str, Any]]:
        """테이블 저장용 리스트[딕셔너리] (헤더 키로 매핑)."""
        return [row.to_dict() for row in self.entries]
