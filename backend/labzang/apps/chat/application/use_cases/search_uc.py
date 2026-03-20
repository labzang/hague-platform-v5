"""
검색 유스케이스 — SearchInputPort 구현. SearchSpoke 위임.
"""

from ..DTOs import SearchQueryDto, SearchResultDto
from ..ports.input import SearchInputPort
from .spokes import SearchSpoke


class SearchUC(SearchInputPort):
    """벡터 검색만 수행하는 유스케이스."""

    def __init__(self, search_spoke: SearchSpoke):
        self._spoke = search_spoke

    def execute(self, query: SearchQueryDto) -> SearchResultDto:
        """검색 실행."""
        return self._spoke.run(query)
