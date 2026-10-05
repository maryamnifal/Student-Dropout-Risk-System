"""Pydantic schemas for request validation and response formatting.

All 52 raw fields expected by the preprocessor are validated here.
Post-outcome fields (e.g., final_result, date_unregistration) are strictly forbidden.
"""

from typing import Dict, List, Literal
from pydantic import BaseModel, ConfigDict, Field

# Categorical Literals matching exact preprocessor categories
CodeModuleType = Literal["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG"]
CodePresentationType = Literal["2013B", "2013J", "2014B", "2014J"]
GenderType = Literal["F", "M"]
RegionType = Literal[
    "East Anglian Region",
    "East Midlands Region",
    "Ireland",
    "London Region",
    "North Region",
    "North Western Region",
    "Scotland",
    "South East Region",
    "South Region",
    "South West Region",
    "Wales",
    "West Midlands Region",
    "Yorkshire Region",
]
HighestEducationType = Literal[
    "A Level or Equivalent",
    "HE Qualification",
    "Lower Than A Level",
    "No Formal quals",
    "Post Graduate Qualification",
]
ImdBandType = Literal[
    "0-10%",
    "10-20",
    "20-30%",
    "30-40%",
    "40-50%",
    "50-60%",
    "60-70%",
    "70-80%",
    "80-90%",
    "90-100%",
]
AgeBandType = Literal["0-35", "35-55", "55<="]
DisabilityType = Literal["N", "Y"]


class StudentRawInput(BaseModel):
    """Raw student attributes available up to Week 10.

    Exactly 52 fields: 8 categorical and 44 numerical.
    Extra fields are strictly forbidden to prevent data leakage or invalid payload.
    """

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
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
        },
    )

    # 8 Categorical fields
    code_module: CodeModuleType = Field(
        ..., description="Module code (AAA-GGG)"
    )
    code_presentation: CodePresentationType = Field(
        ..., description="Presentation cohort identifier"
    )
    gender: GenderType = Field(..., description="Student gender (M/F)")
    region: RegionType = Field(..., description="Geographical region")
    highest_education: HighestEducationType = Field(
        ..., description="Highest prior education level attained"
    )
    imd_band: ImdBandType = Field(
        ..., description="Index of Multiple Deprivation decile band"
    )
    age_band: AgeBandType = Field(
        ..., description="Student age cohort at course commencement"
    )
    disability: DisabilityType = Field(
        ..., description="Disability indicator (Y/N)"
    )

    # 44 Numerical fields
    num_of_prev_attempts: int = Field(
        ..., ge=0, description="Number of previous module attempts"
    )
    studied_credits: int = Field(
        ..., ge=0, description="Total credits currently being studied"
    )
    date_registration: float = Field(
        ..., description="Day of course registration relative to start"
    )
    module_presentation_length: int = Field(
        ..., gt=0, description="Total planned duration of the module in days"
    )
    assessments_submitted_week10: int = Field(
        ..., ge=0, description="Assessments submitted up to week 10"
    )
    average_score_week10: float = Field(
        ..., ge=0.0, le=100.0, description="Mean assessment score up to week 10"
    )
    highest_score_week10: float = Field(
        ..., ge=0.0, le=100.0, description="Highest assessment score up to week 10"
    )
    average_submission_day_week10: float = Field(
        ..., description="Average submission day relative to module start"
    )
    banked_assessment_count_week10: int = Field(
        ..., ge=0, description="Count of transferred/banked assessments"
    )
    tma_count_week10: int = Field(
        ..., ge=0, description="Tutor Marked Assessments submitted up to week 10"
    )
    cma_count_week10: int = Field(
        ..., ge=0, description="Computer Marked Assessments submitted up to week 10"
    )
    exam_count_week10: int = Field(
        ..., ge=0, description="Exams submitted up to week 10"
    )
    assessment_weight_week10: float = Field(
        ..., ge=0.0, description="Total assessment weight submitted up to week 10"
    )
    weighted_average_score_week10: float = Field(
        ..., ge=0.0, description="Weighted average score up to week 10"
    )
    total_clicks_week10: int = Field(
        ..., ge=0, description="Total VLE interaction clicks up to week 10"
    )
    first_vle_activity_day: float = Field(
        ..., description="First day of VLE activity relative to module start"
    )
    last_vle_activity_day_week10: float = Field(
        ..., description="Last day of VLE activity up to week 10"
    )
    active_vle_days_week10: int = Field(
        ..., ge=0, description="Distinct days with VLE activity up to week 10"
    )
    unique_vle_sites_week10: int = Field(
        ..., ge=0, description="Distinct VLE resources/materials accessed"
    )
    dataplus_clicks_week10: int = Field(..., ge=0)
    dualpane_clicks_week10: int = Field(..., ge=0)
    externalquiz_clicks_week10: int = Field(..., ge=0)
    forumng_clicks_week10: int = Field(..., ge=0)
    glossary_clicks_week10: int = Field(..., ge=0)
    homepage_clicks_week10: int = Field(..., ge=0)
    htmlactivity_clicks_week10: int = Field(..., ge=0)
    oucollaborate_clicks_week10: int = Field(..., ge=0)
    oucontent_clicks_week10: int = Field(..., ge=0)
    ouelluminate_clicks_week10: int = Field(..., ge=0)
    ouwiki_clicks_week10: int = Field(..., ge=0)
    page_clicks_week10: int = Field(..., ge=0)
    questionnaire_clicks_week10: int = Field(..., ge=0)
    quiz_clicks_week10: int = Field(..., ge=0)
    repeatactivity_clicks_week10: int = Field(..., ge=0)
    resource_clicks_week10: int = Field(..., ge=0)
    sharedsubpage_clicks_week10: int = Field(..., ge=0)
    subpage_clicks_week10: int = Field(..., ge=0)
    url_clicks_week10: int = Field(..., ge=0)
    has_assessment_activity_week10: int = Field(
        ..., ge=0, le=1, description="Binary flag: submitted any assessment by week 10"
    )
    has_vle_activity_week10: int = Field(
        ..., ge=0, le=1, description="Binary flag: engaged with VLE by week 10"
    )
    vle_engagement_consistency_week10: float = Field(
        ..., ge=0.0, description="Consistency metric of VLE interactions"
    )
    score_range_week10: float = Field(
        ..., ge=0.0, description="Score spread/range across week 10 assessments"
    )
    late_submission_ratio_week10: float = Field(
        ..., ge=0.0, description="Ratio of late assessment submissions"
    )
    clicks_per_site_week10: float = Field(
        ..., ge=0.0, description="Average clicks per visited VLE site"
    )


class RootResponse(BaseModel):
    """Response model for root health endpoint."""

    name: str
    version: str
    status: str


class HealthResponse(BaseModel):
    """Response model for /health endpoint."""

    status: str
    model_loaded: bool
    preprocessor_loaded: bool
    label_encoder_loaded: bool
    raw_feature_count: int
    processed_feature_count: int
    classes: List[str]


class PredictionResponse(BaseModel):
    """Response model for /predict endpoint."""

    predicted_outcome: str
    confidence: float
    probabilities: Dict[str, float]
    withdrawal_probability: float
    risk_level: str
    advisor_message: str
