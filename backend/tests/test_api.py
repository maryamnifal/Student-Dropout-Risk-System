"""Initial and prediction API endpoint tests for University Student Dropout Risk Prediction System."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Valid student record extracted from X_train_raw.csv (row 0)
VALID_REAL_STUDENT_RECORD = {
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
    "clicks_per_site_week10": 16.0294,
}


@pytest.fixture(scope="module")
def client():
    """Create a test client with application lifespan execution."""
    with TestClient(app) as test_client:
        yield test_client


def test_root_endpoint(client: TestClient):
    """Test GET / endpoint returns running status and correct API name."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "University Student Dropout Risk Prediction API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"


def test_health_endpoint(client: TestClient):
    """Test GET /health endpoint confirms model and preprocessor readiness."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["preprocessor_loaded"] is True
    assert data["label_encoder_loaded"] is True
    assert data["raw_feature_count"] == 52
    assert data["processed_feature_count"] == 90
    assert data["classes"] == ["Distinction", "Fail", "Pass", "Withdrawn"]


def test_invalid_route(client: TestClient):
    """Test accessing an unknown route returns 404."""
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404


def test_predict_real_valid_record(client: TestClient):
    """Test POST /predict with a real valid record from X_train_raw.csv."""
    response = client.post("/predict", json=VALID_REAL_STUDENT_RECORD)
    assert response.status_code == 200
    data = response.json()

    # 1. Valid outcome class
    assert data["predicted_outcome"] in ["Distinction", "Fail", "Pass", "Withdrawn"]

    # 2. Four class probabilities present
    probs = data["probabilities"]
    assert set(probs.keys()) == {"Distinction", "Fail", "Pass", "Withdrawn"}

    # 3. Probabilities sum to approximately 1.0
    total_prob = sum(probs.values())
    assert total_prob == pytest.approx(1.0, abs=0.01)

    # 4. Confidence corresponds to predicted class probability
    assert data["confidence"] == pytest.approx(probs[data["predicted_outcome"]], abs=1e-4)

    # 5. Withdrawal probability corresponds to Withdrawn class
    assert data["withdrawal_probability"] == pytest.approx(probs["Withdrawn"], abs=1e-4)

    # 6. Risk level and advisory message generated correctly
    assert data["risk_level"] in ["Low", "Moderate", "High"]
    assert isinstance(data["advisor_message"], str) and len(data["advisor_message"]) > 0


def test_predict_missing_required_field(client: TestClient):
    """Test POST /predict returns 422 when a required field is missing."""
    payload = VALID_REAL_STUDENT_RECORD.copy()
    del payload["code_module"]

    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_predict_invalid_categorical_value(client: TestClient):
    """Test POST /predict returns 422 when a categorical value is invalid."""
    payload = VALID_REAL_STUDENT_RECORD.copy()
    payload["code_module"] = "ZZZ"  # Invalid code_module

    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_predict_unexpected_field_final_result(client: TestClient):
    """Test POST /predict returns 422 when an unexpected/target field is provided."""
    payload = VALID_REAL_STUDENT_RECORD.copy()
    payload["final_result"] = "Pass"  # Forbidden post-outcome field

    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_predict_invalid_numeric_value(client: TestClient):
    """Test POST /predict returns 422 when numeric constraints are violated."""
    payload = VALID_REAL_STUDENT_RECORD.copy()
    payload["average_score_week10"] = 150.0  # Violates le=100.0 constraint

    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
