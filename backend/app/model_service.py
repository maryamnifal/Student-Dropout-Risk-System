"""Model service module.

Handles loading deployment artifacts, transforming raw student inputs,
and generating predictions using the trained XGBoost pipeline.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import joblib
import pandas as pd

from app.risk_service import evaluate_withdrawal_risk


class ModelService:
    """Singleton service to load model artifacts and execute inference."""

    def __init__(self, models_dir: Optional[Path] = None) -> None:
        if models_dir is None:
            # Default to backend/models relative to this file
            self.models_dir = Path(__file__).resolve().parent.parent / "models"
        else:
            self.models_dir = Path(models_dir)

        self.model: Optional[Any] = None
        self.preprocessor: Optional[Any] = None
        self.label_encoder: Optional[Any] = None
        self.processed_feature_names: List[str] = []
        self.raw_feature_names: List[str] = []
        self.classes: List[str] = []
        self.is_loaded: bool = False

    def load_artifacts(self) -> None:
        """Load all four deployment artifacts into memory."""
        model_path = self.models_dir / "final_xgboost_model.joblib"
        encoder_path = self.models_dir / "label_encoder.joblib"
        preprocessor_path = self.models_dir / "preprocessor_week10.joblib"
        feature_names_path = self.models_dir / "processed_feature_names.csv"

        for path in [model_path, encoder_path, preprocessor_path, feature_names_path]:
            if not path.exists():
                raise FileNotFoundError(f"Deployment artifact missing: {path}")

        # Load artifacts
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load(encoder_path)
        self.preprocessor = joblib.load(preprocessor_path)

        # Load processed feature names
        df_features = pd.read_csv(feature_names_path)
        self.processed_feature_names = df_features["Feature_Name"].tolist()

        # Cache class names and raw expected feature names
        self.classes = [str(cls) for cls in self.label_encoder.classes_]
        self.raw_feature_names = [str(col) for col in self.preprocessor.feature_names_in_]

        # Verify integrity
        if len(self.raw_feature_names) != 52:
            raise ValueError(
                f"Expected 52 raw features in preprocessor, got {len(self.raw_feature_names)}"
            )

        if len(self.processed_feature_names) != 90:
            raise ValueError(
                f"Expected 90 processed features in CSV, got {len(self.processed_feature_names)}"
            )

        self.is_loaded = True

    def get_health_status(self) -> Dict[str, Any]:
        """Return status information for health check endpoint."""
        return {
            "status": "healthy" if self.is_loaded else "unhealthy",
            "model_loaded": self.model is not None,
            "preprocessor_loaded": self.preprocessor is not None,
            "label_encoder_loaded": self.label_encoder is not None,
            "raw_feature_count": len(self.raw_feature_names),
            "processed_feature_count": len(self.processed_feature_names),
            "classes": self.classes,
        }

    def predict(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the full inference pipeline for a single student record.

        Pipeline:
          1. Validate and convert raw 52-feature input into a single-row DataFrame.
          2. Reorder columns to match preprocessor.feature_names_in_.
          3. Preprocess to obtain 90 transformed features.
          4. Call model.predict() and model.predict_proba().
          5. Decode class and assemble advisor risk assessment.
        """
        if not self.is_loaded:
            raise RuntimeError("ModelService artifacts are not loaded.")

        # 1 & 2: DataFrame creation and exact column alignment
        raw_df = pd.DataFrame([raw_input])
        raw_df = raw_df[self.raw_feature_names]

        # 3: Preprocess raw input
        try:
            transformed_features = self.preprocessor.transform(raw_df)
        except Exception as e:
            raise ValueError(f"Preprocessing failed on input data: {str(e)}") from e

        # 4: Verify transformed shape
        transformed_feature_count = transformed_features.shape[1]
        if transformed_feature_count != 90:
            raise ValueError(
                f"Expected 90 transformed features, but preprocessor produced {transformed_feature_count}"
            )

        # 5: Execute prediction
        try:
            preds = self.model.predict(transformed_features)
            probas = self.model.predict_proba(transformed_features)[0]
        except Exception as e:
            raise RuntimeError(f"Model prediction failed: {str(e)}") from e

        # 6: Decode outcome
        predicted_outcome = str(self.label_encoder.inverse_transform(preds)[0])

        # 7: Format probabilities mapping exact class order
        probabilities = {
            cls_name: round(float(prob), 4)
            for cls_name, prob in zip(self.classes, probas)
        }

        confidence = probabilities.get(predicted_outcome, 0.0)
        withdrawal_prob = probabilities.get("Withdrawn", 0.0)

        # 8: Evaluate supportive advisory risk tier
        risk_level, advisor_message = evaluate_withdrawal_risk(withdrawal_prob)

        return {
            "predicted_outcome": predicted_outcome,
            "confidence": confidence,
            "probabilities": probabilities,
            "withdrawal_probability": withdrawal_prob,
            "risk_level": risk_level,
            "advisor_message": advisor_message,
        }


# Global model service instance
model_service = ModelService()
