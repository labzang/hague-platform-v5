"""RAG 체인 설정 및 관리 (LLM 외부 주입 지원)."""

from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai import ChatOpenAI

from labzang.core.rag.settings import openai_api_key


def create_rag_chain(
    vectorstore,
    llm: Optional[BaseLanguageModel] = None,
):
    """RAG (Retrieval-Augmented Generation) 체인 생성.

    Args:
        vectorstore: 검색에 사용할 PGVector 인스턴스.
        llm: 선택적 LLM 인스턴스. 주입하지 않으면 기존 설정을 사용합니다.

    Returns:
        LangChain Runnable 객체 (invoke(question: str) 지원).
    """
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
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return rag_chain

    if openai_api_key:
        import os
        os.environ["OPENAI_API_KEY"] = openai_api_key
        default_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | default_llm
            | StrOutputParser()
        )
        return rag_chain

    def dummy_rag_function(question: str) -> str:
        docs = retriever.invoke(question)
        context = "\n".join([f"- {doc.page_content}" for doc in docs])
        return f"""🔍 검색된 관련 문서들:
{context}

💡 더미 응답: 위의 문서들이 '{question}' 질문과 관련된 내용입니다.
실제 AI 응답을 받으려면 OpenAI API 키를 설정해주세요.
하지만 벡터 검색 기능은 정상적으로 작동하고 있습니다!"""

    return RunnableLambda(dummy_rag_function)
