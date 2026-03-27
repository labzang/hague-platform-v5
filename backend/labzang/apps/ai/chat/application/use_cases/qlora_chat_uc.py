"""
QLoRA 대화 생성 유스케이스 — QLoRAChatPort만 의존
"""

from typing import Any, Dict, List, Optional

from labzang.apps.ai.chat.application.ports.output import QLoRAChatPort


class QLoRAChatUC:
    """QLoRA 포트를 사용한 대화 생성 오케스트레이션."""

    def __init__(self, qlora_port: QLoRAChatPort):
        self._port = qlora_port

    def execute(
        self,
        message: str,
        *,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        do_sample: bool = True,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """메시지에 대한 응답 생성."""
        return self._port.chat(
            message,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
            conversation_history=conversation_history,
        )
