"""Repository adapter: persist sentiment resource rows to DB."""

from __future__ import annotations

from typing import Dict, List

from sqlalchemy import select

from labzang.apps.ai.sentiment.adapter.outbound.orm import SentimentReviewORM
from labzang.apps.ai.sentiment.application.ports.output import SentimentRepository
from labzang.apps.ai.sentiment.domain.entities import SentimentReview
from labzang.core.database import SessionLocal


class SentimentRepositoryImpl(SentimentRepository):
    async def upsert_batch(self, reviews: List[SentimentReview]) -> Dict[str, int]:
        inserted = 0
        updated = 0
        errors = 0

        with SessionLocal() as session:
            for review in reviews:
                try:
                    res = session.execute(
                        select(SentimentReviewORM).where(
                            SentimentReviewORM.review_id == review.review_id
                        )
                    )
                    row = res.scalar_one_or_none()
                    if row is None:
                        row = SentimentReviewORM(review_id=review.review_id)
                        session.add(row)
                        inserted += 1
                    else:
                        updated += 1

                    row.movie_id = review.movie_id
                    row.author = review.author
                    row.review = review.review
                    row.rating = review.rating
                    row.sentiment_label = review.sentiment_label
                    row.reviewed_at = review.reviewed_at
                except Exception:
                    errors += 1
                    session.rollback()

            try:
                session.commit()
            except Exception:
                session.rollback()
                errors += len(reviews)
                inserted = 0
                updated = 0

        return {
            "inserted_count": inserted,
            "updated_count": updated,
            "error_count": errors,
        }
