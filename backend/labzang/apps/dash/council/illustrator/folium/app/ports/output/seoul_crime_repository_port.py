"""아웃바운드 Repository 포트 — 서울 범죄 전처리 결과 저장(쓰기) 전용."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SeoulCrimeRepositoryPort(Protocol):
    """파일 기반 persistence: save_dir에 crime.csv 쓰기."""

    def get_save_dir(self) -> str:
        """전처리 결과 저장 디렉터리 경로(문자열)."""
        ...

    def save_crime(self, crime_df: Any) -> str:
        """전처리된 범죄 DataFrame을 저장하고 저장 파일 경로를 반환."""
        ...


__all__ = ["SeoulCrimeRepositoryPort"]
