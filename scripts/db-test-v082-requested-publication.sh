#!/usr/bin/env bash
set -euo pipefail
REHEARSAL_DB=slavery_atlas_d125_rehearsal
REHEARSAL_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${REHEARSAL_DB}"
cleanup() {
  docker compose exec -T db sh -lc "dropdb --if-exists -U \"\$POSTGRES_USER\" '${REHEARSAL_DB}'" >/dev/null 2>&1 || true
}
trap cleanup EXIT
cleanup
docker compose exec -T db sh -lc "createdb -U \"\$POSTGRES_USER\" '${REHEARSAL_DB}'"
docker compose run --rm -e DATABASE_URL="$REHEARSAL_URL" tooling python tools/migrate.py up
docker compose run --rm -e DATABASE_URL="$REHEARSAL_URL" tooling python tools/load_land_fabric.py
docker compose run --rm -e DATABASE_URL="$REHEARSAL_URL" tooling python tools/restore_full_state_bundle.py data/releases/v0.8.2/authority-state.json --cartography-fingerprint data/releases/v0.8.2/cartography-recovery-fingerprint.json --receipt build/v082-requested-recovery-receipt.json
docker compose run --rm -e DATABASE_URL="$REHEARSAL_URL" -e CI=true tooling python tools/rehearse_v082_requested_publication.py
