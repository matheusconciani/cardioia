from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd

from src.config import RAW_DATA_PATH, PROCESSED_DATA_PATH

TARGET_COLUMN = "pico_risco"
FEATURE_COLUMNS = [
    "idade",
    "pressao_sistolica",
    "frequencia_cardiaca",
    "colesterol_total",
    "saturacao_o2",
    "historico_familiar",
    "tabagista",
]


@dataclass(frozen=True)
class DatasetBundle:
    dataframe: pd.DataFrame
    X: pd.DataFrame
    y: pd.Series


def _clip(arr: np.ndarray, min_value: float, max_value: float) -> np.ndarray:
    return np.clip(arr, min_value, max_value)


def generate_synthetic_dataset(n_samples: int = 1200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    idade = _clip(rng.normal(56, 14, n_samples).round(), 25, 90)
    pressao_sistolica = _clip(rng.normal(132, 22, n_samples).round(), 90, 220)
    frequencia_cardiaca = _clip(rng.normal(82, 15, n_samples).round(), 45, 180)
    colesterol_total = _clip(rng.normal(205, 42, n_samples).round(), 110, 380)
    saturacao_o2 = _clip(rng.normal(96, 2.4, n_samples).round(), 82, 100)
    historico_familiar = rng.integers(0, 2, n_samples)
    tabagista = rng.integers(0, 2, n_samples)

    risk_signal = (
        0.020 * (idade - 45)
        + 0.022 * (pressao_sistolica - 120)
        + 0.020 * (frequencia_cardiaca - 75)
        + 0.010 * (colesterol_total - 180)
        - 0.085 * (saturacao_o2 - 95)
        + 0.55 * historico_familiar
        + 0.40 * tabagista
        + rng.normal(0, 0.7, n_samples)
    )
    probs = 1 / (1 + np.exp(-0.075 * risk_signal))
    pico_risco = (probs >= 0.5).astype(int)

    return pd.DataFrame(
        {
            "idade": idade.astype(int),
            "pressao_sistolica": pressao_sistolica.astype(int),
            "frequencia_cardiaca": frequencia_cardiaca.astype(int),
            "colesterol_total": colesterol_total.astype(int),
            "saturacao_o2": saturacao_o2.astype(int),
            "historico_familiar": historico_familiar.astype(int),
            "tabagista": tabagista.astype(int),
            TARGET_COLUMN: pico_risco.astype(int),
        }
    )


def load_or_create_dataset() -> DatasetBundle:
    if RAW_DATA_PATH.exists():
        df = pd.read_csv(RAW_DATA_PATH)
    else:
        df = generate_synthetic_dataset()
        RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(RAW_DATA_PATH, index=False)

    missing = [c for c in FEATURE_COLUMNS + [TARGET_COLUMN] if c not in df.columns]
    if missing:
        raise ValueError(f"Base sem colunas obrigatorias: {missing}")

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    return DatasetBundle(dataframe=df, X=df[FEATURE_COLUMNS].copy(), y=df[TARGET_COLUMN].copy())

