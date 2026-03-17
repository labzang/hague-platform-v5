"""
도메인 값 객체 (순수, 외부 라이브러리 미참조)
"""
from dataclasses import dataclass
from typing import Any, List


@dataclass
class ChartResult:
    """차트 크롤링 결과."""
    chart_type: str
    total_count: int
    songs: List[dict]
    raw: Any = None
