"""RAG chain builder."""

from __future__ import annotations

from typing import Optional

from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

from labzang.core.rag.settings import openai_api_key


def create_rag_chain(vectorstore, llm: Optional[BaseLanguageModel] = None):
    prompt = ChatPromptTemplate.from_template(
        """
다음 컨텍스트를 바탕으로 질문에 답해주세요:

컨텍스트: {context}

질문: {question}

답변:
"""
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    if llm is not None:
        return (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    if openai_api_key:
        import os

        os.environ["OPENAI_API_KEY"] = openai_api_key
        default_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        return (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | default_llm
            | StrOutputParser()
        )

    def _dummy(question: str) -> str:
        docs = retriever.invoke(question)
        context = "\n".join([f"- {doc.page_content}" for doc in docs])
        return (
            "🔍 검색된 관련 문서들:\n"
            f"{context}\n\n"
            f"💡 더미 응답: 위의 문서들이 '{question}' 질문과 관련된 내용입니다.\n"
            "실제 AI 응답을 받으려면 OpenAI API 키를 설정해주세요."
        )

    return RunnableLambda(_dummy)
