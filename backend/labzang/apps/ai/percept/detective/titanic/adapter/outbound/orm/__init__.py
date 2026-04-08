"""Titanic ORM 모델 (Alembic env에서 metadata 로딩용)."""

from labzang.apps.ai.percept.detective.titanic.adapter.outbound.orm.titanic_feature_orm import (
    TitanicFeatureORM,
)
from labzang.apps.ai.percept.detective.titanic.adapter.outbound.orm.titanic_orm import TitanicORM

__all__ = ("TitanicORM", "TitanicFeatureORM")

