"""
서울 범죄 도메인 엔티티 (순수 파이썬)
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SeoulCrime:
    """서울 범죄 데이터 처리 Run — 식별자·메타."""
    run_id: str = ""
    message: Optional[str] = None
