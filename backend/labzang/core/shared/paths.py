"""Project path constants used across apps."""

from __future__ import annotations

from pathlib import Path

LABZANG_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = LABZANG_ROOT.parent
APPS_ROOT = LABZANG_ROOT / "apps"
LEARNING_ROOT = BACKEND_ROOT / "learning"
ML_ROOT = BACKEND_ROOT / "ml"
CRAWLER_ROOT = APPS_ROOT / "ext" / "crawler"
TRANSFORMER_ROOT = APPS_ROOT / "ai" / "transformer"
CHAT_ROOT = APPS_ROOT / "com" / "chat"
SHARED_ROOT = LABZANG_ROOT / "shared"
