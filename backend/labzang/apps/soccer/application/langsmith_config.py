"""LangSmith 연동 설정 (선택). 환경 변수가 없으면 None."""
import os
from typing import Any, Dict, List, Optional


def get_langsmith_config() -> Optional[Dict[str, Any]]:
    """LangGraph 등에 넘길 LangSmith config 딕셔너리. 미설정 시 None."""
    key = os.getenv("LANGCHAIN_API_KEY") or os.getenv("LANGSMITH_API_KEY")
    if not key:
        return None
    tags: List[str] = []
    metadata: Dict[str, Any] = {"source": "labzang.soccer"}
    return {
        "tags": tags,
        "metadata": metadata,
        "configurable": {"langchain_api_key": key},
    }
