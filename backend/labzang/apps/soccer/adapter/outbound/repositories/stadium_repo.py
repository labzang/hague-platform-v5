"""경기장 데이터 Repo."""

import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from labzang.apps.soccer.adapter.outbound.models.stadium_model import StadiumModel

logger = logging.getLogger(__name__)


class StadiumRepo:
    """경기장 데이터 Repo.

    Neon `stadiums` 테이블 CRUD.
    """

    def __init__(self, session: AsyncSession):
        """StadiumRepo 초기화.

        Args:
            session: 데이터베이스 세션
        """
        self.session = session
        logger.debug("[Repo] StadiumRepo 초기화")

    async def find_by_id(self, stadium_id: int) -> Optional[StadiumModel]:
        """ID로 경기장을 조회합니다."""
        result = await self.session.execute(
            select(StadiumModel).where(StadiumModel.id == stadium_id)
        )
        return result.scalar_one_or_none()

    async def create(self, stadium_data: Dict[str, Any]) -> StadiumModel:
        """새 경기장을 생성합니다."""
        new_stadium = StadiumModel(**stadium_data)
        self.session.add(new_stadium)
        logger.debug(f"[Repo] 경기장 생성: ID {stadium_data.get('id')}")
        return new_stadium

    async def update(
        self, stadium: StadiumModel, stadium_data: Dict[str, Any]
    ) -> StadiumModel:
        """기존 경기장을 업데이트합니다."""
        for key, value in stadium_data.items():
            if key != "id":
                setattr(stadium, key, value)
        logger.debug(f"[Repo] 경기장 업데이트: ID {stadium.id}")
        return stadium

    async def upsert_batch(
        self, stadiums_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """여러 경기장을 일괄 upsert (insert or update) 합니다."""
        inserted_count = 0
        updated_count = 0
        error_count = 0
        errors: List[Dict[str, Any]] = []

        for stadium_data in stadiums_data:
            try:
                stadium_id = stadium_data.get("id")
                if not stadium_id:
                    error_msg = "ID가 없습니다"
                    logger.warning(f"[Repo] {error_msg}: {stadium_data}")
                    error_count += 1
                    errors.append({"item": stadium_data, "error": error_msg})
                    continue

                existing_stadium = await self.find_by_id(stadium_id)

                if existing_stadium:
                    await self.update(existing_stadium, stadium_data)
                    updated_count += 1
                    logger.debug(f"[Repo] 경기장 업데이트: ID {stadium_id}")
                else:
                    await self.create(stadium_data)
                    inserted_count += 1
                    logger.debug(f"[Repo] 경기장 삽입: ID {stadium_id}")

            except IntegrityError as e:
                error_count += 1
                error_msg = f"무결성 제약 조건 위반: {str(e)}"
                logger.error(
                    f"[Repo] {error_msg}: ID {stadium_data.get('id')}",
                    exc_info=True,
                )
                errors.append({"item": stadium_data, "error": error_msg})
            except Exception as e:
                error_count += 1
                error_msg = f"처리 중 오류: {str(e)}"
                logger.error(
                    f"[Repo] {error_msg}: ID {stadium_data.get('id')}",
                    exc_info=True,
                )
                errors.append({"item": stadium_data, "error": error_msg})

        return {
            "inserted_count": inserted_count,
            "updated_count": updated_count,
            "error_count": error_count,
            "errors": errors,
        }

    async def commit(self) -> None:
        """변경사항을 커밋합니다."""
        try:
            await self.session.commit()
            logger.debug("[Repo] 커밋 완료")
        except Exception as e:
            await self.session.rollback()
            logger.error(f"[Repo] 커밋 실패, 롤백: {e}", exc_info=True)
            raise
