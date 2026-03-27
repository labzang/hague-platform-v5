"""Sentiment review aggregate for persistence and inference."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


def _parse_date(raw: str | None) -> datetime | None:
    if not raw:
        return None
    for fmt in ("%y.%m.%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


@dataclass(frozen=True)
class SentimentReview:
    review_id: str
    movie_id: str
    author: str
    review: str
    rating: int | None
    reviewed_at: datetime | None

    @property
    def sentiment_label(self) -> str | None:
        if self.rating is None:
            return None
        return "positive" if self.rating >= 6 else "negative"

    @classmethod
    def from_json_dict(cls, raw: dict) -> "SentimentReview":
        review_id = str(raw.get("review_id", "")).strip()
        movie_id = str(raw.get("movie_id", "")).strip()
        author = str(raw.get("author", "")).strip()
        review = str(raw.get("review", "")).strip()
        rating_raw = str(raw.get("rating", "")).strip()

        if not review_id or not movie_id or not review:
            raise ValueError("review_id, movie_id, review are required")

        rating = int(rating_raw) if rating_raw.isdigit() else None
        reviewed_at = _parse_date(str(raw.get("date", "")).strip())
        return cls(
            review_id=review_id,
            movie_id=movie_id,
            author=author,
            review=review,
            rating=rating,
            reviewed_at=reviewed_at,
        )
