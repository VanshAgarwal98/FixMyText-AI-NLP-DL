"""
FixMyText AI — Train TF-IDF + Logistic Regression baseline.

Usage:  python ml/train_baseline.py
Output: models/complaint_classifier.joblib
        artifacts/baseline_metrics.json
"""

from pathlib import Path
import sys
import json

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "complaints.csv"
MODELS = ROOT / "models"
ARTIFACTS = ROOT / "artifacts"
MODELS.mkdir(exist_ok=True)
ARTIFACTS.mkdir(exist_ok=True)

# Add project root to path so preprocessing can be imported
sys.path.insert(0, str(ROOT))
from src.preprocessing import normalize_text


def main():
    print("Loading dataset ...")
    df = pd.read_csv(DATA).dropna(subset=["text", "category"])
    df["text"] = df["text"].apply(normalize_text)
    df = df[df["text"].str.len() > 0]

    if df["category"].nunique() < 2 or len(df) < 12:
        raise SystemExit("Dataset too small: need ≥12 labelled examples across ≥2 categories.")

    print(f"  {len(df)} examples, {df['category'].nunique()} categories")

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["category"],
        test_size=0.25, random_state=42, stratify=df["category"],
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=12000, sublinear_tf=True)),
        ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)),
    ])
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, pred, average="macro", zero_division=0)
    labels = sorted(df["category"].unique().tolist())

    metrics = {
        "model": "TF-IDF + Logistic Regression",
        "test_size": int(len(y_test)),
        "train_size": int(len(y_train)),
        "accuracy": float(accuracy_score(y_test, pred)),
        "macro_precision": float(precision),
        "macro_recall": float(recall),
        "macro_f1": float(f1),
        "labels": labels,
        "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, pred, labels=labels).tolist(),
        "note": "Metrics are from a synthetic starter dataset; not a real-world performance estimate.",
    }

    model_path = MODELS / "complaint_classifier.joblib"
    metrics_path = ARTIFACTS / "baseline_metrics.json"

    joblib.dump(model, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    # Print summary
    summary = {k: v for k, v in metrics.items() if k not in ("classification_report", "confusion_matrix")}
    print(json.dumps(summary, indent=2))
    print(f"Saved model  -> {model_path}")
    print(f"Saved metrics -> {metrics_path}")


if __name__ == "__main__":
    main()
