"""
RAG 오케스트레이터 — 검색 스포크 + 답변 생성 스포크를 조합해 RAGQueryInputPort 구현.
"""
from labzang.apps.chat.application.dtos import (
    ChatRequestDto,
    RAGQueryDto,
    RAGResultDto,
    SearchQueryDto,
)
from labzang.apps.chat.application.ports.input import RAGQueryInputPort
from labzang.apps.chat.application.use_cases.spokes import GenerateAnswerSpoke, SearchSpoke


class RAGOrchestrator(RAGQueryInputPort):
    """RAG 플로우: 검색 → 컨텍스트 결합 → LLM 답변 생성."""

    def __init__(
        self,
        search_spoke: SearchSpoke,
        generate_answer_spoke: GenerateAnswerSpoke,
    ):
        self._search = search_spoke
        self._generate = generate_answer_spoke

    def execute(self, query: RAGQueryDto) -> RAGResultDto:
        """질문으로 검색 후, 컨텍스트를 붙여 답변 생성."""
        # 1) 검색
        search_query = SearchQueryDto(query=query.question, k=query.k)
        search_result = self._search.run(search_query)

        # 2) 컨텍스트 문자열 조립
        context_parts = [
            f"문서 {i + 1}:\n{doc.content}"
            for i, doc in enumerate(search_result.documents)
        ]
        context = "\n\n".join(context_parts) if context_parts else "(검색된 문서 없음)"

        prompt_with_context = f"""다음 컨텍스트를 바탕으로 질문에 답해주세요.

컨텍스트:
{context}

질문: {query.question}

답변:"""

        # 3) 답변 생성
        chat_request = ChatRequestDto(
            message=prompt_with_context,
            max_new_tokens=query.max_new_tokens,
            temperature=query.temperature,
            conversation_history=None,
        )
        chat_response = self._generate.run(chat_request)

        return RAGResultDto(
            question=query.question,
            answer=chat_response.answer,
            sources=search_result.documents,
            retrieved_count=search_result.count,
        )
