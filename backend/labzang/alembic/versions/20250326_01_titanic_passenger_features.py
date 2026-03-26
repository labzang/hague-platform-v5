"""titanic_passenger_features 테이블 생성

Revision ID: 20250326_01
Revises:
Create Date: 2025-03-26

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20250326_01"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "titanic_passenger_features",
        sa.Column("passenger_id", sa.BigInteger(), nullable=False),
        sa.Column("dataset_split", sa.String(length=10), nullable=False),
        sa.Column("pclass", sa.Integer(), nullable=False),
        sa.Column("embarked", sa.Integer(), nullable=False),
        sa.Column("title", sa.Integer(), nullable=False),
        sa.Column("gender", sa.Integer(), nullable=False),
        sa.Column("age_group", sa.Integer(), nullable=False),
        sa.Column("fare_band", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("passenger_id"),
    )


def downgrade() -> None:
    op.drop_table("titanic_passenger_features")
