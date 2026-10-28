"""Page 1 — Overview / Home dashboard."""

import streamlit as st
import pandas as pd
import plotly.express as px

from src.database import get_complaints, get_stats
from src.styling import hero, metric_card, empty_state, PALETTE


def render():
    hero(
        "FixMyText AI",
        "Turn unstructured campus complaints into classified, prioritised, and actionable work orders — powered by Natural Language Processing.",
        tag="Incident & Complaint Intelligence",
    )

    stats = get_stats()

    # ── Quick Action Shortcuts ──────────────────────────────────────
    col_act1, col_act2, col_act3, _ = st.columns([1.2, 1.2, 1.2, 2.4])
    with col_act1:
        st.markdown(
            """<div style="font-size:0.8rem; font-weight:600; color:#475569; margin-bottom:4px;">QUICK ACTIONS</div>""",
            unsafe_allow_html=True,
        )
    st.write("")

    # ── KPI cards ────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total Complaints", stats["total"], subtext="All logged incidents")
    with c2:
        metric_card("Pending Action", stats["open"], subtext="In queue or in progress")
    with c3:
        metric_card("Resolved", stats["resolved"], subtext="Completed work orders")
    with c4:
        metric_card("High Priority", stats["high"], subtext="Safety & urgent flags")

    st.write("")

    if stats["total"] == 0:
        empty_state(
            "No complaints yet",
            "Submit your first complaint using the 'Submit Complaint' tab or seed sample data from Settings.",
        )
        return

    # ── Charts ───────────────────────────────────────────────────────
    left, right = st.columns(2)

    brand_colors = [
        PALETTE["teal_brand"],
        PALETTE["mint"],
        "#0284c7",
        "#f59e0b",
        "#10b981",
        "#8b5cf6",
        "#64748b",
    ]

    with left:
        st.markdown("#### 📂 Complaints by Category")
        cat_df = pd.DataFrame(stats["by_category"])
        if not cat_df.empty:
            fig = px.bar(
                cat_df,
                x="predicted_category",
                y="cnt",
                labels={"predicted_category": "Category", "cnt": "Volume"},
                color="predicted_category",
                color_discrete_sequence=brand_colors,
            )
            fig.update_layout(
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=20, b=0),
                font=dict(family="Plus Jakarta Sans, sans-serif"),
                xaxis=dict(title="", tickangle=-25),
                yaxis=dict(title="Complaints", gridcolor="#e2e8f0"),
            )
            st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### 🔄 Workflow Status Breakdown")
        status_df = pd.DataFrame(stats["by_status"])
        if not status_df.empty:
            fig = px.pie(
                status_df,
                names="status",
                values="cnt",
                hole=0.55,
                color_discrete_sequence=[
                    PALETTE["teal_brand"],
                    PALETTE["mint"],
                    "#38bdf8",
                    "#f59e0b",
                    "#94a3b8",
                ],
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=20, b=0),
                font=dict(family="Plus Jakarta Sans, sans-serif"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            )
            st.plotly_chart(fig, use_container_width=True)

    st.write("")

    # ── Recent complaints table ──────────────────────────────────────
    st.markdown("#### 📋 Recent Incident Feed")
    complaints = get_complaints()
    if complaints:
        df = pd.DataFrame(complaints)
        display_cols = [
            "id", "title", "predicted_category", "suggested_department",
            "priority", "status", "created_at"
        ]
        display_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(
            df[display_cols].head(8),
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("Ticket ID", format="FX-%04d"),
                "title": st.column_config.TextColumn("Complaint Summary"),
                "predicted_category": st.column_config.TextColumn("Category"),
                "suggested_department": st.column_config.TextColumn("Assigned Department"),
                "priority": st.column_config.TextColumn("Priority"),
                "status": st.column_config.TextColumn("Status"),
                "created_at": st.column_config.TextColumn("Logged Date"),
            },
        )

    # ── Complaints over time ─────────────────────────────────────────
    if stats.get("by_date"):
        st.markdown("#### 📈 Incident Submission Velocity")
        date_df = pd.DataFrame(stats["by_date"])
        fig = px.area(
            date_df,
            x="day",
            y="cnt",
            labels={"day": "Date", "cnt": "Complaints"},
            color_discrete_sequence=[PALETTE["teal_brand"]],
        )
        fig.update_traces(line=dict(width=2.5, color=PALETTE["teal_brand"]))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=20, b=0),
            font=dict(family="Plus Jakarta Sans, sans-serif"),
            xaxis=dict(title="", gridcolor="#e2e8f0"),
            yaxis=dict(title="Volume", gridcolor="#e2e8f0"),
        )
        st.plotly_chart(fig, use_container_width=True)
