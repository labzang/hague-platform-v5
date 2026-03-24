"""선수 데이터 Repo."""

import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from labzang.apps.soccer.adapter.outbound.models.player_model import PlayerModel

logger = logging.getLogger(__name__)


class PlayerRepo:
    """선수 데이터 Repo.

    Neon `players` 테이블 CRUD.
    """

    def __init__(self, session: AsyncSession):
        """PlayerRepo 초기화.

        Args:
            session: 데이터베이스 세션
        """
        self.session = session
        logger.debug("[Repo] PlayerRepo 초기화")

    async def find_by_id(self, player_id: int) -> Optional[PlayerModel]:
        """ID로 선수를 조회합니다."""
        result = await self.session.execute(
            select(PlayerModel).where(PlayerModel.id == player_id)
        )
        return result.scalar_one_or_none()

    async def create(self, player_data: Dict[str, Any]) -> PlayerModel:
        """새 선수를 생성합니다."""
        new_player = PlayerModel(**player_data)
        self.session.add(new_player)
        logger.debug(f"[Repo] 선수 생성: ID {player_data.get('id')}")
        return new_player

    async def update(
        self, player: PlayerModel, player_data: Dict[str, Any]
    ) -> PlayerModel:
        """기존 선수를 업데이트합니다."""
        for key, value in player_data.items():
            if key != "id":
                setattr(player, key, value)
        logger.debug(f"[Repo] 선수 업데이트: ID {player.id}")
        return player

    async def upsert_batch(
        self, players_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """여러 선수를 일괄 upsert (insert or update) 합니다."""
        inserted_count = 0
        updated_count = 0
        error_count = 0
        errors: List[Dict[str, Any]] = []

        for player_data in players_data:
            try:
                player_id = player_data.get("id")
                if not player_id:
                    error_msg = "ID가 없습니다"
                    logger.warning(f"[Repo] {error_msg}: {player_data}")
                    error_count += 1
                    errors.append({"item": player_data, "error": error_msg})
                    continue

                existing_player = await self.find_by_id(player_id)

                if existing_player:
                    await self.update(existing_player, player_data)
                    updated_count += 1
                    logger.debug(f"[Repo] 선수 업데이트: ID {player_id}")
                else:
                    await self.create(player_data)
                    inserted_count += 1
                    logger.debug(f"[Repo] 선수 삽입: ID {player_id}")

            except IntegrityError as e:
                error_count += 1
                error_msg = f"무결성 제약 조건 위반: {str(e)}"
                logger.error(
                    f"[Repo] {error_msg}: ID {player_data.get('id')}",
                    exc_info=True,
                )
                errors.append({"item": player_data, "error": error_msg})
            except Exception as e:
                error_count += 1
                error_msg = f"처리 중 오류: {str(e)}"
                logger.error(
                    f"[Repo] {error_msg}: ID {player_data.get('id')}",
                    exc_info=True,
                )
                errors.append({"item": player_data, "error": error_msg})

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
