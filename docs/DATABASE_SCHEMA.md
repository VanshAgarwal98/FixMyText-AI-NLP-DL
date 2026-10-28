# Database Schema — FixMyText AI

Database: SQLite (`fixmytext.db`).

## Table: complaints

| Column | Type | Rules | Meaning |
|---|---|---|---|
| id | INTEGER | PK, autoincrement | Internal complaint ID |
| title | TEXT | NOT NULL | Short issue title |
| description | TEXT | NOT NULL | Full complaint text |
| location | TEXT | nullable | User-provided location/building |
| is_anonymous | INTEGER | NOT NULL, default 0 | Anonymous submission flag |
| predicted_category | TEXT | NOT NULL | Model-predicted category |
| confidence | REAL | nullable | Model probability for selected category |
| suggested_department | TEXT | NOT NULL | Department mapped from category |
| priority | TEXT | NOT NULL, default Medium | Rule-based suggested priority |
| priority_reason | TEXT | nullable | Human-readable rule explanation |
| status | TEXT | NOT NULL, default Submitted | Current workflow state |
| created_at | TEXT | NOT NULL | Creation timestamp |
| updated_at | TEXT | NOT NULL | Last update timestamp |

## Table: complaint_history

| Column | Type | Rules | Meaning |
|---|---|---|---|
| id | INTEGER | PK, autoincrement | History record ID |
| complaint_id | INTEGER | FK → complaints.id | Related complaint |
| previous_status | TEXT | nullable | Status before transition |
| new_status | TEXT | NOT NULL | New status |
| note | TEXT | nullable | Reason/action note |
| created_at | TEXT | NOT NULL | Transition timestamp |

## Relationships
- One complaint has many history rows.
- Deleting a complaint cascades to its history rows.
- Indexes are created on status and predicted category.

## Suggested production extensions
- `users`: identity, password hash/identity-provider ID, role, created timestamp.
- `departments`: canonical department IDs and names.
- `assignments`: complaint, department, assignee, assigned timestamp.
- `internal_notes`: private notes with author and timestamp.
- `model_predictions`: model version, category, confidence, timestamp.
- `audit_log`: actor, action, entity, timestamp.

## Data handling
Do not store unnecessary personal data. Avoid exporting contact information by default. The MVP deliberately omits contact details and user accounts to keep the starter smaller and safer.
