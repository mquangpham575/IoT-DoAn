import json
import logging
import time
from typing import Any

from pydantic import ValidationError

from app.config import settings
from app.database import insert_sensor_reading
from app.schemas import SensorReadingCreate
from app.services.comfort_service import evaluate_sensor_reading
from app.services.notification_service import notify_if_needed

logger = logging.getLogger(__name__)


def _payload_to_dict(payload: SensorReadingCreate) -> dict[str, Any]:
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    return payload.dict()


def _create_mqtt_client():
    import paho.mqtt.client as mqtt

    try:
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=settings.MQTT_CLIENT_ID,
        )
    except Exception:
        client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID)

    if settings.MQTT_USERNAME:
        client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD or None)

    return client


def _handle_sensor_payload(payload_dict: dict[str, Any]) -> None:
    payload = SensorReadingCreate(**payload_dict)
    raw_data = _payload_to_dict(payload)

    processed = evaluate_sensor_reading(raw_data)
    processed["source"] = "mqtt"

    new_id = insert_sensor_reading(processed)
    processed["id"] = new_id

    notify_if_needed(processed)

    logger.info(
        "MQTT reading saved: device=%s status=%s risk=%s",
        processed.get("device_id"),
        processed.get("status_label"),
        processed.get("risk_score"),
    )


def start_mqtt_subscriber(app=None):
    """
    Start MQTT subscriber in a background network loop.

    Expected MQTT payload uses the same schema as HTTP API:
    {
      "device_id": "esp32_01",
      "temperature": 30.5,
      "humidity": 72.0,
      "gas": 1250,
      "light": 650,
      "noise": 320
    }
    """
    if not settings.ENABLE_MQTT:
        logger.info("MQTT subscriber disabled.")
        return None

    client = _create_mqtt_client()

    def on_connect(client, userdata, flags, reason_code, *extra):
        if str(reason_code) in {"0", "Success"} or reason_code == 0:
            logger.info("Connected to MQTT broker at %s:%s", settings.MQTT_HOST, settings.MQTT_PORT)
            client.subscribe(settings.MQTT_TOPIC)
            logger.info("Subscribed to MQTT topic: %s", settings.MQTT_TOPIC)
        else:
            logger.error("MQTT connection failed: %s", reason_code)

    def on_message(client, userdata, message):
        try:
            raw_payload = message.payload.decode("utf-8")
            payload_dict = json.loads(raw_payload)
            _handle_sensor_payload(payload_dict)
            if app is not None:
                app.state.last_seen = time.time()
        except json.JSONDecodeError:
            logger.exception("Invalid MQTT JSON payload on topic %s.", message.topic)
        except ValidationError:
            logger.exception("Invalid MQTT sensor schema on topic %s.", message.topic)
        except Exception:
            logger.exception("Unexpected MQTT processing error on topic %s.", message.topic)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect_async(settings.MQTT_HOST, settings.MQTT_PORT, keepalive=60)
        client.loop_start()
        logger.info("MQTT subscriber loop started.")
        return client
    except Exception:
        logger.exception("Failed to start MQTT subscriber.")
        return None


def stop_mqtt_subscriber(client) -> None:
    if client is None:
        return

    try:
        client.loop_stop()
        client.disconnect()
        logger.info("MQTT subscriber stopped.")
    except Exception:
        logger.exception("Failed to stop MQTT subscriber cleanly.")
