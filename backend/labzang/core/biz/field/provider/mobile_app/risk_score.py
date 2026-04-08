# apps/chat_bot/domain/values/risk_score.py
from dataclasses import dataclass

@dataclass(frozen=True)
class RiskScore:
    value: int  # 0 ~ 100 점 사이

    def __post_init__(self):
        # 앱 특화 제약: 리스크 점수는 반드시 0~100 사이여야 함
        if not (0 <= self.value <= 100):
            raise ValueError("App Rule: Risk score must be between 0 and 100")

    @property
    def level(self) -> str:
        # 앱 특화 로직: 점수에 따른 등급 분류
        if self.value > 80: return "HIGH"
        if self.value > 40: return "MEDIUM"
        return "LOW"