"""
타이타닉 헥사고날 API (인바운드 어댑터)
- 유스케이스는 조립 루트(dependencies)에서 주입받음. 출력 어댑터 직접 참조 없음.
"""

from fastapi import APIRouter, Depends, HTTPException, Request

from labzang.apps.data.kaggle.santander.adapter.inbound.api.schemas.titanic_req import (
    parse_jsonl_to_rows,
)
from labzang.apps.data.kaggle.santander.adapter.inbound.dependencies import (
    get_evaluate_titanic_use_case,
    get_preprocess_titanic_use_case,
    get_submit_titanic_use_case,
)
from labzang.apps.data.kaggle.santander.application.dtos.titanic_dto import EvaluationResult
from labzang.apps.data.kaggle.santander.application.use_cases import (
    EvaluateTitanicUC,
    PreprocessTitanicUC,
    SubmitTitanicUC,
)
from labzang.apps.data.kaggle.titanic.adapter.inbound.api.v1.titanic_batch_router import (
    router as titanic_batch_router,
)
from labzang.apps.data.kaggle.titanic.adapter.inbound.api.v1.titanic_query_router import (
    router as titanic_query_router,
)
from labzang.shared import create_response

router = APIRouter(prefix="/titanic", tags=["titanic-hex"])
router.include_router(titanic_batch_router, prefix="/batch")
router.include_router(titanic_query_router, prefix="/query")


@router.post("/train/ingest")
async def ingest_train_jsonl(request: Request):
    """
    train.csv 데이터를 JSONL 형태로 수신.
    한 줄당 하나의 JSON 객체 (PassengerId, Survived, Pclass, Name, Sex, Age, ...).
    파싱된 행 수와 요약만 반환. 실제 DB insert는 다음 단계에서 연동.
    """
    try:
        body = await request.body()
        jsonl_text = body.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"본문 디코딩 실패: {e}")

    try:
        rows = parse_jsonl_to_rows(jsonl_text)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"JSONL 파싱 실패: {e}",
        )

    if not rows:
        return create_response(
            data={"accepted": 0, "rows": [], "message": "수신된 행이 없습니다."},
            message="JSONL 파싱 완료 (0건)",
        )

    # 라우터 단계: 파싱 결과만 반환. insert는 다음 단계에서 주입할 서비스/유스케이스에서 수행
    return create_response(
        data={
            "accepted": len(rows),
            "rows": [r.model_dump(by_alias=True) for r in rows[:10]],  # 샘플 10건
            "total": len(rows),
        },
        message=f"JSONL 파싱 완료 ({len(rows)}건). 다음 단계에서 insert 연동 예정.",
    )


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
    use_case: PreprocessTitanicUC = Depends(get_preprocess_titanic_use_case),
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
    use_case: EvaluateTitanicUC = Depends(get_evaluate_titanic_use_case),
):
    """모델 평가 실행 (유스케이스)."""
    try:
        result = use_case.execute()
        if not isinstance(result, EvaluationResult):
            raise HTTPException(
                status_code=500,
                detail=f"평가 결과 타입 오류: {type(result).__name__}",
            )
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
    use_case: SubmitTitanicUC = Depends(get_submit_titanic_use_case),
):
    """제출 파일 생성 (유스케이스)."""
    try:
        result = use_case.execute()
        return create_response(data=result, message="제출 파일이 생성되었습니다")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
