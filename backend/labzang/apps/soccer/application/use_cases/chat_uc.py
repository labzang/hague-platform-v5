"""챗팅 질문 처리 유스케이스.

사용자 질문을 받아 도메인별 UC로 라우팅합니다.
"""
import logging
from typing import Any, Dict

from labzang.apps.soccer.application.use_cases.player_uc import PlayerUC
from labzang.apps.soccer.application.use_cases.schedule_uc import ScheduleUC
from labzang.apps.soccer.application.use_cases.stadium_uc import StadiumUC
from labzang.apps.soccer.application.use_cases.team_uc import TeamUC
from labzang.apps.soccer.domain.classifiers.question_classifier import QuestionClassifier

logger = logging.getLogger(__name__)


class ChatUC:
    """챗팅 질문 처리 UC.

    질문을 분석하여 적절한 도메인 UC로 라우팅합니다.
    """

    def __init__(self) -> None:
        """ChatUC 초기화."""
        self.classifier = QuestionClassifier(use_model=False)

        self._player_uc: PlayerUC | None = None
        self._schedule_uc: ScheduleUC | None = None
        self._stadium_uc: StadiumUC | None = None
        self._team_uc: TeamUC | None = None

        logger.info("[ChatUC] 초기화 완료")

    @property
    def player_uc(self) -> PlayerUC:
        """PlayerUC 인스턴스 (지연 로딩)."""
        if self._player_uc is None:
            self._player_uc = PlayerUC()
        return self._player_uc

    @property
    def schedule_uc(self) -> ScheduleUC:
        """ScheduleUC 인스턴스 (지연 로딩)."""
        if self._schedule_uc is None:
            self._schedule_uc = ScheduleUC()
        return self._schedule_uc

    @property
    def stadium_uc(self) -> StadiumUC:
        """StadiumUC 인스턴스 (지연 로딩)."""
        if self._stadium_uc is None:
            self._stadium_uc = StadiumUC()
        return self._stadium_uc

    @property
    def team_uc(self) -> TeamUC:
        """TeamUC 인스턴스 (지연 로딩)."""
        if self._team_uc is None:
            self._team_uc = TeamUC()
        return self._team_uc

    async def process_query(self, question: str) -> Dict[str, Any]:
        """사용자 질문을 처리합니다."""
        logger.info(f"[ChatUC] 질문 수신: {question}")
        print(f"[ChatUC] 사용자 질문: {question}")

        classification_result = self.classifier.classify(question)
        domain = classification_result["domain"]
        confidence = classification_result["confidence"]

        logger.info(
            f"[ChatUC] 질문 분류 완료: 도메인={domain}, "
            f"신뢰도={confidence:.2f}, 방법={classification_result['method']}"
        )
        print(f"[ChatUC] 분류 결과: {domain} (신뢰도: {confidence:.2f})")

        if domain == "player":
            logger.info("[ChatUC] PlayerUC로 라우팅")
            result = await self.player_uc.process_query(question)
        elif domain == "schedule":
            logger.info("[ChatUC] ScheduleUC로 라우팅")
            result = await self.schedule_uc.process_query(question)
        elif domain == "stadium":
            logger.info("[ChatUC] StadiumUC로 라우팅")
            result = await self.stadium_uc.process_query(question)
        elif domain == "team":
            logger.info("[ChatUC] TeamUC로 라우팅")
            result = await self.team_uc.process_query(question)
        else:
            logger.warning(f"[ChatUC] 알 수 없는 도메인: {domain}")
            result = {
                "success": False,
                "message": "질문을 이해할 수 없습니다. 축구 관련 질문을 입력해주세요.",
                "domain": domain,
                "confidence": confidence,
            }

        result["classification"] = classification_result
        result["routed_domain"] = domain

        logger.info(f"[ChatUC] 질문 처리 완료: 도메인={domain}")
        return result
