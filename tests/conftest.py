from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from iol_mill.api.v1.jobs import JobStore, get_store
from iol_mill.config import Settings
from iol_mill.main import create_app


@pytest.fixture
def settings() -> Settings:
    return Settings(environment="test", debug=False)


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    app = create_app(settings)
    store = JobStore()
    app.dependency_overrides[get_store] = lambda: store
    with TestClient(app) as c:
        yield c
