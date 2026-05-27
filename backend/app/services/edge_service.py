from typing import Any
from app.config import settings


def calculate_edge_assessment(sensor_data: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluate environmental comfort and health risk using configurable settings thresholds
    and return structured reason codes for decoupled notifications.
    """
    temperature = float(sensor_data["temperature"])
    humidity = float(sensor_data["humidity"])
    gas = int(sensor_data["gas"])
    light = float(sensor_data["light"])
    noise = int(sensor_data["noise"])

    risk_score = 0
    reasons: list[str] = []
    reason_codes: list[str] = []
    critical_flag = False

    # Temperature rules
    if temperature > settings.TEMP_CRITICAL:
        risk_score += 35
        reasons.append("Critical temperature level")
        reason_codes.append("temp_critical")
        critical_flag = True
    elif temperature > settings.TEMP_HIGH:
        risk_score += 20
        reasons.append("High temperature")
        reason_codes.append("temp_high")
    elif temperature < settings.TEMP_LOW:
        risk_score += 10
        reasons.append("Low temperature")
        reason_codes.append("temp_low")

    # Humidity rules
    if humidity > settings.HUMID_VERY_HIGH:
        risk_score += 20
        reasons.append("Very high humidity")
        reason_codes.append("humid_very_high")
    elif humidity > settings.HUMID_HIGH:
        risk_score += 15
        reasons.append("High humidity")
        reason_codes.append("humid_high")
    elif humidity < settings.HUMID_LOW:
        risk_score += 10
        reasons.append("Low humidity")
        reason_codes.append("humid_low")

    # Gas / air quality rules
    if gas > settings.GAS_CRITICAL:
        risk_score += 40
        reasons.append("Critical gas concentration")
        reason_codes.append("gas_critical")
        critical_flag = True
    elif gas > settings.GAS_HIGH:
        risk_score += 25
        reasons.append("Poor air quality / high gas concentration")
        reason_codes.append("gas_high")
    elif gas > settings.GAS_MODERATE:
        risk_score += 10
        reasons.append("Moderate air quality risk")
        reason_codes.append("gas_moderate")

    # Light rules
    if light < settings.LIGHT_EXTREMELY_LOW:
        risk_score += 15
        reasons.append("Extremely low light")
        reason_codes.append("light_extremely_low")
    elif light < settings.LIGHT_LOW:
        risk_score += 8
        reasons.append("Low light")
        reason_codes.append("light_low")

    # Noise rules
    if noise > settings.NOISE_HIGH:
        risk_score += 20
        reasons.append("High noise level")
        reason_codes.append("noise_high")
    elif noise > settings.NOISE_MODERATE:
        risk_score += 10
        reasons.append("Moderate noise level")
        reason_codes.append("noise_moderate")

    # Compound risk: multiple abnormal indicators at the same time
    if len(reasons) >= 3:
        risk_score += 10
        reasons.append("Multiple abnormal environmental indicators")
        reason_codes.append("multiple_abnormal")

    risk_score = max(0, min(risk_score, 100))

    if critical_flag or risk_score >= 75:
        comfort_level = 2
        status_label = "CRITICAL"
    elif risk_score >= 25 or reasons:
        comfort_level = 1
        status_label = "WARNING"
    else:
        comfort_level = 0
        status_label = "NORMAL"
        reasons = ["All monitored indicators are within acceptable range"]

    return {
        "comfort_level": comfort_level,
        "status_label": status_label,
        "risk_score": risk_score,
        "reasons": reasons,
        "reason_codes": reason_codes,
    }
