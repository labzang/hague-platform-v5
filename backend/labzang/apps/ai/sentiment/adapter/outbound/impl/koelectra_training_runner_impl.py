"""Outbound adapter to run KoELECTRA training process."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

from labzang.apps.ai.sentiment.application.ports.output.training_runner import (
    TrainingRunnerPort,
)


class KoELECTRATrainingRunnerImpl(TrainingRunnerPort):
    def __init__(self):
        root = Path(__file__).resolve().parents[3]
        self._state_dir = root / "resources"
        self._state_dir.mkdir(parents=True, exist_ok=True)
        self._pid_file = self._state_dir / "training.pid"
        self._meta_file = self._state_dir / "training.meta.json"
        self._log_file = self._state_dir / "training.log"

    def _is_running(self, pid: int) -> bool:
        if pid <= 0:
            return False
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def _read_meta(self) -> Dict[str, Any]:
        if not self._meta_file.exists():
            return {}
        try:
            return json.loads(self._meta_file.read_text(encoding="utf-8"))
        except Exception:
            return {}

    async def trigger_training(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if self._pid_file.exists():
            try:
                pid = int(self._pid_file.read_text(encoding="utf-8").strip())
                if self._is_running(pid):
                    return {
                        "accepted": False,
                        "status": "already_running",
                        "pid": pid,
                        "message": "Training process is already running.",
                    }
            except Exception:
                pass

        self._log_file.parent.mkdir(parents=True, exist_ok=True)
        log_handle = open(self._log_file, "a", encoding="utf-8")
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "labzang.apps.ai.sentiment.application.inference.run_training",
            stdout=log_handle,
            stderr=log_handle,
        )
        self._pid_file.write_text(str(process.pid), encoding="utf-8")
        self._meta_file.write_text(
            json.dumps({"payload": payload, "pid": process.pid}, ensure_ascii=False),
            encoding="utf-8",
        )
        return {
            "accepted": True,
            "status": "started",
            "pid": process.pid,
            "log_file": str(self._log_file),
        }

    async def training_status(self) -> Dict[str, Any]:
        pid = None
        running = False
        if self._pid_file.exists():
            try:
                pid = int(self._pid_file.read_text(encoding="utf-8").strip())
                running = self._is_running(pid)
            except Exception:
                pid = None
                running = False

        data = {
            "status": "running" if running else "idle",
            "pid": pid,
            "meta": self._read_meta(),
            "log_file": str(self._log_file),
        }
        return data
