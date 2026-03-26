"""
학습용 데이터셋 관리 — TrainingDatasetRepositoryPort 구현.
학습용 데이터셋(HF Dataset, 로컬 파일) 로드/저장 및 메타 정보 관리.
"""
from typing import Any, Dict, List, Optional

from labzang.apps.com.chat.application.ports.output import TrainingDatasetRepositoryPort


class TrainingDatasetRepositoryAdapter(TrainingDatasetRepositoryPort):
    """학습 데이터셋 저장소 아웃바운드 어댑터."""

    def load_dataset(self, name: str) -> Any:
        """데이터셋 이름으로 로드."""
        raise NotImplementedError(
            "TrainingDatasetRepositoryAdapter.load_dataset: persistence 구현 필요"
        )

    def save_dataset(
        self,
        name: str,
        data: Any,
        meta: Optional[Dict[str, Any]] = None,
    ) -> str:
        """데이터셋 저장. 반환: 저장 경로 또는 식별자."""
        raise NotImplementedError(
            "TrainingDatasetRepositoryAdapter.save_dataset: persistence 구현 필요"
        )

    def get_meta(self, name: str) -> Optional[Dict[str, Any]]:
        """데이터셋 메타 정보 조회."""
        raise NotImplementedError(
            "TrainingDatasetRepositoryAdapter.get_meta: persistence 구현 필요"
        )

    def list_datasets(self) -> List[Dict[str, Any]]:
        """데이터셋 목록(이름·용도·메타) 반환."""
        raise NotImplementedError(
            "TrainingDatasetRepositoryAdapter.list_datasets: persistence 구현 필요"
        )
