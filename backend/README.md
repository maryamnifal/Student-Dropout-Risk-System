# University Student Dropout Risk Prediction System - Backend API

The **University Student Dropout Risk Prediction System** is a backend decision-support API designed for academic advisors. It predicts a student's final course outcome using early engagement, demographic, and assessment data available up to **Week 10** of the semester.

The system empowers advisors to provide early, supportive interventions to students who may be at risk of withdrawing or failing, well before the semester ends.

---

## Key Principles & Safety Guidelines

- **Early Intervention:** Predictions are based strictly on data captured up to Week 10.
- **No Data Leakage:** Post-outcome metrics (such as `final_result`, `date_unregistration`, or post-week-10 activity) are not used and are strictly rejected by the API schema.
- **Supportive Decision-Support:** Risk indicators and messages are framed as advisor decision-support recommendations, not punitive actions or deterministic student labels.

---

## Project Structure

```text
backend/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI app, lifespan setup, and endpoints
│   ├── schemas.py           # Pydantic request/response models (52 raw fields)
│   ├── model_service.py     # Artifact loading and inference pipeline
│   └── risk_service.py      # Supportive advisor risk level mapping
├── models/
│   ├── final_xgboost_model.joblib      # Trained XGBoost pipeline (with sampler)
│   ├── label_encoder.joblib            # Outcome label encoder (4 classes)
│   ├── preprocessor_week10.joblib      # Fitted ColumnTransformer (52 -> 90 features)
│   └── processed_feature_names.csv     # 90 transformed feature names
├── tests/
│   └── test_api.py          # API route and health validation tests
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
└── .gitignore               # Ignored files
```

---

## Machine Learning Pipeline & Prediction Flow

```text
Raw Student Data (52 raw fields: 8 categorical, 44 numerical)
   │
   ▼
Week-10 Preprocessor (`preprocessor_week10.joblib`)
   ├── Imputation & Scaling (StandardScaler) for 44 numerical fields
   └── Imputation & One-Hot Encoding for 8 categorical fields
   │
   ▼
Transformed Feature Matrix (90 features matching `processed_feature_names.csv`)
   │
   ▼
XGBoost Model Pipeline (`final_xgboost_model.joblib`)
   └── Predicts class probabilities using `multi:softprob`
   │
   ▼
Label Decoder (`label_encoder.joblib`)
   └── Decodes numeric index to: ['Distinction', 'Fail', 'Pass', 'Withdrawn']
   │
   ▼
Supportive Risk Evaluation (`risk_service.py`)
   └── Maps withdrawal probability to Low, Moderate, or High advisory guidance
```

---

## Installation

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.13 / 3.14)
- Pip package manager

### 2. Install Dependencies
From the `backend` directory, run:

```bash
pip install -r requirements.txt
```

---

## Running the API

Start the FastAPI application with Uvicorn:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

*(Note: Run the command from inside the `backend` directory so that `app` is directly importable.)*

---

## Interactive Documentation (Swagger UI)

Once the server is running, navigate to:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### 1. `GET /`
Returns service name, version, and running status.

**Example Response:**
```json
{
  "name": "University Student Dropout Risk Prediction API",
  "version": "1.0.0",
  "status": "running"
}
```

### 2. `GET /health`
Validates that machine learning artifacts are loaded in memory and confirms feature counts.

**Example Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "preprocessor_loaded": true,
  "label_encoder_loaded": true,
  "raw_feature_count": 52,
  "processed_feature_count": 90,
  "classes": [
    "Distinction",
    "Fail",
    "Pass",
    "Withdrawn"
  ]
}
```

### 3. `POST /predict`
Receives 52 raw student features up to Week 10, validates inputs, executes the preprocessing and inference pipeline, and returns the predicted outcome along with probabilities and supportive advisory guidance.

#### **Real Example Request (Student from `X_train_raw.csv`, Row 0):**
```json
{
  "code_module": "AAA",
  "code_presentation": "2013J",
  "gender": "M",
  "region": "East Anglian Region",
  "highest_education": "HE Qualification",
  "imd_band": "90-100%",
  "age_band": "55<=",
  "num_of_prev_attempts": 0,
  "studied_credits": 240,
  "disability": "N",
  "date_registration": -159.0,
  "module_presentation_length": 268,
  "assessments_submitted_week10": 2,
  "average_score_week10": 81.5,
  "highest_score_week10": 85.0,
  "average_submission_day_week10": 35.5,
  "banked_assessment_count_week10": 0,
  "tma_count_week10": 2,
  "cma_count_week10": 0,
  "exam_count_week10": 0,
  "assessment_weight_week10": 30.0,
  "weighted_average_score_week10": 82.6667,
  "total_clicks_week10": 545,
  "first_vle_activity_day": -5.0,
  "last_vle_activity_day_week10": 65.0,
  "active_vle_days_week10": 19,
  "unique_vle_sites_week10": 34,
  "dataplus_clicks_week10": 0,
  "dualpane_clicks_week10": 0,
  "externalquiz_clicks_week10": 0,
  "forumng_clicks_week10": 98,
  "glossary_clicks_week10": 0,
  "homepage_clicks_week10": 70,
  "htmlactivity_clicks_week10": 0,
  "oucollaborate_clicks_week10": 0,
  "oucontent_clicks_week10": 344,
  "ouelluminate_clicks_week10": 0,
  "ouwiki_clicks_week10": 0,
  "page_clicks_week10": 0,
  "questionnaire_clicks_week10": 0,
  "quiz_clicks_week10": 0,
  "repeatactivity_clicks_week10": 0,
  "resource_clicks_week10": 9,
  "sharedsubpage_clicks_week10": 0,
  "subpage_clicks_week10": 23,
  "url_clicks_week10": 1,
  "has_assessment_activity_week10": 1,
  "has_vle_activity_week10": 1,
  "vle_engagement_consistency_week10": 28.6842,
  "score_range_week10": 7.0,
  "late_submission_ratio_week10": 0.0,
  "clicks_per_site_week10": 16.0294
}
```

#### **Real Prediction Response:**
```json
{
  "predicted_outcome": "Pass",
  "confidence": 0.7624,
  "probabilities": {
    "Distinction": 0.1038,
    "Fail": 0.054,
    "Pass": 0.7624,
    "Withdrawn": 0.0798
  },
  "withdrawal_probability": 0.0798,
  "risk_level": "Low",
  "advisor_message": "Current predicted withdrawal risk is low. Continue normal academic monitoring."
}
```

---

## Running Automated Tests

Run the test suite from the `backend` directory using `pytest`:

```bash
pytest
```
