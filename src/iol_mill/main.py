"""FastAPI application factory and entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from iol_mill import __version__
from iol_mill.api.health import router as health_router
from iol_mill.api.v1.router import router as v1_router
from iol_mill.config import Settings, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup and shutdown hooks. Open shared resources here later."""
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the application. Accepts settings so tests can override them."""
    settings = settings or get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        debug=settings.debug,
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.include_router(health_router)
    app.include_router(v1_router, prefix=settings.api_prefix)
    return app


app = create_app()


def run() -> None:
    """Console-script entry point used by `iol-mill`."""
    settings = get_settings()
    uvicorn.run(
        "iol_mill.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level,
    )


if __name__ == "__main__":
    run()
