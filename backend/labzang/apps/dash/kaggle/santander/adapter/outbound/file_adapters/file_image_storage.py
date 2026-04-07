"""
이미지 저장 포트의 파일 시스템 구현.
"""
from pathlib import Path
from typing import Any, Dict

from labzang.apps.data.wordcloud.samsung_report.application.ports.output.wordcloud_ports import ImageStoragePort


class FileImageStorageAdapter(ImageStoragePort):
    """이미지 바이트를 디스크에 저장."""

    def __init__(self, base_dir: Path) -> None:
        self._base = Path(base_dir).resolve()

    def save(
        self,
        subdir: str,
        filename: str,
        image_bytes: bytes,
    ) -> Dict[str, Any]:
        save_dir = self._base / subdir / "save"
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / filename
        save_path.write_bytes(image_bytes)
        return {
            "filename": filename,
            "path": str(save_path),
            "size_bytes": save_path.stat().st_size,
            "exists": save_path.exists(),
        }
