"""벅스 차트 조회 입력 포트(UseCase 계약)."""

from abc import ABC, abstractmethod
from typing import List

from labzang.apps.ext.bridge.crawler.music.domain.entities.bugsmusic import BugsmusicChart


class BugsCrawlerPort(ABC):
    """아웃바운드 크롤러 포트(원시 차트 수집)."""

    @abstractmethod
    def fetch_chart(self) -> List[dict]:
        """차트 원시 데이터 조회."""
        ...


class BugsQueryPort(ABC):
    """인바운드 조회 유스케이스 계약."""

    @abstractmethod
    def execute(self) -> BugsmusicChart:
        """벅스 차트를 도메인 엔티티로 반환."""
        ...
