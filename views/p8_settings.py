"""Page 8 — Settings & Help."""

import json
from pathlib import Path

import streamlit as st

from src.classifier import (
    DEPARTMENT_MAP, CATEGORIES, BASELINE_PATH, BILSTM_PATH,
    get_model_version, LOW_CONFIDENCE_THRESHOLD,
)
from src.database import DB_PATH, list_users, get_stats
from src.styling import hero, metric_card
from src.auth import is_admin

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"


def render():
    hero("Settings & Help", "Application configuration, model status, and usage instructions.")

    # ── Application info ─────────────────────────────────────────────
    st.markdown("##### Application Information")
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("App Version", "1.0.0")
    with c2:
        metric_card("Active Model", get_model_version())
    with c3:
        db_size_kb = DB_PATH.stat().st_size / 1024 if DB_PATH.exists() else 0
        metric_card("Database Size", f"{db_size_kb:.0f} KB")

    st.write("")

    # ── Model status ─────────────────────────────────────────────────
    st.markdown("##### Model Status")
    col_bl, col_dl = st.columns(2)
    with col_bl:
        if BASELINE_PATH.exists():
            st.success("✓ TF-IDF + Logistic Regression model loaded")
        else:
            st.warning("✗ Baseline model not trained")
    with col_dl:
        if BILSTM_PATH.exists():
            st.success("✓ BiLSTM model loaded")
        else:
            st.info("BiLSTM model not available (requires TensorFlow)")

    # ── Dataset info ─────────────────────────────────────────────────
    st.markdown("##### Dataset Information")
    csv_path = ROOT / "data" / "complaints.csv"
    if csv_path.exists():
        import pandas as pd
        data = pd.read_csv(csv_path)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Total examples", len(data))
        with c2:
            st.metric("Categories", data["category"].nunique())
        with st.expander("Category distribution"):
            st.dataframe(
                data["category"].value_counts().reset_index().rename(
                    columns={"index": "Category", "category": "Category", "count": "Count"}
                ),
                use_container_width=True,
                hide_index=True,
            )
        st.caption("This is a synthetic starter dataset created for academic demonstration purposes.")
    else:
        st.warning("Dataset file not found at data/complaints.csv")

    # ── Category → Department mapping ────────────────────────────────
    st.markdown("##### Category → Department Mapping")
    mapping_data = [{"Category": k, "Department": v} for k, v in DEPARTMENT_MAP.items()]
    st.dataframe(
        mapping_data,
        use_container_width=True,
        hide_index=True,
    )

    # ── Thresholds ───────────────────────────────────────────────────
    st.markdown("##### Configuration")
    st.markdown(f"- **Confidence threshold:** {LOW_CONFIDENCE_THRESHOLD:.0%} — predictions below this are flagged for manual review")
    st.markdown("- **Default similarity threshold:** 20% — configurable per search on the Similar Complaints page")

    # ── Training instructions ────────────────────────────────────────
    st.markdown("##### How to Train Models")
    st.code("""# 1. Train the baseline model
python ml/train_baseline.py

# 2. Train LSTM (requires TensorFlow + Python 3.11/3.12)
python ml/train_lstm.py

# 3. Train BiLSTM
python ml/train_bilstm.py

# 4. Evaluate all models
python ml/evaluate_models.py""", language="bash")

    # ── Startup instructions ─────────────────────────────────────────
    st.markdown("##### How to Start the Application")
    st.code("""# Using python -m streamlit (recommended if streamlit is not on PATH)
python -m streamlit run app.py

# Or if streamlit is on PATH
streamlit run app.py""", language="bash")

    # ── Default admin credentials ────────────────────────────────────
    st.markdown("##### Default Admin Account")
    st.markdown("""
    | Setting | Default |
    |---------|---------|
    | Username | `admin` |
    | Password | `admin123` |

    For production use, set `FIXMYTEXT_ADMIN_USER` and `FIXMYTEXT_ADMIN_PASS` environment variables
    before the first application start.
    """)

    # ── User list & Demo Data (admin only) ───────────────────────────
    if is_admin():
        st.divider()
        st.markdown("##### Registered Users")
        users = list_users()
        if users:
            st.dataframe(users, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("##### Demo Data Management")
        st.markdown("Populate realistic academic complaints, categories, priorities, and workflow states for demonstration.")
        if st.button("Seed Realistic Demo Complaints", type="secondary"):
            try:
                from ml.seed_database import seed
                seed()
                st.success("Sample demo complaints seeded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Seeding failed: {e}")

    # ── Disclaimer ───────────────────────────────────────────────────
    st.divider()
    st.markdown("##### Important Disclaimer")
    st.info(
        "FixMyText AI is a local academic demonstration project. "
        "It has **not** been deployed in any real institution, and the included dataset is synthetic. "
        "The application requires additional security review before any public deployment."
    )
