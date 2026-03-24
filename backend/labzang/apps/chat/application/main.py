"""Chat app legacy entrypoint.

기존 독립 실행 파일은 모놀리식 통합 후 유지보수용 래퍼로만 남깁니다.
"""

from labzang.bootstrap.entrypoint import app, config, run

__all__ = ["app", "config", "run"]

if __name__ == "__main__":
    run()