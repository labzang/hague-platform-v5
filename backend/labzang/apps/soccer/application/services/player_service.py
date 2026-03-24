"""선수 데이터 규칙 기반 서비스."""
import logging
import numpy as np
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from sqlalchemy import select

from labzang.apps.soccer.adapter.outbound.models.player_model import PlayerModel
from labzang.apps.soccer.adapter.outbound.persistence.async_session import AsyncSessionLocal
from labzang.apps.soccer.adapter.outbound.repositories.player_repo import PlayerRepo
from labzang.apps.soccer.application.orchestrators.spokes.embedding.embedding_client import (
    EmbeddingClient,
)

logger = logging.getLogger(__name__)


class PlayerService:
    """선수 데이터를 규칙 기반으로 처리하는 서비스.

    JSONL 데이터를 players 테이블에 삽입하는 규칙 기반 처리를 수행합니다.
    """

    def __init__(self):
        """PlayerService 초기화."""
        logger.info("[서비스] PlayerService 초기화")
        self.client = EmbeddingClient()

    def _normalize_player_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """선수 데이터를 정규화합니다.

        Args:
            item: 원본 선수 데이터

        Returns:
            정규화된 선수 데이터
        """
        normalized = {}

        # 필드 매핑 및 타입 변환
        if "id" in item:
            normalized["id"] = int(item["id"]) if item["id"] is not None else None

        if "team_id" in item:
            normalized["team_id"] = int(item["team_id"]) if item["team_id"] is not None else None

        if "player_name" in item:
            normalized["player_name"] = str(item["player_name"])[:20] if item["player_name"] else None

        if "e_player_name" in item:
            normalized["e_player_name"] = str(item["e_player_name"])[:40] if item["e_player_name"] else None

        if "nickname" in item:
            normalized["nickname"] = str(item["nickname"])[:30] if item["nickname"] else None

        if "join_yyyy" in item:
            normalized["join_yyyy"] = str(item["join_yyyy"])[:10] if item["join_yyyy"] else None

        if "position" in item:
            normalized["position"] = str(item["position"])[:10] if item["position"] else None

        if "back_no" in item:
            normalized["back_no"] = int(item["back_no"]) if item["back_no"] is not None else None

        if "nation" in item:
            normalized["nation"] = str(item["nation"])[:20] if item["nation"] else None

        if "birth_date" in item:
            birth_date = item["birth_date"]
            if birth_date:
                try:
                    # 문자열을 날짜로 변환
                    if isinstance(birth_date, str):
                        normalized["birth_date"] = datetime.strptime(birth_date, "%Y-%m-%d").date()
                    else:
                        normalized["birth_date"] = birth_date
                except (ValueError, TypeError):
                    logger.warning(f"[서비스] 생년월일 파싱 실패: {birth_date}")
                    normalized["birth_date"] = None
            else:
                normalized["birth_date"] = None

        if "solar" in item:
            normalized["solar"] = str(item["solar"])[:10] if item["solar"] else None

        if "height" in item:
            normalized["height"] = int(item["height"]) if item["height"] is not None else None

        if "weight" in item:
            normalized["weight"] = int(item["weight"]) if item["weight"] is not None else None

        return normalized

    async def _save_players_to_database(
        self,
        normalized_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """정규화된 선수 데이터를 Repository를 통해 데이터베이스에 저장합니다.

        Args:
            normalized_items: 정규화된 선수 데이터 리스트

        Returns:
            저장 결과 딕셔너리
        """
        async with AsyncSessionLocal() as session:
            # Repository 인스턴스 생성
            repository = PlayerRepo(session)

            # 일괄 upsert 수행
            logger.info("[서비스] Repository를 통해 데이터베이스 저장 시작...")
            db_result = await repository.upsert_batch(normalized_items)

            # 커밋
            await repository.commit()
            logger.info(
                f"[서비스] 데이터베이스 저장 완료: "
                f"삽입 {db_result['inserted_count']}개, "
                f"업데이트 {db_result['updated_count']}개, "
                f"오류 {db_result['error_count']}개"
            )

        return db_result

    async def process_players(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """선수 데이터를 규칙 기반으로 처리하고 데이터베이스에 삽입합니다.

        Args:
            items: 처리할 선수 데이터 리스트

        Returns:
            처리 결과 딕셔너리
        """
        logger.info(f"[서비스] 규칙 기반 처리 시작: {len(items)}개 항목")

        # 1. 데이터 정규화
        logger.info("[서비스] 데이터 정규화 시작...")
        normalized_items = []
        for item in items:
            try:
                normalized = self._normalize_player_data(item)
                normalized_items.append(normalized)
            except Exception as e:
                logger.error(f"[서비스] 데이터 정규화 실패: {item.get('id', 'unknown')} - {e}", exc_info=True)

        logger.info(f"[서비스] 정규화 완료: {len(normalized_items)}개 항목")

        # 2. Repository를 통해 데이터베이스에 저장
        logger.info("[서비스] Repository를 통해 데이터베이스 저장 시작...")
        db_result = await self._save_players_to_database(normalized_items)

        result = {
            "success": True,
            "method": "rule_based",
            "total_items": len(items),
            "normalized_count": len(normalized_items),
            "database_result": db_result,
        }

        logger.info(
            f"[서비스] 규칙 기반 처리 완료: "
            f"총 {len(items)}개, 삽입 {db_result['inserted_count']}개, "
            f"업데이트 {db_result['updated_count']}개, 오류 {db_result['error_count']}개"
        )
        return result

    def _create_player_content(self, player: PlayerModel) -> str:
        """선수 데이터로부터 임베딩용 텍스트를 생성합니다.

        Args:
            player: Player 모델 인스턴스

        Returns:
            임베딩용 텍스트
        """
        parts = []
        if player.player_name:
            parts.append(player.player_name)
        if player.e_player_name:
            parts.append(player.e_player_name)
        if player.position:
            parts.append(player.position)
        if player.nation:
            parts.append(player.nation)
        if player.back_no is not None:
            parts.append(f"등번호 {player.back_no}")
        if player.nickname:
            parts.append(player.nickname)

        return ", ".join(parts) if parts else ""

    async def run_batch_indexing(self, batch_size: int = 100) -> Dict[str, Any]:
        """DB에 있는 모든 선수 데이터를 임베딩 테이블로 벡터화합니다.

        Args:
            batch_size: 배치 처리 크기 (기본값: 100)

        Returns:
            처리 결과 딕셔너리
        """
        logger.info("[서비스] 배치 임베딩 인덱싱 시작")

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(PlayerModel))
            players = result.scalars().all()

            logger.info(f"[서비스] 총 {len(players)}명의 선수 데이터 조회 완료")

            processed_count = 0
            error_count = 0
            updated_count = 0
            created_count = 0

            for player in players:
                try:
                    content = self._create_player_content(player)
                    if not content.strip():
                        logger.warning(f"[서비스] 선수 ID {player.id}의 내용이 비어있어 스킵합니다.")
                        continue

                    vector = await self.client.get_embedding(content)
                    embedding_array = np.array(vector, dtype=np.float32)

                    had_embedding = player.embedding is not None
                    player.embedding_text = content
                    player.embedding = embedding_array
                    player.embedding_at = datetime.now(timezone.utc)
                    if had_embedding:
                        updated_count += 1
                        logger.debug(f"[서비스] 선수 ID {player.id} 임베딩 업데이트")
                    else:
                        created_count += 1
                        logger.debug(f"[서비스] 선수 ID {player.id} 임베딩 생성")

                    processed_count += 1

                    if processed_count % batch_size == 0:
                        await session.commit()
                        logger.info(
                            f"[서비스] {processed_count}개 임베딩 처리 완료 "
                            f"(생성: {created_count}, 업데이트: {updated_count}, 오류: {error_count})"
                        )

                except Exception as e:
                    error_count += 1
                    logger.error(
                        f"[서비스] 선수 ID {player.id} 임베딩 처리 실패: {str(e)}",
                        exc_info=True
                    )

            await session.commit()

            result = {
                "success": True,
                "total_players": len(players),
                "processed_count": processed_count,
                "created_count": created_count,
                "updated_count": updated_count,
                "error_count": error_count
            }

            logger.info(
                f"[서비스] 배치 임베딩 인덱싱 완료: "
                f"총 {len(players)}개, 처리 {processed_count}개, "
                f"생성 {created_count}개, 업데이트 {updated_count}개, 오류 {error_count}개"
            )

            return result

