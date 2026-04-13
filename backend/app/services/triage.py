from typing import List, Set, Tuple

from ..models import UrgencyLevel
from .knowledge_base import CONDITION_RULES, EMERGENCY_RULES, URGENT_RULES


def detect_urgency(symptoms: Set[str]) -> Tuple[UrgencyLevel, str]:
    for rule in EMERGENCY_RULES:
        if rule.issubset(symptoms):
            reason = (
                f"Matched emergency rule with symptoms: {', '.join(sorted(rule))}."
            )
            return UrgencyLevel.EMERGENCY, reason

    for rule in URGENT_RULES:
        if rule.issubset(symptoms):
            reason = f"Matched urgent rule with symptoms: {', '.join(sorted(rule))}."
            return UrgencyLevel.URGENT, reason

    return UrgencyLevel.NORMAL, "No urgent or emergency rule was matched."


def rank_conditions(symptoms: Set[str]) -> List[str]:
    scored = []

    for condition, rule_symptoms in CONDITION_RULES.items():
        overlap = len(symptoms & rule_symptoms)
        if overlap > 0:
            scored.append((condition, overlap, len(rule_symptoms)))

    scored.sort(key=lambda item: (item[1], -item[2]), reverse=True)

    if not scored:
        return ["undetermined non-specific condition"]

    return [item[0] for item in scored[:3]]