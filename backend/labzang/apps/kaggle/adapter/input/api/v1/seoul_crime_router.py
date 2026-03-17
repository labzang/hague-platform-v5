"""
서울 범죄 헥사고날 API (인바운드 어댑터)
- 포트 구현체 조립 → 유스케이스 주입 → HTTP → 유스케이스
"""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from labzang.core.paths import LEARNING_ROOT
from labzang.apps.kaggle.domain.ports.seoul_ports import (
    ISeoulDataPort,
    ISeoulPreprocessorPort,
    IGeocodePort,
)
from labzang.apps.kaggle.application.use_cases.seoul_crime_use_cases import (
    PreprocessSeoulCrimeUseCase,
)
from labzang.apps.kaggle.adapter.output import (
    SeoulDataAdapter,
    SeoulPreprocessorAdapter,
    KakaoGeocodeAdapter,
)
from labzang.shared import create_response

router = APIRouter(tags=["seoul-hex"])  # prefix는 main에서 /seoul 로 등록

_base_dir: Optional[Path] = None


def _get_seoul_base_dir() -> Path:
    global _base_dir
    if _base_dir is not None:
        return _base_dir
    _base_dir = (LEARNING_ROOT / "application" / "seoul_crime").resolve()
    return _base_dir


def _create_data_port() -> ISeoulDataPort:
    d = _get_seoul_base_dir()
    return SeoulDataAdapter(d / "data", d / "save")


def _create_preprocessor_port() -> ISeoulPreprocessorPort:
    return SeoulPreprocessorAdapter()


def _create_geocode_port() -> IGeocodePort:
    return KakaoGeocodeAdapter()


@router.get("/")
async def seoul_hex_root() -> JSONResponse:
    """서울 범죄 헥사고날 서비스 루트."""
    body = create_response(
        data={
            "service": "mlservice",
            "module": "seoul-hex",
            "architecture": "hexagonal",
            "status": "running",
        },
        message="Seoul Crime Hexagonal API is running",
    )
    return JSONResponse(content=body)


@router.get("/preprocess")
async def preprocess():
    """서울 범죄 전처리 실행 (데이터 로드, cctv-pop 머지, 지오코딩, 저장)."""
    try:
        data_port = _create_data_port()
        preprocessor_port = _create_preprocessor_port()
        geocode_port = _create_geocode_port()
        use_case = PreprocessSeoulCrimeUseCase(
            data_port, preprocessor_port, geocode_port
        )
        result = use_case.execute()
        return create_response(
            data={
                "status": result.status,
                "cctv_rows": result.cctv_rows,
                "cctv_columns": result.cctv_columns,
                "crime_rows": result.crime_rows,
                "crime_columns": result.crime_columns,
                "pop_rows": result.pop_rows,
                "pop_columns": result.pop_columns,
                "cctv_pop_rows": result.cctv_pop_rows,
                "cctv_pop_columns": result.cctv_pop_columns,
                "cctv_preview": result.cctv_preview,
                "crime_preview": result.crime_preview,
                "pop_preview": result.pop_preview,
                "cctv_pop_preview": result.cctv_pop_preview,
                "message": result.message,
            },
            message=result.message,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
