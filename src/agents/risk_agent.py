from __future__ import annotations

from typing import Any

from src.agents.tools import predict_risk_tool


class RiskAnalystAgent:
    name = "Agente Analista de Risco"

    def run(self, patient_data: dict[str, Any]) -> dict[str, Any]:
        prediction = predict_risk_tool(patient_data)
        return {
            "agente": self.name,
            "tool": prediction["tool"],
            "probabilidade_pico_risco": prediction["probabilidade_pico_risco"],
            "classe_risco": prediction["classe_risco"],
            "predicao_binaria": prediction["predicao_binaria"],
        }

