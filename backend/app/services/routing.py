from typing import Set, Tuple

from app.services.knowledge_base import SPECIALIST_MAPPING


def choose_specialist(symptoms: Set[str]) -> Tuple[str, str]:
    scores: dict[str, int] = {}
    matched_by_specialist: dict[str, list[str]] = {}

    for symptom in symptoms:
        specialist = SPECIALIST_MAPPING.get(symptom)
        if specialist:
            scores[specialist] = scores.get(specialist, 0) + 1
            matched_by_specialist.setdefault(specialist, []).append(symptom)

    if not scores:
        return "Therapist", "No specialist-specific symptom match was found, so default routing was used."

    best_specialist = max(scores.items(), key=lambda item: item[1])[0]
    matched_symptoms = ", ".join(sorted(matched_by_specialist[best_specialist]))

    reason = (
        f"{best_specialist} was selected because these symptoms matched its routing rules: "
        f"{matched_symptoms}."
    )
    return best_specialist, reason