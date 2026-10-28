"""Unit tests for src/preprocessing.py."""

from src.preprocessing import normalize_text, remove_stopwords, preprocess


def test_normalize_text_basic():
    assert normalize_text("Hello World!") == "hello world"
    assert normalize_text("  Extra   Spaces  \n") == "extra spaces"
    assert normalize_text("") == ""
    assert normalize_text(None) == ""


def test_normalize_text_urls():
    text = "Check this out https://example.com/test and www.google.com for info"
    normalized = normalize_text(text)
    assert "https://" not in normalized
    assert "www.google.com" not in normalized
    assert normalized == "check this out and for info"


def test_remove_stopwords_preserving_negations():
    # Negations should be retained because "not working" is critical for sentiment/complaints
    text = "the wifi is not working in my room"
    cleaned = remove_stopwords(text, keep_negation=True)
    assert "not" in cleaned
    assert "working" in cleaned
    assert "the" not in cleaned.split()
    assert "is" not in cleaned.split()
    assert "in" not in cleaned.split()
    assert "my" not in cleaned.split()


def test_preprocess_pipeline():
    raw = "The bathroom TAP is NOT working at all! Visit http://hostel.edu"
    processed = preprocess(raw, remove_stops=True)
    assert "not" in processed
    assert "working" in processed
    assert "tap" in processed
    assert "!" not in processed
