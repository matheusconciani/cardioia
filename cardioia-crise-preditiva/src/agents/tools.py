from __future__ import annotations

import json
from typing import Any

from src.config import PROTOCOLS_PATH
from src.predict import predict_risk

REQUIRED_PATIENT_FIELDS = [
    "idade",
    "pressao_sistolica",
    "frequencia_cardiaca",
    "colesterol_total",
    "saturacao_o2",
    "historico_familiar",
    "tabagista",
]


def validate_patient_input(patient_data: dict[str, Any]) -> None:
    if not isinstance(patient_data, dict):
        raise ValueError("Entrada invalida: dados do paciente devem ser um objeto JSON.")
    missing = [field for field in REQUIRED_PATIENT_FIELDS if field not in patient_data]
    if missing:
        raise ValueError(f"Entrada invalida: campos obrigatorios ausentes: {missing}")


def predict_risk_tool(patient_data: dict[str, Any]) -> dict[str, Any]:
    validate_patient_input(patient_data)
    prediction = predict_risk(patient_data)
    return {
        "tool": "predict_risk_tool",
        "probabilidade_pico_risco": prediction.probabilidade_pico_risco,
        "classe_risco": prediction.classe_risco,
        "predicao_binaria": prediction.predicao_binaria,
    }


def get_protocols_tool(classe_risco: str) -> dict[str, Any]:
    if not PROTOCOLS_PATH.exists():
        raise FileNotFoundError(f"Arquivo de protocolos nao encontrado: {PROTOCOLS_PATH}")
    with open(PROTOCOLS_PATH, "r", encoding="utf-8") as fp:
        protocolos = json.load(fp)
    if classe_risco not in protocolos:
        raise ValueError(f"Classe de risco invalida para protocolos: {classe_risco}")
    return {
        "tool": "get_protocols_tool",
        "classe_risco": classe_risco,
        "protocolos": protocolos[classe_risco],
    }

