import time
from typing import Any

from app.config import settings
from app.services.discord_service import send_discord_alert


_last_alert_sent: dict[str, float] = {}


def _cooldown_key(reading: dict[str, Any]) -> str:
    return f"{reading.get('device_id', 'unknown')}:{reading.get('status_label', 'UNKNOWN')}"


def notify_if_needed(reading: dict[str, Any]) -> dict[str, Any]:
    """
    Notify external channels when the reading is WARNING or CRITICAL.

    Cooldown prevents spamming Discord when sensor data is sent frequently.
    """
    status_label = reading.get("status_label")

    if status_label not in {"WARNING", "CRITICAL"}:
        return {"sent": False, "reason": "status_not_alertable"}

    if not settings.ENABLE_DISCORD_ALERT:
        return {"sent": False, "reason": "discord_disabled"}

    key = _cooldown_key(reading)
    now = time.time()
    last_sent = _last_alert_sent.get(key, 0)

    if now - last_sent < settings.ALERT_COOLDOWN_SECONDS:
        return {"sent": False, "reason": "cooldown_active"}

    sent = send_discord_alert(reading)

    if sent:
        _last_alert_sent[key] = now
        return {"sent": True, "reason": "discord_sent"}

    return {"sent": False, "reason": "discord_failed"}
