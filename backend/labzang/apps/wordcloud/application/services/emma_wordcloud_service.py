"""
Emma 워드클라우드 애플리케이션 서비스 (순수 로직, I/O 없음).
- 텍스트·폰트 경로·옵션을 받아 빈도와 PNG 이미지 바이트 반환.
"""
import io
import logging
from typing import Any, Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from nltk import FreqDist  # type: ignore[import-untyped]
from nltk.tokenize import RegexpTokenizer  # type: ignore[import-untyped]
from nltk.tag import pos_tag  # type: ignore[import-untyped]
from wordcloud import WordCloud  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)

DEFAULT_STOPWORDS = {"Mr.", "Mrs.", "Miss", "Mr", "Mrs", "Dear"}


class EmmaWordcloudService:
    """Emma 소설 고유명사(NNP) 기반 워드클라우드 생성 로직만 담당."""

    def __init__(self) -> None:
        self._tokenizer = RegexpTokenizer(r"[\w]+")

    def process(
        self,
        text: str,
        font_path: str,
        *,
        width: int = 1000,
        height: int = 600,
        background_color: str = "white",
        max_words: int = 100,
    ) -> Tuple[bytes, Dict[str, int], int, List[Tuple[str, int]]]:
        """
        텍스트에서 고유명사 우선 빈도 추출 후 워드클라우드 PNG 바이트 생성.
        Returns: (image_bytes, freq_dict, word_count, most_common_10)
        """
        tokens = self._tokenizer.tokenize(text)
        pos_tagged = pos_tag(tokens)
        proper_nouns = [
            w for w, tag in pos_tagged
            if tag == "NNP" and w not in DEFAULT_STOPWORDS
        ]
        if not proper_nouns:
            freq_dist = FreqDist(tokens)
        else:
            freq_dist = FreqDist(proper_nouns)

        freq_dict = dict(freq_dist.most_common(max_words))
        wc = WordCloud(
            font_path=font_path,
            width=width,
            height=height,
            background_color=background_color,
            max_words=max_words,
            random_state=42,
        )
        wordcloud = wc.generate_from_frequencies(freq_dict)

        img_bytes = self._figure_to_png_bytes(wordcloud, width, height)
        word_count = len(freq_dict)
        most_common = freq_dist.most_common(10)
        return img_bytes, freq_dict, word_count, most_common

    def _figure_to_png_bytes(self, wordcloud: Any, width: int, height: int) -> bytes:
        plt.figure(figsize=(width / 100, height / 100))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", dpi=100)
        plt.close()
        buf.seek(0)
        return buf.read()
