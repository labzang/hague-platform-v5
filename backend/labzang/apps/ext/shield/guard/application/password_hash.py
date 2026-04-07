"""비밀번호 PBKDF2 해시 (표준 라이브러리만 사용)."""

from __future__ import annotations

import hashlib
import secrets


def hash_password(plain: str) -> str:
    """salt$hexdigest 형태로 저장."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        plain.encode("utf-8"),
        salt.encode("ascii"),
        120_000,
    )
    return f"{salt}${dk.hex()}"


def verify_password(plain: str, stored: str) -> bool:
    if "$" not in stored:
        return False
    salt, hex_digest = stored.split("$", 1)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        plain.encode("utf-8"),
        salt.encode("ascii"),
        120_000,
    )
    return secrets.compare_digest(dk.hex(), hex_digest)
