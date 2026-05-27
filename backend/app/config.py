from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from the root directory .env file
root_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=root_env_path)


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
    MODEL_PATH = BACKEND_DIR / "comfort_model.pkl"

    DASHBOARD_TOKEN = os.getenv("DASHBOARD_TOKEN", "umacore_secret")

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

    # Threshold settings for comfort evaluation
    TEMP_CRITICAL = float(os.getenv("TEMP_CRITICAL", "40.0"))
    TEMP_HIGH = float(os.getenv("TEMP_HIGH", "35.0"))
    TEMP_LOW = float(os.getenv("TEMP_LOW", "18.0"))

    HUMID_VERY_HIGH = float(os.getenv("HUMID_VERY_HIGH", "90.0"))
    HUMID_HIGH = float(os.getenv("HUMID_HIGH", "85.0"))
    HUMID_LOW = float(os.getenv("HUMID_LOW", "30.0"))

    GAS_CRITICAL = int(os.getenv("GAS_CRITICAL", "3000"))
    GAS_HIGH = int(os.getenv("GAS_HIGH", "2000"))
    GAS_MODERATE = int(os.getenv("GAS_MODERATE", "1200"))

    LIGHT_EXTREMELY_LOW = float(os.getenv("LIGHT_EXTREMELY_LOW", "10.0"))
    LIGHT_LOW = float(os.getenv("LIGHT_LOW", "50.0"))

    NOISE_HIGH = int(os.getenv("NOISE_HIGH", "3000"))
    NOISE_MODERATE = int(os.getenv("NOISE_MODERATE", "2000"))


settings = Settings()
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
