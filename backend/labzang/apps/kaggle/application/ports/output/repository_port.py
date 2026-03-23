"""
범용 저장소 아웃바운드 포트 (ml 앱 — 확장용 placeholder).
"""
from abc import ABC


class RepositoryPort(ABC):
    """도메인별 리포지토리 계약의 기본 마커. 구체 메서드는 하위 포트에서 정의."""
