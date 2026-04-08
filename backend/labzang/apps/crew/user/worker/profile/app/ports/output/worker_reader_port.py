"""출력 포트: 워커 조회(읽기)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from labzang.apps.crew.user.worker.profile.domain.entities.worker import Worker


@runtime_checkable
class WorkerReaderPort(Protocol):
    def find_by_id(self, user_id: str) -> Worker | None:
        ...

    def find_all(self) -> list[Worker]:
        ...


__all__ = ["WorkerReaderPort"]
