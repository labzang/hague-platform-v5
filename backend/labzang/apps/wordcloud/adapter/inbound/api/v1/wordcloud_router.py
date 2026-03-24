"""
워드클라우드·NLP 관련 라우터 (삼성/Emma 워드클라우드, 말뭉치, 텍스트 분석 등)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, Optional
import logging

from labzang.apps.kaggle.adapter.inbound.dependencies import (
    get_emma_wordcloud_use_case,
    get_samsung_wordcloud_use_case,
    get_wordcloud_resp_dep,
)
from labzang.apps.wordcloud.application.use_cases.emma_wordcloud import NLTKService
from labzang.apps.wordcloud.application.use_cases.emma_wordcloud_uc import (
    GenerateEmmaWordcloudUC,
)
from labzang.apps.wordcloud.application.use_cases.samsung_wordcloud_uc import (
    GenerateSamsungWordcloudUC,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["wordcloud"])

# 서비스 인스턴스 생성 (싱글톤 패턴)
_service_instance: Optional[NLTKService] = None


def get_service() -> NLTKService:
    """NLTKService 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = NLTKService()
    return _service_instance


@router.get("/")
async def wordcloud_root(
    get_wordcloud_resp=Depends(get_wordcloud_resp_dep),
):
    """워드클라우드 서비스 루트"""
    return get_wordcloud_resp(
        data={"service": "mlservice", "module": "wordcloud", "status": "running"},
        message="Wordcloud Service is running",
    )


@router.get("/samsung")
async def generate_samsung_wordcloud(
    use_case: GenerateSamsungWordcloudUC = Depends(get_samsung_wordcloud_use_case),
    get_wordcloud_resp=Depends(get_wordcloud_resp_dep),
):
    """삼성전자 지속가능경영보고서 2018 워드클라우드 생성 (헥사고날 유스케이스)."""
    try:
        result = use_case.execute()
        freq_txt = result.get("freq_txt") or {}
        freq_data = dict(list(freq_txt.items())[:30])

        return get_wordcloud_resp(
            data={
                "processing_status": result.get("전처리 결과", "완료"),
                "top_keywords": [
                    {"word": word, "frequency": int(freq)}
                    for word, freq in freq_data.items()
                ],
                "keyword_count": len(freq_data),
                "saved_file": result.get("saved_file", {}),
                "report_info": {
                    "title": "삼성전자 지속가능경영보고서 2018",
                    "source": "kr-Report_2018.txt",
                },
            },
            message="삼성전자 워드클라우드 분석이 완료되었습니다",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"삼성 워드클라우드 분석 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"삼성 워드클라우드 분석 실패: {str(e)}"
        )


@router.get("/emma")
async def generate_emma_wordcloud(
    use_case: GenerateEmmaWordcloudUC = Depends(get_emma_wordcloud_use_case),
    get_wordcloud_resp=Depends(get_wordcloud_resp_dep),
    width: int = Query(1000, description="워드클라우드 이미지 너비"),
    height: int = Query(600, description="워드클라우드 이미지 높이"),
    background_color: str = Query(
        "white", description="배경색 (white, black, blue 등)"
    ),
    max_words: int = Query(100, description="최대 단어 수"),
):
    """
    Emma 소설 워드클라우드 생성 (헥사고날 유스케이스).
    - Jane Austen의 Emma 소설에서 등장인물 이름을 추출하여 워드클라우드 생성
    - 고유명사(NNP) 태그를 가진 단어들을 우선적으로 사용
    - 결과는 base64 인코딩된 이미지로 반환
    """
    try:
        logger.info("Emma 워드클라우드 생성 중...")
        result = use_case.execute(
            width=width,
            height=height,
            background_color=background_color,
            max_words=max_words,
            max_chars=50000,
        )
        if result.get("status") != "success":
            raise HTTPException(
                status_code=500,
                detail="Emma 워드클라우드 생성 실패",
            )
        logger.info("Emma 워드클라우드 생성 완료")
        return get_wordcloud_resp(
            data={
                "wordcloud": result,
                "text_info": result.get("text_info", {}),
            },
            message="Emma 워드클라우드가 성공적으로 생성되었습니다",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Emma 워드클라우드 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"워드클라우드 생성 중 오류가 발생했습니다: {str(e)}",
        )


@router.get("/corpus")
async def get_corpus_info(
    get_wordcloud_resp=Depends(get_wordcloud_resp_dep),
):
    """
    NLTK 말뭉치 정보 조회
    - Gutenberg 말뭉치의 파일 목록과 정보 반환
    """
    try:
        service = get_service()
        corpus_info = service.get_corpus_info()

        if "error" in corpus_info:
            raise HTTPException(
                status_code=500, detail=f"말뭉치 정보 조회 실패: {corpus_info['error']}"
            )

        return get_wordcloud_resp(
            data=corpus_info, message="말뭉치 정보 조회가 완료되었습니다"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"말뭉치 정보 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"말뭉치 정보 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/analyze")
async def analyze_text_endpoint(
    request: Dict[str, Any],
    get_wordcloud_resp=Depends(get_wordcloud_resp_dep),
):
    """
    텍스트 종합 분석
    - 요청 본문: {"text": "분석할 텍스트", "name": "문서명(선택사항)"}
    - 토큰화, 품사 태깅, 빈도 분석 등 종합적인 텍스트 분석 수행
    """
    try:
        text = request.get("text")
        name = request.get("name", "Document")

        if not text:
            raise HTTPException(
                status_code=400, detail="분석할 텍스트가 제공되지 않았습니다"
            )

        service = get_service()
        analysis_result = service.analyze_text(text, name)

        if "error" in analysis_result:
            raise HTTPException(
                status_code=500, detail=f"텍스트 분석 실패: {analysis_result['error']}"
            )

        return get_wordcloud_resp(
            data=analysis_result, message="텍스트 분석이 완료되었습니다"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"텍스트 분석 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"텍스트 분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/wordcloud")
async def generate_custom_wordcloud(
    request: Dict[str, Any],
    get_wordcloud_resp=Depends(get_wordcloud_resp_dep),
):
    """
    커스텀 워드클라우드 생성
    - 요청 본문: {"text": "텍스트", "width": 1000, "height": 600, "background_color": "white", "max_words": 100}
    - 사용자가 제공한 텍스트로 워드클라우드 생성
    """
    try:
        text = request.get("text")
        width = request.get("width", 1000)
        height = request.get("height", 600)
        background_color = request.get("background_color", "white")
        max_words = request.get("max_words", 100)

        if not text:
            raise HTTPException(
                status_code=400,
                detail="워드클라우드 생성을 위한 텍스트가 제공되지 않았습니다",
            )

        service = get_service()
        wordcloud_result = service.generate_wordcloud(
            text=text,
            width=width,
            height=height,
            background_color=background_color,
            max_words=max_words,
        )

        if "error" in wordcloud_result:
            raise HTTPException(
                status_code=500,
                detail=f"워드클라우드 생성 실패: {wordcloud_result['error']}",
            )

        return get_wordcloud_resp(
            data=wordcloud_result,
            message="커스텀 워드클라우드가 성공적으로 생성되었습니다",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"커스텀 워드클라우드 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"워드클라우드 생성 중 오류가 발생했습니다: {str(e)}",
        )


@router.post("/pos-tagging")
async def pos_tagging_endpoint(
    request: Dict[str, Any],
    get_wordcloud_resp=Depends(get_wordcloud_resp_dep),
):
    """
    품사 태깅 분석
    - 요청 본문: {"text": "분석할 텍스트"}
    - 텍스트의 각 단어에 품사 태그를 부착하여 반환
    """
    try:
        text = request.get("text")

        if not text:
            raise HTTPException(
                status_code=400, detail="품사 태깅을 위한 텍스트가 제공되지 않았습니다"
            )

        service = get_service()
        pos_result = service.pos_tagging(text)

        if "error" in pos_result:
            raise HTTPException(
                status_code=500, detail=f"품사 태깅 실패: {pos_result['error']}"
            )

        return get_wordcloud_resp(data=pos_result, message="품사 태깅이 완료되었습니다")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"품사 태깅 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"품사 태깅 중 오류가 발생했습니다: {str(e)}"
        )
