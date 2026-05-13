from fastapi import APIRouter

from app.services.device_service import get_default_device
from app.utils.response_utils import success_response


router = APIRouter(prefix="/api/v1/devices", tags=["Device"])


@router.get("/default")
def read_default_device():
    return success_response(data=get_default_device(), message="Default device metadata")
