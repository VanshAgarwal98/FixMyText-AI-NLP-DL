# Product Requirements Document (PRD) — FixMyText AI

## 1. Product summary
FixMyText AI is a small, AI-assisted complaint triage application for college, hostel, office, and residential environments. It accepts natural-language complaints, predicts a category, recommends a department, identifies textually similar reports, and tracks complaint status.

## 2. Problem statement
Manual complaint triage is repetitive and inconsistent. Administrators must read each report, decide which team should handle it, and spot duplicate or related reports. The product reduces repetitive sorting while retaining human review.

## 3. Goals
- Classify complaint text into a defined set of categories.
- Suggest a department based on category.
- Store complaints persistently.
- Find potentially similar reports.
- Allow a demo administrator to update status and record history.
- Show transparent, database-backed analytics.
- Demonstrate a traditional ML baseline and an optional deep-learning model.

## 4. Non-goals
- Not a production grievance platform.
- Not an emergency response service.
- Not an automated adjudication system.
- Not proof that similar reports describe the same event.
- No automatic dispatch, email/SMS, payment, or third-party integrations in MVP.

## 5. Target users
- Submitter: describes an issue and receives a complaint ID.
- Administrator: reviews complaints, updates status, and examines analytics.
- Project evaluator: reviews the model methodology and project implementation.

## 6. MVP user stories
1. As a submitter, I can enter a title, description, and optional location.
2. As a submitter, I receive a persistent complaint ID.
3. As a submitter, I see a category and department suggestion, including a low-confidence warning where applicable.
4. As an administrator, I can search and filter complaints.
5. As an administrator, I can change status and add a note.
6. As an administrator, I can see the status history.
7. As an administrator, I can find potentially similar reports.
8. As an evaluator, I can inspect real model evaluation metrics.
9. As an administrator, I can export a report to CSV.

## 7. Categories
- Water Supply
- Electricity
- Internet/Wi-Fi
- Cleanliness
- Food/Mess
- Maintenance
- Other

## 8. Success criteria
- A valid complaint is saved to SQLite and survives application restart.
- Model predictions are generated from a saved trained model, not hardcoded labels.
- The application displays a warning if a model is unavailable or uncertain.
- Similarity results are ranked by actual text similarity.
- Dashboard metrics reflect database rows.
- Status changes are recorded in history.
- Core workflows can be demonstrated locally.

## 9. Risks and mitigations
- Small or synthetic data may produce misleading metrics: disclose provenance and evaluate on a held-out set.
- Ambiguous complaints may be misclassified: show confidence and support manual review.
- Keyword-based priority may miss context: expose reason and require human review.
- Demo admin mode is insecure: keep local-only and replace before deployment.
- Similarity false positives: label matches as potential, never auto-merge.

## 10. Future enhancements
- Proper authentication and role management.
- Multilingual/Hinglish classifier.
- Email notifications.
- Department assignment rules.
- A larger human-labelled dataset.
- Model monitoring and drift analysis.
