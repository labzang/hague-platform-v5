"""
NLTK 기반 말뭉치·텍스트 분석 (wordcloud HTTP 라우터용).
"""
import base64
import io
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class NLTKService:
    """Gutenberg 말뭉치 조회, 토큰/품사 분석, 간단 워드클라우드."""

    def get_corpus_info(self) -> Dict[str, Any]:
        try:
            import nltk
            from nltk.corpus import gutenberg

            try:
                nltk.data.find("corpora/gutenberg")
            except LookupError:
                nltk.download("gutenberg", quiet=True)
            return {
                "corpus": "gutenberg",
                "files": list(gutenberg.fileids()),
            }
        except Exception as e:
            logger.exception("get_corpus_info")
            return {"error": str(e)}

    def analyze_text(self, text: str, name: str = "Document") -> Dict[str, Any]:
        try:
            import nltk
            from nltk import FreqDist
            from nltk.tokenize import word_tokenize

            try:
                nltk.data.find("tokenizers/punkt")
            except LookupError:
                nltk.download("punkt", quiet=True)
            tokens = word_tokenize(text)
            fd = FreqDist(tokens)
            return {
                "name": name,
                "token_count": len(tokens),
                "unique_tokens": len(fd),
                "most_common": fd.most_common(20),
            }
        except Exception as e:
            logger.exception("analyze_text")
            return {"error": str(e)}

    def generate_wordcloud(
        self,
        text: str,
        width: int = 1000,
        height: int = 600,
        background_color: str = "white",
        max_words: int = 100,
    ) -> Dict[str, Any]:
        try:
            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            from wordcloud import WordCloud

            wc = WordCloud(
                width=width,
                height=height,
                background_color=background_color,
                max_words=max_words,
            ).generate(text)
            buf = io.BytesIO()
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
            plt.close()
            raw = buf.getvalue()
            return {
                "image_base64": base64.b64encode(raw).decode("ascii"),
                "width": width,
                "height": height,
            }
        except Exception as e:
            logger.exception("generate_wordcloud")
            return {"error": str(e)}

    def pos_tagging(self, text: str) -> Dict[str, Any]:
        try:
            import nltk
            from nltk.tag import pos_tag
            from nltk.tokenize import word_tokenize

            try:
                nltk.data.find("taggers/averaged_perceptron_tagger")
            except LookupError:
                nltk.download("averaged_perceptron_tagger", quiet=True)
            try:
                nltk.data.find("tokenizers/punkt")
            except LookupError:
                nltk.download("punkt", quiet=True)
            tokens = word_tokenize(text)
            tagged: List[tuple[str, str]] = pos_tag(tokens)
            return {"tags": tagged[:500], "count": len(tagged)}
        except Exception as e:
            logger.exception("pos_tagging")
            return {"error": str(e)}
