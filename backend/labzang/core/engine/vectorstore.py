"""벡터스토어 설정 및 관리 (Neon Postgres + pgvector).

로컬 Docker 컨테이너의 Postgres/pgvector 대신,
외부에서 제공되는 Postgres (예: Neon) 인스턴스를 사용합니다.

연결 정보는 `app.config.Settings.database_url` 을 통해 주입되며,
이는 `.env` 의 `DATABASE_URL` 값(없으면 기존 POSTGRES_* 조합)을 사용합니다.
"""

from typing import List

from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import PGVector



class SimpleEmbeddings(Embeddings):
    """간단한 더미 임베딩 클래스 (OpenAI API 키가 없을 때 사용)."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """문서들을 임베딩으로 변환."""
        return [[0.1, 0.2, 0.3, 0.4, 0.5] for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        """쿼리를 임베딩으로 변환."""
        return [0.1, 0.2, 0.3, 0.4, 0.5]




# 라우터에서 사용할 타입 별칭
VectorStoreType = PGVector
