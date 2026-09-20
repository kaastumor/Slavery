#!/usr/bin/env bash
set -euo pipefail
docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /workspace/db/tests/005_release_channel.sql'
docker compose run --rm tooling python -m py_compile /workspace/tools/set_release_channel.py
