"""WorkerQueryPort 구현."""

from __future__ import annotations

from labzang.apps.crew.user.worker.profile.app.ports.input.worker_query import (
    WorkerQueryPort,
)
from labzang.apps.crew.user.worker.profile.app.ports.output.worker_reader import (
    WorkerReaderPort,
)
from labzang.apps.crew.user.worker.profile.domain.entities.worker import Worker


class WorkerQueryImpl(WorkerQueryPort):
    def __init__(self, reader: WorkerReaderPort) -> None:
        self._reader = reader

    def find_by_id(self, user_id: str) -> Worker | None:
        return self._reader.find_by_id(user_id)

    def find_all(self) -> list[Worker]:
        return self._reader.find_all()
