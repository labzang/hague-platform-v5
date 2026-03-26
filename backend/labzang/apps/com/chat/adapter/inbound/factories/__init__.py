"""인바운드 팩토리 — 설정/조립으로 서비스(LLM 등)를 생성하는 진입점."""
from labzang.apps.com.chat.adapter.inbound.factories.create_llm import create_llm_from_config

__all__ = ["create_llm_from_config"]
