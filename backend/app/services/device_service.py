from app.config import settings


def get_default_device() -> dict:
    """
    Minimal device metadata for demo.

    This can be expanded later when the project supports multiple ESP32 nodes.
    """
    return {
        "device_id": settings.DEFAULT_DEVICE_ID,
        "name": "ESP32 Environment Node",
        "type": "ESP32",
        "status": "configured",
    }
