"""OpenAI 기반 LLM provider."""
from typing import Any

from langchain_openai import ChatOpenAI

from labzang.apps.com.chat.adapter.outbound.llm.llm_types import LLMType


def create_openai_chat_llm(
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0.0,
    **kwargs: Any,
) -> LLMType:
    """OpenAI Chat LLM 인스턴스를 생성합니다."""
    return ChatOpenAI(model=model_name, temperature=temperature, **kwargs)
