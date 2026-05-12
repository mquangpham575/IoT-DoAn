from typing import Any


def calculate_edge_assessment(sensor_data: dict[str, Any]) -> dict[str, Any]:
    """
    Server-side edge logic.

    This function evaluates environmental comfort and health risk using
    deterministic rules. It is suitable for IoT coursework because the logic
    is explainable, testable, and easy to demo without real hardware.
    """
    temperature = float(sensor_data["temperature"])
    humidity = float(sensor_data["humidity"])
    gas = int(sensor_data["gas"])
    light = float(sensor_data["light"])
    noise = int(sensor_data["noise"])

    risk_score = 0
    reasons: list[str] = []
    critical_flag = False

    # Temperature rules
    if temperature > 40:
        risk_score += 35
        reasons.append("Critical temperature level")
        critical_flag = True
    elif temperature > 35:
        risk_score += 20
        reasons.append("High temperature")
    elif temperature < 18:
        risk_score += 10
        reasons.append("Low temperature")

    # Humidity rules
    if humidity > 90:
        risk_score += 20
        reasons.append("Very high humidity")
    elif humidity > 85:
        risk_score += 15
        reasons.append("High humidity")
    elif humidity < 30:
        risk_score += 10
        reasons.append("Low humidity")

    # Gas / air quality rules
    if gas > 3000:
        risk_score += 40
        reasons.append("Critical gas concentration")
        critical_flag = True
    elif gas > 2000:
        risk_score += 25
        reasons.append("Poor air quality / high gas concentration")
    elif gas > 1200:
        risk_score += 10
        reasons.append("Moderate air quality risk")

    # Light rules
    if light < 10:
        risk_score += 15
        reasons.append("Extremely low light")
    elif light < 50:
        risk_score += 8
        reasons.append("Low light")

    # Noise rules
    if noise > 3000:
        risk_score += 20
        reasons.append("High noise level")
    elif noise > 2000:
        risk_score += 10
        reasons.append("Moderate noise level")

    # Compound risk: multiple abnormal indicators at the same time
    if len(reasons) >= 3:
        risk_score += 10
        reasons.append("Multiple abnormal environmental indicators")

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
    }
