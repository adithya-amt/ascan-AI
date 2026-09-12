#!/usr/bin/env bash
# Installed as a Claude Code SessionStart hook. Makes sure the project's
# dependencies are present so tests and linters run in fresh web sessions.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found; installing" >&2
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

uv sync --extra dev --quiet
echo "iol-mill: dependencies ready (uv sync --extra dev)"
