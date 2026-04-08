"""입력 포트: 워커 조회 유스케이스."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from labzang.apps.crew.user.worker.profile.domain.entities.worker import Worker


@runtime_checkable
class WorkerQueryPort(Protocol):
    def find_by_id(self, user_id: str) -> Worker | None:
        """user_id 로 단일 워커를 조회한다."""

    def find_all(self) -> list[Worker]:
        """전체 워커 목록을 조회한다."""


__all__ = ["WorkerQueryPort"]
