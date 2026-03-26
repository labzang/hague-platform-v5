"""PGVector-backed vector store helpers."""

from __future__ import annotations

from typing import List

from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from labzang.core.rag.settings import database_url, openai_api_key


class SimpleEmbeddings(Embeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [[0.1, 0.2, 0.3, 0.4, 0.5] for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        return [0.1, 0.2, 0.3, 0.4, 0.5]


def get_embeddings() -> Embeddings:
    if openai_api_key:
        import os

        os.environ["OPENAI_API_KEY"] = openai_api_key
        return OpenAIEmbeddings()
    return SimpleEmbeddings()


def get_connection_string() -> str:
    return database_url


def get_vectorstore() -> PGVector:
    return PGVector(
        connection_string=get_connection_string(),
        embedding_function=get_embeddings(),
        collection_name="langchain_collection",
    )


def add_sample_documents(vectorstore: PGVector) -> None:
    sample_docs = [
        Document(page_content="LangChain은 LLM 앱 프레임워크입니다."),
        Document(page_content="pgvector는 PostgreSQL 벡터 검색 확장입니다."),
        Document(page_content="FastAPI는 타입 기반 웹 프레임워크입니다."),
    ]
    vectorstore.add_documents(sample_docs)


def initialize_vectorstore() -> PGVector:
    vectorstore = get_vectorstore()
    try:
        existing_docs = vectorstore.similarity_search("test", k=1)
        if not existing_docs:
            add_sample_documents(vectorstore)
    except Exception:
        add_sample_documents(vectorstore)
    return vectorstore


VectorStoreType = PGVector
