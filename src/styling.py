"""
FixMyText AI — Premium Design System and Custom CSS.

Brand Palette:
- Deep Teal: #2b6777 / #1e4e5b
- Mint Green: #52ab98
- Pale Blue: #c8d8e4
- Light Gray: #f8fafc / #f1f5f9
- Pure White: #ffffff
"""

import streamlit as st

# Design tokens
PALETTE = {
    "bg": "#f8fafc",
    "surface": "#ffffff",
    "surface_alt": "#f1f5f9",
    "border": "#e2e8f0",
    "border_light": "#edf2f7",
    "text_primary": "#0f172a",
    "text_secondary": "#475569",
    "text_muted": "#94a3b8",
    "teal_dark": "#163b45",
    "teal": "#1e4e5b",
    "teal_brand": "#2b6777",
    "mint": "#52ab98",
    "mint_light": "#e6f7f2",
    "mint_dark": "#0d765e",
    "pale_blue": "#c8d8e4",
    "pale_blue_light": "#f0f5f9",
    "pale_blue_dark": "#1e5568",
    "success": "#10b981",
    "success_light": "#ecfdf5",
    "warning": "#f59e0b",
    "warning_light": "#fffbeb",
    "danger": "#ef4444",
    "danger_light": "#fef2f2",
    "info": "#3b82f6",
    "info_light": "#eff6ff",
    "accent": "#2b6777",
    "accent_light": "#e6f7f2",
    "accent_hover": "#1e4e5b",
}


def apply_styles():
    """Inject the complete modern SaaS theme."""
    st.markdown(f"""
    <style>
    /* ───────── Google Fonts: Plus Jakarta Sans & Inter ───────── */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* ───────── Global Reset & Typography ───────── */
    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: {PALETTE['bg']} !important;
        color: {PALETTE['text_primary']} !important;
        -webkit-font-smoothing: antialiased;
    }}

    /* Remove excess top padding in Streamlit */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1200px !important;
    }}

    /* ───────── Hide Streamlit default auto-generated page navigation ───────── */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavLink"],
    [data-testid="stSidebarNavLinkContainer"],
    [data-testid="stSidebarNavSeparator"],
    [data-testid="stSidebarNavViewButton"],
    section[data-testid="stSidebar"] div:has(> ul[data-testid="stSidebarNavItems"]),
    section[data-testid="stSidebar"] nav,
    ul[data-testid="stSidebarNavItems"],
    div[data-testid="stSidebarNavSeparator"] {{
        display: none !important;
        height: 0px !important;
        max-height: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
        opacity: 0 !important;
        pointer-events: none !important;
        visibility: hidden !important;
    }}

    /* ───────── Sleek Dark-Teal Sidebar ───────── */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #132b33 0%, #1a3842 60%, #1e434f 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 2px 0 16px rgba(0, 0, 0, 0.12);
    }}

    /* Sidebar Headings and Labels */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] .stMarkdown {{
        color: #e2e8f0;
    }}

    section[data-testid="stSidebar"] .stCaption {{
        color: #94a3b8 !important;
    }}

    /* Sidebar Divider */
    section[data-testid="stSidebar"] hr {{
        border-color: rgba(255, 255, 255, 0.12) !important;
        margin: 14px 0 !important;
    }}

    /* Fix Sidebar Inputs so text is NEVER invisible */
    section[data-testid="stSidebar"] input {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.22) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }}
    section[data-testid="stSidebar"] input::placeholder {{
        color: rgba(255, 255, 255, 0.5) !important;
    }}
    section[data-testid="stSidebar"] input:focus {{
        border-color: {PALETTE['mint']} !important;
        box-shadow: 0 0 0 2px rgba(82, 171, 152, 0.35) !important;
    }}

    /* Sidebar Tabs */
    section[data-testid="stSidebar"] .stTabs [data-baseweb="tab-list"] {{
        background: rgba(0, 0, 0, 0.2);
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
    }}
    section[data-testid="stSidebar"] .stTabs [data-baseweb="tab"] {{
        color: #cbd5e1 !important;
        border-radius: 6px;
        padding: 6px 12px;
        font-weight: 500;
        font-size: 0.82rem;
    }}
    section[data-testid="stSidebar"] .stTabs [aria-selected="true"] {{
        background: {PALETTE['mint']} !important;
        color: #ffffff !important;
    }}

    /* Sidebar Navigation Pills */
    section[data-testid="stSidebar"] div[role="radiogroup"] {{
        gap: 4px;
        display: flex;
        flex-direction: column;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        background: transparent !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        margin: 1px 0 !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        border: 1px solid transparent !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
        transform: translateX(3px);
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
        background: linear-gradient(90deg, rgba(82, 171, 152, 0.24) 0%, rgba(43, 103, 119, 0.2) 100%) !important;
        border-left: 3px solid {PALETTE['mint']} !important;
        border-color: rgba(82, 171, 152, 0.3) !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label span {{
        color: #f1f5f9 !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span {{
        color: #ffffff !important;
        font-weight: 700 !important;
    }}

    /* ───────── Hero Header Banner ───────── */
    .hero {{
        background: linear-gradient(135deg, {PALETTE['teal_dark']} 0%, {PALETTE['teal']} 40%, {PALETTE['teal_brand']} 100%);
        border-radius: 18px;
        padding: 30px 36px;
        margin-bottom: 24px;
        color: #ffffff;
        box-shadow: 0 10px 28px -6px rgba(30, 78, 91, 0.28);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(200, 216, 228, 0.2);
    }}
    .hero::before {{
        content: '';
        position: absolute;
        top: -60px;
        right: -60px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(82, 171, 152, 0.35) 0%, rgba(82, 171, 152, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }}
    .hero h1 {{
        color: #ffffff !important;
        margin: 0 0 8px 0;
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }}
    .hero p {{
        color: rgba(255, 255, 255, 0.88) !important;
        margin: 0;
        font-size: 0.95rem;
        font-weight: 400;
        max-width: 780px;
        line-height: 1.5;
    }}
    .hero-tag {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        background: rgba(82, 171, 152, 0.22);
        border: 1px solid rgba(82, 171, 152, 0.45);
        color: #d1fae5;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }}

    /* ───────── Metric Cards ───────── */
    .metric-card {{
        background: {PALETTE['surface']};
        border: 1px solid {PALETTE['border']};
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    .metric-card:hover {{
        box-shadow: 0 10px 25px -4px rgba(43, 103, 119, 0.12);
        transform: translateY(-2px);
        border-color: {PALETTE['pale_blue']};
    }}
    .metric-card::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, {PALETTE['teal_brand']} 0%, {PALETTE['mint']} 100%);
    }}
    .metric-label {{
        color: {PALETTE['text_secondary']};
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }}
    .metric-value {{
        color: {PALETTE['text_primary']};
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }}
    .metric-sub {{
        color: {PALETTE['text_muted']};
        font-size: 0.76rem;
        font-weight: 500;
        margin-top: 6px;
    }}

    /* ───────── Cards & Content Panels ───────── */
    .card {{
        background: {PALETTE['surface']};
        border: 1px solid {PALETTE['border']};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
    }}

    /* ───────── Status & Priority Badges ───────── */
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        line-height: 1.4;
    }}
    .badge-submitted {{ background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }}
    .badge-reviewed  {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
    .badge-assigned  {{ background: #e0e7ff; color: #3730a3; border: 1px solid #c7d2fe; }}
    .badge-progress  {{ background: #fef9c3; color: #854d0e; border: 1px solid #fef08a; }}
    .badge-resolved  {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
    .badge-reopened  {{ background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }}
    .badge-rejected  {{ background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }}
    .badge-high      {{ background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }}
    .badge-medium    {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
    .badge-low       {{ background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }}

    /* ───────── Buttons ───────── */
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {PALETTE['teal_brand']} 0%, {PALETTE['mint']} 100%) !important;
        border: none !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 9px 26px !important;
        box-shadow: 0 4px 14px rgba(43, 103, 119, 0.28) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button[kind="primary"]:hover {{
        box-shadow: 0 6px 20px rgba(82, 171, 152, 0.4) !important;
        transform: translateY(-1px) !important;
    }}

    div.stButton > button[kind="secondary"],
    div.stFormSubmitButton > button[kind="secondary"] {{
        background: #ffffff !important;
        border: 1px solid {PALETTE['border']} !important;
        color: {PALETTE['text_primary']} !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 8px 20px !important;
        transition: all 0.2s !important;
    }}
    div.stButton > button[kind="secondary"]:hover,
    div.stFormSubmitButton > button[kind="secondary"]:hover {{
        border-color: {PALETTE['mint']} !important;
        color: {PALETTE['mint_dark']} !important;
        background: {PALETTE['mint_light']} !important;
    }}

    /* ───────── Form Controls & Inputs ───────── */
    div[data-testid="stForm"] {{
        background: {PALETTE['surface']};
        padding: 28px;
        border-radius: 16px;
        border: 1px solid {PALETTE['border']};
        box-shadow: 0 2px 12px rgba(15, 23, 42, 0.04);
    }}

    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {{
        border-radius: 10px !important;
        border: 1px solid {PALETTE['border']} !important;
        background-color: #ffffff !important;
        font-size: 0.92rem !important;
        color: {PALETTE['text_primary']} !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {PALETTE['mint']} !important;
        box-shadow: 0 0 0 3px rgba(82, 171, 152, 0.25) !important;
    }}

    /* ───────── Dataframes & Tables ───────── */
    .stDataFrame {{
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid {PALETTE['border']};
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.02);
    }}

    /* ───────── Expanders ───────── */
    div[data-testid="stExpander"] {{
        background: {PALETTE['surface']};
        border: 1px solid {PALETTE['border']};
        border-radius: 14px;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
        margin-bottom: 12px;
    }}
    div[data-testid="stExpander"] summary {{
        font-weight: 600;
        color: {PALETTE['text_primary']};
        border-radius: 14px;
    }}

    /* ───────── Timeline Component ───────── */
    .timeline-item {{
        position: relative;
        padding: 12px 0 12px 30px;
        border-left: 2px solid {PALETTE['border']};
    }}
    .timeline-item::before {{
        content: '';
        position: absolute;
        left: -6px;
        top: 16px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: {PALETTE['teal_brand']};
        border: 2px solid #ffffff;
    }}
    .timeline-item.active::before {{
        background: {PALETTE['mint']};
        box-shadow: 0 0 0 4px {PALETTE['mint_light']};
    }}
    .timeline-label {{
        font-weight: 600;
        font-size: 0.9rem;
        color: {PALETTE['text_primary']};
    }}
    .timeline-meta {{
        font-size: 0.78rem;
        color: {PALETTE['text_muted']};
        margin-top: 2px;
    }}

    /* ───────── Prediction Highlight Card ───────── */
    .prediction-box {{
        background: linear-gradient(135deg, {PALETTE['pale_blue_light']} 0%, #ffffff 100%);
        border: 1.5px solid {PALETTE['pale_blue']};
        border-radius: 14px;
        padding: 20px 22px;
        margin: 16px 0;
    }}

    /* ───────── Empty State ───────── */
    .empty-state {{
        text-align: center;
        padding: 50px 24px;
        background: {PALETTE['surface']};
        border-radius: 16px;
        border: 1.5px dashed {PALETTE['border']};
        color: {PALETTE['text_secondary']};
    }}
    .empty-state h3 {{
        color: {PALETTE['text_primary']};
        font-weight: 700;
        margin-bottom: 6px;
    }}
    .empty-state p {{
        font-size: 0.9rem;
        color: {PALETTE['text_muted']};
    }}
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Reusable HTML helpers
# ---------------------------------------------------------------------------

def hero(title: str, subtitle: str, tag: str = "Academic AI Demonstration"):
    st.markdown(
        f'<div class="hero">'
        f'<div class="hero-tag">⚡ {tag}</div>'
        f'<h1>{title}</h1>'
        f'<p>{subtitle}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value, subtext: str | None = None):
    sub_html = f'<div class="metric-sub">{subtext}</div>' if subtext else ''
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'{sub_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


_BADGE_MAP = {
    "Submitted": "submitted",
    "Reviewed": "reviewed",
    "Under Review": "reviewed",
    "Assigned": "assigned",
    "In Progress": "progress",
    "Resolved": "resolved",
    "Reopened": "reopened",
    "Rejected": "rejected",
    "High": "high",
    "Medium": "medium",
    "Low": "low",
}


def badge(text: str) -> str:
    cls = _BADGE_MAP.get(text, "submitted")
    return f'<span class="badge badge-{cls}">{text}</span>'


def empty_state(title: str, message: str):
    st.markdown(
        f'<div class="empty-state"><h3>{title}</h3><p>{message}</p></div>',
        unsafe_allow_html=True,
    )


def timeline_item(label: str, meta: str, active: bool = False):
    cls = "timeline-item active" if active else "timeline-item"
    st.markdown(
        f'<div class="{cls}">'
        f'<div class="timeline-label">{label}</div>'
        f'<div class="timeline-meta">{meta}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
