"""
Outbound: LLM 모델 호출 인터페이스
- 구현: adapter/output/llm_client (LangChain 기반 GPT-4, Claude 등)
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ILlmPort(ABC):
    """LLM 호출 포트."""

    @abstractmethod
    def invoke(self, prompt: str, **kwargs: Any) -> str:
        """프롬프트 전달 후 응답 텍스트 반환."""
        ...

    @abstractmethod
    def invoke_with_messages(
        self, messages: list, **kwargs: Any
    ) -> str:
        """메시지 리스트로 채팅 완성."""
        ...
