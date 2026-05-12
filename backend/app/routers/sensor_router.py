from fastapi import APIRouter, Header, HTTPException, Query

from app.config import settings
from app.database import get_latest_reading, get_reading_history, insert_sensor_reading
from app.schemas import ApiResponse, SensorReadingCreate
from app.services.comfort_service import evaluate_sensor_reading
from app.utils.response_utils import success_response


router = APIRouter(prefix="/api/v1/sensor", tags=["Sensor"])
legacy_router = APIRouter(tags=["Legacy"])


def _payload_to_dict(payload: SensorReadingCreate) -> dict:
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    return payload.dict()


def _validate_api_key(x_api_key: str | None) -> None:
    if settings.REQUIRE_API_KEY and x_api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


def _process_sensor_reading(payload: SensorReadingCreate) -> dict:
    raw_data = _payload_to_dict(payload)
    processed = evaluate_sensor_reading(raw_data)
    new_id = insert_sensor_reading(processed)
    processed["id"] = new_id
    return processed


@router.post("/readings", response_model=ApiResponse)
async def create_sensor_reading(
    payload: SensorReadingCreate,
    x_api_key: str | None = Header(default=None, alias="X-API-KEY"),
):
    """
    Main API for ESP32/simulator to send sensor data.
    """
    _validate_api_key(x_api_key)
    processed = _process_sensor_reading(payload)
    return success_response(data=processed, message="Sensor reading saved")


@router.get("/latest", response_model=ApiResponse)
def read_latest_sensor_reading():
    latest = get_latest_reading()
    return success_response(data=latest, message="Latest sensor reading")


@router.get("/history", response_model=ApiResponse)
def read_sensor_history(limit: int = Query(default=50, ge=1, le=500)):
    history = get_reading_history(limit=limit)
    return success_response(data=history, message="Sensor reading history")


# Backward-compatible endpoints for the old dashboard/simulator.
@legacy_router.post("/data")
async def legacy_create_sensor_reading(
    payload: SensorReadingCreate,
    x_api_key: str | None = Header(default=None, alias="X-API-KEY"),
):
    _validate_api_key(x_api_key)
    processed = _process_sensor_reading(payload)
    return {
        "status": "success",
        "comfort": processed["comfort_level"],
        "method": "rule_based_edge",
        "risk_score": processed["risk_score"],
        "status_label": processed["status_label"],
        "reasons": processed["reasons"],
        "recommendation": processed["recommendation"],
    }


@legacy_router.get("/history")
def legacy_read_history(limit: int = Query(default=50, ge=1, le=500)):
    """
    Keep old format as a list so the existing dashboard can still run.
    """
    history = get_reading_history(limit=limit)

    legacy_rows = []
    for item in history:
        legacy_rows.append(
            {
                "id": item["id"],
                "device_id": item["device_id"],
                "temp": item["temperature"],
                "humid": item["humidity"],
                "gas": item["gas"],
                "light": item["light"],
                "noise": item["noise"],
                "comfort_level": item["comfort_level"],
                "status_label": item["status_label"],
                "risk_score": item["risk_score"],
                "reasons": item["reasons"],
                "recommendation": item["recommendation"],
                "timestamp": item["created_at"],
                "method": "rule_based_edge",
            }
        )

    return legacy_rows
