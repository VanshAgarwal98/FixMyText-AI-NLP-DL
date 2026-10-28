"""Page 5 — Similar Complaint Detection."""

import streamlit as st

from src.database import get_complaints
from src.similarity import find_similar
from src.styling import hero, badge, empty_state, PALETTE


def render():
    hero(
        "Similar Complaint Radar",
        "Detect duplicate reports, recurring campus issues, and cluster similar incidents in real time using TF-IDF n-gram cosine similarity.",
        tag="NLP Duplicate Detection",
    )

    st.markdown(
        """
        <div style="background: #f0f5f9; border-left: 4px solid #2b6777; padding: 12px 18px; border-radius: 8px; margin-bottom: 20px;">
            <span style="font-weight: 600; color: #1e4e5b;">ℹ️ Academic Methodology:</span>
            <span style="color: #475569; font-size: 0.9rem;">
                Similarity scores represent lexical & unigram/bigram overlap between complaint descriptions. 
                High similarity helps facility teams bundle work orders and prevent duplicate dispatches.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    complaints = get_complaints()

    tab_text, tab_id = st.tabs(["🔍 Search by Free Text", "📋 Match Against Existing Ticket"])

    # ── Tab 1: Free text search ──────────────────────────────────────
    with tab_text:
        query = st.text_area(
            "Enter text or incident description to compare against database",
            height=110,
            placeholder="e.g., The tap on the 2nd floor bathroom is leaking water all over the floor...",
        )
        col_thresh, col_limit = st.columns(2)
        with col_thresh:
            threshold = st.slider("Minimum Similarity Threshold", 0.05, 0.80, 0.20, 0.01, key="sim_thresh_text")
        with col_limit:
            limit = st.slider("Max Returned Matches", 1, 15, 5, key="sim_limit_text")

        if st.button("⚡ Scan for Similar Complaints", type="primary", key="btn_sim_text"):
            if not query.strip():
                st.warning("Please enter description text to perform similarity matching.")
            elif not complaints:
                empty_state("No complaints in database", "Submit complaints first to enable similarity search.")
            else:
                results = find_similar(query, complaints, limit=limit, threshold=threshold)
                _display_results(results)

    # ── Tab 2: Compare existing complaint ────────────────────────────
    with tab_id:
        if not complaints:
            empty_state("No complaints", "Submit complaints first.")
            return

        ids = [c["id"] for c in complaints]
        chosen = st.selectbox(
            "Select an existing ticket",
            ids,
            format_func=lambda x: f"FX-{x:04d} — {next((c['title'] for c in complaints if c['id'] == x), '')}",
        )
        comp = next((c for c in complaints if c["id"] == chosen), None)
        if comp:
            st.markdown(
                f"""
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; margin: 8px 0 16px 0;">
                    <div style="font-weight: 700; color: #1e4e5b; font-size: 0.95rem;">{comp['title']}</div>
                    <div style="color: #475569; font-size: 0.88rem; margin-top: 4px;">{comp['description']}</div>
                    <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 6px;">Category: <strong>{comp['predicted_category']}</strong> · Priority: <strong>{comp['priority']}</strong></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        col_thresh2, col_limit2 = st.columns(2)
        with col_thresh2:
            threshold2 = st.slider("Minimum Similarity Threshold", 0.05, 0.80, 0.20, 0.01, key="sim_thresh_id")
        with col_limit2:
            limit2 = st.slider("Max Returned Matches", 1, 15, 5, key="sim_limit_id")

        if st.button("⚡ Scan Against Selected Ticket", type="primary", key="btn_sim_id"):
            if comp:
                results = find_similar(
                    comp["description"],
                    complaints,
                    limit=limit2,
                    threshold=threshold2,
                    exclude_id=comp["id"],
                )
                _display_results(results)


def _display_results(results: list[dict]):
    """Render modern similarity result cards."""
    if not results:
        st.info("No existing complaints exceeded the selected similarity threshold.")
        return

    st.markdown(f"##### 🎯 Found {len(results)} Potential Match(es)")
    for item in results:
        c = item["complaint"]
        score = item["similarity"]
        pct = int(score * 100)

        if score >= 0.5:
            pill_bg = "#ecfdf5"
            pill_text = "#047857"
            pill_border = "#a7f3d0"
            match_label = "Strong Match"
        elif score >= 0.3:
            pill_bg = "#fef3c7"
            pill_text = "#92400e"
            pill_border = "#fde68a"
            match_label = "Moderate Match"
        else:
            pill_bg = "#f0f5f9"
            pill_text = "#1e5568"
            pill_border = "#c8d8e4"
            match_label = "Partial Match"

        st.markdown(
            f"""
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px 22px; margin-bottom: 12px; box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                    <div>
                        <span style="font-weight: 800; color: #1e4e5b; font-size: 1.05rem;">FX-{c['id']:04d}</span> · 
                        <span style="font-weight: 700; color: #0f172a; font-size: 1.02rem;">{c['title']}</span>
                    </div>
                    <span style="background: {pill_bg}; color: {pill_text}; border: 1px solid {pill_border}; font-weight: 800; font-size: 0.82rem; padding: 4px 12px; border-radius: 20px;">
                        {pct}% ({match_label})
                    </span>
                </div>
                <div style="display: flex; gap: 8px; margin-bottom: 10px;">
                    {badge(c['status'])}
                    {badge(c['priority'])}
                    <span style="background: #f1f5f9; color: #475569; font-size: 0.76rem; font-weight: 600; padding: 3px 10px; border-radius: 20px;">
                        📍 {c.get('location') or 'Campus'}
                    </span>
                    <span style="background: #f1f5f9; color: #475569; font-size: 0.76rem; font-weight: 600; padding: 3px 10px; border-radius: 20px;">
                        🏷️ {c['predicted_category']}
                    </span>
                </div>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                    {c['description']}
                </p>
                <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 10px;">
                    Logged on {c['created_at']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
