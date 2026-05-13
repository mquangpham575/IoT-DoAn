from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routers import dashboard_router, device_router, sensor_router, system_router
from app.services.mqtt_service import start_mqtt_subscriber, stop_mqtt_subscriber


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Backend API for IoT environmental health monitoring system.",
    )

    # Helps significantly on slow/mobile networks by compressing HTML/JSON responses.
    app.add_middleware(GZipMiddleware, minimum_size=500)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if settings.STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

    app.include_router(dashboard_router.router)
    app.include_router(sensor_router.router)
    app.include_router(sensor_router.legacy_router)
    app.include_router(device_router.router)
    app.include_router(system_router.router)

    @app.on_event("startup")
    async def on_startup() -> None:
        init_db()
        app.state.last_seen = 0
        app.state.mqtt_client = start_mqtt_subscriber()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        stop_mqtt_subscriber(getattr(app.state, "mqtt_client", None))

    return app


app = create_app()
