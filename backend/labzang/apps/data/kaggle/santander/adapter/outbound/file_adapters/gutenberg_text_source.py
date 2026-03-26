"""
TextSourcePort의 Gutenberg 말뭉치 구현.
- emma_corpus: NLTK Gutenberg austen-emma.txt
- font_path: base_dir 기준 D2Coding.ttf 경로
"""
from pathlib import Path

import nltk  # type: ignore[import-untyped]

from labzang.apps.data.wordcloud.samsung_report.application.ports.output.wordcloud_ports import TextSourcePort

KEY_EMMA_CORPUS = "emma_corpus"
KEY_FONT_PATH = "font_path"
EMMA_FILENAME = "austen-emma.txt"


def _ensure_nltk_data() -> None:
    try:
        nltk.download("punkt", quiet=True)
        nltk.download("averaged_perceptron_tagger", quiet=True)
    except Exception:
        pass


class GutenbergTextSourceAdapter(TextSourcePort):
    """NLTK Gutenberg 말뭉치 + 폰트 경로 제공."""

    def __init__(self, base_dir: Path) -> None:
        self._base = Path(base_dir).resolve()
        self._data_dir = self._base / "data"

    def get_text(self, key: str) -> str:
        if key == KEY_EMMA_CORPUS:
            _ensure_nltk_data()
            return nltk.corpus.gutenberg.raw(EMMA_FILENAME)
        if key == KEY_FONT_PATH:
            return str(self._data_dir / "D2Coding.ttf")
        return ""
