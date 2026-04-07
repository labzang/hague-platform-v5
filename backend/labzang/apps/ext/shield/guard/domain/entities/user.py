"""
사용자 도메인 엔티티 (순수 파이썬) — API/ORM과 필드 의미 정렬용.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from labzang.apps.ext.guard.domain.value_objects.user_vo import (
    Email,
    Name,
    Password,
    Phone,
    Username,
)


@dataclass
class User:
    """등록된 사용자."""

    id: str
    username: Username
    role: str
    password: Optional[Password] = None
    name: Optional[Name] = None
    phone: Optional[Phone] = None
    email: Optional[Email] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    address_main: Optional[str] = None
    address_detail: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
