"""Page 7 — Reports & Analytics."""

import streamlit as st
import pandas as pd
import plotly.express as px

from src.database import get_complaints, get_stats
from src.styling import hero, empty_state, PALETTE
from src.auth import is_admin


def render():
    hero("Reports & Analytics", "Visual insights generated from real complaint data in the database.")

    complaints = get_complaints()
    if not complaints:
        empty_state(
            "No data available",
            "Submit complaints to generate analytics charts and reports.",
        )
        return

    df = pd.DataFrame(complaints)
    df["created_date"] = pd.to_datetime(df["created_at"]).dt.date
    stats = get_stats()

    # ── Date filter (admin only) ─────────────────────────────────────
    if is_admin():
        col_from, col_to = st.columns(2)
        min_date = df["created_date"].min()
        max_date = df["created_date"].max()
        with col_from:
            from_date = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
        with col_to:
            to_date = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date)
        df = df[(df["created_date"] >= from_date) & (df["created_date"] <= to_date)]

    # ── Charts ───────────────────────────────────────────────────────
    row1_left, row1_right = st.columns(2)

    with row1_left:
        st.markdown("##### Complaints by Category")
        cat_counts = df["predicted_category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig = px.bar(
            cat_counts, x="Category", y="Count",
            color_discrete_sequence=[PALETTE["teal_brand"]],
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), xaxis_title="", yaxis_title="",
        )
        st.plotly_chart(fig, use_container_width=True)

    with row1_right:
        st.markdown("##### Complaints by Department")
        dept_col = "assigned_department" if "assigned_department" in df.columns else "suggested_department"
        dept_counts = df[dept_col].value_counts().reset_index()
        dept_counts.columns = ["Department", "Count"]
        fig = px.bar(
            dept_counts, x="Count", y="Department", orientation="h",
            color_discrete_sequence=[PALETTE["mint"]],
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), xaxis_title="", yaxis_title="",
        )
        st.plotly_chart(fig, use_container_width=True)

    row2_left, row2_right = st.columns(2)

    with row2_left:
        st.markdown("##### Status Distribution")
        status_counts = df["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig = px.pie(
            status_counts, names="Status", values="Count", hole=0.5,
            color_discrete_sequence=[PALETTE["teal_brand"], PALETTE["mint"], "#38bdf8", "#f59e0b", "#94a3b8"],
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with row2_right:
        st.markdown("##### Priority Distribution")
        pri_counts = df["priority"].value_counts().reset_index()
        pri_counts.columns = ["Priority", "Count"]
        color_map = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}
        fig = px.bar(
            pri_counts, x="Priority", y="Count",
            color="Priority", color_discrete_map=color_map,
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), xaxis_title="", yaxis_title="",
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Complaints over time ─────────────────────────────────────────
    st.markdown("##### Complaints Over Time")
    time_counts = df.groupby("created_date").size().reset_index(name="Count")
    time_counts.columns = ["Date", "Count"]
    fig = px.area(
        time_counts, x="Date", y="Count",
        color_discrete_sequence=[PALETTE["teal_brand"]],
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Average resolution time ──────────────────────────────────────
    resolved_df = df[df["status"] == "Resolved"].copy()
    if not resolved_df.empty and "resolved_at" in resolved_df.columns:
        resolved_df = resolved_df.dropna(subset=["resolved_at"])
        if not resolved_df.empty:
            resolved_df["created_dt"] = pd.to_datetime(resolved_df["created_at"])
            resolved_df["resolved_dt"] = pd.to_datetime(resolved_df["resolved_at"])
            resolved_df["hours"] = (resolved_df["resolved_dt"] - resolved_df["created_dt"]).dt.total_seconds() / 3600
            avg_hours = resolved_df["hours"].mean()
            st.markdown("##### Average Resolution Time")
            if avg_hours < 1:
                st.metric("Average", f"{avg_hours * 60:.0f} minutes")
            else:
                st.metric("Average", f"{avg_hours:.1f} hours")

    # ── Top reported topics ──────────────────────────────────────────
    st.markdown("##### Frequently Reported Topics")
    top = df["title"].value_counts().head(10).reset_index()
    top.columns = ["Title", "Occurrences"]
    st.dataframe(top, use_container_width=True, hide_index=True)

    # ── CSV export (admin only) ──────────────────────────────────────
    if is_admin():
        st.divider()
        st.markdown("##### Export Data")
        export_cols = ["id", "title", "predicted_category", "priority", "status",
                       "suggested_department", "assigned_department", "location",
                       "created_at", "updated_at", "resolved_at"]
        export_cols = [c for c in export_cols if c in df.columns]
        csv = df[export_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV Report",
            csv,
            "fixmytext_report.csv",
            "text/csv",
            type="primary",
        )
        st.caption("The export does not include contact information or internal notes.")
