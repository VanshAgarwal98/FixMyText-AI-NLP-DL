"""
FixMyText AI — Database seeding script for demonstration.

Populates realistic sample complaints, users, status workflows, and internal
notes using the active ML classifier for real-time predictions.

Usage:
    python ml/seed_database.py
"""

from pathlib import Path
import sys
import random
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.database import (
    init_db,
    ensure_admin,
    create_user,
    create_complaint,
    update_status,
    add_internal_note,
    get_stats,
    connect,
)
from src.classifier import predict_category, suggest_priority, DEPARTMENT_MAP, get_model_version


SAMPLE_COMPLAINTS = [
    # Water Supply
    {
        "title": "No running water on 3rd floor hostel",
        "description": "Hostel block B bathroom taps have no running water since 7 AM.",
        "location": "Hostel Block B, 3rd Floor",
        "user": "student1",
        "status": "In Progress",
        "days_ago": 2,
    },
    {
        "title": "Drinking water cooler leaking heavily",
        "description": "The water cooler in the central library entrance is leaking dirty brownish water all over the corridor.",
        "location": "Central Library Ground Floor",
        "user": "priya_sharma",
        "status": "Submitted",
        "days_ago": 1,
    },
    {
        "title": "Bathroom tap dripping continuously",
        "description": "Continuous dripping from ceiling pipe and basin tap in washroom 204.",
        "location": "Academic Block A, Room 204",
        "user": "student1",
        "status": "Resolved",
        "days_ago": 6,
    },

    # Electricity
    {
        "title": "Short circuit and sparks in laboratory",
        "description": "Short circuit happened in lab 302 and there is continuous electrical sparking from the main switch.",
        "location": "Science Block, Lab 302",
        "user": "faculty_user",
        "status": "In Progress",
        "days_ago": 1,
    },
    {
        "title": "Power outlet dead in seminar room",
        "description": "The wall socket for the projector power cut off and has no electricity.",
        "location": "Management Block, Room 105",
        "user": "faculty_user",
        "status": "Resolved",
        "days_ago": 5,
    },
    {
        "title": "Ceiling fan making loud grinding noise",
        "description": "Hostel room 412 ceiling fan is wobbling and dangerously close to falling.",
        "location": "Hostel Block C, Room 412",
        "user": "student1",
        "status": "Submitted",
        "days_ago": 0,
    },

    # Internet/Wi-Fi
    {
        "title": "Wi-Fi disconnected across Hostel Wing",
        "description": "Hostel Wi-Fi router is completely dead and disconnected, no internet access for students.",
        "location": "Hostel Block A, West Wing",
        "user": "priya_sharma",
        "status": "In Progress",
        "days_ago": 2,
    },
    {
        "title": "Very high ping and packet drop in CS lab",
        "description": "Campus Wi-Fi connection keeps dropping every five minutes in computer center.",
        "location": "Computer Center Lab 1",
        "user": "student1",
        "status": "Resolved",
        "days_ago": 4,
    },
    {
        "title": "Portal DNS not resolving on eduroam",
        "description": "Unable to access student ERP portal when connected to college campus Wi-Fi network.",
        "location": "Campus-wide",
        "user": "student1",
        "status": "Under Review",
        "days_ago": 3,
    },

    # Cleanliness
    {
        "title": "Garbage bin overflowing near cafeteria",
        "description": "Dustbin outside cafeteria is overflowing with food waste and flies have gathered.",
        "location": "Main Cafeteria Courtyard",
        "user": "priya_sharma",
        "status": "In Progress",
        "days_ago": 1,
    },
    {
        "title": "Corridor floor sticky and uncleaned",
        "description": "The 2nd floor passage has not been mopped for three days and smells foul.",
        "location": "Hostel Block B, 2nd Floor Corridor",
        "user": "student1",
        "status": "Resolved",
        "days_ago": 7,
    },
    {
        "title": "Washroom hygiene poor and uncleaned",
        "description": "Common washrooms in engineering block need urgent deep cleaning and sanitization.",
        "location": "Mechanical Block, 1st Floor Washroom",
        "user": "student1",
        "status": "Submitted",
        "days_ago": 0,
    },

    # Food/Mess
    {
        "title": "Stale food served in lunch mess",
        "description": "Food served today had a sour smell and undercooked lentils in evening dinner.",
        "location": "Dining Hall 1",
        "user": "student1",
        "status": "Under Review",
        "days_ago": 2,
    },
    {
        "title": "Insect found in mess drinking water",
        "description": "Found a dead fly inside the drinking water jug served on table 4.",
        "location": "Dining Hall 2",
        "user": "priya_sharma",
        "status": "In Progress",
        "days_ago": 3,
    },
    {
        "title": "Drinking glasses greasy and unwashed",
        "description": "Mess utensils and water glasses are not being washed properly with hot water.",
        "location": "Dining Hall 1",
        "user": "student1",
        "status": "Resolved",
        "days_ago": 8,
    },

    # Maintenance
    {
        "title": "Broken window pane in classroom",
        "description": "Classroom 204 window glass is shattered and sharp glass pieces could fall during storm.",
        "location": "Academic Block B, Room 204",
        "user": "faculty_user",
        "status": "In Progress",
        "days_ago": 3,
    },
    {
        "title": "Door lock jammed from outside",
        "description": "Hostel room 118 door latch is jammed and key gets stuck inside the lock.",
        "location": "Hostel Block A, Room 118",
        "user": "student1",
        "status": "Resolved",
        "days_ago": 9,
    },

    # Other
    {
        "title": "Missing library book return drop box",
        "description": "Request to install a 24-hour book drop box outside the library entrance for night returns.",
        "location": "Central Library",
        "user": "priya_sharma",
        "status": "Under Review",
        "days_ago": 4,
    },
    {
        "title": "Stray dogs entering campus sports ground",
        "description": "Multiple stray dogs entered the athletic ground creating a safety hazard for morning runners.",
        "location": "Sports Complex",
        "user": "student1",
        "status": "Resolved",
        "days_ago": 10,
    },
]


def seed():
    print("Initializing database...")
    init_db()
    ensure_admin()

    # Create demo users
    user_map = {}
    demo_users = [
        ("student1", "student123", "user"),
        ("priya_sharma", "pass123", "user"),
        ("faculty_user", "faculty123", "user"),
    ]
    for u, p, r in demo_users:
        uid = create_user(u, p, r)
        if uid is None:
            # Already exists
            with connect() as con:
                row = con.execute("SELECT id FROM users WHERE username=?", (u,)).fetchone()
                uid = row["id"] if row else None
        user_map[u] = uid
        print(f"  User '{u}' ready (id={uid})")

    now = datetime.now()
    model_ver = get_model_version()
    count = 0

    for item in SAMPLE_COMPLAINTS:
        # Predict using actual ML model
        category, conf, _ = predict_category(item["description"])
        suggested_dept = DEPARTMENT_MAP.get(category, "General Administration")
        priority, priority_reason = suggest_priority(item["description"])

        created_dt = now - timedelta(days=item["days_ago"], hours=random.randint(1, 12))
        created_str = created_dt.isoformat(timespec="seconds")

        uid = user_map.get(item["user"])
        cid = create_complaint(
            title=item["title"],
            description=item["description"],
            location=item["location"],
            is_anonymous=False,
            category=category,
            confidence=conf,
            department=suggested_dept,
            priority=priority,
            priority_reason=priority_reason,
            user_id=uid,
            contact_info=f"{item['user']}@campus.edu",
            model_version=model_ver,
        )

        # Fix timestamp to simulate history over time
        with connect() as con:
            con.execute("UPDATE complaints SET created_at=?, updated_at=? WHERE id=?",
                        (created_str, created_str, cid))
            con.execute("UPDATE complaint_history SET created_at=? WHERE complaint_id=?",
                        (created_str, cid))

        # Advance status if not Submitted
        st = item["status"]
        if st in ("Under Review", "In Progress", "Resolved"):
            update_status(cid, st, note=f"Status advanced to {st}", changed_by="admin")
            if st == "Resolved":
                res_dt = created_dt + timedelta(hours=random.randint(6, 48))
                with connect() as con:
                    con.execute("UPDATE complaints SET resolved_at=? WHERE id=?",
                                (res_dt.isoformat(timespec="seconds"), cid))
                add_internal_note(cid, admin_id=None, note="Issue inspected and resolved by duty maintenance team.")

        count += 1

    stats = get_stats()
    print(f"\n[OK] Successfully seeded {count} complaints into database!")
    print(f"Stats summary: {stats['total']} total, {stats['open']} open, {stats['resolved']} resolved, {stats['high']} high-priority.")


if __name__ == "__main__":
    seed()
