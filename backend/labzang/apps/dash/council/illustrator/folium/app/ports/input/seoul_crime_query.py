"""Input port (Query side): 서울 범죄 도메인의 조회 유스케이스."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SeoulCrimeQueryPort(ABC):
    """
    CQRS - Query 전용 포트.

    - 상태를 변경하지 않는 읽기 모델/대시보드/미리보기 조회만 정의한다.
    - 저장/전처리/생성 같은 write 책임은 `seoul_crime_command.py` 로 분리한다.
    """

    @abstractmethod
    def get_raw_snapshot(self) -> dict[str, Any]:
        """원본(raw) 입력 데이터 요약(행 수, 컬럼, 샘플 등)을 조회한다."""
        ...

    @abstractmethod
    def get_processed_snapshot(self) -> dict[str, Any]:
        """전처리 결과(processed) 요약을 조회한다."""
        ...

    @abstractmethod
    def get_police_norm_summary(self) -> dict[str, Any]:
        """`police_norm_in_seoul.csv` 기준 통계 요약을 조회한다."""
        ...

    @abstractmethod
    def get_map_html(self) -> str:
        """저장된/생성된 서울 범죄 지도 HTML(read model)을 조회한다."""
        ...

    @abstractmethod
    def list_artifacts(self) -> dict[str, str]:
        """조회 가능한 산출물 파일 경로 목록을 반환한다."""
        ...
