# JSON Request/Response 규격 (Pydantic)
from labzang.apps.com.chat.adapter.inbound.api.schemas.chat_req import SearchRequest
from labzang.apps.com.chat.adapter.inbound.api.schemas.chat_resp import (
    DocumentResp,
    SearchResp,
)

__all__ = ["DocumentResp", "SearchRequest", "SearchResp"]
