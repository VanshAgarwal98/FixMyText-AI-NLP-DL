# FixMyText AI

**FixMyText AI** is an intelligent complaint classification, similarity detection, and academic administration system powered by Machine Learning and Natural Language Processing (NLP).

Built with Python, Streamlit, Scikit-learn, SQLite, and optional TensorFlow (LSTM/BiLSTM).

---

## Brand Palette

- **Deep Teal:** `#2b6777` (Primary brand color & headers)
- **Mint Green:** `#52ab98` (Accents, success badges, key buttons)
- **Pale Blue:** `#c8d8e4` (Containers, chips, borders)
- **Light Gray:** `#f2f2f2` (Page backgrounds)
- **Pure White:** `#ffffff` (Card backgrounds)

---

## Key Features

1. **AI-Powered Complaint Classification:**
   - Multi-class NLP classifier (TF-IDF + Logistic Regression baseline and optional BiLSTM neural network).
   - Classifies complaints into 7 campus categories (*Water Supply, Electricity, Internet/Wi-Fi, Cleanliness, Food/Mess, Maintenance, Other*).
   - Generates confidence scores and flags low-confidence predictions (< 40%) for manual human verification.

2. **Automated Department Routing & Priority Assessment:**
   - Automatically maps categories to responsible departments (*IT Support, Housekeeping, Electrical Maintenance, Facilities, Mess Management, etc.*).
   - Transparent rule-based safety urgency detection: flags fire hazards, electrical shock, gas leaks, and flooding as **High Priority**.

3. **Complaint Similarity & Duplicate Detection:**
   - Real-time TF-IDF cosine similarity search across historical complaints.
   - Prevents duplicate work orders and groups related issues across campus hostels and facilities.
   - Adjustable similarity thresholds and detailed comparison views.

4. **Role-Based Complaint Management Lifecycle:**
   - Secure authentication with **bcrypt password hashing** and session state.
   - **Student / User Portal:** Submit complaints, track status history, and view internal notes.
   - **Admin Management Console:** Update statuses (*Submitted -> Under Review -> In Progress -> Resolved / Rejected*), reassign departments, change priorities, log admin notes, and export filtered reports.

5. **Analytics & Performance Dashboards:**
   - Interactive Plotly visualizations: complaint trends over time, category breakdowns, department workloads, resolution turnaround, and priority distribution.
   - Model Performance Dashboard: accuracy, precision, recall, macro-F1, confusion matrices, and training loss curves.

---

## Project Structure

```text
FixMyTextAI/
├── app.py                      # Main Streamlit navigation & theme setup
├── requirements.txt            # Python dependencies
├── fixmytext.db                # SQLite database (auto-generated)
├── data/
│   └── complaints.csv          # Starter training dataset (210 samples)
├── src/
│   ├── auth.py                 # User authentication & session management
│   ├── classifier.py           # Model inference & priority rules
│   ├── database.py             # SQLite CRUD operations, migrations, & stats
│   ├── preprocessing.py        # Text normalisation & negation handling
│   ├── similarity.py           # TF-IDF cosine similarity search
│   └── styling.py              # CSS styles, metric cards, badges, & banners
├── pages/
│   ├── p1_home.py              # Landing page & quick stats
│   ├── p2_submit.py            # AI complaint submission & preview
│   ├── p3_my_complaints.py     # Student complaint tracking
│   ├── p4_admin.py             # Administrative workflow management
│   ├── p5_similar.py           # Similarity search & duplicate analysis
│   ├── p6_model.py             # Model metrics & confusion matrices
│   ├── p7_analytics.py         # Visual reports & CSV export
│   └── p8_settings.py          # App config, demo data seed, & admin users
├── ml/
│   ├── prepare_dataset.py      # Dataset validation & class balance checks
│   ├── train_baseline.py       # TF-IDF + Logistic Regression training
│   ├── train_lstm.py           # Deep learning LSTM model training
│   ├── train_bilstm.py         # Deep learning BiLSTM model training
│   ├── evaluate_models.py      # Multi-model performance evaluation
│   └── seed_database.py        # Realistic demo complaint data populator
├── tests/
│   ├── test_preprocessing.py   # Text cleaning & negation tests
│   ├── test_classifier.py      # Classification & priority tests
│   ├── test_similarity.py      # Cosine similarity & threshold tests
│   └── test_database.py        # SQLite lifecycle, users, & analytics tests
├── models/
│   └── complaint_classifier.joblib  # Trained baseline classifier
├── artifacts/
│   └── baseline_metrics.json   # Model evaluation metrics & confusion matrix
└── docs/
    ├── PRD.md                  # Product Requirements Document
    ├── TRD.md                  # Technical Requirements Document
    ├── APP_FLOW.md             # Navigation & lifecycle flow
    ├── DATABASE_SCHEMA.md      # Schema & entity relationship guide
    ├── UI_UX_SPEC.md           # Design tokens, typography, & layouts
    ├── architecture.md         # System architecture diagram
    └── viva_questions.md       # Academic viva & defense Q&A preparation
```

---

## Quickstart Guide

### 1. Prerequisites & Environment Setup

Open Windows PowerShell in the project directory:

```powershell
# Create virtual environment (Python 3.11 or later)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Note:** If PowerShell restricts script execution, run:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### 2. Prepare Data & Train Baseline Model

```powershell
# Validate the dataset
python ml/prepare_dataset.py

# Train the baseline classifier
python ml/train_baseline.py

# Evaluate model metrics
python ml/evaluate_models.py
```

### 3. Seed Demo Data (Optional but Recommended)

Populate 19 realistic campus complaints across various workflow stages, categories, and priority levels:

```powershell
python ml/seed_database.py
```

### 4. Run the Application

```powershell
streamlit run app.py
```

Or using the Python module syntax:
```powershell
python -m streamlit run app.py
```

---

## Default Credentials

| Role | Username | Password | Notes |
|------|----------|----------|-------|
| **Admin** | `admin` | `admin123` | Full access to Admin Console, Analytics, and Settings |
| **Student** | `student1` | `student123` | Created by seed script |
| **Student** | `priya_sharma` | `pass123` | Created by seed script |
| **Faculty** | `faculty_user` | `faculty123` | Created by seed script |

You can also register new user accounts directly through the application sidebar.

---

## Running the Automated Test Suite

Execute the complete pytest suite:

```powershell
python -m pytest tests/ -v
```

All 17 unit and integration tests validate:
- Text normalization, URL stripping, and negation word preservation.
- Rule-based safety priority identification and classifier confidence limits.
- Cosine similarity ranking and self-exclusion filters.
- SQLite database schema generation, user authentication, and complaint state progression.

---

## Academic Demonstration Notes

1. **Synthetic Starter Dataset:** The included dataset (`data/complaints.csv`) contains 210 synthetic records for demonstration. For institutional production deployment, train on real student tickets.
2. **Deep Learning Models:** LSTM and BiLSTM training scripts are included in `ml/train_lstm.py` and `ml/train_bilstm.py` (requires TensorFlow).
3. **Defense Preparation:** A comprehensive academic presentation guide is available in [`docs/viva_questions.md`](file:///c:/Users/agarw/Desktop/MINOR%20PROJECT%202%20SEM/FixMyTextAI/docs/viva_questions.md).
