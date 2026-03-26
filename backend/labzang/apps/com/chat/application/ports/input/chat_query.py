"""
인바운드(드라이빙) 포트: 채팅 요청 — API/인바운드가 호출하는 유스케이스 계약.
구현: use_cases 또는 use_cases/hub/orchestrators.
"""
from abc import ABC, abstractmethod

from labzang.apps.com.chat.application.dtos import ChatRequestDto, ChatResponseDto


class ChatQueryInputPort(ABC):
    """채팅 유스케이스 입력 포트. 인바운드 어댑터가 이 인터페이스를 호출합니다."""

    @abstractmethod
    def execute(self, request: ChatRequestDto) -> ChatResponseDto:
        """메시지에 대한 응답 생성해 반환."""
        ...
