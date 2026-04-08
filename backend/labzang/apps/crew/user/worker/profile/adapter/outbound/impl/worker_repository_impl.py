"""WorkerRepositoryPort 스텁(영속 구현 전까지 미구현)."""

from __future__ import annotations

from labzang.apps.crew.user.worker.profile.app.ports.output.worker_repository import (
    WorkerRepositoryPort,
)
from labzang.apps.crew.user.worker.profile.domain.entities.worker import Worker


class WorkerRepositoryImpl(WorkerRepositoryPort):
    def create(self, worker: Worker) -> None:
        raise NotImplementedError

    def update(self, worker: Worker) -> None:
        raise NotImplementedError

    def delete(self, user_id: str) -> None:
        raise NotImplementedError
