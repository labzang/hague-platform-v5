"""
타이타닉 헥사고날 API (인바운드 어댑터)
- 도메인 포트 구현체 조립 → 유스케이스 주입 → HTTP → 유스케이스
"""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException

from labzang.core.paths import KAGGLE_ROOT
from labzang.apps.kaggle.domain.ports import (
    ITitanicDataPort,
    IPreprocessorPort,
    IModelRunnerPort,
)
from labzang.apps.kaggle.application.use_cases import (
    PreprocessTitanicUseCase,
    EvaluateTitanicUseCase,
    SubmitTitanicUseCase,
)
from labzang.apps.kaggle.adapter.output import (
    CsvTitanicDataAdapter,
    TitanicPreprocessorAdapter,
    SklearnTitanicModelAdapter,
)
from labzang.shared import create_response

router = APIRouter(prefix="/titanic", tags=["titanic-hex"])

# 데이터 경로: kaggle/data/titanic (application과 분리)
_resources_dir: Optional[Path] = None


def _get_resources_dir() -> Path:
    global _resources_dir
    if _resources_dir is not None:
        return _resources_dir
    _resources_dir = (KAGGLE_ROOT / "data" / "titanic").resolve()
    return _resources_dir


def _create_data_port() -> ITitanicDataPort:
    return CsvTitanicDataAdapter(_get_resources_dir())


def _create_preprocessor_port() -> IPreprocessorPort:
    return TitanicPreprocessorAdapter()


def _create_model_port() -> IModelRunnerPort:
    return SklearnTitanicModelAdapter()


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
async def preprocess():
    """전처리 실행 (유스케이스)."""
    try:
        data_port = _create_data_port()
        preprocessor_port = _create_preprocessor_port()
        use_case = PreprocessTitanicUseCase(data_port, preprocessor_port)
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
async def evaluate():
    """모델 평가 실행 (유스케이스)."""
    try:
        data_port = _create_data_port()
        preprocessor_port = _create_preprocessor_port()
        model_port = _create_model_port()
        use_case = EvaluateTitanicUseCase(data_port, preprocessor_port, model_port)
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
async def submit():
    """제출 파일 생성 (유스케이스)."""
    try:
        data_port = _create_data_port()
        preprocessor_port = _create_preprocessor_port()
        model_port = _create_model_port()
        use_case = SubmitTitanicUseCase(data_port, preprocessor_port, model_port)
        result = use_case.execute()
        return create_response(data=result, message="제출 파일이 생성되었습니다")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
