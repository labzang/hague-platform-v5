"""프로세스 기동·모놀리식 FastAPI 조립."""

from labzang.bootstrap.monolith_app import create_monolith_app
from labzang.bootstrap.entrypoint import app, config, run

__all__ = ["create_monolith_app", "app", "config", "run"]
