from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routers import dashboard_router, device_router, sensor_router, system_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Backend API for IoT environmental health monitoring system.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_db()

    if settings.STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

    app.include_router(dashboard_router.router)
    app.include_router(sensor_router.router)
    app.include_router(sensor_router.legacy_router)
    app.include_router(device_router.router)
    app.include_router(system_router.router)

    return app


app = create_app()
