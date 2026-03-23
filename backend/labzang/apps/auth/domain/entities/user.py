"""
사용자 도메인 엔티티 (순수 파이썬)
- User ORM 컬럼과 1:1 대응.
"""
from dataclasses import dataclass
from typing import Optional

from labzang.apps.auth.domain.value_objects.user_vo import (
    CreatedAt,
    Email,
    Name,
    Password,
    Phone,
    UpdatedAt,
    Username,
)


@dataclass
class User:
    """사용자 엔티티."""

    username: Optional[Username] = None
    password: Optional[Password] = None
    name: Optional[Name] = None
    phone: Optional[Phone] = None
    email: Optional[Email] = None
    created_at: Optional[CreatedAt] = None
    updated_at: Optional[UpdatedAt] = None


@dataclass
class UserModels:
    """사용자 모델 메타 정보 (TitanicModels 대응)."""

    last_login_at: Optional[str] = None
    status: Optional[str] = None
