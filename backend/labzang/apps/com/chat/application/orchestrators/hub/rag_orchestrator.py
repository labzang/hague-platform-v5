"""
RAG orchestrator.
Composes search and answer-generation spokes to implement RAGQueryInputPort.
"""
from labzang.apps.com.chat.application.dtos import (
    ChatRequestDto,
    RAGQueryDto,
    RAGResultDto,
    SearchQueryDto,
)
from labzang.apps.com.chat.application.orchestrators.spokes import (
    GenerateAnswerSpoke,
    SearchSpoke,
)
from labzang.apps.com.chat.application.ports.input import RAGQueryInputPort


class RAGOrchestrator(RAGQueryInputPort):
    """RAG flow: retrieve -> build context -> generate answer."""

    def __init__(
        self,
        search_spoke: SearchSpoke,
        generate_answer_spoke: GenerateAnswerSpoke,
    ):
        self._search = search_spoke
        self._generate = generate_answer_spoke

    def execute(self, query: RAGQueryDto) -> RAGResultDto:
        """Search first, then generate answer with retrieved context."""
        search_query = SearchQueryDto(query=query.question, k=query.k)
        search_result = self._search.run(search_query)

        context_parts = [
            f"Document {i + 1}:\n{doc.content}"
            for i, doc in enumerate(search_result.documents)
        ]
        context = "\n\n".join(context_parts) if context_parts else "(No retrieved documents)"

        prompt_with_context = f"""Answer the question using the context below.

Context:
{context}

Question: {query.question}

Answer:"""

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