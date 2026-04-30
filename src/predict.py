from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import joblib
import pandas as pd

from src.config import MODEL_PATH


@dataclass(frozen=True)
class RiskPrediction:
    probabilidade_pico_risco: float
    classe_risco: str
    predicao_binaria: int


def _class_from_probability(probability: float) -> str:
    if probability < 0.33:
        return "baixo"
    if probability < 0.66:
        return "medio"
    return "alto"


def predict_risk(patient_data: Dict[str, int | float]) -> RiskPrediction:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo nao encontrado em {MODEL_PATH}. Rode `python -m src.train_model` primeiro."
        )

    artifact = joblib.load(MODEL_PATH)
    model = artifact["model"]
    features = artifact["features"]
    missing = [f for f in features if f not in patient_data]
    if missing:
        raise ValueError(f"Paciente sem campos obrigatorios: {missing}")

    row = {f: patient_data[f] for f in features}
    X_new = pd.DataFrame([row])
    pred = int(model.predict(X_new)[0])
    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(X_new)[0][1])
    else:
        prob = float(pred)

    return RiskPrediction(
        probabilidade_pico_risco=round(prob, 4),
        classe_risco=_class_from_probability(prob),
        predicao_binaria=pred,
    )

