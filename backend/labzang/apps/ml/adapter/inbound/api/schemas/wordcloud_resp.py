"""
워드클라우드 API 응답 빌더 (create_response 래핑).
- 라우터는 get_wordcloud_resp를 주입받아 사용.
"""

from typing import Any, Dict

from labzang.shared import create_response


def get_wordcloud_resp(
    data: Any,
    message: str = "Success",
    status: str = "success",
) -> Dict[str, Any]:
    """워드클라우드용 표준 응답 생성 (create_response 사용)."""
    return create_response(data=data, message=message, status=status)
