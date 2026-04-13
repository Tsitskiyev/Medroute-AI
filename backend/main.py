from enum import Enum
from typing import List, Set

from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import traceback


app = FastAPI(title="MedRoute AI API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



DISCLAIMER = (
    "This is not a diagnosis and does not replace a licensed physician. "
    "If symptoms are severe, worsening, or suggest an emergency, seek immediate medical care."
)


class UrgencyLevel(str, Enum):
    NORMAL = "Normal"
    URGENT = "Urgent"
    EMERGENCY = "Emergency"


class TriageRequest(BaseModel):
    symptoms: List[str] = Field(..., min_length=1)


class TriageResponse(BaseModel):
    possible_conditions: List[str]
    recommended_specialist: str
    urgency_level: UrgencyLevel
    disclaimer: str
    detected_symptoms: List[str]
    explanation: str


SYMPTOM_SYNONYMS = {
    "pain in chest": "chest pain",
    "difficulty breathing": "shortness of breath",
    "breathlessness": "shortness of breath",
    "skin rash": "rash",
    "high temperature": "fever",
    "fainted": "loss of consciousness",
    "slurred speech": "speech difficulty",
}

SPECIALIST_MAPPING = {
    "chest pain": "Cardiologist",
    "palpitations": "Cardiologist",
    "shortness of breath": "Pulmonologist",
    "cough": "Pulmonologist",
    "rash": "Dermatologist",
    "itching": "Dermatologist",
    "abdominal pain": "Gastroenterologist",
    "nausea": "Gastroenterologist",
    "vomiting": "Gastroenterologist",
    "headache": "Neurologist",
    "speech difficulty": "Neurologist",
    "one-sided weakness": "Neurologist",
    "fever": "Therapist",
    "fatigue": "Therapist",
}

EMERGENCY_RULES = [
    {"chest pain", "shortness of breath"},
    {"speech difficulty", "one-sided weakness"},
    {"loss of consciousness"},
]

URGENT_RULES = [
    {"chest pain"},
    {"shortness of breath"},
    {"abdominal pain", "vomiting"},
    {"fever"},
]

CONDITION_RULES = {
    "possible angina": {"chest pain", "palpitations", "shortness of breath"},
    "possible respiratory infection": {"cough", "fever"},
    "possible dermatitis": {"rash", "itching"},
    "possible gastroenteritis": {"abdominal pain", "nausea", "vomiting"},
    "possible stroke": {"speech difficulty", "one-sided weakness"},
}


def normalize_symptom(value: str) -> str:
    symptom = value.strip().lower()
    return SYMPTOM_SYNONYMS.get(symptom, symptom)


def normalize_symptoms(symptoms: List[str]) -> List[str]:
    normalized = [normalize_symptom(s) for s in symptoms if s.strip()]
    return list(dict.fromkeys(normalized))


def detect_urgency(symptoms: Set[str]) -> UrgencyLevel:
    for rule in EMERGENCY_RULES:
        if rule.issubset(symptoms):
            return UrgencyLevel.EMERGENCY

    for rule in URGENT_RULES:
        if rule.issubset(symptoms):
            return UrgencyLevel.URGENT

    return UrgencyLevel.NORMAL


def rank_conditions(symptoms: Set[str]) -> List[str]:
    scored = []

    for condition, rule_symptoms in CONDITION_RULES.items():
        overlap = len(symptoms & rule_symptoms)
        if overlap > 0:
            scored.append((condition, overlap, len(rule_symptoms)))

    scored.sort(key=lambda x: (x[1], -x[2]), reverse=True)

    if not scored:
        return ["undetermined non-specific condition"]

    return [item[0] for item in scored[:3]]


def choose_specialist(symptoms: Set[str]) -> str:
    scores = {}

    for symptom in symptoms:
        specialist = SPECIALIST_MAPPING.get(symptom)
        if specialist:
            scores[specialist] = scores.get(specialist, 0) + 1

    if not scores:
        return "Therapist"

    return max(scores.items(), key=lambda x: x[1])[0]


def build_explanation(symptoms: List[str], urgency: UrgencyLevel, specialist: str) -> str:
    return (
        f"Detected symptoms: {', '.join(symptoms)}. "
        f"Urgency was classified as {urgency.value} based on symptom matching rules. "
        f"Recommended specialist: {specialist}."
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/triage", response_model=TriageResponse)
def triage(payload: TriageRequest) -> TriageResponse:
    detected = normalize_symptoms(payload.symptoms)
    symptom_set = set(detected)

    urgency = detect_urgency(symptom_set)
    conditions = rank_conditions(symptom_set)
    specialist = choose_specialist(symptom_set)
    explanation = build_explanation(detected, urgency, specialist)

    return TriageResponse(
        possible_conditions=conditions,
        recommended_specialist=specialist,
        urgency_level=urgency,
        disclaimer=DISCLAIMER,
        detected_symptoms=detected,
        explanation=explanation,
    )
