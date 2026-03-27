"""SQLAlchemy mapping for sentiment reviews."""

from sqlalchemy import Column, DateTime, Integer, String, Text

from labzang.core.database import Base


class SentimentReviewORM(Base):
    __tablename__ = "sentiment_reviews"

    review_id = Column(String(30), primary_key=True, comment="원본 리뷰 ID")
    movie_id = Column(String(20), nullable=False, index=True, comment="영화 ID")
    author = Column(String(50), nullable=True, comment="작성자")
    review = Column(Text, nullable=False, comment="리뷰 본문")
    rating = Column(Integer, nullable=True, comment="원본 평점")
    sentiment_label = Column(String(20), nullable=True, comment="평점기반 라벨")
    reviewed_at = Column(DateTime, nullable=True, comment="리뷰 작성 일자")
