"""
삼성 워드클라우드 애플리케이션 서비스 (순수 로직, I/O 없음).
- 텍스트·스톱워드·폰트 경로를 받아 빈도와 이미지 바이트 반환.
"""
import io
import re
import logging
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from konlpy.tag import Okt  # type: ignore[import-untyped]
from nltk import FreqDist  # type: ignore[import-untyped]
from wordcloud import WordCloud  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)

# 한글 공백 기준 토큰 분리 (원본 change_token 대체; word_tokenize 미사용)
def _tokenize(text: str) -> List[str]:
    return text.split()


class SamsungWordcloudService:
    """워드클라우드 생성 로직만 담당. 파일/디스크 접근 없음."""

    def __init__(self) -> None:
        self._okt = Okt()

    def process(
        self,
        report_text: str,
        stopwords_text: str,
        font_path: str,
        *,
        width: int = 1200,
        height: int = 800,
        max_words: int = 100,
    ) -> Tuple[Dict[str, int], bytes]:
        """
        보고서 텍스트와 스톱워드로 전처리 후 빈도 dict와 PNG 이미지 바이트 반환.
        """
        # Okt 워밍업 (원본과 동일)
        self._okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)

        cleaned = self._extract_hangeul(report_text)
        tokens = _tokenize(cleaned)
        noun_text = self._extract_noun_from_tokens(tokens)
        noun_tokens = _tokenize(noun_text)
        stopwords = set(_tokenize(stopwords_text.strip()))
        filtered = [t for t in noun_tokens if t not in stopwords]

        freq = dict(FreqDist(filtered))
        freq_sorted = dict(
            sorted(freq.items(), key=lambda x: -x[1])
        )
        logger.info("freq top ~30: %s", list(freq_sorted.items())[:30])

        image_bytes = self._generate_wordcloud_image(
            filtered,
            font_path=font_path,
            width=width,
            height=height,
            max_words=max_words,
        )
        return freq_sorted, image_bytes

    def _extract_hangeul(self, text: str) -> str:
        temp = text.replace("\n", " ")
        tokenizer = re.compile(r"[^ ㄱ-힣]+")
        return tokenizer.sub("", temp)

    def _extract_noun_from_tokens(self, tokens: List[str]) -> str:
        noun_tokens: List[str] = []
        for part in tokens:
            pos = self._okt.pos(part)
            nouns = [p[0] for p in pos if p[1] == "Noun"]
            word = "".join(nouns)
            if len(word) > 1:
                noun_tokens.append(word)
        return " ".join(noun_tokens)

    def _generate_wordcloud_image(
        self,
        tokens: List[str],
        *,
        font_path: str,
        width: int = 1200,
        height: int = 800,
        max_words: int = 100,
    ) -> bytes:
        text = " ".join(tokens)
        wc = WordCloud(
            font_path=font_path,
            relative_scaling=0.2,
            background_color="white",
            width=width,
            height=height,
            max_words=max_words,
        ).generate(text)
        fig = plt.figure(figsize=(12, 12))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        buf = io.BytesIO()
        plt.savefig(
            buf,
            format="png",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none",
        )
        plt.close(fig)
        buf.seek(0)
        return buf.read()
