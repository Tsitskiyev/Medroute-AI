from typing import Iterable, List

from app.services.knowledge_base import SYMPTOM_SYNONYMS


def normalize_symptom(value: str) -> str:
    symptom = value.strip().lower()
    return SYMPTOM_SYNONYMS.get(symptom, symptom)


def normalize_symptoms(symptoms: Iterable[str]) -> List[str]:
    normalized = [normalize_symptom(item) for item in symptoms if item and item.strip()]
    return list(dict.fromkeys(normalized))