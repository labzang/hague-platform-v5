"""
Search use case implementation of SearchInputPort.
Delegates actual retrieval to SearchSpoke.
"""

from labzang.apps.ai.chat.application.dtos import SearchQueryDto, SearchResultDto
from labzang.apps.ai.chat.application.orchestrators.spokes import SearchSpoke
from labzang.apps.ai.chat.application.ports.input import SearchInputPort


class SearchUC(SearchInputPort):
    """Use case for vector similarity search."""

    def __init__(self, search_spoke: SearchSpoke):
        self._spoke = search_spoke

    def execute(self, query: SearchQueryDto) -> SearchResultDto:
        """Execute search and return DTO result."""
        return self._spoke.run(query)