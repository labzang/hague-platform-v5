"""
LLM 생성 유스케이스 (포트만 의존)
"""
from typing import Any, Optional

from ...domain.ports import IChatLLMPort
from ...domain.value_objects import LlmConfig


class CreateLlmFromConfigUseCase:
    def __init__(self, llm_port: IChatLLMPort):
        self._llm_port = llm_port

    def execute(self, config: LlmConfig) -> Optional[Any]:
        """설정에 따라 LLM 인스턴스를 생성해 반환."""
        return self._llm_port.create_llm(config)