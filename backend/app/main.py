"""FastAPI application entrypoint for the University Student Dropout Risk Prediction System."""

from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.model_service import model_service
from app.schemas import (
    HealthResponse,
    PredictionResponse,
    RootResponse,
    StudentRawInput,
)

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Load machine-learning deployment artifacts when the API starts."""

    logger.info("Initializing model service and loading artifacts...")

    try:
        model_service.load_artifacts()
        logger.info("All deployment artifacts loaded successfully.")

    except Exception as e:
        logger.error(
            f"Failed to load deployment artifacts: {e}",
            exc_info=True,
        )

    yield

    logger.info("Application shutting down.")


app = FastAPI(
    title="University Student Dropout Risk Prediction System",
    description=(
        "Backend decision-support API for academic advisors predicting student "
        "outcomes and withdrawal risk using week-10 early-semester data."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------
# Allows the local React/Vite frontend to communicate
# with the FastAPI backend during development.

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Validation Error Handler
# ---------------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request,
    exc: RequestValidationError,
):
    """Return clean validation errors without exposing stack traces."""

    errors = []

    for error in exc.errors():

        field_loc = " -> ".join(
            [
                str(loc)
                for loc in error.get("loc", [])
                if loc != "body"
            ]
        )

        errors.append(
            {
                "field": field_loc or "body",
                "message": error.get(
                    "msg",
                    "Invalid value",
                ),
                "type": error.get(
                    "type",
                    "value_error",
                ),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": (
                "Input validation error: "
                "please verify student raw input fields."
            ),
            "errors": errors,
        },
    )


# ---------------------------------------------------------
# Generic Error Handler
# ---------------------------------------------------------

@app.exception_handler(Exception)
async def generic_exception_handler(
    request,
    exc: Exception,
):
    """Prevent raw Python stack traces from being exposed."""

    logger.error(
        f"Unhandled server error: {exc}",
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": (
                "An internal server error occurred "
                "while processing the request."
            )
        },
    )


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@app.get(
    "/",
    response_model=RootResponse,
    summary="Root service status",
    tags=["Status"],
)
async def root() -> RootResponse:
    """Return API identity and running status."""

    return RootResponse(
        name="University Student Dropout Risk Prediction API",
        version="1.0.0",
        status="running",
    )


# ---------------------------------------------------------
# Health Endpoint
# ---------------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Model and service health check",
    tags=["Status"],
)
async def health() -> HealthResponse:
    """Check whether all machine-learning artifacts are loaded."""

    if not model_service.is_loaded:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Model service is uninitialized or "
                "deployment artifacts failed to load."
            ),
        )

    health_info = model_service.get_health_status()

    return HealthResponse(
        **health_info
    )


# ---------------------------------------------------------
# Prediction Endpoint
# ---------------------------------------------------------

@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict student final outcome and withdrawal risk",
    tags=["Prediction"],
)
async def predict(
    student_input: StudentRawInput,
) -> PredictionResponse:
    """
    Receive 52 raw student features available up to week 10
    and return the predicted outcome and withdrawal-risk assessment.

    Process:
    - Validate categorical levels and numerical constraints
    - Apply saved week-10 preprocessing
    - Transform raw input into 90 model features
    - Predict multiclass outcome using XGBoost
    - Obtain class probabilities
    - Calculate advisor-facing withdrawal-risk guidance
    """

    if not model_service.is_loaded:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Model service is currently unavailable."
            ),
        )

    try:

        raw_dict = student_input.model_dump()

        result = model_service.predict(
            raw_dict
        )

        return PredictionResponse(
            **result
        )

    except ValueError as ve:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Preprocessing or input validation error: "
                f"{str(ve)}"
            ),
        )

    except RuntimeError as re:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Prediction error: "
                f"{str(re)}"
            ),
        )