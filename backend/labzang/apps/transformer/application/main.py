"""
TransformerService - KoELECTRA 감성분석 서비스
FastAPI 기반 한국어 감성분석 마이크로서비스
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from pathlib import Path

# 절대경로: labzang 루트 및 transformer 앱 루트
_labzang_root = Path(__file__).resolve().parent.parent.parent.parent
_transformer_root = _labzang_root / "apps" / "transformer"
for _p in (_labzang_root, _transformer_root):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

try:
    from labzang.shared import setup_logging
    logger = setup_logging("transformerservice")
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("transformerservice")

from labzang.apps.transformer.application.koelectra.koelectra_router import router as koelectra_router

# ============================================================================
# FastAPI 애플리케이션 설정
# ============================================================================

app = FastAPI(
    title="TransformerService - KoELECTRA 감성분석",
    description="""
    🤖 **KoELECTRA 기반 한국어 감성분석 서비스**
    
    ## 주요 기능
    - 🎭 **영화 리뷰 감성분석**: 긍정/부정 감성 분류
    - 🚀 **실시간 분석**: 빠른 응답 속도
    - 📊 **배치 처리**: 여러 텍스트 동시 분석
    - 🎯 **높은 정확도**: KoELECTRA 모델 기반
    
    ## API 엔드포인트
    - `POST /api/transformer/koelectra/analyze` - 단일 텍스트 감성분석
    - `POST /api/transformer/koelectra/batch` - 배치 텍스트 감성분석
    - `GET /api/transformer/koelectra/quick` - 빠른 감성분석 (GET)
    - `GET /api/transformer/koelectra/health` - 서비스 상태 확인
    
    ## 사용 예시
    ```json
    {
        "text": "이 영화는 정말 재미있고 감동적이었어요!"
    }
    ```
    
    **응답:**
    ```json
    {
        "sentiment": "긍정",
        "confidence": 0.9234,
        "probabilities": {
            "긍정": 0.9234,
            "부정": 0.0766
        }
    }
    ```
    """,
    version="1.0.0",
    contact={
        "name": "Labzang AI Team",
        "url": "https://labzang.com",
    },
    license_info={
        "name": "MIT License",
    },
)

# ============================================================================
# 미들웨어 설정
# ============================================================================

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# 라우터 등록
# ============================================================================

# KoELECTRA 감성분석 라우터
app.include_router(
    koelectra_router,
    prefix="/api/transformer/koelectra",
    tags=["KoELECTRA 감성분석"]
)

# ============================================================================
# 기본 엔드포인트
# ============================================================================

@app.get("/")
async def root():
    """서비스 루트 엔드포인트"""
    return {
        "service": "TransformerService",
        "description": "KoELECTRA 기반 한국어 감성분석 서비스",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "koelectra_sentiment": "/api/transformer/koelectra",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """전체 서비스 상태 확인"""
    try:
        # KoELECTRA 서비스 상태 확인
        from labzang.apps.transformer.application.koelectra.koelectra_service import get_sentiment_service
        
        sentiment_service = get_sentiment_service()
        koelectra_health = sentiment_service.health_check()
        
        overall_status = "healthy" if koelectra_health["status"] == "healthy" else "degraded"
        
        return JSONResponse(
            status_code=200 if overall_status == "healthy" else 503,
            content={
                "service": "TransformerService",
                "status": overall_status,
                "timestamp": "2024-12-12T12:00:00Z",
                "components": {
                    "koelectra_sentiment": koelectra_health
                },
                "message": f"서비스 상태: {overall_status}"
            }
        )
        
    except Exception as e:
        logger.error(f"헬스체크 오류: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "service": "TransformerService",
                "status": "error",
                "error": str(e),
                "message": "서비스 상태 확인 중 오류가 발생했습니다"
            }
        )

@app.get("/api/transformer")
async def transformer_root():
    """Transformer API 루트"""
    return {
        "service": "TransformerService",
        "module": "transformer",
        "available_models": [
            {
                "name": "KoELECTRA",
                "description": "한국어 감성분석",
                "endpoint": "/api/transformer/koelectra",
                "tasks": ["sentiment_analysis"]
            }
        ],
        "status": "running"
    }

# ============================================================================
# 예외 처리
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP 예외 처리"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            },
            "timestamp": "2024-12-12T12:00:00Z"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """일반 예외 처리"""
    logger.error(f"예상치 못한 오류: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "내부 서버 오류가 발생했습니다"
            },
            "timestamp": "2024-12-12T12:00:00Z"
        }
    )

# ============================================================================
# 애플리케이션 시작/종료 이벤트
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    logger.info("🚀 TransformerService 시작 중...")
    logger.info("📊 KoELECTRA 감성분석 서비스 초기화...")
    
    try:
        # 서비스 사전 로딩 (선택사항)
        from labzang.apps.transformer.application.koelectra.koelectra_service import get_sentiment_service
        service = get_sentiment_service()
        logger.info("✅ KoELECTRA 서비스 준비 완료")
        
    except Exception as e:
        logger.warning(f"⚠️ 서비스 사전 로딩 실패 (지연 로딩으로 진행): {str(e)}")
    
    logger.info("🎉 TransformerService 시작 완료!")

@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info("🛑 TransformerService 종료 중...")
    logger.info("👋 TransformerService 종료 완료!")

# ============================================================================
# 개발 서버 실행 (선택사항)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🔧 개발 모드로 서버 시작...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9020,
        reload=True,
        log_level="info"
    )
