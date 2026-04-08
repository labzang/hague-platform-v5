"""Project path constants used across apps."""

from __future__ import annotations

from pathlib import Path

CORE_ROOT = Path(__file__).resolve().parent
LABZANG_ROOT = CORE_ROOT.parent
BACKEND_ROOT = LABZANG_ROOT.parent
APPS_ROOT = LABZANG_ROOT / "apps"
LEARNING_ROOT = BACKEND_ROOT / "learning"
ML_ROOT = BACKEND_ROOT / "ml"
CRAWLER_ROOT = APPS_ROOT / "ext" / "bridge" / "crawler" / "music"
TRANSFORMER_ROOT = APPS_ROOT / "ai" / "transformer"
CHAT_ROOT = APPS_ROOT / "ai" / "intel" / "advisor" / "inquiry"
# 공용 유틸·문서 등 (물리 폴더가 없을 수 있음 — pathlib 연산용 앵커)
SHARED_ROOT = CORE_ROOT / "ext" / "shield" / "guard" / "http"
