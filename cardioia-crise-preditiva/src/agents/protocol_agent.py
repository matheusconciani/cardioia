from __future__ import annotations

from typing import Any

from src.agents.tools import get_protocols_tool


class ProtocolSpecialistAgent:
    name = "Agente Especialista em Protocolos"

    def run(self, classe_risco: str) -> dict[str, Any]:
        protocolos = get_protocols_tool(classe_risco)
        return {
            "agente": self.name,
            "classe_risco": classe_risco,
            "tool": protocolos["tool"],
            "protocolos": protocolos["protocolos"],
        }

