"""출력 포트: 워커 영속화(쓰기)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from labzang.apps.crew.user.worker.profile.domain.entities.worker import Worker


@runtime_checkable
class WorkerRepositoryPort(Protocol):
    def create(self, worker: Worker) -> None:
        """워커를 새로 저장한다."""

    def update(self, worker: Worker) -> None:
        """기존 워커를 갱신한다."""

    def delete(self, user_id: str) -> None:
        """user_id 기준 삭제."""


__all__ = ["WorkerRepositoryPort"]
