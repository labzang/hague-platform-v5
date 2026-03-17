"""LLM 타입 정의 (adapter 계층 - LangChain 의존)."""
from langchain_core.language_models.base import BaseLanguageModel

LLMType = BaseLanguageModel

__all__ = ["LLMType", "BaseLanguageModel"]
