"""
타이타닉 헥사고날 API (인바운드 어댑터)
- 도메인 포트 구현체 조립 → 유스케이스 주입 → HTTP → 유스케이스
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

router = APIRouter(prefix="/titanic", tags=["titanic-hex"])

# 리소스 경로: learning/application/resources/titanic (기존 구조 활용)
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


@router.get("/")
async def titanic_hex_root():
    """헥사고날 타이타닉 서비스 루트."""
    try:
        from common.utils import create_response
    except ImportError:
        def create_response(*, data, message): return {"data": data, "message": message}
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
        from common.utils import create_response
    except ImportError:
        def create_response(*, data, message): return {"data": data, "message": message}
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
        from common.utils import create_response
    except ImportError:
        def create_response(*, data, message): return {"data": data, "message": message}
    try:
        data_port = _create_data_port()
        preprocessor_port = _create_preprocessor_port()
        model_port = _create_model_port()
        use_case = EvaluateTitanicUseCase(
            data_port, preprocessor_port, model_port
        )
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
        from common.utils import create_response
    except ImportError:
        def create_response(*, data, message): return {"data": data, "message": message}
    try:
        data_port = _create_data_port()
        preprocessor_port = _create_preprocessor_port()
        model_port = _create_model_port()
        use_case = SubmitTitanicUseCase(
            data_port, preprocessor_port, model_port
        )
        result = use_case.execute()
        return create_response(data=result, message="제출 파일이 생성되었습니다")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
