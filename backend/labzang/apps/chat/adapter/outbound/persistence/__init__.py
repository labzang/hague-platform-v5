"""
Persistence 아웃바운드 어댑터 — 도메인 포트 구현체.
- 포트: labzang.apps.chat.domain.ports
"""
from labzang.apps.chat.adapter.outbound.persistence.document_repo import DocumentRepositoryAdapter
from labzang.apps.chat.adapter.outbound.persistence.training_dataset_repo import TrainingDatasetRepositoryAdapter
from labzang.apps.chat.adapter.outbound.persistence.model_checkpoint_repo import ModelCheckpointRepositoryAdapter
from labzang.apps.chat.adapter.outbound.persistence.vector_repo import VectorRepositoryAdapter

__all__ = [
    "DocumentRepositoryAdapter",
    "TrainingDatasetRepositoryAdapter",
    "ModelCheckpointRepositoryAdapter",
    "VectorRepositoryAdapter",
]
