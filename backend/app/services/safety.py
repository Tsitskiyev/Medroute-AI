from typing import Set

from app.models import UrgencyLevel


EMERGENCY_KEYWORDS = {
    "gangrene",
    "necrosis",
    "blackened skin",
    "black tissue",
    "loss of consciousness",
    "speech difficulty",
    "one-sided weakness",
    "chest pain",
    "shortness of breath",
    "sepsis",
    "confusion",
}


def apply_safety_override(
    detected_symptoms: Set[str],
    urgency_level: UrgencyLevel,
    urgency_reason: str
) -> tuple[UrgencyLevel, str]:
    matched = sorted(
        symptom for symptom in detected_symptoms
        if symptom.lower() in EMERGENCY_KEYWORDS
    )

    if matched and urgency_level != UrgencyLevel.EMERGENCY:
        override_reason = (
            "Safety override applied because high-risk symptoms were detected: "
            + ", ".join(matched)
            + "."
        )
        return UrgencyLevel.EMERGENCY, override_reason

    return urgency_level, urgency_reason