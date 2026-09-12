from uuid import uuid4

from fastapi.testclient import TestClient

BASE = "/api/v1/jobs"


def test_list_empty(client: TestClient) -> None:
    assert client.get(BASE).json() == []


def test_create_and_get(client: TestClient) -> None:
    created = client.post(BASE, json={"name": "first run", "description": "smoke"})
    assert created.status_code == 201
    body = created.json()
    assert body["name"] == "first run"
    assert body["status"] == "queued"

    fetched = client.get(f"{BASE}/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == body

    assert len(client.get(BASE).json()) == 1


def test_create_validation(client: TestClient) -> None:
    assert client.post(BASE, json={"name": ""}).status_code == 422


def test_get_missing(client: TestClient) -> None:
    assert client.get(f"{BASE}/{uuid4()}").status_code == 404


def test_delete(client: TestClient) -> None:
    job_id = client.post(BASE, json={"name": "to delete"}).json()["id"]
    assert client.delete(f"{BASE}/{job_id}").status_code == 204
    assert client.get(f"{BASE}/{job_id}").status_code == 404
    assert client.delete(f"{BASE}/{job_id}").status_code == 404
