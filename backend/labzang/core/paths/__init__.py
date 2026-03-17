"""
backend/labzang 기준 절대 경로 (단일 소스)
- 모든 경로는 .resolve()로 절대경로 보장
"""
from pathlib import Path

# labzang 루트 (core/paths/__init__.py 기준 상위 3단계)
_LABZANG_ROOT: Path = Path(__file__).resolve().parent.parent.parent
LABZANG_ROOT: Path = _LABZANG_ROOT.resolve()

# 앱 루트들 (절대경로)
APPS_ROOT: Path = LABZANG_ROOT / "apps"
LEARNING_ROOT: Path = APPS_ROOT / "learning"
KAGGLE_ROOT: Path = APPS_ROOT / "kaggle"
CRAWLER_ROOT: Path = APPS_ROOT / "crawler"
TRANSFORMER_ROOT: Path = APPS_ROOT / "transformer"
CHAT_ROOT: Path = APPS_ROOT / "chat"

# shared
SHARED_ROOT: Path = LABZANG_ROOT / "shared"

__all__ = [
    "LABZANG_ROOT",
    "APPS_ROOT",
    "LEARNING_ROOT",
    "KAGGLE_ROOT",
    "CRAWLER_ROOT",
    "TRANSFORMER_ROOT",
    "CHAT_ROOT",
    "SHARED_ROOT",
]
