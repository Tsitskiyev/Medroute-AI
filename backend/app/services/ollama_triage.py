import json
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from ..models import LlmTriageResult

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")

print("OLLAMA_BASE_URL =", OLLAMA_BASE_URL)
print("OLLAMA_MODEL =", OLLAMA_MODEL)

def build_prompt(user_text: str) -> str:
    return f"""
You are a cautious medical triage assistant for educational decision support.

Tasks:
1. Extract symptoms from the user's message.
2. Infer a preliminary non-diagnostic list of possible conditions.
3. Recommend the most relevant specialist.
4. Estimate urgency level:
   - Normal
   - Urgent
   - Emergency
5. Explain urgency and specialist choice.
6. Return valid JSON only.

Rules:
- This is NOT a diagnosis.
- Be conservative with dangerous symptoms.
- If the user describes gangrene, necrosis, black tissue, spreading infection,
  severe chest pain, severe shortness of breath, stroke signs, sepsis-like signs,
  or loss of consciousness, prefer Emergency.
- recommended_specialist must be one specialist title only.
- possible_conditions must be phrased as preliminary possibilities.

Return JSON in this exact shape:
{{
  "detected_symptoms": ["..."],
  "possible_conditions": ["..."],
  "recommended_specialist": "...",
  "specialist_reason": "...",
  "urgency_level": "Normal",
  "urgency_reason": "...",
  "unmatched_fragments": [],
  "confidence_note": "..."
}}

User text:
{user_text}
""".strip()


def _extract_text_from_response(data: dict[str, Any]) -> str:
    if "response" in data and isinstance(data["response"], str):
        return data["response"].strip()

    message = data.get("message")
    if isinstance(message, dict):
        content = message.get("content")
        if isinstance(content, str):
            return content.strip()

    raise RuntimeError("Ollama response did not contain text output.")


def run_ollama_triage(user_text: str) -> LlmTriageResult:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": build_prompt(user_text),
        "stream": False,
        "format": "json",
    }

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    raw_data = response.json()
    text = _extract_text_from_response(raw_data)
    parsed = json.loads(text)

    return LlmTriageResult(**parsed)

