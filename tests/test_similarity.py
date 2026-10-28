"""Unit tests for src/similarity.py."""

from src.similarity import find_similar


def test_similarity_empty_inputs():
    assert find_similar("", []) == []
    assert find_similar("wifi is down", []) == []
    assert find_similar("", [{"id": 1, "description": "wifi is down"}]) == []


def test_similarity_matching():
    existing = [
        {"id": 1, "title": "Internet dead", "description": "Hostel Wi-Fi router is completely dead and disconnected."},
        {"id": 2, "title": "Water problem", "description": "No running water on third floor bathroom since morning."},
        {"id": 3, "title": "Power switch burnt", "description": "Switch board sparking in corridor."},
    ]

    results = find_similar("Wi-Fi is not connecting in hostel", existing, threshold=0.1)
    assert len(results) > 0
    top = results[0]
    assert top["complaint"]["id"] == 1
    assert top["similarity"] > 0.1


def test_similarity_exclude_id():
    existing = [
        {"id": 1, "title": "Water leak", "description": "Water leaking from ceiling in room 101"},
        {"id": 2, "title": "Water leak again", "description": "Water dripping from bathroom ceiling room 101"},
    ]
    # If comparing complaint #1 against the list, exclude_id=1 should not return itself
    results = find_similar(existing[0]["description"], existing, exclude_id=1, threshold=0.1)
    for r in results:
        assert r["complaint"]["id"] != 1
