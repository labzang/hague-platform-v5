"""
아웃바운드 포트 (Application 계층) — 구현은 adapter/outbound
"""
from .repository_port import IRepositoryPort
from .vector_db_port import IVectorDbPort
from .llm_port import ILlmPort
from .seoul_ports import ISeoulDataPort, ISeoulPreprocessorPort, IGeocodePort
from .titanic_ports import ITitanicDataPort, IPreprocessorPort, IModelRunnerPort

__all__ = [
    "IRepositoryPort",
    "IVectorDbPort",
    "ILlmPort",
    "ISeoulDataPort",
    "ISeoulPreprocessorPort",
    "IGeocodePort",
    "ITitanicDataPort",
    "IPreprocessorPort",
    "IModelRunnerPort",
]
