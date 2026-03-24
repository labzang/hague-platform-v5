"""Unified runtime entrypoint for monolithic Labzang API.

Legacy per-app ``application/main.py`` modules should re-export symbols from here.
"""

from __future__ import annotations

from fastapi import FastAPI

from labzang.bootstrap.monolith_app import create_monolith_app
from labzang.core.config import ChatbotServiceConfig

config = ChatbotServiceConfig()
app: FastAPI = create_monolith_app()


def run() -> None:
    """Run monolith app with configured host/port."""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=config.port, reload=False)
