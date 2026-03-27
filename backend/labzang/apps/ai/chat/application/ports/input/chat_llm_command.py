"""
아웃바운드 포트: 설정에 따른 LLM 생성 (구현: adapter/outbound/llm)
"""
from abc import ABC, abstractmethod
from typing import Any, Optional

from labzang.apps.ai.chat.domain.value_objects import LlmConfig


class ChatLLMPort(ABC):
    """설정(LlmConfig)에 따라 LLM 인스턴스를 생성하는 포트."""

    @abstractmethod
    def create_llm(self, config: LlmConfig) -> Optional[Any]:
        """설정에 맞는 LLM 인스턴스를 생성해 반환. 미지원 시 None."""
        ...
