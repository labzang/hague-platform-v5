"""호환용 re-export: `labzang.core.vectorstore` import 경로를 유지한다."""

from labzang.core.rag.vectorstore import (
    VectorStoreType,
    get_vectorstore,
    initialize_vectorstore,
)

__all__ = [
    "VectorStoreType",
    "get_vectorstore",
    "initialize_vectorstore",
]
