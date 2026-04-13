import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str) -> Any:
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


SYMPTOM_SYNONYMS = load_json("symptom_synonyms.json")
SPECIALIST_MAPPING = load_json("specialist_mapping.json")
EMERGENCY_RULES = [set(rule) for rule in load_json("emergency_rules.json")]
URGENT_RULES = [set(rule) for rule in load_json("urgent_rules.json")]

_raw_condition_rules = load_json("condition_rules.json")
if not isinstance(_raw_condition_rules, dict):
    raise ValueError("condition_rules.json must contain a JSON object.")

CONDITION_RULES = {
    key: set(value)
    for key, value in _raw_condition_rules.items()
}

CANONICAL_SYMPTOMS = sorted(
    set(SPECIALIST_MAPPING.keys()) | set(SYMPTOM_SYNONYMS.values())
)