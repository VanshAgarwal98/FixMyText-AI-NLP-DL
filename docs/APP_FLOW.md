# Application Flow — FixMyText AI

## Main navigation
Overview → Submit complaint → Complaints → Similar complaints → Model & insights → About.

## Complaint submission flow
1. User opens Submit complaint.
2. User enters title, description, optional location, and anonymous preference.
3. Frontend validates required fields.
4. Text normalization runs.
5. Saved classifier predicts category and probability.
6. Category maps to a suggested department.
7. Transparent keyword rules suggest priority and provide a reason.
8. Similarity service compares the description with existing records.
9. Complaint and initial status-history row are inserted into SQLite.
10. UI displays complaint ID, prediction, confidence, priority, and potential matches.

## Admin status flow
1. Demo admin mode is enabled locally.
2. Administrator searches/filters complaints.
3. Administrator chooses a complaint and a new status.
4. Service reads previous status.
5. Database updates status and updated timestamp.
6. A history row records old status, new status, note, and timestamp.
7. UI refreshes to show current values.

## Similarity flow
1. User enters a query.
2. Existing complaint descriptions are collected.
3. TF-IDF vectors are generated for the query and candidates.
4. Cosine similarity scores are calculated.
5. Candidates are sorted by score.
6. Results above the configured threshold are shown.
7. UI labels results as potentially similar, not confirmed duplicates.

## Analytics flow
1. Read persisted complaint rows from SQLite.
2. Convert to a dataframe.
3. Apply category/status/date filters where implemented.
4. Aggregate actual records.
5. Render Plotly charts and CSV export.

## Failure states
- No trained model → Unclassified result and training instructions.
- Empty complaint → validation message.
- No database records → empty state.
- No similarity above threshold → no-results state.
- Low confidence → manual review warning.
