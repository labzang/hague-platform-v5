# -*- coding: utf-8 -*-
"""`users` 테이블 — 회원가입(랩장 아카데미) 스키마."""

from __future__ import annotations

from sqlalchemy import Column, Date, DateTime, String, Text, func

from labzang.core.database import Base


class UserORM(Base):
    """사용자 행. PK `id`는 UUID 문자열."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, comment="UUID PK")
    username = Column(String(50), unique=True, nullable=False, index=True, comment="로그인 아이디")
    password_hash = Column(String(255), nullable=False, comment="PBKDF2 해시")
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    address_main = Column(Text, nullable=False)
    address_detail = Column(Text, nullable=True)
    role = Column(String(32), nullable=False, comment="역할")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
