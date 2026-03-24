"""
Labzang FastAPI 모놀리식 루트 진입점.
실제 앱/실행 로직은 ``labzang.bootstrap.entrypoint``에서 관리한다.
"""

import sys
from pathlib import Path

_backend_dir = Path(__file__).resolve().parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

# labzang 패키지는 ``sys.path``에 backend 부모가 있어야 로드됨 (Ruff E402).
from labzang.bootstrap import app as _app, run  # noqa: E402

app = _app

if __name__ == "__main__":
    run()
