"""설정에 따라 LLM 인스턴스를 생성하는 인바운드 팩토리."""
from typing import Any, Optional

from ....domain.value_objects import LlmConfig
from ....application.use_cases import CreateLlmFromConfigUseCase
from ...outbound import ChatLLMAdapter, LLMType


def create_llm_from_config(settings: Any) -> Optional[LLMType]:
    """설정에 따라 LLM을 생성합니다.

    Args:
        settings: llm_provider, openai_api_key, local_model_dir 속성을 가진 설정 객체.

    Returns:
        생성된 LLM 인스턴스. 설정이 불완전하면 None.
    """
    provider = getattr(settings, "llm_provider", None) or ""
    config = LlmConfig(
        provider=provider,
        openai_api_key=getattr(settings, "openai_api_key", None),
        local_model_dir=getattr(settings, "local_model_dir", None),
    )
    adapter = ChatLLMAdapter()
    use_case = CreateLlmFromConfigUseCase(adapter)
    return use_case.execute(config)


__all__ = ["create_llm_from_config"]
