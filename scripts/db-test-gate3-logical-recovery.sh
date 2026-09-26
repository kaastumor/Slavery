#!/usr/bin/env bash
set -euo pipefail

RECOVERY_DB="slavery_atlas_gate3_recovery"
RECOVERY_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${RECOVERY_DB}"
BUNDLE="reviews/db-canonicalization/gate3/gate3-live-full-state-bundle.json"
RECEIPT="build/gate3-logical-recovery-receipt.json"

cleanup() {
  docker compose exec -T db sh -lc "dropdb --if-exists -U \"\$POSTGRES_USER\" '${RECOVERY_DB}'" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker compose exec -T db sh -lc "dropdb --if-exists -U \"\$POSTGRES_USER\" '${RECOVERY_DB}'"
docker compose exec -T db sh -lc "createdb -U \"\$POSTGRES_USER\" '${RECOVERY_DB}'"

echo "==> migrate fresh recovery database"
docker compose run --rm \
  -e DATABASE_URL="$RECOVERY_URL" \
  tooling python tools/migrate.py up

echo "==> reconstruct pinned canonical land fabric"
docker compose run --rm \
  -e DATABASE_URL="$RECOVERY_URL" \
  tooling python tools/load_land_fabric.py

echo "==> restore exact Gate-3 reviewed state"
docker compose run --rm \
  -e DATABASE_URL="$RECOVERY_URL" \
  tooling python tools/restore_full_state_bundle.py "$BUNDLE" --receipt "$RECEIPT"

echo "==> verify receipt"
python3 - <<'PY'
import json
from pathlib import Path
receipt=json.loads(Path("build/gate3-logical-recovery-receipt.json").read_text())
assert receipt["restored"] is True
assert receipt["verification"] == "EXACT_OBJECT_DIGESTS_AND_PORTABLE_CARTOGRAPHY_MATCH"
assert receipt["database_state_sha256"] == "31b7a7b675445e5758ffd68d64ff0f0cde83df1b0ea65f29835246deb2ae26ff"
cart = receipt["cartography_recovery"]
assert cart["source_identity_verified"] is True
assert cart["srid"] == 4326
assert cart["geometry_valid"] is True
assert cart["geometry_nonempty"] is True
print(json.dumps(receipt, indent=2, sort_keys=True))
PY
