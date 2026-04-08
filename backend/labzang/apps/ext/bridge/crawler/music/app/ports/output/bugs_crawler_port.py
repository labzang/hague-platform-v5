"""
벅스 크롤러 아웃바운드 포트.
- 외부 사이트/HTTP 의존 구현체는 adapter/outbound/impl 에 위치한다.
"""

from abc import ABC, abstractmethod
from typing import List


class BugsCrawlerPort(ABC):
    """벅스 차트 원시 데이터 수집 포트."""

    @abstractmethod
    def fetch_chart(self) -> List[dict]:
        """차트 데이터 조회. 반환: [{"rank", "title", "artist", "album", ...}, ...]."""
        ...


__all__ = ["BugsCrawlerPort"]
