"""RAG/벡터스토어용 설정 (환경 변수). app.config 의존 제거."""
import os


def _get_openai_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "").strip()


def _get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if url:
        return url
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "railway")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


openai_api_key = _get_openai_api_key()
database_url = _get_database_url()
