"""Outbound package exports with safe lazy imports."""

from labzang.apps.ai.chat.adapter.outbound.llm.llm_types import LLMType

try:
    from labzang.apps.ai.chat.adapter.outbound.llm.chat_llm_adapter import ChatLLMAdapter
except Exception:  # pragma: no cover
    ChatLLMAdapter = None  # type: ignore[assignment]

try:
    from labzang.apps.ai.chat.adapter.outbound.qlora import (
        QLoRAChatAdapter,
        create_qlora_chat_adapter,
    )
except Exception:  # pragma: no cover
    QLoRAChatAdapter = None  # type: ignore[assignment]
    create_qlora_chat_adapter = None  # type: ignore[assignment]

__all__ = ["LLMType", "ChatLLMAdapter", "QLoRAChatAdapter", "create_qlora_chat_adapter"]
