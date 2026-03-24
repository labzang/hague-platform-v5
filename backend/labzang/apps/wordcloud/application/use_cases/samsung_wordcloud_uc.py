"""
삼성 워드클라우드 유스케이스 (포트만 의존).
- 텍스트 소스·이미지 저장은 포트로 추상화.
"""

from typing import Any, Dict

from labzang.apps.wordcloud.application.ports.output import (
    ImageStoragePort,
    TextSourcePort,
)
from labzang.apps.wordcloud.application.services.samsung_wordcloud_service import (
    SamsungWordcloudService,
)


# 텍스트 소스 키 (어댑터와 약속)
KEY_SAMSUNG_REPORT = "samsung_report"
KEY_STOPWORDS = "stopwords"
KEY_FONT_PATH = "font_path"


class GenerateSamsungWordcloudUC:
    """삼성 지속가능경영보고서 워드클라우드 생성 유스케이스."""

    def __init__(
        self,
        text_source: TextSourcePort,
        image_storage: ImageStoragePort,
        wordcloud_service: SamsungWordcloudService,
    ) -> None:
        self._text_source = text_source
        self._image_storage = image_storage
        self._wordcloud_service = wordcloud_service

    def execute(self) -> Dict[str, Any]:
        report_text = self._text_source.get_text(KEY_SAMSUNG_REPORT)
        stopwords_text = self._text_source.get_text(KEY_STOPWORDS)
        font_path = self._text_source.get_text(KEY_FONT_PATH)

        freq_dict, image_bytes = self._wordcloud_service.process(
            report_text,
            stopwords_text,
            font_path,
        )

        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"samsung_wordcloud_{timestamp}.png"
        file_info = self._image_storage.save("samsung", filename, image_bytes)

        # 라우터에서 .head(30).to_dict() 하던 것과 호환되도록 상위 30개만 dict 유지
        freq_txt = dict(
            list(freq_dict.items())[:500]
        )  # 빈도 데이터는 상위 500개까지 보관 가능

        return {
            "전처리 결과": "완료",
            "freq_txt": freq_txt,
            "saved_file": file_info,
        }
