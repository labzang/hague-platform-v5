# -*- coding: utf-8 -*-
"""선수 커맨드 입력 포트 (애플리케이션 경계)."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class PlayerCommandPort(ABC):
    """선수 변경 유스케이스 진입점."""

    @abstractmethod
    async def upload_players_batch(
        self, players_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """JSONL에서 파싱한 선수 행 목록을 DB에 일괄 upsert.

        Returns:
            저장소가 반환하는 통계 딕셔너리 (inserted_count, updated_count, error_count 등).
        """
        ...
