"""
LLM 생성 유스케이스 (포트만 의존)
"""

from typing import Any, Optional

from ...domain.value_objects import LlmConfig
from ..ports.output import ChatLLMPort


class CreateLlmFromConfigUC:
    def __init__(self, llm_port: ChatLLMPort):
        self._llm_port = llm_port

    def execute(self, config: LlmConfig) -> Optional[Any]:
        """설정에 따라 LLM 인스턴스를 생성해 반환."""
        return self._llm_port.create_llm(config)
