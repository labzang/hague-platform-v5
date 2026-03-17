"""
아웃바운드 포트: LLM 생성 (구현은 adapter/output)
"""
from abc import ABC, abstractmethod
from typing import Any

from ..value_objects import LlmConfig


class IChatLLMPort(ABC):
    """설정에 따라 LLM 인스턴스를 생성하는 포트."""

    @abstractmethod
    def create_llm(self, config: LlmConfig) -> Any:
        """config.provider에 따라 LLM 생성. 지원하지 않으면 None 또는 예외."""
        ...
