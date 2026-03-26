"""
타이타닉 수치 특성(Pclass, Embarked, Title, Gender, AgeGroup, FareBand) 기준
사이킷런 분류기 교차검증 비교 → 최고 정확도 모델으로 전체 학습 후 제출용 예측.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from icecream import ic
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# `TitanicPreprocessService` 산출 프레임과 동일한 학습용 특성 열
ML_FEATURE_COLUMNS: tuple[str, ...] = (
    "Pclass",
    "Embarked",
    "Title",
    "Gender",
    "AgeGroup",
    "FareBand",
)


class TitanicDataLearningService:
    """
    전처리된 train/test 피처(DataFrame 또는 행렬)를 받아
    결정트리·랜덤포레스트·나이브베이즈·KNN·SVM 검증 정확도를 비교하고,
    가장 높은 모델로 전체 학습 데이터를 학습한다.
    """

    def __init__(
        self,
        train_features: pd.DataFrame | np.ndarray,
        y_train: np.ndarray | pd.Series | None = None,
        test_features: pd.DataFrame | np.ndarray | None = None,
        *,
        random_state: int = 42,
        n_splits: int = 5,
    ) -> None:
        self.random_state = random_state
        self.n_splits = n_splits

        self._train_passenger_ids: np.ndarray | None = None
        self._test_passenger_ids: np.ndarray | None = None

        if isinstance(train_features, pd.DataFrame):
            if "PassengerId" in train_features.columns:
                self._train_passenger_ids = train_features["PassengerId"].to_numpy()
            if y_train is None:
                if "Survived" not in train_features.columns:
                    raise ValueError("train_features에 Survived가 없으면 y_train을 넘겨야 합니다.")
                y_train = train_features["Survived"]
                x_df = train_features.drop(columns=["Survived"], errors="ignore")
            else:
                x_df = train_features
            self.X_train = self._dataframe_to_X(x_df)
        else:
            if y_train is None:
                raise ValueError("행렬만 넘길 때는 y_train이 필요합니다.")
            self.X_train = np.asarray(train_features, dtype=np.float64)

        self.y_train = (
            np.asarray(y_train, dtype=np.int64).ravel()
            if y_train is not None
            else np.array([], dtype=np.int64)
        )

        self.X_test: np.ndarray | None = None
        if test_features is not None:
            if isinstance(test_features, pd.DataFrame):
                if "PassengerId" in test_features.columns:
                    self._test_passenger_ids = test_features["PassengerId"].to_numpy()
                self.X_test = self._dataframe_to_X(test_features)
            else:
                self.X_test = np.asarray(test_features, dtype=np.float64)

        self.model: Any = None
        self.best_model_name: str | None = None
        self.cv_mean_accuracy: dict[str, float] = {}
        self.submission_predictions: np.ndarray | None = None

    @staticmethod
    def _dataframe_to_X(df: pd.DataFrame) -> np.ndarray:
        cols = [c for c in ML_FEATURE_COLUMNS if c in df.columns]
        if len(cols) != len(ML_FEATURE_COLUMNS):
            missing = set(ML_FEATURE_COLUMNS) - set(cols)
            raise ValueError(f"학습용 특성 컬럼이 부족합니다: {sorted(missing)}")
        return df.loc[:, list(ML_FEATURE_COLUMNS)].to_numpy(dtype=np.float64)

    def _build_candidates(self, n_samples: int) -> dict[str, Any]:
        """KNN·SVM은 스케일에 민감해 Pipeline으로 묶는다."""
        knn_k = max(1, min(7, n_samples))
        return {
            "결정트리": DecisionTreeClassifier(
                random_state=self.random_state,
                max_depth=8,
            ),
            "랜덤포레스트": RandomForestClassifier(
                random_state=self.random_state,
                n_estimators=200,
                max_depth=10,
            ),
            "나이브베이즈": GaussianNB(),
            "KNN": Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "knn",
                        KNeighborsClassifier(
                            n_neighbors=knn_k,
                            weights="distance",
                        ),
                    ),
                ]
            ),
            "SVM": Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "svc",
                        SVC(
                            kernel="rbf",
                            random_state=self.random_state,
                            probability=False,
                        ),
                    ),
                ]
            ),
        }

    def _stratified_kfold_or_none(self, y: np.ndarray) -> StratifiedKFold | None:
        """계층 K-fold: 클래스당 최소 개수·표본 수에 맞춰 split 수를 줄인다."""
        y_int = y.astype(np.int64, copy=False)
        if y_int.size < 2:
            return None
        counts = np.bincount(y_int)
        if counts.size == 0:
            return None
        min_class = int(counts.min())
        max_splits = min(self.n_splits, min_class, len(y_int) // 2)
        if max_splits < 2:
            return None
        return StratifiedKFold(
            n_splits=max_splits,
            shuffle=True,
            random_state=self.random_state,
        )

    def learning(self) -> None:
        ic("학습 시작")
        if self.X_train.size == 0 or self.y_train.size == 0:
            raise ValueError("X_train, y_train이 비어 있습니다.")

        X = self.X_train
        y = self.y_train
        candidates = self._build_candidates(len(y))
        self.cv_mean_accuracy.clear()
        skf = self._stratified_kfold_or_none(y)
        if skf is None:
            ic("표본이 적어 Stratified K-fold 대신 훈련셋 적합도(참고용)로 점수를 냅니다.")

        def _eval_one(est: Any) -> float:
            if skf is not None:
                scores = cross_val_score(est, X, y, cv=skf, scoring="accuracy")
                return float(scores.mean())
            fitted = clone(est)
            fitted.fit(X, y)
            return float(accuracy_score(y, fitted.predict(X)))

        self.cv_mean_accuracy["결정트리"] = _eval_one(candidates["결정트리"])
        ic(f"결정트리를 활용한 검증 정확도: {self.cv_mean_accuracy['결정트리']:.4f}")

        self.cv_mean_accuracy["랜덤포레스트"] = _eval_one(candidates["랜덤포레스트"])
        ic(f"랜덤포레스트를 활용한 검증 정확도: {self.cv_mean_accuracy['랜덤포레스트']:.4f}")

        self.cv_mean_accuracy["나이브베이즈"] = _eval_one(candidates["나이브베이즈"])
        ic(f"나이브베이즈를 활용한 검증 정확도: {self.cv_mean_accuracy['나이브베이즈']:.4f}")

        self.cv_mean_accuracy["KNN"] = _eval_one(candidates["KNN"])
        ic(f"KNN를 활용한 검증 정확도: {self.cv_mean_accuracy['KNN']:.4f}")

        self.cv_mean_accuracy["SVM"] = _eval_one(candidates["SVM"])
        ic(f"SVM를 활용한 검증 정확도: {self.cv_mean_accuracy['SVM']:.4f}")

        best_name = max(self.cv_mean_accuracy, key=lambda k: self.cv_mean_accuracy[k])
        self.best_model_name = best_name
        ic(f"검증 정확도 최고 모델: {best_name} ({self.cv_mean_accuracy[best_name]:.4f}) — 전체 학습 데이터로 재학습")

        self.model = clone(candidates[best_name])
        self.model.fit(X, y)

        this = self.model
        ic(f"제출용 추정기 준비 완료: {type(this).__name__}")

        if self.X_test is not None and self.X_test.shape[0] > 0:
            self.submission_predictions = self.model.predict(self.X_test).astype(np.int64)
            ic(f"테스트 예측 행 수: {len(self.submission_predictions)}")

    def submission_dataframe(self) -> pd.DataFrame:
        """캐글 제출 형식: PassengerId, Survived (learning() 이후 호출)."""
        if self.submission_predictions is None:
            raise RuntimeError("learning()을 먼저 호출하고, test_features가 있어야 합니다.")
        if self._test_passenger_ids is None:
            raise RuntimeError("test_features에 PassengerId 컬럼이 필요합니다.")
        return pd.DataFrame(
            {
                "PassengerId": self._test_passenger_ids,
                "Survived": self.submission_predictions,
            }
        )
