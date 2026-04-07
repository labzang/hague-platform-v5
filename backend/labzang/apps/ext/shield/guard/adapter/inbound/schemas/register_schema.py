"""회원가입 요청/응답 스키마."""

from __future__ import annotations

from datetime import date
from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="로그인 아이디")
    password: str = Field(..., min_length=4, max_length=128)
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(
        ...,
        min_length=3,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    phone: str = Field(..., min_length=10, max_length=20)
    birth_date: date
    gender: str = Field(..., min_length=1, max_length=10)
    address_main: str = Field(..., min_length=1)
    address_detail: str = ""


class RegisterResponseData(BaseModel):
    id: str = Field(..., description="UUID PK")
    username: str
    role: str = "customer"
