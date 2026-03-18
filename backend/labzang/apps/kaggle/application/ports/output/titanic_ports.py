"""
Outbound: 타이타닉 데이터·전처리·모델 실행 포트
- 구현: adapter/outbound/persistence (titanic_adapters 등)
"""
from abc import ABC, abstractmethod
from typing import Any, Dict

from labzang.apps.kaggle.domain.value_objects import TitanicDataSet


class ITitanicDataPort(ABC):
    """타이타닉 train/test 로드 및 제출 파일 저장."""

    @abstractmethod
    def load_train(self) -> Any:
        ...

    @abstractmethod
    def load_test(self) -> Any:
        ...

    @abstractmethod
    def save_submission(self, passenger_ids: Any, predictions: Any) -> str:
        ...


class IPreprocessorPort(ABC):
    """타이타닉 전처리 (train/test → TitanicDataSet)."""

    @abstractmethod
    def preprocess(self, train_df: Any, test_df: Any) -> TitanicDataSet:
        ...


class IModelRunnerPort(ABC):
    """타이타닉 모델 평가·예측."""

    @abstractmethod
    def evaluate(self, train_data: Any, target_column: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def predict_for_submit(
        self, train_data: Any, test_data: Any, target_column: str
    ) -> Any:
        ...
