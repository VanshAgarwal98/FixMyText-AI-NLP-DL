"""Page 4 — Admin Panel (requires admin role)."""

import streamlit as st
import pandas as pd

from src.database import (
    get_complaints, get_complaint, update_status, update_complaint_field,
    get_history, add_internal_note, get_internal_notes,
)
from src.classifier import DEPARTMENT_MAP, CATEGORIES
from src.styling import hero, metric_card, badge, empty_state, timeline_item
from src.auth import is_admin, require_login

STATUSES = ["Submitted", "Reviewed", "Assigned", "In Progress", "Resolved", "Reopened"]
DEPARTMENTS = list(DEPARTMENT_MAP.values())


def render():
    hero("Admin Panel", "Search, filter, review, and manage all complaints.")

    if not require_login() or not is_admin():
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 26px; text-align: center; max-width: 540px; margin: 30px auto; box-shadow: 0 4px 14px rgba(15,23,42,0.06);">
            <div style="font-size: 2.2rem; margin-bottom: 8px;">🛡️</div>
            <div style="font-weight: 700; color: #1e4e5b; font-size: 1.15rem; margin-bottom: 6px;">Administrator Privileges Required</div>
            <p style="color: #64748b; font-size: 0.88rem; margin-bottom: 20px;">
                The Admin Console provides authority to update workflow statuses, reassign department routing, add private investigation notes, and export operational datasets.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col_c1, col_c2, col_c3 = st.columns([1, 1.2, 1])
        with col_c2:
            from src.auth import login
            if st.button("🔑 Sign In as Admin (admin / admin123)", type="primary", use_container_width=True):
                login("admin", "admin123")
                st.rerun()
        return

    complaints = get_complaints()
    if not complaints:
        empty_state("No complaints", "The system has no complaints yet.")
        return

    df = pd.DataFrame(complaints)

    # ── Filters ──────────────────────────────────────────────────────
    st.markdown("##### Filters")
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        search = st.text_input("Search", placeholder="Title or description…")
    with fc2:
        cat_opts = ["All"] + sorted(df["predicted_category"].dropna().unique().tolist())
        sel_cat = st.selectbox("Category", cat_opts)
    with fc3:
        sel_status = st.selectbox("Status", ["All"] + STATUSES)
    with fc4:
        sel_priority = st.selectbox("Priority", ["All", "High", "Medium", "Low"])

    filtered = df.copy()
    if search:
        mask = (
            filtered["title"].str.contains(search, case=False, na=False)
            | filtered["description"].str.contains(search, case=False, na=False)
        )
        filtered = filtered[mask]
    if sel_cat != "All":
        filtered = filtered[filtered["predicted_category"] == sel_cat]
    if sel_status != "All":
        filtered = filtered[filtered["status"] == sel_status]
    if sel_priority != "All":
        filtered = filtered[filtered["priority"] == sel_priority]

    # Sort
    sort_order = st.radio("Sort", ["Newest first", "Oldest first"], horizontal=True)
    if sort_order == "Oldest first":
        filtered = filtered.sort_values("created_at", ascending=True)

    st.caption(f"Showing {len(filtered)} of {len(df)} complaints")

    # ── Table ────────────────────────────────────────────────────────
    display_cols = [
        "id", "title", "predicted_category", "priority", "status",
        "assigned_department", "created_at",
    ]
    display_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(
        filtered[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", format="FX-%05d"),
        },
    )

    if filtered.empty:
        return

    # ── Detail & Management ──────────────────────────────────────────
    st.divider()
    st.markdown("##### Complaint Management")

    ids = filtered["id"].tolist()
    chosen_id = st.selectbox("Select complaint", ids, format_func=lambda x: f"FX-{x:05d}")
    comp = get_complaint(chosen_id)
    if not comp:
        return

    # Info cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Category", comp["predicted_category"])
    with c2:
        metric_card("Confidence", f"{comp['prediction_confidence']:.0%}" if comp.get("prediction_confidence") else "N/A")
    with c3:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">PRIORITY</div>'
            f'<div class="metric-value">{badge(comp["priority"])}</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">STATUS</div>'
            f'<div class="metric-value">{badge(comp["status"])}</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")

    with st.expander("Full Complaint Text", expanded=True):
        st.markdown(f"**{comp['title']}**")
        st.write(comp["description"])
        if comp.get("location"):
            st.caption(f"📍 {comp['location']}")
        if comp.get("priority_reason"):
            st.caption(f"Priority reason: {comp['priority_reason']}")

    # ── Actions ──────────────────────────────────────────────────────
    act_left, act_right = st.columns(2)

    with act_left:
        st.markdown("**Update Status**")
        new_status = st.selectbox("New status", STATUSES, key="admin_status")
        status_note = st.text_input("Note", value="", placeholder="Reason for status change", key="admin_note")
        if st.button("Save Status", type="primary", key="btn_save_status"):
            update_status(chosen_id, new_status, note=status_note or "Status updated by admin",
                          changed_by=st.session_state.get("username", "admin"))
            st.success(f"Status updated to {new_status}.")
            st.rerun()

    with act_right:
        st.markdown("**Assign Department**")
        current_dept = comp.get("assigned_department") or comp["suggested_department"]
        dept_idx = DEPARTMENTS.index(current_dept) if current_dept in DEPARTMENTS else 0
        new_dept = st.selectbox("Department", DEPARTMENTS, index=dept_idx, key="admin_dept")
        if st.button("Save Department", key="btn_save_dept"):
            update_complaint_field(chosen_id, assigned_department=new_dept)
            st.success(f"Department updated to {new_dept}.")
            st.rerun()

    # ── Internal notes ───────────────────────────────────────────────
    st.divider()
    st.markdown("##### Internal Notes")
    st.caption("These notes are only visible to administrators.")
    notes = get_internal_notes(chosen_id)
    if notes:
        for n in notes:
            st.markdown(f"**{n['created_at']}** — {n['note']}")
    else:
        st.caption("No internal notes yet.")

    new_note = st.text_area("Add a note", key="admin_int_note", height=80)
    if st.button("Add Note", key="btn_add_note"):
        if new_note.strip():
            add_internal_note(chosen_id, st.session_state.get("user_id"), new_note.strip())
            st.success("Note added.")
            st.rerun()

    # ── History ──────────────────────────────────────────────────────
    st.divider()
    st.markdown("##### Status History")
    history = get_history(chosen_id)
    for entry in history:
        is_current = entry["new_status"] == comp["status"]
        label = f"{entry.get('previous_status') or '—'} → {entry['new_status']}"
        meta_parts = [entry["created_at"]]
        if entry.get("changed_by"):
            meta_parts.append(f"by {entry['changed_by']}")
        if entry.get("note"):
            meta_parts.append(entry["note"])
        timeline_item(label, " · ".join(meta_parts), active=is_current)
