"""
서울 범죄 헥사고날 API (인바운드 어댑터)
- 유스케이스는 조립 루트(dependencies)에서 주입받음. 출력 어댑터 직접 참조 없음.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from labzang.apps.data.geospatial.adapter.inbound.dependencies import (
    get_preprocess_seoul_use_case,
)
from labzang.apps.data.geospatial.application.use_cases.seoul_crime_uc import (
    PreprocessSeoulCrimeUC,
)
from labzang.shared import create_response

from labzang.apps.data.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_cctv_router import (
    router as seoul_cctv_router,
)
from labzang.apps.data.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_map_router import (
    router as seoul_map_router,
)
from labzang.apps.data.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_population_router import (
    router as seoul_population_router,
)

router = APIRouter(tags=["seoul-hex"])  # prefix는 main에서 /seoul 로 등록
router.include_router(seoul_cctv_router, prefix="/cctv")
router.include_router(seoul_population_router, prefix="/population")
router.include_router(seoul_map_router, prefix="/map")


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
async def preprocess(
    use_case: PreprocessSeoulCrimeUC = Depends(get_preprocess_seoul_use_case),
):
    """서울 범죄 전처리 실행 (데이터 로드, cctv-pop 머지, 지오코딩, 저장)."""
    try:
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
