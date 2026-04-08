"""애플리케이션 계층 전달용 DTO."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkerDto:
    user_id: str
    name: str
    role: str
