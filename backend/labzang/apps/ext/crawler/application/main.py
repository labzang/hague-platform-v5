"""
Crawler 서비스 레거시 진입점.
통합 이후에는 루트 모놀리식 앱을 재노출한다.
"""
from labzang.bootstrap.entrypoint import app, config, run

__all__ = ["app", "config", "run"]

if __name__ == "__main__":
    run()
