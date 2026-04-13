from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class UrgencyLevel(str, Enum):
    NORMAL = "Normal"
    URGENT = "Urgent"
    EMERGENCY = "Emergency"


class TriageMode(str, Enum):
    OLLAMA = "ollama"
    GROQ = "groq"
    RULES = "rules"


class TriageRequest(BaseModel):
    text: Optional[str] = Field(default=None)
    symptoms: Optional[List[str]] = Field(default=None)

    @model_validator(mode="after")
    def validate_input(self) -> "TriageRequest":
        has_text = bool(self.text and self.text.strip())
        has_symptoms = bool(
            self.symptoms and any(item and item.strip() for item in self.symptoms)
        )
        if not has_text and not has_symptoms:
            raise ValueError("Either 'text' or 'symptoms' must be provided.")
        return self


class LlmTriageResult(BaseModel):
    detected_symptoms: List[str]
    possible_conditions: List[str]
    recommended_specialist: str
    specialist_reason: str
    urgency_level: UrgencyLevel
    urgency_reason: str
    unmatched_fragments: List[str] = []
    confidence_note: str


class XRayAnalysisResult(BaseModel):
    """Result of X-Ray image analysis for pneumonia detection."""
    is_pneumonia: bool
    confidence: float
    confidence_percent: float
    class_label: str
    error: Optional[str] = None


class XRayRequest(BaseModel):
    """Request for X-Ray image analysis with optional symptoms."""
    # File will be handled by FastAPI File parameter
    symptoms: Optional[List[str]] = Field(default=None)
    patient_notes: Optional[str] = Field(default=None)


class TriageResponse(BaseModel):
    input_text: Optional[str]
    mode_used: TriageMode
    detected_symptoms: List[str]
    unmatched_fragments: List[str]
    possible_conditions: List[str]
    recommended_specialist: str
    specialist_reason: str
    urgency_level: UrgencyLevel
    urgency_reason: str
    confidence_note: str
    disclaimer: str
    explanation: str
    xray_analysis: Optional[XRayAnalysisResult] = None