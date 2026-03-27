"""
인바운드(드라이빙) 포트: RAG 질의 — API/인바운드가 호출하는 유스케이스 계약.
구현: use_cases/hub/orchestrators.
"""
from abc import ABC, abstractmethod

from labzang.apps.ai.chat.application.dtos import RAGQueryDto, RAGResultDto


class RAGQueryInputPort(ABC):
    """RAG 질의 유스케이스 입력 포트. 인바운드 어댑터가 이 인터페이스를 호출합니다."""

    @abstractmethod
    def execute(self, query: RAGQueryDto) -> RAGResultDto:
        """질문에 대해 검색 후 답변 생성해 반환."""
        ...
