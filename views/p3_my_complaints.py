"""Page 3 — My Complaints (requires login)."""

import streamlit as st
import pandas as pd

from src.database import get_complaints, get_history, get_complaint
from src.styling import hero, metric_card, badge, empty_state, timeline_item, PALETTE
from src.auth import require_login, current_user_id, current_username

STATUSES_ORDER = ["Submitted", "Reviewed", "Assigned", "In Progress", "Resolved"]


def render():
    hero("My Complaints", "Track the complaints you have submitted and view their current status.")

    if not require_login():
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 24px; text-align: center; max-width: 550px; margin: 30px auto; box-shadow: 0 4px 12px rgba(15,23,42,0.05);">
            <div style="font-size: 2rem; margin-bottom: 8px;">🔐</div>
            <div style="font-weight: 700; color: #1e4e5b; font-size: 1.1rem; margin-bottom: 6px;">Sign In to View Your Complaints</div>
            <p style="color: #64748b; font-size: 0.88rem; margin-bottom: 18px;">
                Personal complaint tracking, department updates, and resolution histories are tied to your account.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
        with col_c2:
            from src.auth import login
            if st.button("🎓 Sign In as Student (student1)", type="primary", use_container_width=True):
                login("student1", "student123")
                st.rerun()
            if st.button("🔑 Sign In as Admin (admin)", type="secondary", use_container_width=True):
                login("admin", "admin123")
                st.rerun()
        return

    uid = current_user_id()
    complaints = get_complaints(user_id=uid)

    if not complaints:
        empty_state(
            "No complaints found",
            "You have not submitted any complaints yet. Use 'Submit Complaint' to get started.",
        )
        return

    df = pd.DataFrame(complaints)

    # ── Filters ──────────────────────────────────────────────────────
    col_search, col_status = st.columns([2, 1])
    with col_search:
        search = st.text_input("Search", placeholder="Search title or description…", label_visibility="collapsed")
    with col_status:
        status_filter = st.selectbox("Status", ["All"] + STATUSES_ORDER + ["Reopened"])

    filtered = df.copy()
    if search:
        mask = (
            filtered["title"].str.contains(search, case=False, na=False)
            | filtered["description"].str.contains(search, case=False, na=False)
        )
        filtered = filtered[mask]
    if status_filter != "All":
        filtered = filtered[filtered["status"] == status_filter]

    # ── Table ────────────────────────────────────────────────────────
    display_cols = ["id", "title", "predicted_category", "priority", "status", "created_at"]
    display_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(
        filtered[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", format="FX-%05d"),
        },
    )

    # ── Detail view ──────────────────────────────────────────────────
    st.markdown("##### Complaint Detail")
    ids = filtered["id"].tolist() if not filtered.empty else []
    if not ids:
        st.caption("No complaints match the current filter.")
        return

    chosen_id = st.selectbox("Select a complaint", ids, format_func=lambda x: f"FX-{x:05d}")
    comp = get_complaint(chosen_id)
    if not comp:
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Category", comp["predicted_category"])
    with c2:
        metric_card("Department", comp.get("assigned_department") or comp["suggested_department"])
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">STATUS</div>'
                     f'<div class="metric-value">{badge(comp["status"])}</div></div>',
                     unsafe_allow_html=True)

    st.write("")

    with st.expander("Full complaint text", expanded=False):
        st.write(comp["description"])
        if comp.get("location"):
            st.caption(f"📍 {comp['location']}")

    # ── Timeline ─────────────────────────────────────────────────────
    st.markdown("##### Status Timeline")
    history = get_history(chosen_id)
    for entry in history:
        is_current = entry["new_status"] == comp["status"]
        label = f"{entry.get('previous_status') or '—'} → {entry['new_status']}"
        meta = f"{entry['created_at']}"
        if entry.get("note"):
            meta += f" · {entry['note']}"
        timeline_item(label, meta, active=is_current)
