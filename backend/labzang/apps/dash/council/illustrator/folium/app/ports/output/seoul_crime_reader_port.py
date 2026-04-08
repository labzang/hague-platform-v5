"""
아웃바운드 Reader 포트 — 서울 범죄 원천 데이터 조회 전용.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SeoulCrimeReaderPort(Protocol):
    """파일 기반 read model: data_dir의 CSV/XLS 읽기."""

    def get_data_dir(self) -> str:
        ...

    def load_cctv(self) -> Any:
        ...

    def load_crime(self) -> Any:
        ...

    def load_pop(self) -> Any:
        ...


__all__ = ["SeoulCrimeReaderPort"]
