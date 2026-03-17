"""
레거시 경로용 타이타닉 API (인바운드 어댑터)
- /titanic 경로. Use Case + Output Port만 사용 (TitanicService 제거, Application 계층 통합)
"""
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException

from domain.ports import ITitanicDataPort, IPreprocessorPort, IModelRunnerPort
from application.use_cases import (
    PreprocessTitanicUseCase,
    EvaluateTitanicUseCase,
    SubmitTitanicUseCase,
)
from adapter.output import (
    CsvTitanicDataAdapter,
    TitanicPreprocessorAdapter,
    SklearnTitanicModelAdapter,
)

router = APIRouter(tags=["titanic"])

_resources_dir: Optional[Path] = None


def _get_resources_dir() -> Path:
    global _resources_dir
    if _resources_dir is not None:
        return _resources_dir
    base = Path(__file__).resolve().parent.parent.parent.parent.parent
    _resources_dir = base / "application" / "resources" / "titanic"
    return _resources_dir


def _create_data_port() -> ITitanicDataPort:
    return CsvTitanicDataAdapter(_get_resources_dir())


def _create_preprocessor_port() -> IPreprocessorPort:
    return TitanicPreprocessorAdapter()


def _create_model_port() -> IModelRunnerPort:
    return SklearnTitanicModelAdapter()


def _response(data, message):
    try:
        from common.utils import create_response
        return create_response(data=data, message=message)
    except ImportError:
        return {"data": data, "message": message}


@router.get("/")
async def titanic_root():
    return _response(
        data={"service": "mlservice", "module": "titanic", "status": "running"},
        message="Titanic Service is running",
    )


@router.get("/preprocess")
async def preprocess_data():
    try:
        data_port = _create_data_port()
        preprocessor_port = _create_preprocessor_port()
        use_case = PreprocessTitanicUseCase(data_port, preprocessor_port)
        result = use_case.execute()
        return _response(
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
async def evaluate_model():
    try:
        data_port = _create_data_port()
        preprocessor_port = _create_preprocessor_port()
        model_port = _create_model_port()
        use_case = EvaluateTitanicUseCase(data_port, preprocessor_port, model_port)
        result = use_case.execute()
        return _response(
            data={"best_model": result.best_model, "results": result.results},
            message="모델 평가가 완료되었습니다",
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/submit")
async def submit_model():
    try:
        data_port = _create_data_port()
        preprocessor_port = _create_preprocessor_port()
        model_port = _create_model_port()
        use_case = SubmitTitanicUseCase(data_port, preprocessor_port, model_port)
        result = use_case.execute()
        return _response(data=result, message="제출 파일이 생성되었습니다")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
