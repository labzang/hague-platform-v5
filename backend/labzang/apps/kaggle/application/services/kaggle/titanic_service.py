"""
Titanic Spoke: 타이타닉 분석 전용 로직
- Use Case(Preprocess/Evaluate/Submit) 호출 또는 직접 Port 조합
"""

from typing import Any, cast

from labzang.apps.ml.application.dtos.titanic_dto import EvaluationResult, PreprocessResult


def _run_preprocess(data_port: Any, preprocessor_port: Any) -> dict:
    from labzang.apps.ml.application.use_cases.kaggle.titanic_uc import PreprocessTitanicUC

    pre = cast(
        PreprocessResult,
        PreprocessTitanicUC(data_port, preprocessor_port).execute(),
    )
    return {"status": pre.status, "rows": pre.rows, "columns": pre.columns}


def _run_evaluate(data_port: Any, preprocessor_port: Any, model_port: Any) -> dict:
    from labzang.apps.ml.application.use_cases.kaggle.evaluate_titanic_uc import (
        EvaluateTitanicUC,
    )

    raw = EvaluateTitanicUC(data_port, preprocessor_port, model_port).execute()
    # ports 패키지가 깨져 있으면 Pyright가 execute() 반환을 잘못 붙이는 경우가 있어 명시적으로 좁힘
    if not isinstance(raw, EvaluationResult):
        raise TypeError(f"expected EvaluationResult, got {type(raw).__name__}")
    return {"best_model": raw.best_model, "results": raw.results}


def _run_submit(data_port: Any, preprocessor_port: Any, model_port: Any) -> dict:
    from labzang.apps.ml.application.use_cases.kaggle.titanic_uc import SubmitTitanicUC

    return SubmitTitanicUC(data_port, preprocessor_port, model_port).execute()


def run_titanic_analysis(
    action: str,
    data_port: Any,
    preprocessor_port: Any,
    model_port: Any,
) -> dict:
    """액션에 따라 타이타닉 전처리/평가/제출 중 하나 실행."""
    if action == "preprocess":
        return _run_preprocess(data_port, preprocessor_port)
    if action == "evaluate":
        return _run_evaluate(data_port, preprocessor_port, model_port)
    if action == "submit":
        return _run_submit(data_port, preprocessor_port, model_port)
    return {"error": f"unknown action: {action}"}
