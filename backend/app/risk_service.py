"""Risk assessment service for academic advisors.

Maps predicted withdrawal probabilities to supportive, non-punitive risk bands
and advisor-facing decision-support guidance.
"""

from typing import Tuple


def evaluate_withdrawal_risk(withdrawal_probability: float) -> Tuple[str, str]:
    """Evaluate withdrawal probability and return a supportive risk tier and advisory message.

    Thresholds:
      - Low: < 0.30
      - Moderate: 0.30 <= p < 0.60
      - High: >= 0.60

    Returns:
      Tuple[str, str]: (risk_level, advisor_message)
    """
    if withdrawal_probability < 0.30:
        risk_level = "Low"
        advisor_message = (
            "Current predicted withdrawal risk is low. Continue normal academic monitoring."
        )
    elif withdrawal_probability < 0.60:
        risk_level = "Moderate"
        advisor_message = (
            "This student shows a moderate predicted withdrawal risk. "
            "Consider reviewing engagement and assessment progress."
        )
    else:
        risk_level = "High"
        advisor_message = (
            "This student shows a high predicted withdrawal risk and may "
            "benefit from early academic support and outreach."
        )

    return risk_level, advisor_message
