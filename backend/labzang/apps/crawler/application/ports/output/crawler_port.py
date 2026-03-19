"""
크롤러 아웃바운드 포트 (차트 크롤링).
- 구현은 adapter/outbound/client 등에 위치.
"""
from abc import ABC, abstractmethod
from typing import List


class CrawlerPort(ABC):
    """차트 크롤링용 포트 (벅스 등). 구현체는 HTTP 클라이언트 등."""

    @abstractmethod
    def fetch_chart(self) -> List[dict]:
        """차트 데이터 조회. 반환: [{"rank", "title", "artist", "album", ...}, ...]"""
        ...
