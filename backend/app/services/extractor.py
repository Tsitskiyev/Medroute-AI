import re
from typing import List, Optional

from app.services.knowledge_base import CANONICAL_SYMPTOMS, SYMPTOM_SYNONYMS
from app.services.normalization import normalize_symptoms


WORD_SPLIT_PATTERN = re.compile(r"[,\n;]+")
NON_LETTER_PATTERN = re.compile(r"[^\w\s\-]", flags=re.UNICODE)


def clean_text(text: str) -> str:
    text = text.strip().lower()
    text = NON_LETTER_PATTERN.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_from_symptom_list(symptoms: Optional[List[str]]) -> List[str]:
    if not symptoms:
        return []
    return normalize_symptoms(symptoms)


def extract_from_text(text: Optional[str]) -> tuple[List[str], List[str]]:
    if not text or not text.strip():
        return [], []

    cleaned = clean_text(text)
    detected: List[str] = []

    # 1. Поиск по ключам словаря синонимов
    for raw_phrase, canonical in SYMPTOM_SYNONYMS.items():
        phrase = raw_phrase.lower().strip()
        if phrase and phrase in cleaned:
            detected.append(canonical)

    # 2. Поиск канонических симптомов напрямую
    for canonical in CANONICAL_SYMPTOMS:
        phrase = canonical.lower().strip()
        if phrase and phrase in cleaned:
            detected.append(canonical)

    detected = list(dict.fromkeys(detected))

    # 3. Попытка выделить нераспознанные фрагменты
    fragments = [
        clean_text(part)
        for part in WORD_SPLIT_PATTERN.split(text)
        if clean_text(part)
    ]

    normalized_detected = set(detected)
    unmatched_fragments: List[str] = []

    for fragment in fragments:
        matched = False

        for raw_phrase in SYMPTOM_SYNONYMS.keys():
            if raw_phrase in fragment:
                matched = True
                break

        if not matched:
            for canonical in CANONICAL_SYMPTOMS:
                if canonical in fragment:
                    matched = True
                    break

        if not matched:
            unmatched_fragments.append(fragment)

    unmatched_fragments = list(dict.fromkeys(unmatched_fragments))
    return detected, unmatched_fragments


def extract_symptoms(
    text: Optional[str],
    symptoms: Optional[List[str]]
) -> tuple[List[str], List[str]]:
    list_symptoms = extract_from_symptom_list(symptoms)
    text_symptoms, unmatched_fragments = extract_from_text(text)

    combined = list(dict.fromkeys(list_symptoms + text_symptoms))
    combined = normalize_symptoms(combined)

    return combined, unmatched_fragments