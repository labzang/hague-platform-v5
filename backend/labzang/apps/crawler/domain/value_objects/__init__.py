"""
아웃바운드 포트 및 값 객체 (도메인 계층) - 구현은 adapter 계층에 위치
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List


class ChartCrawlPort(ABC):
    """차트 크롤링용 포트 (벅스 등)."""

    @abstractmethod
    def fetch_chart(self) -> List[dict]:
        """차트 데이터 조회. 반환: [{"rank", "title", "artist", "album", ...}, ...]"""
        ...


@dataclass
class ChartResult:
    """차트 크롤링 결과."""

    chart_type: str
    total_count: int
    songs: List[dict]
    raw: Any = None


__all__ = ["ChartCrawlPort", "ChartResult"]
