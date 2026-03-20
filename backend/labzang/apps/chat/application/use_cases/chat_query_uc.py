"""
채팅 유스케이스 — ChatQueryInputPort 구현. QLoRAChatPort만 사용.
"""

from ..DTOs import ChatRequestDto, ChatResponseDto
from ..ports.input import ChatQueryInputPort
from ..ports.output import QLoRAChatPort


class ChatQueryUC(ChatQueryInputPort):
    """단순 채팅 (검색 없이 메시지 → 답변)."""

    def __init__(self, chat_port: QLoRAChatPort):
        self._chat = chat_port

    def execute(self, request: ChatRequestDto) -> ChatResponseDto:
        """메시지에 대한 응답 생성."""
        history = None
        if request.conversation_history:
            history = [
                {"role": m.role, "content": m.content}
                for m in request.conversation_history
            ]
        answer = self._chat.chat(
            request.message,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            conversation_history=history,
        )
        return ChatResponseDto(answer=answer, model_info=None)
