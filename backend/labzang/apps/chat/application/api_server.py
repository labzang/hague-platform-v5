"""Deprecated chat API server module.

독립 서버 엔트리포인트는 모놀리식 통합 후 중단되었으며,
호환을 위해 루트 모놀리식 앱을 재노출한다.
"""

from labzang.bootstrap.entrypoint import app, config, run

__all__ = ["app", "config", "run"]

if __name__ == "__main__":
    run()