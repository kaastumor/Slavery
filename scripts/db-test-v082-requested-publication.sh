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
# Rehearse the exact production schema 0034; 0035 is an unpromoted render policy.
# Keep the production schema guard intact and use the checksum-enforced runner.
docker compose run --rm -e DATABASE_URL="$REHEARSAL_URL" tooling python -c 'import sys,os; sys.path.insert(0,"tools"); import migrate,psycopg; discover=migrate.discover; migrate.discover=lambda: [p for p in discover() if p.name[:4] <= "0034"]; conn=psycopg.connect(os.environ["DATABASE_URL"]); raise SystemExit(migrate.up(conn))'
docker compose run --rm -e DATABASE_URL="$REHEARSAL_URL" tooling python tools/load_land_fabric.py
docker compose run --rm -e DATABASE_URL="$REHEARSAL_URL" tooling python tools/restore_full_state_bundle.py data/releases/v0.8.2/authority-state.json --cartography-fingerprint data/releases/v0.8.2/cartography-recovery-fingerprint.json --receipt build/v082-requested-recovery-receipt.json
docker compose run --rm -e DATABASE_URL="$REHEARSAL_URL" -e CI=true tooling python tools/rehearse_v082_requested_publication.py
