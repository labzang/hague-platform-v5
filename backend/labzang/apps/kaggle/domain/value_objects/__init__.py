"""
도메인 값 객체 (순수: 외부 라이브러리 미참조)
- 비즈니스 규칙이 담긴 불변/구조화된 데이터
"""
from .titanic import TitanicDataSet, PreprocessResult, EvaluationResult
from .seoul_crime import SeoulPreprocessResult

__all__ = [
    "TitanicDataSet",
    "PreprocessResult",
    "EvaluationResult",
    "SeoulPreprocessResult",
]
