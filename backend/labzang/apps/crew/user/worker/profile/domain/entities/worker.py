"""Worker aggregate root (user_id 기준 단일 프로필)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Worker:
    """user_id, name, role 만을 갖는 워커 엔티티."""

    user_id: str
    name: str
    role: str
