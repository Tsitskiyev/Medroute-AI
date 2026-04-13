import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from ..models import LlmTriageResult

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3-32b")

print("GROQ_MODEL =", GROQ_MODEL)
print("GROQ_API_KEY exists =", bool(GROQ_API_KEY))


def build_prompt(user_text: str) -> str:
    return f"""
You are a cautious medical triage assistant for educational decision support.

Return ONLY valid JSON with exactly these fields:
- detected_symptoms: string[]
- possible_conditions: string[]
- recommended_specialist: string
- specialist_reason: string
- urgency_level: "Normal" | "Urgent" | "Emergency"
- urgency_reason: string
- unmatched_fragments: string[]
- confidence_note: string

Rules:
- This is NOT a diagnosis.
- Be conservative with dangerous symptoms.
- If the user describes chest pain, severe shortness of breath, stroke signs,
  sepsis-like signs, loss of consciousness, black tissue, gangrene, or necrosis,
  prefer Emergency.
- If a numeric symptom is ambiguous but potentially dangerous, do NOT mark Normal.
- recommended_specialist must be one specialist title only.
- possible_conditions must be phrased as preliminary possibilities.
- Return JSON only. No markdown. No code fences.

User text:
{user_text}
""".strip()


def _extract_json_text(raw_text: str) -> str:
    text = raw_text.strip()

    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise RuntimeError(f"Groq did not return valid JSON. Raw response: {raw_text}")

    return text[start:end + 1]


def run_groq_triage(user_text: str) -> LlmTriageResult:
    print("Entered run_groq_triage")

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set.")

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a strict JSON-only medical triage formatter."
            },
            {
                "role": "user",
                "content": build_prompt(user_text)
            },
        ],
    )

    message = response.choices[0].message.content
    if not message:
        raise RuntimeError("Groq returned empty content.")

    print("GROQ RAW RESPONSE:", message)

    json_text = _extract_json_text(message)

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to decode Groq JSON: {exc}; raw={message}") from exc

    return LlmTriageResult.model_validate(parsed)