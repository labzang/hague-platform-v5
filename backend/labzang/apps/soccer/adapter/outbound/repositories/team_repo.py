"""팀 데이터 Repo."""

import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from labzang.apps.soccer.adapter.outbound.models.team_model import TeamModel

logger = logging.getLogger(__name__)


class TeamRepo:
    """팀 데이터 Repo.

    Neon `teams` 테이블 CRUD.
    """

    def __init__(self, session: AsyncSession):
        """TeamRepo 초기화.

        Args:
            session: 데이터베이스 세션
        """
        self.session = session
        logger.debug("[Repo] TeamRepo 초기화")

    async def find_by_id(self, team_id: int) -> Optional[TeamModel]:
        """ID로 팀을 조회합니다."""
        result = await self.session.execute(
            select(TeamModel).where(TeamModel.id == team_id)
        )
        return result.scalar_one_or_none()

    async def create(self, team_data: Dict[str, Any]) -> TeamModel:
        """새 팀을 생성합니다."""
        new_team = TeamModel(**team_data)
        self.session.add(new_team)
        logger.debug(f"[Repo] 팀 생성: ID {team_data.get('id')}")
        return new_team

    async def update(self, team: TeamModel, team_data: Dict[str, Any]) -> TeamModel:
        """기존 팀을 업데이트합니다."""
        for key, value in team_data.items():
            if key != "id":
                setattr(team, key, value)
        logger.debug(f"[Repo] 팀 업데이트: ID {team.id}")
        return team

    async def upsert_batch(self, teams_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """여러 팀을 일괄 upsert (insert or update) 합니다."""
        inserted_count = 0
        updated_count = 0
        error_count = 0
        errors: List[Dict[str, Any]] = []

        for team_data in teams_data:
            try:
                team_id = team_data.get("id")
                if not team_id:
                    error_msg = "ID가 없습니다"
                    logger.warning(f"[Repo] {error_msg}: {team_data}")
                    error_count += 1
                    errors.append({"item": team_data, "error": error_msg})
                    continue

                existing_team = await self.find_by_id(team_id)

                if existing_team:
                    await self.update(existing_team, team_data)
                    updated_count += 1
                    logger.debug(f"[Repo] 팀 업데이트: ID {team_id}")
                else:
                    await self.create(team_data)
                    inserted_count += 1
                    logger.debug(f"[Repo] 팀 삽입: ID {team_id}")

            except IntegrityError as e:
                error_count += 1
                error_msg = f"무결성 제약 조건 위반: {str(e)}"
                logger.error(
                    f"[Repo] {error_msg}: ID {team_data.get('id')}",
                    exc_info=True,
                )
                errors.append({"item": team_data, "error": error_msg})
            except Exception as e:
                error_count += 1
                error_msg = f"처리 중 오류: {str(e)}"
                logger.error(
                    f"[Repo] {error_msg}: ID {team_data.get('id')}",
                    exc_info=True,
                )
                errors.append({"item": team_data, "error": error_msg})

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
