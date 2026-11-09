"""Application entry point: `uvicorn app.main:app`."""

import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config import Settings, get_settings
from app.db import Database
from app.logging_config import setup_logging
from app.routes import drops, health
from app.seed import seed_if_empty

logger = logging.getLogger("app")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    setup_logging(settings.log_level)
    db = Database(settings.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        db.create_schema()
        if settings.seed_demo_data:
            with db.session_factory() as session:
                seed_if_empty(session)
        logger.info("DropZone API started", extra={"version": __version__})
        yield
        db.engine.dispose()

    app = FastAPI(title="DropZone API", version=__version__, lifespan=lifespan)
    app.state.db = db

    if settings.cors_origin_list:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origin_list,
            allow_methods=["GET", "POST"],
            allow_headers=["Content-Type"],
        )

    @app.middleware("http")
    async def access_log(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        # Health checks and scrapes run every few seconds: keep them out of the INFO logs.
        quiet = request.url.path.startswith(("/health", "/metrics"))
        logger.log(
            logging.DEBUG if quiet else logging.INFO,
            "request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round((time.perf_counter() - start) * 1000, 1),
            },
        )
        return response

    app.include_router(health.router)
    app.include_router(drops.router)
    return app


app = create_app()
