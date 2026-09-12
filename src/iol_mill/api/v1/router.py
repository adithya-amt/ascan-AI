"""Aggregates all v1 routers. Register new resources here."""

from fastapi import APIRouter

from iol_mill.api.v1 import jobs

router = APIRouter()
router.include_router(jobs.router)
