"""DTOs for sentiment application layer."""

from pydantic import BaseModel


class SentimentAnalyzeResultDTO(BaseModel):
    text: str
    sentiment: str
    confidence: float
    probabilities: dict[str, float]
    model_info: dict


class SentimentIngestResultDTO(BaseModel):
    parsed_count: int
    inserted_count: int
    updated_count: int
    error_count: int
