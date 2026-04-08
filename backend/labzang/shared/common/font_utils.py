"""한글 폰트 유틸 — core 대시 이사 경로 re-export."""

from labzang.core.dash.council.illustrator.cloud.korean_fonts import (
    get_available_korean_fonts,
    setup_korean_font,
    test_korean_font,
)

__all__ = [
    "get_available_korean_fonts",
    "setup_korean_font",
    "test_korean_font",
]
