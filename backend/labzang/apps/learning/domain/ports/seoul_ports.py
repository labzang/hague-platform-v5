"""
Outbound: 서울 범죄 데이터·전처리·지오코딩 포트
- 구현: adapter/output/seoul_crime_adapters
"""
from abc import ABC, abstractmethod
from typing import Any, List


class ISeoulDataPort(ABC):
    """서울 범죄/인구/CCTV 데이터 로드 및 저장."""

    @abstractmethod
    def get_data_dir(self) -> str:
        ...

    @abstractmethod
    def get_save_dir(self) -> str:
        ...

    @abstractmethod
    def load_cctv(self) -> Any:
        ...

    @abstractmethod
    def load_crime(self) -> Any:
        ...

    @abstractmethod
    def load_pop(self) -> Any:
        ...

    @abstractmethod
    def save_crime(self, crime_df: Any) -> str:
        """crime DataFrame 저장 후 저장 경로 반환."""
        ...


class ISeoulPreprocessorPort(ABC):
    """서울 데이터 전처리(컬럼 정리, 머지 등). pandas는 Adapter에서만."""

    @abstractmethod
    def csv_to_df(self, path: str) -> Any:
        ...

    @abstractmethod
    def xlsx_to_df(self, path: str) -> Any:
        ...

    @abstractmethod
    def df_merge(
        self,
        left: Any,
        right: Any,
        left_on: str,
        right_on: str,
        how: str = "inner",
    ) -> Any:
        ...

    @abstractmethod
    def drop_columns(self, df: Any, columns: List[str]) -> Any:
        """컬럼 제거 (원본 변경 없이 반환)."""
        ...

    @abstractmethod
    def drop_cctv_columns(self, cctv_df: Any, columns: List[str]) -> Any:
        ...

    @abstractmethod
    def filter_pop_columns_and_rows(self, pop_df: Any) -> Any:
        """pop: 자치구 + 4번째 컬럼만 유지, 상위 2·3·4행 제거."""
        ...

    @abstractmethod
    def get_station_names_from_crime(self, crime_df: Any) -> List[str]:
        """crime의 관서명으로 경찰서명 리스트 생성 ('서울'+관서명[:-1]+'경찰서')."""
        ...

    @abstractmethod
    def add_gu_to_crime(self, crime_df: Any, gu_list: List[str]) -> Any:
        """crime에 자치구 컬럼 추가."""
        ...

    @abstractmethod
    def order_crime_columns(self, crime_df: Any, desired_cols: List[str]) -> Any:
        """저장용 컬럼 순서 정렬."""
        ...

    @abstractmethod
    def head_to_dict(self, df: Any, n: int = 3) -> List[dict]:
        """DataFrame 상위 n행을 레코드 리스트로 (응답용)."""
        ...


class IGeocodePort(ABC):
    """주소/장소명 → 좌표·주소 (카카오/구글 등 구현)."""

    @abstractmethod
    def geocode(self, query: str, language: str = "ko") -> List[dict]:
        """반환: [{"formatted_address": str, "lat": float, "lng": float}, ...]"""
        ...
