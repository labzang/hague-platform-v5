import asyncio
import traceback

from fastapi import APIRouter, Depends, HTTPException, Request

from labzang.apps.chat.adapter.inbound.api.schemas.chat_req import RAGRequest
from labzang.apps.chat.adapter.inbound.api.schemas.chat_resp import (
    DocumentResp,
    RAGResp,
)
from labzang.core.rag import (
    VectorStoreType,
    create_rag_chain,
    get_vectorstore,
)

"""
😎😎 FastAPI 기준의 API 엔드포인트 계층입니다.

chat_router.py
POST /api/chat
세션 ID, 메시지 리스트 등을 받아 대화형 응답 반환.
"""


router = APIRouter(prefix="/chat", tags=["chat"])


def get_vectorstore_dependency() -> VectorStoreType:
    """벡터스토어 의존성 주입."""
    try:
        print("🔧 벡터스토어 의존성 주입 중...")
        vectorstore = get_vectorstore()
        print("✅ 벡터스토어 의존성 주입 완료")
        return vectorstore
    except Exception as e:
        print(f"❌ 벡터스토어 의존성 주입 실패: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"벡터스토어 초기화 실패: {str(e)}")


@router.post("", response_model=RAGResp)
@router.post("/query", response_model=RAGResp)
async def rag_query(
    request: RAGRequest,
    fastapi_request: Request,
    vectorstore: VectorStoreType = Depends(get_vectorstore_dependency),
) -> RAGResp:
    """
    RAG (Retrieval-Augmented Generation) 질의를 수행합니다.

    - **question**: 질문 내용
    - **k**: 검색에 사용할 문서 개수 (1-10)
    """
    try:
        print(f"📝 RAG 질의 수신: question='{request.question}', k={request.k}")

        # Chat Service가 설정되어 있으면 사용
        chat_service = getattr(fastapi_request.app.state, "chat_service", None)
        if chat_service is not None:
            print("✅ Chat Service 사용")
        else:
            print("⚠️ Chat Service 미설정, 기존 RAG 체인 사용")

        # 검색된 문서 가져오기 (참조용)
        print("🔍 문서 검색 중...")
        print(f"🔍 Vectorstore type: {type(vectorstore)}")
        try:
            retriever = vectorstore.as_retriever(search_kwargs={"k": request.k})
            print(f"🔍 Retriever created: {type(retriever)}")
            source_docs = retriever.invoke(request.question)
            print(f"✅ {len(source_docs)}개 문서 검색 완료")
        except Exception as search_error:
            print(f"❌ 문서 검색 오류: {str(search_error)}")
            traceback.print_exc()
            raise

        if chat_service is not None:
            # Chat Service를 사용하여 대화 생성
            # 검색된 문서를 컨텍스트로 포함
            context = "\n\n".join(
                [
                    f"문서 {i + 1}:\n{doc.page_content}"
                    for i, doc in enumerate(source_docs)
                ]
            )

            # 컨텍스트를 포함한 프롬프트 생성
            prompt_with_context = f"""다음 컨텍스트를 바탕으로 질문에 답해주세요:

컨텍스트:
{context}

질문: {request.question}

답변:"""

            # Chat Service로 응답 생성 (동기 함수를 비동기로 실행)
            print("🤖 Chat Service로 응답 생성 중...")
            try:
                # Python 3.9+ 지원
                import sys

                if sys.version_info >= (3, 9):
                    answer = await asyncio.to_thread(
                        chat_service.chat,
                        prompt_with_context,
                        max_new_tokens=512,
                        temperature=0.7,
                    )
                else:
                    # Python 3.8 이하: 별도 스레드에서 실행
                    loop = asyncio.get_event_loop()
                    answer = await loop.run_in_executor(
                        None,
                        lambda: chat_service.chat(
                            prompt_with_context,
                            max_new_tokens=512,
                            temperature=0.7,
                        ),
                    )
                print("✅ Chat Service 응답 생성 완료")
            except Exception as chat_error:
                print(f"❌ Chat Service 오류: {str(chat_error)}")
                traceback.print_exc()
                # Chat Service 실패 시 fallback으로 RAG 체인 사용
                print("🔄 RAG 체인으로 fallback...")
                llm = getattr(fastapi_request.app.state, "llm", None)
                rag_chain = create_rag_chain(vectorstore, llm=llm)
                answer = rag_chain.invoke(request.question)
        else:
            # 기존 RAG 체인 사용 (fallback)
            print("🤖 RAG 체인으로 응답 생성 중...")
            llm = getattr(fastapi_request.app.state, "llm", None)
            rag_chain = create_rag_chain(vectorstore, llm=llm)
            answer = rag_chain.invoke(request.question)
            print("✅ RAG 체인 응답 생성 완료")

        # 응답 모델 생성
        sources = [
            DocumentResp(
                content=doc.page_content,
                metadata=dict(doc.metadata),
            )
            for doc in source_docs
        ]

        return RAGResp(
            question=request.question,
            answer=answer,
            sources=sources,
            retrieved_documents=sources,
            retrieved_count=len(sources) if sources else 0,
        )
    except HTTPException:
        # HTTPException은 그대로 전달
        raise
    except Exception as e:
        # 상세한 에러 정보 로깅
        error_msg = str(e)
        print(f"❌ RAG 질의 중 오류 발생: {error_msg}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"RAG 질의 중 오류 발생: {error_msg}"
        )


@router.get("/health")
async def rag_health() -> dict:
    """RAG 서비스 헬스체크."""
    return {"status": "healthy", "service": "rag"}
