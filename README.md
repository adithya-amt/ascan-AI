# IOL MILL

FastAPI service for IOL MILL. Python 3.11+, managed with [uv](https://docs.astral.sh/uv/).

## Quick start

```bash
uv sync --extra dev          # create .venv and install everything
cp .env.example .env         # optional: local overrides
make dev                     # http://localhost:8000, docs at /docs
```

Without `make`:

```bash
uv run uvicorn iol_mill.main:app --reload
```

## Layout

```
src/iol_mill/
  main.py          app factory (create_app) and `iol-mill` entry point
  config.py        Settings, read from IOL_MILL_* env vars / .env
  api/health.py    GET /health
  api/v1/router.py registers versioned resources
  api/v1/jobs.py   sample CRUD resource at /api/v1/jobs (in-memory store)
tests/             pytest suite using FastAPI's TestClient
```

## Development

| Command          | What it does                          |
| ---------------- | ------------------------------------- |
| `make test`      | run pytest                            |
| `make lint`      | ruff check                            |
| `make format`    | ruff format + autofix                 |
| `make typecheck` | mypy in strict mode                   |
| `make check`     | lint, typecheck and test              |

## Configuration

All settings live in `src/iol_mill/config.py` and are prefixed `IOL_MILL_`.
See `.env.example` for the available keys.

## Adding an endpoint

1. Create a module under `src/iol_mill/api/v1/` with an `APIRouter`.
2. Include it in `src/iol_mill/api/v1/router.py`.
3. Add tests under `tests/`. The `client` fixture in `tests/conftest.py`
   builds a fresh app per test.
