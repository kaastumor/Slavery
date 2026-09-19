#!/usr/bin/env bash
set -euo pipefail
mkdir -p backups
stamp="$(date +%Y%m%d_%H%M%S)"
docker compose exec -T db sh -lc "pg_dump -Fc -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\" -f /workspace/backups/slavery_atlas_${stamp}.dump"
echo "Created backups/slavery_atlas_${stamp}.dump"
