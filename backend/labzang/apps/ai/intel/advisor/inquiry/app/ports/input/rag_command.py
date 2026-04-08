"""RAG 관련 명령 입력 포트 (확장용)."""

from abc import ABC


class RAGCommandInputPort(ABC):
    """RAG 색인/동기화 같은 쓰기성 유스케이스 계약을 위한 베이스 포트."""

    pass
