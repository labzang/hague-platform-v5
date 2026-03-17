"""
서울 범죄 유스케이스 (포트만 의존, 비즈니스 오케스트레이션)
"""
from domain.ports import (
    ISeoulDataPort,
    ISeoulPreprocessorPort,
    IGeocodePort,
)
from domain.value_objects import SeoulPreprocessResult


def _extract_gu(formatted_address: str) -> str:
    """주소 문자열에서 '구'로 끝나는 자치구명 추출 (순수 로직)."""
    if not formatted_address:
        return ""
    tokens = formatted_address.split()
    for t in tokens:
        if len(t) > 0 and t[-1] == "구":
            return t
    return ""


class PreprocessSeoulCrimeUseCase:
    def __init__(
        self,
        data_port: ISeoulDataPort,
        preprocessor_port: ISeoulPreprocessorPort,
        geocode_port: IGeocodePort,
    ):
        self._data = data_port
        self._preprocessor = preprocessor_port
        self._geocode = geocode_port

    def execute(self) -> SeoulPreprocessResult:
        # 로드
        cctv = self._data.load_cctv()
        crime = self._data.load_crime()
        pop = self._data.load_pop()

        # 전처리: 컬럼 정리
        cctv = self._preprocessor.drop_cctv_columns(
            cctv, ["2013년도 이전", "2014년", "2015년", "2016년"]
        )
        pop = self._preprocessor.filter_pop_columns_and_rows(pop)

        # cctv-pop 머지
        cctv_pop = self._preprocessor.df_merge(
            cctv, pop, left_on="기관명", right_on="자치구", how="inner"
        )
        cctv_pop = self._preprocessor.drop_columns(cctv_pop, ["기관명"])

        # 경찰서명으로 지오코딩 → 자치구 추출
        station_names = self._preprocessor.get_station_names_from_crime(crime)
        gu_list = []
        for name in station_names:
            results = self._geocode.geocode(name, language="ko")
            if results and len(results) > 0:
                addr = results[0].get("formatted_address", "")
                gu_list.append(_extract_gu(addr))
            else:
                gu_list.append("")

        # crime에 자치구 추가
        crime = self._preprocessor.add_gu_to_crime(crime, gu_list)

        # 저장용 컬럼 순서
        desired_cols = [
            "관서명", "살인 발생", "살인 검거",
            "강도 발생", "강도 검거", "강간 발생", "강간 검거",
            "절도 발생", "절도 검거", "폭력 발생", "폭력 검거",
            "자치구",
        ]
        crime = self._preprocessor.order_crime_columns(crime, desired_cols)
        saved_path = self._data.save_crime(crime)

        # 응답용 미리보기 (포트 통해 변환)
        return SeoulPreprocessResult(
            status="success",
            cctv_rows=len(cctv),
            cctv_columns=list(cctv.columns) if hasattr(cctv, "columns") else [],
            crime_rows=len(crime),
            crime_columns=list(crime.columns) if hasattr(crime, "columns") else [],
            pop_rows=len(pop),
            pop_columns=list(pop.columns) if hasattr(pop, "columns") else [],
            cctv_pop_rows=len(cctv_pop),
            cctv_pop_columns=list(cctv_pop.columns) if hasattr(cctv_pop, "columns") else [],
            cctv_preview=self._preprocessor.head_to_dict(cctv, 3),
            crime_preview=self._preprocessor.head_to_dict(crime, 3),
            pop_preview=self._preprocessor.head_to_dict(pop, 3),
            cctv_pop_preview=self._preprocessor.head_to_dict(cctv_pop, 3),
            message="데이터 전처리 및 머지가 완료되었습니다",
        )
