"""
labzang 패키지.
실행 위치와 관계없이 backend가 sys.path에 있도록 보정합니다.
"""
import sys
from pathlib import Path

# labzang 패키지 디렉터리 = backend/labzang, 그 상위 backend가 path에 있어야 함
_labzang_root = Path(__file__).resolve().parent
_backend_dir = _labzang_root.parent
_backend_str = str(_backend_dir)
if _backend_str not in sys.path:
    sys.path.insert(0, _backend_str)
