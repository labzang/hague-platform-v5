"""입력 포트: 워커 변경 유스케이스."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from labzang.apps.crew.user.worker.profile.domain.entities.worker import Worker


@runtime_checkable
class WorkerCommandPort(Protocol):
    def create_worker(self, user_id: str, name: str, role: str) -> Worker:
        """신규 워커를 저장한다."""

    def update_worker(self, user_id: str, name: str, role: str) -> Worker:
        """기존 워커를 갱신한다."""

    def delete_worker(self, user_id: str) -> None:
        """user_id 기준으로 워커를 삭제한다."""


__all__ = ["WorkerCommandPort"]
