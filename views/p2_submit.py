"""Page 2 — Submit a Complaint."""

import streamlit as st

from src.database import create_complaint, get_complaints
from src.classifier import predict_category, suggest_priority, DEPARTMENT_MAP, get_model_version
from src.similarity import find_similar
from src.styling import hero, metric_card, badge, PALETTE
from src.auth import current_user_id


TEMPLATES = {
    "🌐 Wi-Fi Outage": {
        "title": "Wi-Fi disconnected in hostel block B",
        "desc": "Hostel Wi-Fi router is completely dead and disconnected. Students cannot access course portals.",
        "loc": "Hostel Block B, 2nd Floor",
    },
    "⚡ Electrical Spark": {
        "title": "Short circuit and sparking from wall switch",
        "desc": "Short circuit happened in room 302 and there is continuous electrical sparking from the main switch box.",
        "loc": "Science Block, Room 302",
    },
    "🚰 Water Leakage": {
        "title": "Ceiling pipe leaking in common washroom",
        "desc": "Water is leaking heavily from the ceiling pipe in the second floor washroom, flooding the hallway floor.",
        "loc": "Academic Block A, 2nd Floor Washroom",
    },
    "🍽️ Mess Food": {
        "title": "Undercooked food and cold meal served in lunch",
        "desc": "Food served today in the dining hall had a sour smell and lentils were completely undercooked.",
        "loc": "Dining Hall 1",
    },
}


def render():
    hero(
        "Submit a Complaint",
        "Describe your campus or hostel issue in plain English. Our NLP pipeline will automatically classify the category, recommend the responsible department, and assess safety priority.",
        tag="AI-Powered Ticket Intake",
    )

    # ── Quick Template Selector ──────────────────────────────────────
    st.markdown("##### ⚡ Quick Example Templates (One-Click Pre-fill)")
    t_cols = st.columns(4)
    for idx, (label, data) in enumerate(TEMPLATES.items()):
        with t_cols[idx]:
            if st.button(label, key=f"tpl_{idx}", use_container_width=True):
                st.session_state["f_title"] = data["title"]
                st.session_state["f_desc"] = data["desc"]
                st.session_state["f_loc"] = data["loc"]
                st.rerun()

    def_title = st.session_state.get("f_title", "")
    def_desc = st.session_state.get("f_desc", "")
    def_loc = st.session_state.get("f_loc", "")

    # ── Complaint Form ───────────────────────────────────────────────
    st.write("")
    with st.form("complaint_form"):
        st.markdown("##### 📝 Complaint Details")
        title = st.text_input(
            "Complaint Title *",
            value=def_title,
            placeholder="e.g., Wi-Fi router not working in hostel block B",
        )
        description = st.text_area(
            "Describe the Issue in Detail *",
            value=def_desc,
            height=130,
            placeholder="What happened, where, and when? The NLP classifier uses this text to identify department and priority.",
        )
        col_loc, col_contact = st.columns(2)
        with col_loc:
            location = st.text_input(
                "Location / Room / Building",
                value=def_loc,
                placeholder="e.g., Hostel Block C, Room 204",
            )
        with col_contact:
            contact_info = st.text_input(
                "Contact Info (Optional)",
                placeholder="e.g., roll number or email@campus.edu",
            )

        anonymous = st.checkbox(
            "Submit anonymously",
            help="Your account username will not be linked to this public report.",
        )

        submitted = st.form_submit_button(
            "⚡ Classify & Submit Complaint",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return

    # ── Validation ───────────────────────────────────────────────────
    if len(title.strip()) < 3:
        st.error("Please enter a meaningful title (at least 3 characters).")
        return
    if len(description.strip()) < 8:
        st.error("Please enter a descriptive report (at least 8 characters) for the AI model to analyse.")
        return

    # ── Classification ───────────────────────────────────────────────
    with st.spinner("Classifying incident text with NLP pipeline..."):
        category, confidence, model_note = predict_category(description)
        priority, priority_reason = suggest_priority(description)
        department = DEPARTMENT_MAP.get(category, "General Administration")
        model_ver = get_model_version()
        user_id = None if anonymous else current_user_id()

        cid = create_complaint(
            title=title.strip(),
            description=description.strip(),
            location=location.strip(),
            is_anonymous=anonymous,
            category=category,
            confidence=confidence,
            department=department,
            priority=priority,
            priority_reason=priority_reason,
            user_id=user_id,
            contact_info=contact_info.strip() if contact_info else None,
            model_version=model_ver,
        )

    # ── Result Presentation Card ─────────────────────────────────────
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #e6f7f2 0%, #ffffff 100%); border: 1.5px solid #52ab98; border-radius: 16px; padding: 22px 26px; margin: 20px 0; box-shadow: 0 4px 16px rgba(82, 171, 152, 0.15);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-weight: 800; color: #1e4e5b; font-size: 1.15rem;">Ticket Successfully Logged</span>
                <span style="background: #2b6777; color: #ffffff; padding: 4px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">FX-{cid:04d}</span>
            </div>
            <p style="margin: 0; color: #475569; font-size: 0.92rem;">Your complaint has been processed and routed to the corresponding department work queue.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("AI Category", category, subtext=f"Model: {model_ver.split('(')[0].strip()}")
    with c2:
        metric_card("Routing Target", department, subtext="Assigned department")
    with c3:
        metric_card("Assessed Priority", f"{priority} {badge(priority)}", subtext=priority_reason[:38] + "...")

    st.write("")

    # Confidence progress
    if confidence and confidence > 0:
        pct = min(max(confidence, 0.0), 1.0)
        st.progress(pct, text=f"AI Prediction Confidence: {pct:.1%}")
    if model_note and "Low confidence" in model_note:
        st.warning(f"⚠️ {model_note}")

    # ── Similarity check ─────────────────────────────────────────────
    existing = get_complaints()
    similar = find_similar(description, existing, exclude_id=cid, limit=3, threshold=0.18)
    if similar:
        st.markdown("##### 🔍 Similar Complaints in Database")
        st.caption("The similarity radar checks for duplicate or related reports in the same facility.")
        for item in similar:
            c = item["complaint"]
            sim_pct = int(item["similarity"] * 100)
            st.markdown(
                f"""
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px 18px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span style="font-weight: 700; color: #1e4e5b;">FX-{c['id']:04d}</span> · 
                        <span style="color: #0f172a; font-weight: 500;">{c['title']}</span>
                        <div style="font-size: 0.78rem; color: #64748b; margin-top: 2px;">{c.get('location') or 'Campus'} · {badge(c['status'])}</div>
                    </div>
                    <div>
                        <span style="background: #f0f5f9; color: #1e5568; font-weight: 700; font-size: 0.82rem; padding: 4px 10px; border-radius: 12px; border: 1px solid #c8d8e4;">
                            {sim_pct}% match
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
