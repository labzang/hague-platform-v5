"""
타이타닉 유스케이스 (한 파일에 통합)
- 포트(인터페이스)만 의존, 비즈니스 오케스트레이션
"""

from labzang.apps.kaggle.domain.ports import (
    ITitanicDataPort,
    IPreprocessorPort,
    IModelRunnerPort,
)
from labzang.apps.kaggle.domain.value_objects import PreprocessResult, EvaluationResult


class PreprocessTitanicUseCase:
    def __init__(
        self, data_port: ITitanicDataPort, preprocessor_port: IPreprocessorPort
    ):
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


class EvaluateTitanicUseCase:
    def __init__(
        self,
        data_port: ITitanicDataPort,
        preprocessor_port: IPreprocessorPort,
        model_port: IModelRunnerPort,
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


class SubmitTitanicUseCase:
    def __init__(
        self,
        data_port: ITitanicDataPort,
        preprocessor_port: IPreprocessorPort,
        model_port: IModelRunnerPort,
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
