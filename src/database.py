"""
FixMyText AI — Database layer.

Uses SQLite with parameterized queries.  Tables: users, complaints,
complaint_history, internal_notes.  Passwords are hashed via bcrypt.
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime

import bcrypt

DB_PATH = Path(__file__).resolve().parents[1] / "fixmytext.db"


# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------

def connect():
    """Return a connection with Row factory and foreign keys enabled."""
    con = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


# ---------------------------------------------------------------------------
# Schema initialisation
# ---------------------------------------------------------------------------

def init_db():
    """Create tables if they do not exist."""
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            username     TEXT    NOT NULL UNIQUE,
            password_hash TEXT   NOT NULL,
            role         TEXT    NOT NULL DEFAULT 'user',
            created_at   TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS complaints (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id               INTEGER,
            title                 TEXT    NOT NULL,
            description           TEXT    NOT NULL,
            location              TEXT,
            is_anonymous          INTEGER NOT NULL DEFAULT 0,
            contact_info          TEXT,
            predicted_category    TEXT    NOT NULL,
            prediction_confidence REAL,
            model_version         TEXT,
            suggested_department  TEXT    NOT NULL,
            assigned_department   TEXT,
            priority              TEXT    NOT NULL DEFAULT 'Medium',
            priority_reason       TEXT,
            status                TEXT    NOT NULL DEFAULT 'Submitted',
            created_at            TEXT    NOT NULL,
            updated_at            TEXT    NOT NULL,
            resolved_at           TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS complaint_history (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id    INTEGER NOT NULL,
            previous_status TEXT,
            new_status      TEXT    NOT NULL,
            changed_by      TEXT,
            note            TEXT,
            created_at      TEXT    NOT NULL,
            FOREIGN KEY(complaint_id) REFERENCES complaints(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS internal_notes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id INTEGER NOT NULL,
            admin_id     INTEGER,
            note         TEXT    NOT NULL,
            created_at   TEXT    NOT NULL,
            FOREIGN KEY(complaint_id) REFERENCES complaints(id) ON DELETE CASCADE,
            FOREIGN KEY(admin_id) REFERENCES users(id)
        );

        CREATE INDEX IF NOT EXISTS idx_complaints_status   ON complaints(status);
        CREATE INDEX IF NOT EXISTS idx_complaints_category  ON complaints(predicted_category);
        CREATE INDEX IF NOT EXISTS idx_complaints_user      ON complaints(user_id);
        CREATE INDEX IF NOT EXISTS idx_history_complaint    ON complaint_history(complaint_id);
        CREATE INDEX IF NOT EXISTS idx_notes_complaint      ON internal_notes(complaint_id);
        """)


# ---------------------------------------------------------------------------
# User management
# ---------------------------------------------------------------------------

def create_user(username: str, password: str, role: str = "user") -> int | None:
    """Create a user; return user id or None if username taken."""
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    now = datetime.now().isoformat(timespec="seconds")
    try:
        with connect() as con:
            cur = con.execute(
                "INSERT INTO users (username, password_hash, role, created_at) VALUES (?,?,?,?)",
                (username.strip().lower(), pw_hash, role, now),
            )
            return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


def authenticate_user(username: str, password: str) -> dict | None:
    """Return user dict on success, None on failure."""
    with connect() as con:
        row = con.execute(
            "SELECT * FROM users WHERE username=?", (username.strip().lower(),)
        ).fetchone()
    if row and bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
        return dict(row)
    return None


def get_user(user_id: int) -> dict | None:
    with connect() as con:
        row = con.execute("SELECT id, username, role, created_at FROM users WHERE id=?", (user_id,)).fetchone()
    return dict(row) if row else None


def list_users() -> list[dict]:
    with connect() as con:
        rows = con.execute("SELECT id, username, role, created_at FROM users ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def ensure_admin():
    """Create a default admin if no admin exists (academic demo convenience)."""
    with connect() as con:
        row = con.execute("SELECT id FROM users WHERE role='admin' LIMIT 1").fetchone()
    if not row:
        admin_user = os.environ.get("FIXMYTEXT_ADMIN_USER", "admin")
        admin_pass = os.environ.get("FIXMYTEXT_ADMIN_PASS", "admin123")
        create_user(admin_user, admin_pass, role="admin")


# ---------------------------------------------------------------------------
# Complaint CRUD
# ---------------------------------------------------------------------------

def create_complaint(
    title: str,
    description: str,
    location: str,
    is_anonymous: bool,
    category: str,
    confidence: float | None,
    department: str,
    priority: str,
    priority_reason: str,
    user_id: int | None = None,
    contact_info: str | None = None,
    model_version: str | None = None,
) -> int:
    """Insert a complaint and its initial history row; return the new id."""
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as con:
        cur = con.execute(
            """INSERT INTO complaints
               (user_id, title, description, location, is_anonymous, contact_info,
                predicted_category, prediction_confidence, model_version,
                suggested_department, assigned_department,
                priority, priority_reason, status, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                user_id,
                title,
                description,
                location,
                int(is_anonymous),
                contact_info,
                category,
                confidence,
                model_version,
                department,
                department,   # assigned = suggested initially
                priority,
                priority_reason,
                "Submitted",
                now,
                now,
            ),
        )
        cid = cur.lastrowid
        con.execute(
            """INSERT INTO complaint_history
               (complaint_id, previous_status, new_status, changed_by, note, created_at)
               VALUES (?, NULL, 'Submitted', ?, 'Complaint created', ?)""",
            (cid, "system", now),
        )
        return cid


def get_complaints(user_id: int | None = None) -> list[dict]:
    """Return all complaints (optionally filtered by user)."""
    with connect() as con:
        if user_id is not None:
            rows = con.execute(
                "SELECT * FROM complaints WHERE user_id=? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
        else:
            rows = con.execute(
                "SELECT * FROM complaints ORDER BY created_at DESC"
            ).fetchall()
    return [dict(r) for r in rows]


def get_complaint(cid: int) -> dict | None:
    with connect() as con:
        row = con.execute("SELECT * FROM complaints WHERE id=?", (cid,)).fetchone()
    return dict(row) if row else None


def update_complaint_field(cid: int, **fields) -> bool:
    """Update arbitrary fields on a complaint row."""
    if not fields:
        return False
    now = datetime.now().isoformat(timespec="seconds")
    fields["updated_at"] = now
    set_clause = ", ".join(f"{k}=?" for k in fields)
    values = list(fields.values()) + [cid]
    with connect() as con:
        con.execute(f"UPDATE complaints SET {set_clause} WHERE id=?", values)
    return True


def update_status(cid: int, new_status: str, note: str = "Status updated", changed_by: str = "admin") -> bool:
    """Change status and log to history."""
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as con:
        row = con.execute("SELECT status FROM complaints WHERE id=?", (cid,)).fetchone()
        if not row:
            return False
        previous = row["status"]
        updates = {"status": new_status, "updated_at": now}
        if new_status == "Resolved":
            updates["resolved_at"] = now
        set_clause = ", ".join(f"{k}=?" for k in updates)
        values = list(updates.values()) + [cid]
        con.execute(f"UPDATE complaints SET {set_clause} WHERE id=?", values)
        con.execute(
            """INSERT INTO complaint_history
               (complaint_id, previous_status, new_status, changed_by, note, created_at)
               VALUES (?,?,?,?,?,?)""",
            (cid, previous, new_status, changed_by, note, now),
        )
    return True


def get_history(cid: int) -> list[dict]:
    with connect() as con:
        rows = con.execute(
            "SELECT * FROM complaint_history WHERE complaint_id=? ORDER BY created_at",
            (cid,),
        ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Internal notes
# ---------------------------------------------------------------------------

def add_internal_note(complaint_id: int, admin_id: int | None, note: str) -> int:
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as con:
        cur = con.execute(
            "INSERT INTO internal_notes (complaint_id, admin_id, note, created_at) VALUES (?,?,?,?)",
            (complaint_id, admin_id, note, now),
        )
        return cur.lastrowid


def get_internal_notes(complaint_id: int) -> list[dict]:
    with connect() as con:
        rows = con.execute(
            "SELECT * FROM internal_notes WHERE complaint_id=? ORDER BY created_at",
            (complaint_id,),
        ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------

def get_stats() -> dict:
    """Return aggregate statistics for the dashboard."""
    with connect() as con:
        total = con.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
        open_count = con.execute(
            "SELECT COUNT(*) FROM complaints WHERE status NOT IN ('Resolved')"
        ).fetchone()[0]
        resolved = con.execute(
            "SELECT COUNT(*) FROM complaints WHERE status='Resolved'"
        ).fetchone()[0]
        high = con.execute(
            "SELECT COUNT(*) FROM complaints WHERE priority='High'"
        ).fetchone()[0]
        by_category = con.execute(
            "SELECT predicted_category, COUNT(*) AS cnt FROM complaints GROUP BY predicted_category ORDER BY cnt DESC"
        ).fetchall()
        by_status = con.execute(
            "SELECT status, COUNT(*) AS cnt FROM complaints GROUP BY status ORDER BY cnt DESC"
        ).fetchall()
        by_department = con.execute(
            "SELECT COALESCE(assigned_department, suggested_department) AS dept, COUNT(*) AS cnt "
            "FROM complaints GROUP BY dept ORDER BY cnt DESC"
        ).fetchall()
        by_priority = con.execute(
            "SELECT priority, COUNT(*) AS cnt FROM complaints GROUP BY priority ORDER BY cnt DESC"
        ).fetchall()
        by_date = con.execute(
            "SELECT DATE(created_at) AS day, COUNT(*) AS cnt FROM complaints GROUP BY day ORDER BY day"
        ).fetchall()
    return {
        "total": total,
        "open": open_count,
        "resolved": resolved,
        "high": high,
        "by_category": [dict(r) for r in by_category],
        "by_status": [dict(r) for r in by_status],
        "by_department": [dict(r) for r in by_department],
        "by_priority": [dict(r) for r in by_priority],
        "by_date": [dict(r) for r in by_date],
    }
