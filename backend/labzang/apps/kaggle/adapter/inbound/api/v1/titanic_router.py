"""
타이타닉 헥사고날 API (인바운드 어댑터)
- 유스케이스는 조립 루트(dependencies)에서 주입받음. 출력 어댑터 직접 참조 없음.
"""
from fastapi import APIRouter, Depends, HTTPException

from labzang.apps.kaggle.application.use_cases import (
    PreprocessTitanicUseCase,
    EvaluateTitanicUseCase,
    SubmitTitanicUseCase,
)
from labzang.apps.kaggle.adapter.input.dependencies import (
    get_preprocess_titanic_use_case,
    get_evaluate_titanic_use_case,
    get_submit_titanic_use_case,
)
from labzang.shared import create_response

router = APIRouter(prefix="/titanic", tags=["titanic-hex"])


@router.get("/")
async def titanic_hex_root():
    """헥사고날 타이타닉 서비스 루트."""
    return create_response(
        data={
            "service": "mlservice",
            "module": "titanic-hex",
            "architecture": "hexagonal",
            "status": "running",
        },
        message="Titanic Hexagonal API is running",
    )


@router.get("/preprocess")
async def preprocess(
    use_case: PreprocessTitanicUseCase = Depends(get_preprocess_titanic_use_case),
):
    """전처리 실행 (유스케이스)."""
    try:
        result = use_case.execute()
        return create_response(
            data={
                "status": result.status,
                "rows": result.rows,
                "columns": result.columns,
                "column_count": result.column_count,
                "null_count": result.null_count,
                "sample_data": result.sample_data,
                "dtypes": result.dtypes,
            },
            message="데이터 전처리가 완료되었습니다",
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evaluate")
async def evaluate(
    use_case: EvaluateTitanicUseCase = Depends(get_evaluate_titanic_use_case),
):
    """모델 평가 실행 (유스케이스)."""
    try:
        result = use_case.execute()
        return create_response(
            data={
                "best_model": result.best_model,
                "results": result.results,
            },
            message="모델 평가가 완료되었습니다",
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/submit")
async def submit(
    use_case: SubmitTitanicUseCase = Depends(get_submit_titanic_use_case),
):
    """제출 파일 생성 (유스케이스)."""
    try:
        result = use_case.execute()
        return create_response(data=result, message="제출 파일이 생성되었습니다")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
