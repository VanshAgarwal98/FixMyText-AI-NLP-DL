"""
FixMyText AI — Application entry point.

Configures the Streamlit multipage app, initialises the database,
ensures a default admin account, applies the design system, and
renders the sidebar navigation with authentication controls.
"""

import streamlit as st
import importlib

from src.database import init_db, ensure_admin
from src.styling import apply_styles
from src.auth import render_auth_sidebar, _init_session

# ── Page config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FixMyText AI — Intelligent Complaint Classification",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Bootstrap ────────────────────────────────────────────────────────────
init_db()
ensure_admin()
apply_styles()
_init_session()

# ── Navigation registry with clear iconography ──────────────────────────
PAGES = {
    "📊  Dashboard Overview":        "views.p1_home",
    "📝  Submit Complaint":          "views.p2_submit",
    "📂  My Complaints":             "views.p3_my_complaints",
    "🛡️  Admin Management":          "views.p4_admin",
    "🔍  Similar Complaints":        "views.p5_similar",
    "⚡  AI Model Performance":      "views.p6_model",
    "📈  Reports & Analytics":       "views.p7_analytics",
    "⚙️  Settings & Documentation":  "views.p8_settings",
}

# ── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 6px 0 14px 0;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: linear-gradient(135deg, #2b6777 0%, #52ab98 100%); width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                ⚡
            </div>
            <div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">FixMyText AI</div>
                <div style="font-size: 0.72rem; color: #52ab98; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;">Campus NLP Engine</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("NAVIGATION")
    page = st.radio(
        "Navigation",
        list(PAGES.keys()),
        label_visibility="collapsed",
    )

    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
    st.divider()

    # User / Auth controls
    render_auth_sidebar()

    st.markdown("""
    <div style="margin-top: 20px; padding: 10px 12px; background: rgba(255,255,255,0.04); border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); text-align: center;">
        <span style="font-size: 0.72rem; color: #94a3b8;">FixMyText AI · Academic Edition v1.0</span>
    </div>
    """, unsafe_allow_html=True)

# ── Route to the selected page ───────────────────────────────────────────
module = importlib.import_module(PAGES[page])
module.render()
