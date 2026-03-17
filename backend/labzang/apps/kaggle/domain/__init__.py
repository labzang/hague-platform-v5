"""
도메인 계층 (Hexagonal - 의존성 0, 순수만)
- entities: 순수 파이썬 엔티티
- value_objects: 구조화된 데이터 (외부 라이브러리 미참조)
- ports: 아웃바운드 포트(인터페이스). 구현은 Adapter에.
"""
from .value_objects import (
    TitanicDataSet,
    PreprocessResult,
    EvaluationResult,
)
from .ports import (
    ITitanicDataPort,
    IPreprocessorPort,
    IModelRunnerPort,
    IVectorDbPort,
    ILlmPort,
    IRepositoryPort,
)
from .entities import TitanicModels

__all__ = [
    "TitanicDataSet",
    "PreprocessResult",
    "EvaluationResult",
    "ITitanicDataPort",
    "IPreprocessorPort",
    "IModelRunnerPort",
    "IVectorDbPort",
    "ILlmPort",
    "IRepositoryPort",
    "TitanicModels",
]
