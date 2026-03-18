from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "KRW"

    def __post_init__(self):
        """
        [상사 지적사항 반영] 전역 불변 제약: 금액은 0보다 커야 함.
        생성 시점에 즉시 검증하여 잘못된 객체 생성을 차단 (원샷 원킬)
        """
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        
        # 통계적/전역적 온톨로지 규칙에 따른 통화 코드 대문자 표준화
        object.__setattr__(self, 'currency', self.currency.upper())

    def __add__(self, other: Self) -> Self:
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def is_greater_than(self, other: Self) -> bool:
        return self.amount > other.amount