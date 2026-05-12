from pathlib import Path
import os


class Settings:
    """
    Central configuration for the IoT backend.

    Keep this file simple so the project is easy to run during demo.
    Values can be overridden by environment variables when needed.
    """

    APP_NAME = "IoT Health Monitoring Backend"
    APP_VERSION = "1.0.0"

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


settings = Settings()
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
