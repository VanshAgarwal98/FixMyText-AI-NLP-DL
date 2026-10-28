"""
FixMyText AI — Classifier module.

Loads the saved TF-IDF + Logistic Regression pipeline (and optionally a
Keras LSTM/BiLSTM model) and provides a unified prediction interface.
"""

from pathlib import Path
import json
import re

import joblib
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"
BASELINE_PATH = MODEL_DIR / "complaint_classifier.joblib"
BILSTM_PATH = MODEL_DIR / "complaint_bilstm.keras"
TOKENIZER_PATH = MODEL_DIR / "tokenizer.json"
LABEL_CLASSES_PATH = MODEL_DIR / "label_classes.json"

# ---------------------------------------------------------------------------
# Department mapping (configurable)
# ---------------------------------------------------------------------------

DEPARTMENT_MAP = {
    "Water Supply": "Hostel Maintenance / Facilities",
    "Electricity": "Electrical Maintenance",
    "Internet/Wi-Fi": "IT Support",
    "Cleanliness": "Housekeeping",
    "Food/Mess": "Mess Management",
    "Maintenance": "Facilities",
    "Other": "General Administration",
}

CATEGORIES = list(DEPARTMENT_MAP.keys())

LOW_CONFIDENCE_THRESHOLD = 0.40

# ---------------------------------------------------------------------------
# Text normalisation (matches training preprocessing)
# ---------------------------------------------------------------------------

from src.preprocessing import normalize_text

normalize = normalize_text


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

_baseline_model = None
_bilstm_model = None
_bilstm_tokenizer = None
_bilstm_classes = None


def _load_baseline():
    global _baseline_model
    if _baseline_model is None and BASELINE_PATH.exists():
        _baseline_model = joblib.load(BASELINE_PATH)
    return _baseline_model


def _load_bilstm():
    """Attempt to load Keras model; returns None if TF not available."""
    global _bilstm_model, _bilstm_tokenizer, _bilstm_classes
    if _bilstm_model is not None:
        return _bilstm_model, _bilstm_tokenizer, _bilstm_classes
    if not BILSTM_PATH.exists():
        return None, None, None
    try:
        from tensorflow.keras.models import load_model as keras_load
        from tensorflow.keras.preprocessing.text import tokenizer_from_json
        _bilstm_model = keras_load(str(BILSTM_PATH))
        _bilstm_tokenizer = tokenizer_from_json(TOKENIZER_PATH.read_text(encoding="utf-8"))
        _bilstm_classes = json.loads(LABEL_CLASSES_PATH.read_text(encoding="utf-8"))
        return _bilstm_model, _bilstm_tokenizer, _bilstm_classes
    except Exception:
        return None, None, None


# ---------------------------------------------------------------------------
# Prediction interface
# ---------------------------------------------------------------------------

def predict_category(text: str, prefer_deep: bool = False) -> tuple[str, float | None, str]:
    """
    Return (category, confidence, note).

    * Tries the BiLSTM model first if *prefer_deep* is True and TF is available.
    * Falls back to the baseline TF-IDF + LR pipeline.
    * Returns 'Unclassified' if no model is available.
    """
    cleaned = normalize(text)
    if not cleaned:
        return "Unclassified", 0.0, "Please enter a meaningful complaint."

    # Try BiLSTM
    if prefer_deep:
        model, tokenizer, classes = _load_bilstm()
        if model is not None:
            try:
                from tensorflow.keras.preprocessing.sequence import pad_sequences
                seq = pad_sequences(tokenizer.texts_to_sequences([cleaned]), maxlen=40,
                                    padding="post", truncating="post")
                probs = model.predict(seq, verbose=0)[0]
                idx = int(np.argmax(probs))
                category = classes[idx]
                confidence = float(probs[idx])
                note = "Prediction by BiLSTM deep-learning model."
                if confidence < LOW_CONFIDENCE_THRESHOLD:
                    note = "Low confidence — manual review recommended."
                return category, confidence, note
            except Exception:
                pass  # fall through to baseline

    # Baseline
    baseline = _load_baseline()
    if baseline is None:
        return "Unclassified", 0.0, "Model not trained yet. Run: python ml/train_baseline.py"
    try:
        probs = baseline.predict_proba([cleaned])[0]
        classes = baseline.classes_
        idx = int(probs.argmax())
        category = str(classes[idx])
        confidence = float(probs[idx])
        note = "Prediction by TF-IDF + Logistic Regression baseline."
        if confidence < LOW_CONFIDENCE_THRESHOLD:
            note = "Low confidence — manual review recommended."
        return category, confidence, note
    except Exception as exc:
        return "Unclassified", 0.0, f"Prediction failed safely: {exc.__class__.__name__}"


def get_model_version() -> str:
    """Return a short string describing the currently loaded model."""
    if BILSTM_PATH.exists():
        return "BiLSTM (Keras)"
    if BASELINE_PATH.exists():
        return "TF-IDF + Logistic Regression (scikit-learn)"
    return "No model available"


# ---------------------------------------------------------------------------
# Priority suggestion (rule-based, transparent)
# ---------------------------------------------------------------------------

_HIGH_SIGNALS = [
    ("fire", "possible fire hazard"),
    ("smoke", "smoke reported"),
    ("electric shock", "possible electrocution risk"),
    ("sparking", "electrical sparking"),
    ("exposed wire", "exposed wiring"),
    ("flooding", "flooding reported"),
    ("gas leak", "gas leak"),
    ("short circuit", "short circuit"),
    ("collapse", "structural collapse risk"),
    ("dangerous", "safety concern"),
    ("fell down", "fallen object or fixture"),
]

_MEDIUM_SIGNALS = [
    ("not working", "something not working"),
    ("no water", "water outage"),
    ("water supply", "water supply issue"),
    ("power cut", "power outage"),
    ("no electricity", "electricity outage"),
    ("no power", "power outage"),
    ("wifi", "network issue"),
    ("internet", "network issue"),
    ("broken", "broken item"),
    ("leaking", "leak reported"),
    ("clogged", "blockage"),
    ("pest", "pest issue"),
    ("cockroach", "pest issue"),
    ("rat", "pest issue"),
    ("bed bug", "pest issue"),
    ("stale food", "food quality"),
    ("stomach ache", "health concern from food"),
    ("insect in", "hygiene issue"),
]


def suggest_priority(text: str) -> tuple[str, str]:
    """Return (priority, reason) using keyword rules."""
    t = (text or "").lower()
    for term, reason in _HIGH_SIGNALS:
        if term in t:
            return "High", f"Contains safety-critical phrase '{term}' ({reason}). Human review required."
    for term, reason in _MEDIUM_SIGNALS:
        if term in t:
            return "Medium", f"Contains issue phrase '{term}' ({reason})."
    return "Low", "No configured urgency signal found; administrator should review."
