"""Unit tests for src/classifier.py."""

from src.classifier import (
    normalize,
    suggest_priority,
    predict_category,
    DEPARTMENT_MAP,
    CATEGORIES,
    get_model_version,
)


def test_normalize():
    assert normalize("Wi-Fi NOT Working!!") == "wi fi not working"
    assert normalize("Visit https://support.portal for help") == "visit for help"
    assert normalize("") == ""
    assert normalize(None) == ""


def test_suggest_priority_safety_critical():
    high_samples = [
        "There is smoke coming out of the meter box",
        "Open electric shock risk near hostel entrance",
        "Short circuit happened in lab 302",
        "Dangerous exposed wire near water cooler",
        "Gas leak in the chemistry department kitchen",
    ]
    for text in high_samples:
        priority, reason = suggest_priority(text)
        assert priority == "High", f"Expected High for '{text}'"
        assert "review" in reason.lower() or "safety" in reason.lower()


def test_suggest_priority_medium_and_low():
    priority, _ = suggest_priority("Wi-Fi is not working in room 12")
    assert priority == "Medium"

    priority, _ = suggest_priority("Tap is leaking in second floor washroom")
    assert priority == "Medium"

    priority, _ = suggest_priority("Requesting new curtains for common room")
    assert priority == "Low"


def test_predict_category_baseline():
    cat, conf, note = predict_category("Internet is down and router is offline")
    assert cat in CATEGORIES
    assert conf is not None
    assert 0.0 <= conf <= 1.0

    # Empty text case
    cat, conf, note = predict_category("")
    assert cat == "Unclassified"
    assert conf == 0.0


def test_department_mapping_complete():
    for cat in CATEGORIES:
        assert cat in DEPARTMENT_MAP
        assert len(DEPARTMENT_MAP[cat]) > 0


def test_model_version():
    ver = get_model_version()
    assert "Logistic Regression" in ver or "BiLSTM" in ver
