"""Input port (Command side): 서울 범죄 도메인의 상태 변경 유스케이스."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SeoulCrimeCommandPort(ABC):
    """
    CQRS - Command 전용 포트.

    - 파일 생성/갱신, 전처리 수행, 지오코딩 반영, 지도 산출물 생성 등
      시스템 상태를 변경하는 유스케이스만 정의한다.
    - 조회/미리보기/통계 조회는 `seoul_crime_query.py` 로 분리한다.
    """

    @abstractmethod
    def ingest_raw_files(self) -> dict[str, str]:
        """원본 입력 파일(cctv/crime/pop) 적재 결과를 반환한다."""
        ...

    @abstractmethod
    def preprocess(self, *, force_geocode: bool = False) -> dict[str, Any]:
        """
        전처리 파이프라인을 실행한다.

        예: CCTV 정리, 인구 정리, 경찰서->자치구 지오코딩, police_norm 생성 등.
        """
        ...

    @abstractmethod
    def rebuild_police_norm(self) -> dict[str, Any]:
        """`police_in_seoul.csv`, `police_norm_in_seoul.csv`를 재생성한다."""
        ...

    @abstractmethod
    def generate_map(self) -> dict[str, Any]:
        """
        지도 산출물(HTML 등)을 생성/저장한다.

        조회에 필요한 메타(저장 경로, 행 수 등)만 반환한다.
        """
        ...
