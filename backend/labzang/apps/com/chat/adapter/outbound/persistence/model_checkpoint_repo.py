"""
학습 체크포인트 위치 관리 — ModelCheckpointRepositoryPort 구현.
학습 중/후 체크포인트 경로 관리 (예: checkpoints/epoch-1, best/, 버전 정보).
"""
from typing import Any, Dict, List, Optional

from labzang.apps.com.chat.application.ports.output import ModelCheckpointRepositoryPort


class ModelCheckpointRepositoryAdapter(ModelCheckpointRepositoryPort):
    """체크포인트 저장소 아웃바운드 어댑터."""

    def get_checkpoint_path(self, run_id: str, kind: str = "latest") -> Optional[str]:
        """체크포인트 디렉터리/파일 경로 반환. kind: latest, best, epoch-N 등."""
        raise NotImplementedError(
            "ModelCheckpointRepositoryAdapter.get_checkpoint_path: persistence 구현 필요"
        )

    def save_checkpoint(
        self,
        run_id: str,
        path: str,
        meta: Optional[Dict[str, Any]] = None,
    ) -> str:
        """체크포인트 경로 등록. 반환: 저장된 경로."""
        raise NotImplementedError(
            "ModelCheckpointRepositoryAdapter.save_checkpoint: persistence 구현 필요"
        )

    def list_checkpoints(self, run_id: str) -> List[Dict[str, Any]]:
        """run_id에 대한 체크포인트 목록(경로, 버전, 메타)."""
        raise NotImplementedError(
            "ModelCheckpointRepositoryAdapter.list_checkpoints: persistence 구현 필요"
        )
