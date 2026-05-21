from typing import Any

from app.services.alert_service import build_recommendation
from app.services.edge_service import calculate_edge_assessment
from app.utils.time_utils import now_local_string
from app.config import settings
import joblib
import pandas as pd
import os

# Load ML model once at startup
model = None
if settings.MODEL_PATH.exists():
    try:
        model = joblib.load(settings.MODEL_PATH)
    except Exception as e:
        print(f"Error loading AI model: {e}")


def evaluate_sensor_reading(sensor_data: dict[str, Any]) -> dict[str, Any]:
    """
    Combine raw sensor data with edge assessment and recommendation.

    Future extension:
    - Add ML model prediction here.
    - Combine ML prediction with rule-based result.
    - Keep rule-based fallback for safety.
    """
    assessment = calculate_edge_assessment(sensor_data)
    
    # ML Prediction Integration
    ai_comfort = -1
    if model:
        try:
            # Match training feature set: temp, humid, gas, light, noise
            input_df = pd.DataFrame([[
                sensor_data.get("temperature", 0),
                sensor_data.get("humidity", 0),
                sensor_data.get("gas", 0),
                sensor_data.get("light", 0),
                sensor_data.get("noise", 0)
            ]], columns=['temp', 'humid', 'gas', 'light', 'noise'])
            ai_comfort = int(model.predict(input_df)[0])
        except Exception as e:
            print(f"AI Prediction error: {e}")

    # Combine Hybrid results: Use the highest risk level detected
    final_comfort = max(assessment["comfort_level"], ai_comfort)
    
    if final_comfort != assessment["comfort_level"]:
        # Update labels if AI escalated the risk
        status_map = {0: "NORMAL", 1: "WARNING", 2: "CRITICAL"}
        assessment["comfort_level"] = final_comfort
        assessment["status_label"] = status_map.get(final_comfort, "UNKNOWN")
        assessment["reasons"].append("AI Anomaly Detection")

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
