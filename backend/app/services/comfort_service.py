from typing import Any

from app.services.alert_service import build_recommendation
from app.services.edge_service import calculate_edge_assessment
from app.utils.time_utils import now_local_string


def evaluate_sensor_reading(sensor_data: dict[str, Any]) -> dict[str, Any]:
    """
    Combine raw sensor data with edge assessment and recommendation.

    Future extension:
    - Add ML model prediction here.
    - Combine ML prediction with rule-based result.
    - Keep rule-based fallback for safety.
    """
    assessment = calculate_edge_assessment(sensor_data)
    recommendation = build_recommendation(
        reasons=assessment["reasons"],
        status_label=assessment["status_label"],
    )

    return {
        **sensor_data,
        **assessment,
        "recommendation": recommendation,
        "created_at": now_local_string(),
    }
