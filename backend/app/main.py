import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.models import TriageMode, TriageRequest, TriageResponse, XRayAnalysisResult
from app.services.explanation import build_explanation
from app.services.groq_triage import run_groq_triage
from app.services.ollama_triage import run_ollama_triage
from app.services.rules_fallback import run_rules_fallback
from app.services.safety import apply_safety_override
from app.services.xray_processor import XRayProcessor

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DISCLAIMER = (
    "This is not a diagnosis and does not replace a licensed physician. "
    "If symptoms are severe, worsening, or suggest an emergency, seek immediate medical care immediately."
)

app = FastAPI(title="MedRoute AI API", version="0.8.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def log_env_status() -> None:
    print("=== ENV STATUS ===")
    print("OLLAMA_BASE_URL =", os.getenv("OLLAMA_BASE_URL"))
    print("OLLAMA_MODEL =", os.getenv("OLLAMA_MODEL"))
    print("GROQ_MODEL =", os.getenv("GROQ_MODEL"))
    print("GROQ_API_KEY exists =", bool(os.getenv("GROQ_API_KEY")))
    print("==================")


log_env_status()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

def _normalize_text(value: str) -> str:
    return " ".join((value or "").lower().replace("-", " ").split())


def filter_detected_symptoms(input_text: str, detected_symptoms: list[str]) -> list[str]:
    text = _normalize_text(input_text)
    kept: list[str] = []

    for symptom in detected_symptoms:
        normalized_symptom = _normalize_text(symptom)

        # оставляем симптом только если он явно встречается в тексте пользователя
        if normalized_symptom and normalized_symptom in text:
            kept.append(symptom)

    # убираем дубли, сохраняя порядок
    unique_kept: list[str] = []
    seen = set()
    for item in kept:
        key = _normalize_text(item)
        if key not in seen:
            seen.add(key)
            unique_kept.append(item)

    return unique_kept


def build_response_from_llm(
    input_text: str,
    llm_result,
    mode_used: TriageMode,
) -> TriageResponse:
    filtered_detected_symptoms = filter_detected_symptoms(
        input_text=input_text,
        detected_symptoms=llm_result.detected_symptoms,
    )

    # всё, что LLM "увидел", но чего нет в тексте пользователя, отправляем в unmatched
    filtered_unmatched_fragments = list(llm_result.unmatched_fragments)
    for symptom in llm_result.detected_symptoms:
        if symptom not in filtered_detected_symptoms:
            filtered_unmatched_fragments.append(symptom)

    # убираем дубли в unmatched
    unique_unmatched: list[str] = []
    seen_unmatched = set()
    for item in filtered_unmatched_fragments:
        key = _normalize_text(item)
        if key and key not in seen_unmatched:
            seen_unmatched.add(key)
            unique_unmatched.append(item)

    final_urgency, final_urgency_reason = apply_safety_override(
        detected_symptoms=set(filtered_detected_symptoms),
        urgency_level=llm_result.urgency_level,
        urgency_reason=llm_result.urgency_reason,
    )

    explanation = build_explanation(
        input_text=input_text,
        symptoms=filtered_detected_symptoms,
        unmatched_fragments=unique_unmatched,
        urgency=final_urgency,
        urgency_reason=final_urgency_reason,
        specialist_reason=llm_result.specialist_reason,
        conditions=llm_result.possible_conditions,
        confidence_note=llm_result.confidence_note,
    )

    return TriageResponse(
        input_text=input_text,
        mode_used=mode_used,
        detected_symptoms=filtered_detected_symptoms,
        unmatched_fragments=unique_unmatched,
        possible_conditions=llm_result.possible_conditions,
        recommended_specialist=llm_result.recommended_specialist,
        specialist_reason=llm_result.specialist_reason,
        urgency_level=final_urgency,
        urgency_reason=final_urgency_reason,
        confidence_note=llm_result.confidence_note,
        disclaimer=DISCLAIMER,
        explanation=explanation,
    )

def build_input_text(payload: TriageRequest) -> str:
    if payload.text and payload.text.strip():
        return payload.text.strip()

    return ", ".join(
        item.strip()
        for item in (payload.symptoms or [])
        if item and item.strip()
    )


@app.post("/triage", response_model=TriageResponse)
def triage(payload: TriageRequest) -> TriageResponse:
    input_text = build_input_text(payload)

    print("\n=== TRIAGE START ===")
    print("INPUT TEXT:", input_text)
    print("STRUCTURED SYMPTOMS:", payload.symptoms)

    # 1) Try Ollama first
    try:
        print("Trying Ollama...")
        ollama_result = run_ollama_triage(input_text)
        print("OLLAMA SUCCESS")
        print("OLLAMA DETECTED SYMPTOMS:", ollama_result.detected_symptoms)
        print("OLLAMA URGENCY:", ollama_result.urgency_level)

        return build_response_from_llm(
            input_text=input_text,
            llm_result=ollama_result,
            mode_used=TriageMode.OLLAMA,
        )

    except Exception as ollama_exc:
        print("OLLAMA FAILED:", repr(ollama_exc))

    # 2) Try Groq
    try:
        print("Trying Groq...")
        groq_result = run_groq_triage(input_text)
        print("GROQ SUCCESS")
        print("GROQ DETECTED SYMPTOMS:", groq_result.detected_symptoms)
        print("GROQ URGENCY:", groq_result.urgency_level)

        return build_response_from_llm(
            input_text=input_text,
            llm_result=groq_result,
            mode_used=TriageMode.GROQ,
        )

    except Exception as groq_exc:
        print("GROQ FAILED:", repr(groq_exc))

    # 3) Fallback
    print("USING RULES FALLBACK")

    fallback_response = run_rules_fallback(
        input_text=input_text,
        structured_symptoms=payload.symptoms,
        disclaimer=DISCLAIMER,
        fallback_reason="Both Ollama and Groq failed. See backend logs for details.",
    )

    print("RULES DETECTED SYMPTOMS:", fallback_response.detected_symptoms)
    print("RULES URGENCY:", fallback_response.urgency_level)
    print("=== TRIAGE END ===\n")

    return fallback_response


@app.post("/analyze-xray")
async def analyze_xray(file: UploadFile = File(...)):
    """
    Analyze X-Ray image for pneumonia detection.
    
    Args:
        file: X-Ray image file (JPEG, PNG, etc.)
        
    Returns:
        XRay analysis results with pneumonia detection
    """
    try:
        # Save uploaded file to temp location first
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp.flush()
            tmp_path = tmp.name
        
        try:
            # Now validate the saved file
            is_valid, message = XRayProcessor.validate_image_file(tmp_path)
            if not is_valid:
                return {
                    "error": f"Invalid file: {message}",
                    "is_pneumonia": None,
                    "confidence": None
                }
            
            # Process X-Ray
            xray_processor = XRayProcessor()
            result = xray_processor.predict(tmp_path)
            
            return result
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        return {
            "error": f"Processing error: {str(e)}",
            "is_pneumonia": None,
            "confidence": None
        }


def filter_detected_symptoms(input_text: str, detected_symptoms: list[str]) -> list[str]:
    text = input_text.lower()
    kept = []

    for symptom in detected_symptoms:
        s = symptom.lower().strip()

        # пропускаем только если симптом явно встречается в тексте
        if s in text:
            kept.append(symptom)

    return kept


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)