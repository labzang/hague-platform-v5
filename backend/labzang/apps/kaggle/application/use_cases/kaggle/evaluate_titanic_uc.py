"""
타이타닉 모델 평가 유스케이스 (단일 클래스 — Pyright가 execute() 반환 타입을 Preprocess와 혼동하지 않도록 분리)
"""

from labzang.apps.ml.application.dtos.titanic_dto import EvaluationResult
from labzang.apps.ml.application.ports import (
    TitanicDataPort,
    PreprocessorPort,
    ModelRunnerPort,
)


class EvaluateTitanicUC:
    def __init__(
        self,
        data_port: TitanicDataPort,
        preprocessor_port: PreprocessorPort,
        model_port: ModelRunnerPort,
    ):
        self._data = data_port
        self._preprocessor = preprocessor_port
        self._model = model_port

    def execute(self) -> EvaluationResult:
        train_df = self._data.load_train()
        test_df = self._data.load_test()
        data_set = self._preprocessor.preprocess(train_df, test_df)
        raw = self._model.evaluate(data_set.train, "Survived")
        return EvaluationResult(
            best_model=raw.get("best_model"),
            results=raw.get("results", {}),
        )
