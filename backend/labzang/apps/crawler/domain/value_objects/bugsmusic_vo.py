"""
벅스 차트 한 행에 해당하는 값 객체.
- JSON 직렬화 및 테이블(행) 표현용.
"""
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass(frozen=True)
class BugsmusicChartRow:
    """벅스 차트 한 건: 순위, 아티스트, 제목."""

    rank: int
    artist: str
    title: str

    def to_dict(self) -> Dict[str, Any]:
        """JSON 저장용 딕셔너리."""
        return asdict(self)

    def to_table_row(self) -> list:
        """테이블(CSV 등) 저장용 리스트 [순위, 아티스트, 제목]."""
        return [self.rank, self.artist, self.title]


__all__ = ["BugsmusicChartRow"]
