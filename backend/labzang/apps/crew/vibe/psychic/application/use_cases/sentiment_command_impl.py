"""Sentiment command use case implementation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from labzang.apps.ai.sentiment.application.ports.input import SentimentCommand
from labzang.apps.ai.sentiment.application.ports.output import SentimentRepository
from labzang.apps.ai.sentiment.domain.entities import SentimentReview


class SentimentCommandImpl(SentimentCommand):
    def __init__(self, repository: SentimentRepository, resources_data_dir: Path):
        self._repository = repository
        self._resources_data_dir = resources_data_dir

    async def ingest_reviews(self, rows: List[Dict[str, Any]]) -> Dict[str, int]:
        parsed: list[SentimentReview] = []
        errors = 0
        for raw in rows:
            try:
                parsed.append(SentimentReview.from_json_dict(raw))
            except Exception:
                errors += 1
        saved = await self._repository.upsert_batch(parsed)
        saved["parsed_count"] = len(parsed)
        saved["error_count"] = saved.get("error_count", 0) + errors
        return saved

    async def ingest_resources_data(self) -> Dict[str, int]:
        files = sorted(self._resources_data_dir.glob("*.json"))
        rows: list[dict[str, Any]] = []
        file_errors = 0
        for file_path in files:
            try:
                payload = json.loads(file_path.read_text(encoding="utf-8"))
                if isinstance(payload, list):
                    rows.extend(item for item in payload if isinstance(item, dict))
            except Exception:
                file_errors += 1

        result = await self.ingest_reviews(rows)
        result["source_file_count"] = len(files)
        result["source_file_error_count"] = file_errors
        return result
