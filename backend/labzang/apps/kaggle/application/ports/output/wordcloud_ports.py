"""
아웃바운드 포트: 워드클라우드용 텍스트 소스·이미지 저장.
- 구현: adapter/outbound (파일 시스템 등)
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class TextSourcePort(ABC):
    """텍스트 리소스 조회 포트 (보고서, 스톱워드, 폰트 경로 등)."""

    @abstractmethod
    def get_text(self, key: str) -> str:
        """key에 해당하는 텍스트 또는 경로 문자열 반환."""
        ...


class ImageStoragePort(ABC):
    """이미지 바이트를 저장하는 포트."""

    @abstractmethod
    def save(
        self,
        subdir: str,
        filename: str,
        image_bytes: bytes,
    ) -> Dict[str, Any]:
        """이미지 저장 후 파일 정보 반환 (filename, path, size_bytes, exists 등)."""
        ...
