"""
Titanic Spoke: 타이타닉 분석 전용 로직
- Use Case(Preprocess/Evaluate/Submit) 호출 또는 직접 Port 조합
"""

from typing import Any

# application.use_cases 의 Use Case를 호출하거나,
# 동일한 Port 조합으로 여기서만 쓰는 흐름 정의 가능


def run_titanic_analysis(
    action: str,
    data_port: Any,
    preprocessor_port: Any,
    model_port: Any,
) -> dict:
    """액션에 따라 타이타닉 전처리/평가/제출 중 하나 실행."""
    from labzang.apps.kaggle.application.use_cases import (
        PreprocessTitanicUseCase,
        EvaluateTitanicUseCase,
        SubmitTitanicUseCase,
    )

    if action == "preprocess":
        uc = PreprocessTitanicUseCase(data_port, preprocessor_port)
        r = uc.execute()
        return {"status": r.status, "rows": r.rows, "columns": r.columns}
    if action == "evaluate":
        uc = EvaluateTitanicUseCase(data_port, preprocessor_port, model_port)
        r = uc.execute()
        return {"best_model": r.best_model, "results": r.results}
    if action == "submit":
        uc = SubmitTitanicUseCase(data_port, preprocessor_port, model_port)
        return uc.execute()
    return {"error": f"unknown action: {action}"}
