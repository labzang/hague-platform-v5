"""DB upsert 결과 스키마."""
from typing import TypedDict, List, Dict, Any


class DatabaseResult(TypedDict, total=False):
    inserted_count: int
    updated_count: int
    error_count: int
    errors: List[Dict[str, Any]]
