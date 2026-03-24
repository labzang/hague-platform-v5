"""
Emma 워드클라우드 유스케이스 (포트만 의존).
"""

import base64
from datetime import datetime
from typing import Any, Dict

from labzang.apps.wordcloud.application.ports.output import (
    TextSourcePort,
    ImageStoragePort,
)
from labzang.apps.wordcloud.application.services.emma_wordcloud_service import (
    EmmaWordcloudService,
)

# 어댑터와 약속한 키 (gutenberg_text_source.GutenbergTextSourceAdapter)
KEY_EMMA_CORPUS = "emma_corpus"
KEY_FONT_PATH = "font_path"


class GenerateEmmaWordcloudUC:
    """Emma 소설 고유명사 워드클라우드 생성 유스케이스."""

    def __init__(
        self,
        text_source: TextSourcePort,
        image_storage: ImageStoragePort,
        wordcloud_service: EmmaWordcloudService,
    ) -> None:
        self._text_source = text_source
        self._image_storage = image_storage
        self._wordcloud_service = wordcloud_service

    def execute(
        self,
        *,
        width: int = 1000,
        height: int = 600,
        background_color: str = "white",
        max_words: int = 100,
        max_chars: int = 50000,
    ) -> Dict[str, Any]:
        full_text = self._text_source.get_text(KEY_EMMA_CORPUS)
        text = full_text[:max_chars]
        font_path = self._text_source.get_text(KEY_FONT_PATH)

        image_bytes, freq_dict, word_count, most_common = (
            self._wordcloud_service.process(
                text,
                font_path,
                width=width,
                height=height,
                background_color=background_color,
                max_words=max_words,
            )
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"emma_wordcloud_{timestamp}_{width}x{height}.png"
        saved_file = self._image_storage.save("emma", filename, image_bytes)

        image_base64 = base64.b64encode(image_bytes).decode()

        return {
            "status": "success",
            "word_count": word_count,
            "most_common": list(freq_dict.items())[:10],
            "image_base64": image_base64,
            "saved_file": saved_file,
            "config": {
                "width": width,
                "height": height,
                "background_color": background_color,
                "max_words": max_words,
            },
            "text_info": {
                "filename": "austen-emma.txt",
                "total_length": len(full_text),
                "sample_length": len(text),
            },
        }
