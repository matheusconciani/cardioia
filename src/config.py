from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "base_sintetica_original.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "base_treinamento.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "modelo_pico_risco.joblib"
PROTOCOLS_PATH = PROJECT_ROOT / "data" / "protocolos" / "protocolos_risco.json"

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:e2b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

