#!/usr/bin/env bash
set -euo pipefail
docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /workspace/db/tests/004_private_data_api_boundary.sql'
