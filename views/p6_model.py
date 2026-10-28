"""Page 6 — AI Model Performance dashboard."""

import json
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from src.classifier import BASELINE_PATH, BILSTM_PATH, get_model_version
from src.styling import hero, metric_card, empty_state, PALETTE

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"


def _load_metrics(filename: str) -> dict | None:
    path = ARTIFACTS / filename
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def render():
    hero("AI Model Performance", "Inspect evaluation metrics from actual training runs.")

    baseline = _load_metrics("baseline_metrics.json")
    bilstm = _load_metrics("bilstm_metrics.json")
    lstm = _load_metrics("lstm_metrics.json")

    if not baseline and not bilstm and not lstm:
        empty_state(
            "No evaluation results found",
            "Train the models first using the commands below, then revisit this page.",
        )
        st.code("python ml/train_baseline.py\npython ml/train_lstm.py\npython ml/train_bilstm.py", language="bash")
        return

    st.markdown(f"**Active model for predictions:** {get_model_version()}")
    st.write("")

    # ── Model comparison table ───────────────────────────────────────
    models = []
    for name, m in [("Logistic Regression", baseline), ("LSTM", lstm), ("BiLSTM", bilstm)]:
        if m:
            models.append({
                "Model": name,
                "Accuracy": f"{m['accuracy']:.2%}",
                "Macro Precision": f"{m['macro_precision']:.2%}",
                "Macro Recall": f"{m['macro_recall']:.2%}",
                "Macro F1": f"{m['macro_f1']:.2%}",
                "Test Size": m.get("test_size", "—"),
            })

    if models:
        st.markdown("##### Model Comparison")
        st.dataframe(pd.DataFrame(models), use_container_width=True, hide_index=True)

    # ── Bar chart comparison ─────────────────────────────────────────
    if len(models) > 1:
        chart_data = []
        for name, m in [("Logistic Regression", baseline), ("LSTM", lstm), ("BiLSTM", bilstm)]:
            if m:
                for metric_name in ["accuracy", "macro_precision", "macro_recall", "macro_f1"]:
                    chart_data.append({"Model": name, "Metric": metric_name.replace("_", " ").title(),
                                       "Score": m[metric_name]})
        if chart_data:
            fig = px.bar(
                pd.DataFrame(chart_data), x="Metric", y="Score", color="Model",
                barmode="group",
                color_discrete_sequence=[PALETTE["teal_brand"], PALETTE["mint"], "#0284c7"],
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                yaxis_range=[0, 1],
                margin=dict(l=0, r=0, t=10, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── Per-model detail sections ────────────────────────────────────
    for label, m in [("Logistic Regression Baseline", baseline), ("LSTM", lstm), ("BiLSTM", bilstm)]:
        if not m:
            continue

        st.divider()
        st.markdown(f"##### {label}")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Accuracy", f"{m['accuracy']:.2%}")
        with c2:
            metric_card("Precision", f"{m['macro_precision']:.2%}")
        with c3:
            metric_card("Recall", f"{m['macro_recall']:.2%}")
        with c4:
            metric_card("F1 Score", f"{m['macro_f1']:.2%}")

        # Per-class report
        report = m.get("classification_report")
        if report:
            classes = [k for k in report if k not in ("accuracy", "macro avg", "weighted avg")]
            rows = []
            for cls in classes:
                r = report[cls]
                rows.append({
                    "Category": cls,
                    "Precision": f"{r['precision']:.2%}",
                    "Recall": f"{r['recall']:.2%}",
                    "F1-score": f"{r['f1-score']:.2%}",
                    "Support": int(r["support"]),
                })
            with st.expander("Per-class metrics", expanded=False):
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # Confusion matrix
        cm = m.get("confusion_matrix")
        labels = m.get("labels", [])
        if cm and labels:
            with st.expander("Confusion Matrix", expanded=False):
                cm_array = np.array(cm)
                fig = px.imshow(
                    cm_array,
                    x=labels, y=labels,
                    labels=dict(x="Predicted", y="Actual", color="Count"),
                    color_continuous_scale="Blues",
                    text_auto=True,
                    aspect="auto",
                )
                fig.update_layout(
                    margin=dict(l=0, r=0, t=10, b=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)

        # Training history (loss curves)
        history = m.get("training_history")
        if history:
            with st.expander("Training & Validation Loss", expanded=False):
                hist_df = pd.DataFrame(history)
                if "loss" in hist_df.columns:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(y=hist_df["loss"], name="Training Loss",
                                            line=dict(color=PALETTE["teal_brand"], width=2.5)))
                    if "val_loss" in hist_df.columns:
                        fig.add_trace(go.Scatter(y=hist_df["val_loss"], name="Validation Loss",
                                                 line=dict(color=PALETTE["mint"], width=2.5, dash="dash")))
                    fig.update_layout(
                        xaxis_title="Epoch", yaxis_title="Loss",
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0, r=0, t=10, b=0),
                    )
                    st.plotly_chart(fig, use_container_width=True)

        if m.get("note"):
            st.caption(m["note"])
