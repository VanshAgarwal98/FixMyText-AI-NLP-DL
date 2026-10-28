"""Unit and integration tests for src/database.py."""

import tempfile
from pathlib import Path
import pytest

from src import database


@pytest.fixture(autouse=True)
def isolated_db(monkeypatch, tmp_path):
    """Point database module to a temporary database file for every test."""
    temp_db = tmp_path / "test_fixmytext.db"
    monkeypatch.setattr(database, "DB_PATH", temp_db)
    database.init_db()
    return temp_db


def test_user_creation_and_auth():
    # User creation
    uid = database.create_user("student1", "secret123", role="user")
    assert uid is not None

    # Duplicate username should fail
    uid_dup = database.create_user("student1", "otherpass", role="user")
    assert uid_dup is None

    # Authenticate successfully
    user = database.authenticate_user("student1", "secret123")
    assert user is not None
    assert user["username"] == "student1"
    assert user["role"] == "user"

    # Authenticate failure - bad password
    bad_auth = database.authenticate_user("student1", "wrongpass")
    assert bad_auth is None

    # Authenticate failure - non-existent user
    assert database.authenticate_user("nobody", "pass") is None


def test_ensure_admin():
    database.ensure_admin()
    admin = database.authenticate_user("admin", "admin123")
    assert admin is not None
    assert admin["role"] == "admin"


def test_complaint_crud_lifecycle():
    uid = database.create_user("raj", "pass123")

    # Create complaint
    cid = database.create_complaint(
        title="Wi-Fi router dead",
        description="Wi-Fi router in block B third floor has no power.",
        location="Hostel Block B",
        is_anonymous=False,
        category="Internet/Wi-Fi",
        confidence=0.89,
        department="IT Support",
        priority="Medium",
        priority_reason="Network issue",
        user_id=uid,
        contact_info="raj@campus.edu",
    )
    assert cid > 0

    # Retrieve complaint
    c = database.get_complaint(cid)
    assert c is not None
    assert c["title"] == "Wi-Fi router dead"
    assert c["status"] == "Submitted"
    assert c["assigned_department"] == "IT Support"

    # History was recorded
    hist = database.get_history(cid)
    assert len(hist) == 1
    assert hist[0]["new_status"] == "Submitted"

    # Update status to In Progress
    ok = database.update_status(cid, "In Progress", note="Technician assigned", changed_by="admin")
    assert ok is True

    c2 = database.get_complaint(cid)
    assert c2["status"] == "In Progress"

    # Update status to Resolved
    ok_res = database.update_status(cid, "Resolved", note="Replaced power cable", changed_by="admin")
    assert ok_res is True

    c3 = database.get_complaint(cid)
    assert c3["status"] == "Resolved"
    assert c3["resolved_at"] is not None

    # History records all steps
    hist2 = database.get_history(cid)
    assert len(hist2) == 3

    # Internal notes
    nid = database.add_internal_note(cid, admin_id=None, note="Check warranty first")
    assert nid > 0
    notes = database.get_internal_notes(cid)
    assert len(notes) == 1
    assert "warranty" in notes[0]["note"]


def test_get_stats():
    # Empty stats
    s0 = database.get_stats()
    assert s0["total"] == 0

    # Insert complaint
    database.create_complaint(
        title="Leaky tap",
        description="Washroom tap dripping",
        location="Block A",
        is_anonymous=True,
        category="Water Supply",
        confidence=0.92,
        department="Hostel Maintenance",
        priority="High",
        priority_reason="Flooding risk",
    )

    s1 = database.get_stats()
    assert s1["total"] == 1
    assert s1["high"] == 1
    assert s1["open"] == 1
    assert s1["resolved"] == 0
