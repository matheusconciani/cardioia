from __future__ import annotations

from typing import Any

from ollama import Client

from src.agents.protocol_agent import ProtocolSpecialistAgent
from src.agents.risk_agent import RiskAnalystAgent
from src.agents.tools import validate_patient_input
from src.config import OLLAMA_HOST, OLLAMA_MODEL


class OrchestratorAgent:
    name = "Agente Orquestrador"

    def __init__(self) -> None:
        self.risk_agent = RiskAnalystAgent()
        self.protocol_agent = ProtocolSpecialistAgent()
        self.client = Client(host=OLLAMA_HOST)
        self.history: list[dict[str, Any]] = []

    def _validate_output(self, output: dict[str, Any]) -> None:
        required_fields = ["probabilidade_pico_risco", "classe_risco", "protocolos", "mensagem_final"]
        missing = [field for field in required_fields if field not in output]
        if missing:
            raise ValueError(f"Resposta final invalida. Campos ausentes: {missing}")
        if not isinstance(output["protocolos"].get("acoes"), list) or not output["protocolos"]["acoes"]:
            raise ValueError("Resposta final invalida. 'protocolos.acoes' deve ser lista nao vazia.")

    def _generate_final_message_with_local_llm(
        self, patient_data: dict[str, Any], risk_result: dict[str, Any], protocol_result: dict[str, Any]
    ) -> str:
        prompt = (
            "Voce eh um assistente clinico academico. "
            "Responda em portugues do Brasil com 2 frases curtas. "
            "Nao use linguagem alarmista e inclua aviso de prototipo educacional. "
            f"Dados do paciente: {patient_data}. "
            f"Analise de risco: {risk_result}. "
            f"Protocolos sugeridos: {protocol_result['protocolos']}."
        )

        response = self.client.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2},
        )
        content = response["message"]["content"].strip()
        if not content:
            raise ValueError("LLM local retornou mensagem vazia.")
        return content

    def _record_handoff(self, from_agent: str, to_agent: str, payload: dict[str, Any]) -> None:
        self.history.append(
            {
                "event": "handoff",
                "from": from_agent,
                "to": to_agent,
                "payload": payload,
            }
        )

    def run(self, patient_data: dict[str, Any]) -> dict[str, Any]:
        validate_patient_input(patient_data)
        self.history.append({"event": "input_received", "patient_data": patient_data})

        self._record_handoff(
            from_agent=self.name,
            to_agent=self.risk_agent.name,
            payload={"patient_fields": sorted(patient_data.keys())},
        )
        risk_result = self.risk_agent.run(patient_data)
        self.history.append({"event": "risk_result", "result": risk_result})

        self._record_handoff(
            from_agent=self.name,
            to_agent=self.protocol_agent.name,
            payload={"classe_risco": risk_result["classe_risco"]},
        )
        protocol_result = self.protocol_agent.run(risk_result["classe_risco"])
        self.history.append({"event": "protocol_result", "result": protocol_result})

        self.history.append(
            {
                "event": "llm_call",
                "provider": "ollama",
                "model": OLLAMA_MODEL,
            }
        )
        final_message = self._generate_final_message_with_local_llm(
            patient_data=patient_data, risk_result=risk_result, protocol_result=protocol_result
        )
        self.history.append({"event": "llm_response", "message_preview": final_message[:180]})

        output = {
            "orquestrador": self.name,
            "probabilidade_pico_risco": risk_result["probabilidade_pico_risco"],
            "classe_risco": risk_result["classe_risco"],
            "protocolos": protocol_result["protocolos"],
            "mensagem_final": final_message,
            "historico": self.history,
        }
        self._validate_output(output)
        return output

