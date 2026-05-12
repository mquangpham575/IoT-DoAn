from pathlib import Path
import os


class Settings:
    """
    Central configuration for the IoT backend.

    Keep secrets in environment variables or .env files.
    Do not commit real webhook URLs or production credentials.
    """

    APP_NAME = "IoT Health Monitoring Backend"
    APP_VERSION = "1.1.0"

    HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
    PORT = int(os.getenv("BACKEND_PORT", "8000"))

    API_KEY = os.getenv("IOT_API_KEY", "IOT_SECRET_2026")
    REQUIRE_API_KEY = os.getenv("REQUIRE_API_KEY", "true").lower() == "true"

    BACKEND_DIR = Path(__file__).resolve().parents[1]
    DATA_DIR = BACKEND_DIR / "data"
    DB_PATH = DATA_DIR / "iot_data.db"

    TEMPLATES_DIR = BACKEND_DIR / "templates"
    STATIC_DIR = BACKEND_DIR / "static"

    DEFAULT_DEVICE_ID = "esp32_01"

    # Discord alert configuration
    ENABLE_DISCORD_ALERT = os.getenv("ENABLE_DISCORD_ALERT", "false").lower() == "true"
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
    ALERT_COOLDOWN_SECONDS = int(os.getenv("ALERT_COOLDOWN_SECONDS", "60"))

    # MQTT configuration
    ENABLE_MQTT = os.getenv("ENABLE_MQTT", "false").lower() == "true"
    MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
    MQTT_TOPIC = os.getenv("MQTT_TOPIC", "iot/+/sensor")
    MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "iot-health-backend")
    MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")


settings = Settings()
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
