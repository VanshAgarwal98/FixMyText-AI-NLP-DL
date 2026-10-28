# Technical Requirements Document (TRD) — FixMyText AI

## 1. Architecture
Streamlit UI → Python service modules → classifier/similarity utilities → SQLite database.
Training scripts are separate from the interactive application. Saved model artifacts are loaded for inference.

## 2. Runtime components
- Python 3.11/3.12 recommended for compatibility testing.
- Streamlit for UI and page routing.
- scikit-learn pipeline for TF-IDF + Logistic Regression baseline.
- Optional TensorFlow/Keras for LSTM/BiLSTM training.
- pandas/numpy for data preparation.
- Plotly for charts.
- SQLite for local persistence.

## 3. Functional requirements
- FR-01: Validate complaint title and description.
- FR-02: Predict category using a saved model if available.
- FR-03: Return confidence and a review warning when low.
- FR-04: Map category to suggested department.
- FR-05: Calculate transparent rule-based priority.
- FR-06: Save complaint and initial status history.
- FR-07: Search and filter complaint records.
- FR-08: Update status and append history.
- FR-09: Rank similar complaints with cosine similarity.
- FR-10: Display data-backed charts and allow CSV export.

## 4. Non-functional requirements
- NFR-01: Must run on a standard laptop CPU for the MVP.
- NFR-02: No GPU required for the baseline.
- NFR-03: Database writes use parameterized SQL.
- NFR-04: Missing model files fail safely.
- NFR-05: UI uses the provided five-color palette consistently.
- NFR-06: Synthetic data provenance is disclosed.
- NFR-07: Errors are actionable and do not fabricate predictions.
- NFR-08: Core services are separated from UI code.

## 5. Model pipeline
### Baseline
TF-IDF (unigrams/bigrams) → Logistic Regression with class balancing → saved Joblib pipeline.

### Deep learning extension
Training-only tokenizer → integer sequences → padding → Embedding → Bidirectional LSTM → Dropout → Dense softmax. Use a held-out test set and early stopping. Do not fit tokenizer on test data.

### Metrics
Accuracy, macro precision, macro recall, macro-F1, per-class report, confusion matrix. The dataset is small and synthetic in this starter, so metrics are only a pipeline smoke test.

## 6. Error handling
- Empty or short text: block submission with a clear message.
- Missing model: save as Unclassified and explain how to train baseline.
- Model exception: return safe fallback and log no sensitive content.
- Empty database: show empty states.
- No similar results: display a clear no-results message.

## 7. Security note
The included Admin demo toggle is intentionally not production-grade authentication. Public deployment requires a real identity system, password hashing, authorization enforcement, session hardening, secrets management, and a security review.
