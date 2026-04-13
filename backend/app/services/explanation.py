from typing import List, Optional

from app.models import UrgencyLevel


def build_explanation(
    input_text: Optional[str],
    symptoms: List[str],
    unmatched_fragments: List[str],
    urgency: UrgencyLevel,
    urgency_reason: str,
    specialist_reason: str,
    conditions: List[str],
    confidence_note: str
) -> str:
    parts = [
        f"Detected symptoms: {', '.join(symptoms) if symptoms else 'none'}.",
        f"Urgency level: {urgency.value}.",
        urgency_reason,
        specialist_reason,
        f"Preliminary possible conditions: {', '.join(conditions) if conditions else 'none'}.",
        f"Confidence note: {confidence_note}",
    ]

    if unmatched_fragments:
        parts.append(
            "Unmatched fragments: " + ", ".join(unmatched_fragments) + "."
        )

    if input_text:
        parts.append("This output is non-diagnostic and for triage support only.")

    return " ".join(parts)