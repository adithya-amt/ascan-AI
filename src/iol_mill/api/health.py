"""Liveness and readiness endpoints, unversioned so orchestrators can rely on them."""

from fastapi import APIRouter
from pydantic import BaseModel

from iol_mill import __version__

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)
