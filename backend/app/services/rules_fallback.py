from typing import List, Optional

from ..models import TriageMode, TriageResponse
from .explanation import build_explanation
from .extractor import extract_symptoms
from .routing import choose_specialist
from .triage import detect_urgency, rank_conditions


def run_rules_fallback(
    input_text: Optional[str],
    structured_symptoms: Optional[List[str]],
    disclaimer: str,
    fallback_reason: str,
) -> TriageResponse:
    detected_symptoms, unmatched_fragments = extract_symptoms(
        text=input_text,
        symptoms=structured_symptoms,
    )

    symptom_set = set(detected_symptoms)

    urgency_level, urgency_reason = detect_urgency(symptom_set)
    possible_conditions = rank_conditions(symptom_set)
    recommended_specialist, specialist_reason = choose_specialist(symptom_set)

    confidence_note = (
        "LLM layer was unavailable, so the system used deterministic rule-based triage. "
        f"Fallback reason: {fallback_reason}"
    )

    explanation = build_explanation(
        input_text=input_text,
        symptoms=detected_symptoms,
        unmatched_fragments=unmatched_fragments,
        urgency=urgency_level,
        urgency_reason=urgency_reason,
        specialist_reason=specialist_reason,
        conditions=possible_conditions,
        confidence_note=confidence_note,
    )

    return TriageResponse(
        input_text=input_text,
        mode_used=TriageMode.RULES,
        detected_symptoms=detected_symptoms,
        unmatched_fragments=unmatched_fragments,
        possible_conditions=possible_conditions,
        recommended_specialist=recommended_specialist,
        specialist_reason=specialist_reason,
        urgency_level=urgency_level,
        urgency_reason=urgency_reason,
        confidence_note=confidence_note,
        disclaimer=disclaimer,
        explanation=explanation,
    )