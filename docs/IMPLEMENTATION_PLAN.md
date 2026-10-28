# Implementation Plan

## Milestone 1 — Local app foundation
- Install dependencies.
- Initialize SQLite.
- Run Streamlit app.
- Verify empty states.

## Milestone 2 — Baseline NLP
- Inspect and expand labelled dataset.
- Train TF-IDF + Logistic Regression.
- Inspect metrics and confusion matrix.
- Verify predictions on unseen examples.

## Milestone 3 — Complaint workflow
- Submit complaint.
- Persist model output and priority suggestion.
- Search/filter complaints.
- Update statuses and record history.

## Milestone 4 — Similarity and analytics
- Rank related complaints.
- Tune similarity threshold on representative examples.
- Add category/status charts and CSV export.

## Milestone 5 — Deep-learning experiment
- Install compatible TensorFlow.
- Train LSTM/BiLSTM.
- Use training-only tokenizer and held-out test data.
- Compare macro-F1 with baseline.
- Save real metrics.

## Milestone 6 — Quality and presentation
- Run tests.
- Check access limitations of demo mode.
- Capture real screenshots.
- Finish report, architecture diagram, methodology, and viva notes.

## Definition of done
A feature is done when it runs locally, uses real data/state, handles common errors, and has been manually or automatically tested.
