import logging
from typing import Any

import requests

from app.config import settings

logger = logging.getLogger(__name__)


def send_discord_alert(reading: dict[str, Any]) -> bool:
    """
    Send WARNING/CRITICAL alert to Discord via webhook.

    The webhook URL must be provided through environment variable:
    DISCORD_WEBHOOK_URL
    """
    if not settings.ENABLE_DISCORD_ALERT:
        return False

    if not settings.DISCORD_WEBHOOK_URL:
        logger.warning("Discord alert is enabled but DISCORD_WEBHOOK_URL is empty.")
        return False

    status_label = reading.get("status_label", "UNKNOWN")
    risk_score = reading.get("risk_score", 0)
    device_id = reading.get("device_id", "unknown-device")
    created_at = reading.get("created_at", "unknown-time")
    reasons = reading.get("reasons", [])
    recommendation = reading.get("recommendation", "")

    color = 0xEF4444 if status_label == "CRITICAL" else 0xF59E0B

    payload = {
        "username": "IoT Health Monitor",
        "content": f"🚨 IoT {status_label} alert from `{device_id}`",
        "embeds": [
            {
                "title": f"{status_label} · Risk Score {risk_score}/100",
                "description": recommendation or "No recommendation generated.",
                "color": color,
                "fields": [
                    {"name": "Device", "value": str(device_id), "inline": True},
                    {"name": "Time", "value": str(created_at), "inline": True},
                    {"name": "Temperature", "value": f"{reading.get('temperature')} °C", "inline": True},
                    {"name": "Humidity", "value": f"{reading.get('humidity')} %", "inline": True},
                    {"name": "Gas", "value": str(reading.get("gas")), "inline": True},
                    {"name": "Light", "value": str(reading.get("light")), "inline": True},
                    {"name": "Noise", "value": str(reading.get("noise")), "inline": True},
                    {
                        "name": "Detected reasons",
                        "value": "\n".join([f"- {reason}" for reason in reasons]) or "No reason provided.",
                        "inline": False,
                    },
                ],
            }
        ],
    }

    try:
        response = requests.post(settings.DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code >= 400:
            logger.error(
                "Discord webhook error: %s - %s", 
                response.status_code, 
                response.text
            )
            return False
        
        logger.info("Discord alert sent for %s with status %s.", device_id, status_label)
        return True
    except requests.RequestException as exc:
        logger.error("Network error sending Discord alert: %s", exc)
        return False
