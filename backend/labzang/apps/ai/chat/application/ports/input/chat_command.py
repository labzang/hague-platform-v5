"""
인바운드(드라이빙) 포트: 벡터 검색 — API/인바운드가 호출하는 유스케이스 계약.
구현: spokes 또는 use_cases.
"""
from abc import ABC, abstractmethod

from labzang.apps.ai.chat.application.dtos import SearchQueryDto, SearchResultDto


class SearchInputPort(ABC):
    """벡터 검색 유스케이스 입력 포트."""

    @abstractmethod
    def execute(self, query: SearchQueryDto) -> SearchResultDto:
        """검색 쿼리 실행 후 결과 반환."""
        ...
