"""
타이타닉 유스케이스/어댑터용 DTO — TitanicTrain ORM 컬럼 기준.
- 행 단위: TitanicRowDto (ORM/API 전달용)
- 데이터셋·전처리·평가: TitanicDatasetDto, PreprocessResult, EvaluationResult
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TitanicRowDto:
    """타이타닉 한 행 전달용 DTO. ORM TitanicTrain 컬럼과 1:1 대응 (원시 타입)."""

    passenger_id: int
    survived: Optional[int] = None  # 0=사망, 1=생존
    pclass: Optional[int] = None  # 1, 2, 3
    name: Optional[str] = None
    gender: Optional[str] = None  # "male" | "female"
    age: Optional[float] = None
    sib_sp: Optional[int] = None
    parch: Optional[int] = None
    ticket: Optional[str] = None
    fare: Optional[float] = None
    cabin: Optional[str] = None
    embarked: Optional[str] = None  # "C" | "Q" | "S"


@dataclass
class TitanicDatasetDto:
    """전처리된 train/test 담기 + 메타(경로·레이블 컬럼). 어댑터/포트 간 전달용."""

    train: Any = None
    test: Any = None
    fname: str = ""
    dname: str = ""
    sname: str = ""
    id: str = ""
    label: str = "Survived"


@dataclass
class PreprocessResult:
    """전처리 결과 (유스케이스 반환용)."""

    status: str
    rows: int
    columns: List[str]
    column_count: int
    null_count: int
    sample_data: List[Dict[str, Any]]
    dtypes: Dict[str, str]


@dataclass
class EvaluationResult:
    """모델 평가 결과 (유스케이스 반환용)."""

    best_model: Optional[str]
    results: Dict[str, Dict[str, Any]]
