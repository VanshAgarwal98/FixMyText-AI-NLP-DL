"""
FixMyText AI — Train Bidirectional LSTM model.

Requires TensorFlow (Python 3.11 or 3.12).

Usage:  python ml/train_bilstm.py
Output: models/complaint_bilstm.keras
        models/tokenizer.json
        models/label_classes.json
        artifacts/bilstm_metrics.json
"""

from pathlib import Path
import sys
import json

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.preprocessing import normalize_text

# ── TensorFlow imports ───────────────────────────────────────────────
try:
    import tensorflow as tf
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    from tensorflow.keras.utils import to_categorical
except ImportError:
    raise SystemExit(
        "TensorFlow is not installed or not compatible with this Python version.\n"
        "Install it in a Python 3.11 or 3.12 environment:\n"
        "  pip install tensorflow>=2.15"
    )

MAXLEN = 50
VOCAB_SIZE = 8000
EMBED_DIM = 64
LSTM_UNITS = 32
EPOCHS = 25
BATCH_SIZE = 16

MODELS = ROOT / "models"
ARTIFACTS = ROOT / "artifacts"
MODELS.mkdir(exist_ok=True)
ARTIFACTS.mkdir(exist_ok=True)


def main():
    print("Loading dataset ...")
    df = pd.read_csv(ROOT / "data" / "complaints.csv").dropna(subset=["text", "category"])
    df["text"] = df["text"].apply(normalize_text)
    df = df[df["text"].str.len() > 0]
    print(f"  {len(df)} examples, {df['category'].nunique()} categories")

    encoder = LabelEncoder()
    y = encoder.fit_transform(df["category"])
    num_classes = len(encoder.classes_)

    X_train_text, X_test_text, y_train, y_test = train_test_split(
        df["text"].tolist(), y, test_size=0.25, random_state=42, stratify=y,
    )

    # Tokenize (fit on training data only)
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train_text)
    vocab_size = min(VOCAB_SIZE, len(tokenizer.word_index) + 1)

    X_train = pad_sequences(tokenizer.texts_to_sequences(X_train_text), maxlen=MAXLEN, padding="post", truncating="post")
    X_test = pad_sequences(tokenizer.texts_to_sequences(X_test_text), maxlen=MAXLEN, padding="post", truncating="post")

    y_train_cat = to_categorical(y_train, num_classes)
    y_test_cat = to_categorical(y_test, num_classes)

    # Build model
    print("Building Bidirectional LSTM model ...")
    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=EMBED_DIM, input_length=MAXLEN),
        Bidirectional(LSTM(LSTM_UNITS)),
        Dropout(0.35),
        Dense(32, activation="relu"),
        Dense(num_classes, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.summary()

    history = model.fit(
        X_train, y_train_cat,
        validation_split=0.2,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True)],
        verbose=1,
    )

    # Evaluate
    probs = model.predict(X_test, verbose=0)
    pred = probs.argmax(axis=1)
    p, r, f1, _ = precision_recall_fscore_support(y_test, pred, average="macro", zero_division=0)
    labels = encoder.classes_.tolist()

    metrics = {
        "model": "BiLSTM",
        "test_size": int(len(y_test)),
        "train_size": int(len(y_train)),
        "accuracy": float(accuracy_score(y_test, pred)),
        "macro_precision": float(p),
        "macro_recall": float(r),
        "macro_f1": float(f1),
        "labels": labels,
        "classification_report": classification_report(y_test, pred, target_names=labels, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, pred, labels=range(num_classes)).tolist(),
        "training_history": {k: [float(v) for v in vals] for k, vals in history.history.items()},
        "note": "Small synthetic dataset; results are not a real-world performance estimate.",
    }

    # Save
    model.save(MODELS / "complaint_bilstm.keras")
    (MODELS / "tokenizer.json").write_text(tokenizer.to_json(), encoding="utf-8")
    (MODELS / "label_classes.json").write_text(json.dumps(labels), encoding="utf-8")
    (ARTIFACTS / "bilstm_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    summary = {k: v for k, v in metrics.items() if k not in ("classification_report", "confusion_matrix", "training_history")}
    print(json.dumps(summary, indent=2))
    print(f"Saved model -> {MODELS / 'complaint_bilstm.keras'}")
    print(f"Saved metrics -> {ARTIFACTS / 'bilstm_metrics.json'}")


if __name__ == "__main__":
    main()
