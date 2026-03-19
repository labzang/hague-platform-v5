"""
타이타닉 아웃바운드 repo (한 파일에 통합)
- TitanicDataPort, PreprocessorPort, ModelRunnerPort 구현
"""

# pyright: reportMissingImports=false, reportMissingModuleSource=false
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold, cross_val_score

try:
    from labzang.apps.ml.application.dtos import TitanicDatasetDto
    from labzang.apps.ml.application.ports import (
        TitanicDataPort,
        PreprocessorPort,
        ModelRunnerPort,
    )
except ImportError:
    from abc import ABC, abstractmethod
    from dataclasses import dataclass
    from typing import Any, Dict

    @dataclass
    class TitanicDatasetDto:
        train: Any = None
        test: Any = None

    class _TitanicDataPortStub(ABC):
        @abstractmethod
        def load_train(self) -> Any: ...

        @abstractmethod
        def load_test(self) -> Any: ...

        @abstractmethod
        def save_submission(self, passenger_ids: Any, predictions: Any) -> str: ...

    class _PreprocessorPortStub(ABC):
        @abstractmethod
        def preprocess(self, train_df: Any, test_df: Any) -> Any: ...

    class _ModelRunnerPortStub(ABC):
        @abstractmethod
        def evaluate(self, train_data: Any, target_column: str) -> Dict[str, Any]: ...

        @abstractmethod
        def predict_for_submit(
            self, train_data: Any, test_data: Any, target_column: str
        ) -> Any: ...

    TitanicDataPort = _TitanicDataPortStub  # type: ignore[misc, assignment]
    PreprocessorPort = _PreprocessorPortStub  # type: ignore[misc, assignment]
    ModelRunnerPort = _ModelRunnerPortStub  # type: ignore[misc, assignment]


# --- TitanicDataPort 구현 ---
class CsvTitanicDataAdapter(TitanicDataPort):
    def __init__(self, resources_dir: Path):
        self._dir = Path(resources_dir)
        self._train_path = self._dir / "train.csv"
        self._test_path = self._dir / "test.csv"

    def load_train(self) -> Any:
        if not self._train_path.exists():
            raise FileNotFoundError(f"Train CSV 없음: {self._train_path}")
        return pd.read_csv(self._train_path)

    def load_test(self) -> Any:
        if not self._test_path.exists():
            raise FileNotFoundError(f"Test CSV 없음: {self._test_path}")
        return pd.read_csv(self._test_path)

    def save_submission(self, passenger_ids: Any, predictions: Any) -> str:
        out = self._dir / "submission.csv"
        pd.DataFrame(
            {"PassengerId": passenger_ids, "Survived": predictions.astype(int)}
        ).to_csv(out, index=False)
        return str(out)


# --- PreprocessorPort 구현 ---
class TitanicPreprocessorAdapter(PreprocessorPort):
    def preprocess(self, train_df: Any, test_df: Any) -> TitanicDatasetDto:
        train, test = train_df.copy(), test_df.copy()
        for col in ["SibSp", "Parch", "Cabin", "Ticket"]:
            train.drop(columns=[col], inplace=True, errors="ignore")
            test.drop(columns=[col], inplace=True, errors="ignore")
        for df in (train, test):
            df["Gender"] = df["Sex"].map({"male": 0, "female": 1})
            df.drop(columns=["Sex"], inplace=True)
            df["Embarked"] = df["Embarked"].fillna("S").map({"S": 1, "C": 2, "Q": 3})
            df["Fare"] = pd.qcut(
                df["Fare"].fillna(df["Fare"].median()), 4, labels=[1, 2, 3, 4]
            ).astype(float)
            df["Fare"] = df["Fare"].fillna(1)
            df["Age"] = df["Age"].fillna(-0.5)
            bins, labels = (
                [-1, 0, 5, 12, 18, 24, 35, 60, np.inf],
                [0, 1, 2, 3, 4, 5, 6, 7],
            )
            df["Age"] = (
                pd.cut(df["Age"], bins=bins, labels=labels).astype(float).fillna(0)
            )
            if "Name" in df.columns:
                df["Title"] = df["Name"].str.extract(r"([A-Za-z]+)\.", expand=False)
                df["Title"] = df["Title"].replace(["Countess", "Lady", "Sir"], "Royal")
                df["Title"] = df["Title"].replace(
                    [
                        "Capt",
                        "Col",
                        "Don",
                        "Dr",
                        "Major",
                        "Rev",
                        "Jonkheer",
                        "Dona",
                        "Mme",
                    ],
                    "Rare",
                )
                df["Title"] = df["Title"].replace("Mlle", "Mr").replace("Miss", "Ms")
                df["Title"] = (
                    df["Title"]
                    .map(
                        {"Mr": 1, "Ms": 2, "Mrs": 3, "Master": 4, "Royal": 5, "Rare": 6}
                    )
                    .fillna(0)
                    .astype(int)
                )
                df.drop(columns=["Name"], inplace=True)
            for c in list(df.columns):
                if (
                    df[c].dtype == "object"
                    or getattr(df[c].dtype, "name", "") == "category"
                ):
                    df.drop(columns=[c], inplace=True, errors="ignore")
        return TitanicDatasetDto(train=train, test=test)


# --- ModelRunnerPort 구현 ---
class SklearnTitanicModelAdapter(ModelRunnerPort):
    def _xy(self, train_data: Any, target_column: str):
        if target_column not in train_data.columns:
            raise ValueError(f"타깃 컬럼 없음: {target_column}")
        X = train_data.drop(columns=[target_column]).select_dtypes(include=[np.number])
        return X.values, train_data[target_column].values

    def evaluate(self, train_data: Any, target_column: str) -> Dict[str, Any]:
        X, y = self._xy(train_data, target_column)
        kf = KFold(n_splits=10, shuffle=True, random_state=0)
        models = {
            "knn": KNeighborsClassifier(n_neighbors=13),
            "decision_tree": DecisionTreeClassifier(),
            "random_forest": RandomForestClassifier(n_estimators=13),
            "naive_bayes": GaussianNB(),
            "svm": SVC(),
        }
        results = {}
        for name, clf in models.items():
            try:
                acc = round(
                    float(
                        np.mean(
                            cross_val_score(
                                clf, X, y, cv=kf, n_jobs=1, scoring="accuracy"
                            )
                        )
                    )
                    * 100,
                    2,
                )
                results[name] = {"accuracy": acc, "status": "success"}
            except Exception as e:
                results[name] = {"accuracy": None, "status": str(e)}
        best, best_acc = None, -1.0
        for name, r in results.items():
            a = r.get("accuracy")
            if a is not None and a > best_acc:
                best_acc, best = a, name
        return {"best_model": best, "results": results}

    def predict_for_submit(
        self, train_data: Any, test_data: Any, target_column: str
    ) -> Any:
        X_train = train_data.drop(columns=[target_column]).select_dtypes(
            include=[np.number]
        )
        y_train = train_data[target_column]
        X_test = test_data.select_dtypes(include=[np.number])
        model = SVC(random_state=42, probability=True)
        model.fit(X_train, y_train)
        return model.predict(X_test)
