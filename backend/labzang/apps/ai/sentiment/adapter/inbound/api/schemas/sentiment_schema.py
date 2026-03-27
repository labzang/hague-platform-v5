from typing import Any, Dict, List

from pydantic import BaseModel, Field


class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class BatchSentimentRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, max_length=50)


class IngestRawRequest(BaseModel):
    rows: List[Dict[str, Any]]


class TrainingClickEventRequest(BaseModel):
    source: str = Field(default="vercel")
    actor: str = Field(default="ui")
    reason: str = Field(default="manual-click")
    dry_run: bool = Field(default=False)
