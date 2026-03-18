"""
도메인 계층 (Hexagonal - 의존성 0, 순수만)
- entities: 순수 파이썬 엔티티
- value_objects: 구조화된 데이터 (외부 라이브러리 미참조)
- 포트(인터페이스)는 application/ports에 위치 (input/output 분리)
"""
from .value_objects import (
    TitanicDataSet,
    PreprocessResult,
    EvaluationResult,
)
from .entities import TitanicModels

__all__ = [
    "TitanicDataSet",
    "PreprocessResult",
    "EvaluationResult",
    "TitanicModels",
]
