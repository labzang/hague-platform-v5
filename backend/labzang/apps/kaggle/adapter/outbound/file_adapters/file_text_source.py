"""
텍스트 소스 포트의 파일 시스템 구현.
- key별로 고정 경로에서 텍스트 또는 경로 문자열 반환.
"""
from pathlib import Path

from labzang.apps.ml.application.ports.output import TextSourcePort

# use case와 약속한 키
KEY_SAMSUNG_REPORT = "samsung_report"
KEY_STOPWORDS = "stopwords"
KEY_FONT_PATH = "font_path"


class FileTextSourceAdapter(TextSourcePort):
    """NLP 리소스 디렉터리 기준으로 텍스트/경로 반환."""

    def __init__(self, base_dir: Path) -> None:
        self._base = Path(base_dir).resolve()
        self._data_dir = self._base / "data"

    def get_text(self, key: str) -> str:
        if key == KEY_SAMSUNG_REPORT:
            path = self._data_dir / "kr-Report_2018.txt"
            return path.read_text(encoding="utf-8")
        if key == KEY_STOPWORDS:
            path = self._data_dir / "stopwords.txt"
            return path.read_text(encoding="utf-8")
        if key == KEY_FONT_PATH:
            return str(self._data_dir / "D2Coding.ttf")
        return ""
