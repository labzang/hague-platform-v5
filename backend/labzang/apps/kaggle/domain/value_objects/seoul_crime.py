"""
서울 범죄 도메인 값 객체 (순수: 외부 라이브러리 미참조)
"""
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SeoulPreprocessResult:
    """서울 범죄 전처리 결과."""
    status: str
    cctv_rows: int
    cctv_columns: List[str]
    crime_rows: int
    crime_columns: List[str]
    pop_rows: int
    pop_columns: List[str]
    cctv_pop_rows: int
    cctv_pop_columns: List[str]
    cctv_preview: List[Dict[str, Any]]
    crime_preview: List[Dict[str, Any]]
    pop_preview: List[Dict[str, Any]]
    cctv_pop_preview: List[Dict[str, Any]]
    message: str
