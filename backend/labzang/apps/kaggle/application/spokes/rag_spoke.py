"""
RAG Spoke: RAG 기반 지식 반환 로직
- Vector DB + LLM Port 사용 (adapter가 구현 주입)
"""
from typing import Any, List, Optional

# Port는 application.ports에서 주입받음 (adapter가 구현체 제공)


def run_rag(
    query: str,
    vector_db: Any,  # IVectorDbPort 구현체
    llm: Any,        # ILlmPort 구현체
    top_k: int = 5,
) -> str:
    """RAG 파이프라인: 검색 → 컨텍스트 결합 → LLM 응답."""
    docs = vector_db.search(query, top_k=top_k)
    context = "\n\n".join(getattr(d, "page_content", str(d)) for d in docs)
    prompt = f"""다음 참고 자료를 바탕으로 질문에 답하세요.

참고 자료:
{context}

질문: {query}

답변:"""
    return llm.invoke(prompt)
