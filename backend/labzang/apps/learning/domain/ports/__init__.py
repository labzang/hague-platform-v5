"""
아웃바운드 포트 (도메인 계층)
- 구현은 adapter 계층에 위치
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from domain.value_objects import TitanicDataSet

# --- 타이타닉 (기존) ---
class ITitanicDataPort(ABC):
    @abstractmethod
    def load_train(self) -> Any: ...

    @abstractmethod
    def load_test(self) -> Any: ...

    @abstractmethod
    def save_submission(self, passenger_ids: Any, predictions: Any) -> str: ...


class IPreprocessorPort(ABC):
    @abstractmethod
    def preprocess(self, train_df: Any, test_df: Any) -> TitanicDataSet: ...


class IModelRunnerPort(ABC):
    @abstractmethod
    def evaluate(self, train_data: Any, target_column: str) -> Dict[str, Any]: ...

    @abstractmethod
    def predict_for_submit(
        self, train_data: Any, test_data: Any, target_column: str
    ) -> Any: ...


# --- RAG/LLM/CRUD ---
from domain.ports.vector_db_port import IVectorDbPort
from domain.ports.llm_port import ILlmPort
from domain.ports.repository_port import IRepositoryPort
# --- Seoul Crime ---
from domain.ports.seoul_ports import (
    ISeoulDataPort,
    ISeoulPreprocessorPort,
    IGeocodePort,
)

__all__ = [
    "ITitanicDataPort",
    "IPreprocessorPort",
    "IModelRunnerPort",
    "IVectorDbPort",
    "ILlmPort",
    "IRepositoryPort",
    "ISeoulDataPort",
    "ISeoulPreprocessorPort",
    "IGeocodePort",
]
