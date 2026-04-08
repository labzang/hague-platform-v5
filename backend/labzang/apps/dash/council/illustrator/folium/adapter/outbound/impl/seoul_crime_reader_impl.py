"""서울 범죄 Reader 구현 (쿼리/조회 책임)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from labzang.apps.dash.council.illustrator.folium.app.ports.output.seoul_crime_reader_port import (
    SeoulCrimeReaderPort,
)  # type: ignore[import-untyped]


class SeoulCrimeReaderImpl(SeoulCrimeReaderPort):
    def __init__(self, data_dir: Path):
        self._data_dir = Path(data_dir)

    def get_data_dir(self) -> str:
        return str(self._data_dir)

    def load_cctv(self) -> Any:
        path = self._data_dir / "cctv.csv"
        if not path.exists():
            raise FileNotFoundError(f"cctv.csv 없음: {path}")
        return pd.read_csv(path, encoding="utf-8")

    def load_crime(self) -> Any:
        path = self._data_dir / "crime.csv"
        if not path.exists():
            raise FileNotFoundError(f"crime.csv 없음: {path}")
        return pd.read_csv(path, encoding="utf-8")

    def load_pop(self) -> Any:
        path = self._data_dir / "pop.xls"
        if not path.exists():
            raise FileNotFoundError(f"pop.xls 없음: {path}")
        return pd.read_excel(path)
