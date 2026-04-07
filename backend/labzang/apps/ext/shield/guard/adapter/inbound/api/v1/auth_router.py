"""
ext.guard 인바운드 API — 회원가입 등.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from labzang.apps.ext.guard.adapter.inbound.schemas.register_schema import (
    RegisterRequest,
    RegisterResponseData,
)
from labzang.apps.ext.guard.adapter.outbound.orm.user_orm import UserORM
from labzang.apps.ext.guard.application.password_hash import hash_password
from labzang.core.database import get_db
from labzang.core.utils.utils import create_response

router = APIRouter(prefix="/auth", tags=["ext-guard"])


@router.get("/")
async def auth_root():
    return create_response(
        data={"service": "ext-auth", "status": "running"},
        message="Auth Service is running",
    )


@router.get("/health")
async def health_check():
    return create_response(
        data={"status": "healthy", "service": "ext-auth"},
        message="Service is healthy",
    )


@router.post("/register")
def register_user(
    body: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    회원가입 — `users` 테이블에 저장.
    - `id`: 서버에서 UUID 자동 부여
    - `role`: 이 경로로 가입 시 항상 `customer`
    """
    existing = db.scalars(
        select(UserORM).where(UserORM.username == body.username)
    ).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.")

    new_id = str(uuid.uuid4())
    row = UserORM(
        id=new_id,
        username=body.username.strip(),
        password_hash=hash_password(body.password),
        name=body.name.strip(),
        email=body.email.strip(),
        phone=body.phone.strip(),
        birth_date=body.birth_date,
        gender=body.gender.strip(),
        address_main=body.address_main.strip(),
        address_detail=(body.address_detail or "").strip() or None,
        role="customer",
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    payload = RegisterResponseData(id=new_id, username=row.username, role=row.role)
    return create_response(
        data=payload.model_dump(),
        message="회원가입이 완료되었습니다.",
    )
