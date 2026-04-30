from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.agents.orchestrator_agent import OrchestratorAgent


DEFAULT_PATIENT = {
    "idade": 67,
    "pressao_sistolica": 168,
    "frequencia_cardiaca": 112,
    "colesterol_total": 265,
    "saturacao_o2": 93,
    "historico_familiar": 1,
    "tabagista": 1,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demo do sistema CardioIA multiagente com IA local.")
    parser.add_argument(
        "--patient-json",
        type=str,
        default="",
        help='JSON com dados do paciente. Ex.: \'{"idade":60,"pressao_sistolica":150,...}\'',
    )
    parser.add_argument(
        "--save-output",
        type=str,
        default="",
        help="Caminho para salvar a saida JSON (ex.: docs/exemplo_execucao.json).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    patient_data = json.loads(args.patient_json) if args.patient_json else DEFAULT_PATIENT

    orchestrator = OrchestratorAgent()
    result = orchestrator.run(patient_data)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.save_output:
        output_path = Path(args.save_output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()

