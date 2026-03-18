"""
타이타닉 도메인 값 객체 (순수: 외부 라이브러리 미참조)
- train/test는 Adapter가 채워 넣음. 타입은 Any로만 참조.
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TitanicDataSet:
    """전처리된 학습/테스트 데이터 담기 (구체 타입은 Adapter가 결정)."""
    train: Any = None
    test: Any = None
    fname: str = ""
    dname: str = ""
    sname: str = ""
    id: str = ""
    label: str = "Survived"


@dataclass
class PreprocessResult:
    """전처리 결과."""
    status: str
    rows: int
    columns: List[str]
    column_count: int
    null_count: int
    sample_data: List[Dict[str, Any]]
    dtypes: Dict[str, str]


@dataclass
class EvaluationResult:
    """모델 평가 결과."""
    best_model: Optional[str]
    results: Dict[str, Dict[str, Any]]
