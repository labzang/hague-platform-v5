"""
스포크: 답변 생성 — QLoRAChatPort만 사용.
"""
from ...DTOs import ChatRequestDto, ChatResponseDto
from ...ports.output import QLoRAChatPort


class GenerateAnswerSpoke:
    """컨텍스트가 포함된 프롬프트로 답변 생성만 담당."""

    def __init__(self, chat_port: QLoRAChatPort):
        self._chat = chat_port

    def run(self, request: ChatRequestDto) -> ChatResponseDto:
        """메시지에 대한 응답 생성."""
        history = None
        if request.conversation_history:
            history = [{"role": m.role, "content": m.content} for m in request.conversation_history]
        answer = self._chat.chat(
            request.message,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            conversation_history=history,
        )
        return ChatResponseDto(answer=answer, model_info=None)
