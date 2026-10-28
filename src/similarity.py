"""
FixMyText AI — Similarity detection using TF-IDF cosine similarity.

Falls back gracefully if there are too few complaints to compare.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_similar(
    query: str,
    complaints: list[dict],
    limit: int = 5,
    threshold: float = 0.20,
    exclude_id: int | None = None,
) -> list[dict]:
    """
    Find complaints similar to *query* text.

    Returns a list of dicts: {"complaint": {...}, "similarity": float}
    sorted by descending similarity, above *threshold*.

    *exclude_id*: skip a complaint id (to avoid comparing against itself).
    """
    candidates = [
        c for c in complaints
        if (c.get("description") or "").strip()
        and (exclude_id is None or c.get("id") != exclude_id)
    ]
    if not (query or "").strip() or not candidates:
        return []

    texts = [query] + [c["description"] for c in candidates]
    try:
        matrix = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_features=10000,
        ).fit_transform(texts)
        scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    except ValueError:
        return []

    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [
        {"complaint": c, "similarity": round(float(score), 4)}
        for c, score in ranked[:limit]
        if score >= threshold
    ]
