"""
Titanic use cases in a single module.
Use cases depend only on application ports and DTOs.
"""

from labzang.apps.ai.percept.detective.santander.application.dtos.titanic_dto import (
    EvaluationResult,
    PreprocessResult,
)
from labzang.apps.ai.percept.detective.santander.application.ports import (
    ModelRunnerPort,
    PreprocessorPort,
    TitanicDataPort,
)
from labzang.apps.ai.percept.detective.titanic.app.ports.input.titanic_command import (
    TitanicPreprocessPort,
    TitanicSubmitPort,
)
from labzang.apps.ai.percept.detective.titanic.app.ports.input.titanic_query import (
    TitanicEvaluatePort,
)


class PreprocessTitanicUC(TitanicPreprocessPort):
    def __init__(self, data_port: TitanicDataPort, preprocessor_port: PreprocessorPort):
        self._data = data_port
        self._preprocessor = preprocessor_port

    def execute(self) -> PreprocessResult:
        train_df = self._data.load_train()
        test_df = self._data.load_test()
        data_set = self._preprocessor.preprocess(train_df, test_df)
        train = data_set.train
        null_count = int(train.isnull().sum().sum())
        return PreprocessResult(
            status="success",
            rows=len(train),
            columns=train.columns.tolist(),
            column_count=len(train.columns),
            null_count=null_count,
            sample_data=train.head(5).to_dict(orient="records"),
            dtypes=train.dtypes.astype(str).to_dict(),
        )


class SubmitTitanicUC(TitanicSubmitPort):
    def __init__(
        self,
        data_port: TitanicDataPort,
        preprocessor_port: PreprocessorPort,
        model_port: ModelRunnerPort,
    ):
        self._data = data_port
        self._preprocessor = preprocessor_port
        self._model = model_port

    def execute(self) -> dict:
        train_df = self._data.load_train()
        test_df = self._data.load_test()
        data_set = self._preprocessor.preprocess(train_df, test_df)
        predictions = self._model.predict_for_submit(
            data_set.train, data_set.test, "Survived"
        )
        saved_path = self._data.save_submission(
            data_set.test["PassengerId"], predictions
        )
        return {"status": "success", "saved_path": saved_path, "rows": len(predictions)}


class EvaluateTitanicUC(TitanicEvaluatePort):
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


__all__ = ["EvaluateTitanicUC", "PreprocessTitanicUC", "SubmitTitanicUC"]
