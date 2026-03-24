"""
Titanic Spoke: ?�?��???분석 ?�용 로직
- Use Case(Preprocess/Evaluate/Submit) ?�출 ?�는 직접 Port 조합
"""

from typing import Any, cast

from labzang.apps.kaggle.application.dtos.titanic_dto import EvaluationResult, PreprocessResult


def _run_preprocess(data_port: Any, preprocessor_port: Any) -> dict:
    from labzang.apps.kaggle.application.use_cases.titanic_uc import PreprocessTitanicUC

    pre = cast(
        PreprocessResult,
        PreprocessTitanicUC(data_port, preprocessor_port).execute(),
    )
    return {"status": pre.status, "rows": pre.rows, "columns": pre.columns}


def _run_evaluate(data_port: Any, preprocessor_port: Any, model_port: Any) -> dict:
    from labzang.apps.kaggle.application.use_cases.titanic_uc import EvaluateTitanicUC

    raw = EvaluateTitanicUC(data_port, preprocessor_port, model_port).execute()
    # ports ?�키지가 깨져 ?�으�?Pyright가 execute() 반환???�못 붙이??경우가 ?�어 명시?�으�?좁힘
    if not isinstance(raw, EvaluationResult):
        raise TypeError(f"expected EvaluationResult, got {type(raw).__name__}")
    return {"best_model": raw.best_model, "results": raw.results}


def _run_submit(data_port: Any, preprocessor_port: Any, model_port: Any) -> dict:
    from labzang.apps.kaggle.application.use_cases.titanic_uc import SubmitTitanicUC

    return SubmitTitanicUC(data_port, preprocessor_port, model_port).execute()


def run_titanic_analysis(
    action: str,
    data_port: Any,
    preprocessor_port: Any,
    model_port: Any,
) -> dict:
    """?�션???�라 ?�?��????�처�??��?/?�출 �??�나 ?�행."""
    if action == "preprocess":
        return _run_preprocess(data_port, preprocessor_port)
    if action == "evaluate":
        return _run_evaluate(data_port, preprocessor_port, model_port)
    if action == "submit":
        return _run_submit(data_port, preprocessor_port, model_port)
    return {"error": f"unknown action: {action}"}
