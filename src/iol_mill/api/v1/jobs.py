"""Mill jobs resource.

Backed by an in-memory store for now so the API shape can be exercised end to end.
Replace `JobStore` with a database-backed repository when persistence is added.
"""

from datetime import UTC, datetime
from typing import Annotated, Literal
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/jobs", tags=["jobs"])

JobStatus = Literal["queued", "running", "completed", "failed"]


class JobCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None


class Job(JobCreate):
    id: UUID
    status: JobStatus = "queued"
    created_at: datetime


class JobStore:
    """Process-local job storage."""

    def __init__(self) -> None:
        self._jobs: dict[UUID, Job] = {}

    def list(self) -> list[Job]:
        return sorted(self._jobs.values(), key=lambda j: j.created_at)

    def get(self, job_id: UUID) -> Job | None:
        return self._jobs.get(job_id)

    def create(self, data: JobCreate) -> Job:
        job = Job(id=uuid4(), created_at=datetime.now(UTC), **data.model_dump())
        self._jobs[job.id] = job
        return job

    def delete(self, job_id: UUID) -> bool:
        return self._jobs.pop(job_id, None) is not None

    def clear(self) -> None:
        self._jobs.clear()


_store = JobStore()


def get_store() -> JobStore:
    """Dependency hook. Tests override this to inject a fresh store."""
    return _store


StoreDep = Annotated[JobStore, Depends(get_store)]


@router.get("", response_model=list[Job])
async def list_jobs(store: StoreDep) -> list[Job]:
    return store.list()


@router.post("", response_model=Job, status_code=status.HTTP_201_CREATED)
async def create_job(data: JobCreate, store: StoreDep) -> Job:
    return store.create(data)


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: UUID, store: StoreDep) -> Job:
    job = store.get(job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: UUID, store: StoreDep) -> None:
    if not store.delete(job_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
