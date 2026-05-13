from typing import Any

from pydantic import BaseModel, Field

from app.config import settings


class SensorReadingCreate(BaseModel):
    """
    Payload sent by ESP32 or simulator.

    Field names are intentionally explicit so firmware, backend, and mobile
    can share the same API contract.
    """

    device_id: str = Field(default=settings.DEFAULT_DEVICE_ID, min_length=1)
    temperature: float = Field(..., ge=-20, le=80)
    humidity: float = Field(..., ge=0, le=100)
    gas: int = Field(..., ge=0)
    light: float = Field(..., ge=0)
    noise: int = Field(..., ge=0)


class SensorReadingOut(BaseModel):
    id: int | None = None
    device_id: str
    temperature: float
    humidity: float
    gas: int
    light: float
    noise: int
    comfort_level: int
    status_label: str
    risk_score: int
    reasons: list[str]
    recommendation: str
    created_at: str


class ApiResponse(BaseModel):
    status: str
    data: Any | None = None
    message: str | None = None


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    database: str
    device: str
