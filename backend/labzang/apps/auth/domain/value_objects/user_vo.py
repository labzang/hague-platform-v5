"""
사용자 도메인 값 객체 (순수: 외부 라이브러리 미참조)
- User ORM 컬럼 기준: username, password, name, phone, email, created_at, updated_at
- 도메인 의미·검증이 있는 값만 VO로 정의.
"""
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass(frozen=True)
class Username:
    """사용자 아이디. 공백 제거 후 3~50자."""

    value: str

    def __post_init__(self) -> None:
        v = (self.value or "").strip()
        if not (3 <= len(v) <= 50):
            raise ValueError("Username must be between 3 and 50 characters")
        object.__setattr__(self, "value", v)


@dataclass(frozen=True)
class Password:
    """비밀번호(해시 포함). 공백 제거 후 최소 8자."""

    value: str

    def __post_init__(self) -> None:
        v = (self.value or "").strip()
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        object.__setattr__(self, "value", v)


@dataclass(frozen=True)
class Name:
    """사용자 이름. 공백 제거 후 비어 있지 않아야 함."""

    value: str

    def __post_init__(self) -> None:
        v = (self.value or "").strip()
        if not v:
            raise ValueError("Name must be non-empty")
        object.__setattr__(self, "value", v)


@dataclass(frozen=True)
class Phone:
    """전화번호. 숫자/+, -, 공백만 허용, 길이 7~20."""

    value: str

    def __post_init__(self) -> None:
        v = (self.value or "").strip()
        if not (7 <= len(v) <= 20):
            raise ValueError("Phone must be between 7 and 20 characters")
        if not re.fullmatch(r"[0-9+\-\s]+", v):
            raise ValueError("Phone contains invalid characters")
        object.__setattr__(self, "value", v)


@dataclass(frozen=True)
class Email:
    """이메일 주소. 기본 형식(local@domain) 검증."""

    value: str

    def __post_init__(self) -> None:
        v = (self.value or "").strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", v):
            raise ValueError("Email format is invalid")
        object.__setattr__(self, "value", v)


@dataclass(frozen=True)
class CreatedAt:
    """계정 생성 시각."""

    value: datetime


@dataclass(frozen=True)
class UpdatedAt:
    """계정 수정 시각."""

    value: datetime
