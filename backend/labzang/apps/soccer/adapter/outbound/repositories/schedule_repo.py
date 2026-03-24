"""경기 일정 데이터 Repo."""

import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from labzang.apps.soccer.adapter.outbound.models.schedule_model import ScheduleModel

logger = logging.getLogger(__name__)


class ScheduleRepo:
    """경기 일정 데이터 Repo.

    Neon `schedules` 테이블 CRUD.
    """

    def __init__(self, session: AsyncSession):
        """ScheduleRepo 초기화.

        Args:
            session: 데이터베이스 세션
        """
        self.session = session
        logger.debug("[Repo] ScheduleRepo 초기화")

    async def find_by_id(self, schedule_id: int) -> Optional[ScheduleModel]:
        """ID로 경기 일정을 조회합니다."""
        result = await self.session.execute(
            select(ScheduleModel).where(ScheduleModel.id == schedule_id)
        )
        return result.scalar_one_or_none()

    async def create(self, schedule_data: Dict[str, Any]) -> ScheduleModel:
        """새 경기 일정을 생성합니다."""
        new_schedule = ScheduleModel(**schedule_data)
        self.session.add(new_schedule)
        logger.debug(f"[Repo] 경기 일정 생성: ID {schedule_data.get('id')}")
        return new_schedule

    async def update(
        self, schedule: ScheduleModel, schedule_data: Dict[str, Any]
    ) -> ScheduleModel:
        """기존 경기 일정을 업데이트합니다."""
        for key, value in schedule_data.items():
            if key != "id":
                setattr(schedule, key, value)
        logger.debug(f"[Repo] 경기 일정 업데이트: ID {schedule.id}")
        return schedule

    async def upsert_batch(
        self, schedules_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """여러 경기 일정을 일괄 upsert (insert or update) 합니다."""
        inserted_count = 0
        updated_count = 0
        error_count = 0
        errors: List[Dict[str, Any]] = []

        for schedule_data in schedules_data:
            try:
                schedule_id = schedule_data.get("id")
                if not schedule_id:
                    error_msg = "ID가 없습니다"
                    logger.warning(f"[Repo] {error_msg}: {schedule_data}")
                    error_count += 1
                    errors.append({"item": schedule_data, "error": error_msg})
                    continue

                existing_schedule = await self.find_by_id(schedule_id)

                if existing_schedule:
                    await self.update(existing_schedule, schedule_data)
                    updated_count += 1
                    logger.debug(f"[Repo] 경기 일정 업데이트: ID {schedule_id}")
                else:
                    await self.create(schedule_data)
                    inserted_count += 1
                    logger.debug(f"[Repo] 경기 일정 삽입: ID {schedule_id}")

            except IntegrityError as e:
                error_count += 1
                error_msg = f"무결성 제약 조건 위반: {str(e)}"
                logger.error(
                    f"[Repo] {error_msg}: ID {schedule_data.get('id')}",
                    exc_info=True,
                )
                errors.append({"item": schedule_data, "error": error_msg})
            except Exception as e:
                error_count += 1
                error_msg = f"처리 중 오류: {str(e)}"
                logger.error(
                    f"[Repo] {error_msg}: ID {schedule_data.get('id')}",
                    exc_info=True,
                )
                errors.append({"item": schedule_data, "error": error_msg})

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
