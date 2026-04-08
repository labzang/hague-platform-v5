"""WorkerReaderPort 스텁(조회 구현 전까지 미구현)."""

from __future__ import annotations

from labzang.apps.crew.user.worker.profile.app.ports.output.worker_reader import (
    WorkerReaderPort,
)
from labzang.apps.crew.user.worker.profile.domain.entities.worker import Worker


class WorkerReaderImpl(WorkerReaderPort):
    def find_by_id(self, user_id: str) -> Worker | None:
        raise NotImplementedError

    def find_all(self) -> list[Worker]:
        raise NotImplementedError
