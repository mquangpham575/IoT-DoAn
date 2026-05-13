from fastapi import APIRouter, Request
import time

from app.config import settings
from app.database import get_connection
from app.schemas import HealthResponse


router = APIRouter(prefix="/api/v1/system", tags=["System"])


@router.get("/health", response_model=HealthResponse)
def health_check(request: Request):
    database_status = "ok"
    
    # Check device heartbeat
    last_seen = getattr(request.app.state, "last_seen", 0)
    device_status = "online" if (time.time() - last_seen) < 45 else "offline"

    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
    except Exception:
        database_status = "error"

    return {
        "status": "ok" if database_status == "ok" else "degraded",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": database_status,
        "device": device_status,
    }
