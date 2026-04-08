"""WorkerCommandPort 구현."""

from __future__ import annotations

from labzang.apps.crew.user.worker.profile.app.ports.input.worker_command_port import (
    WorkerCommandPort,
)
from labzang.apps.crew.user.worker.profile.app.ports.output.worker_repository_port import (
    WorkerRepositoryPort,
)
from labzang.apps.crew.user.worker.profile.domain.entities.worker import Worker


class WorkerCommandImpl(WorkerCommandPort):
    def __init__(self, repository: WorkerRepositoryPort) -> None:
        self._repository = repository

    def create_worker(self, user_id: str, name: str, role: str) -> Worker:
        worker = Worker(user_id=user_id, name=name, role=role)
        self._repository.create(worker)
        return worker

    def update_worker(self, user_id: str, name: str, role: str) -> Worker:
        worker = Worker(user_id=user_id, name=name, role=role)
        self._repository.update(worker)
        return worker

    def delete_worker(self, user_id: str) -> None:
        self._repository.delete(user_id)
