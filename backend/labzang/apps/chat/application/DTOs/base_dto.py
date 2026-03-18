"""Application 계층 DTO 공통 베이스 (검증·직렬화용)."""
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class BaseDto(BaseModel):
    """Application DTO 공통 베이스. 도메인/어댑터 의존 없음."""

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 직렬화 (어댑터/API 전달용)."""
        return self.model_dump()
