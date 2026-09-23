#!/usr/bin/env bash
set -euo pipefail

CACHE_PATH="build/cliopatria-v0.2.0-ad28a691.geojson.zip"
COMMON_ARGS=(
  --cache-path "$CACHE_PATH"
  --schema-sql experiments/m2/cliopatria_raw_staging.sql
  --expected-profile validation/cliopatria_v0.2.0_profile.json
  --reconcile-sql experiments/m2/cliopatria_reconciliation.sql
)

echo "==> first full-corpus Cliopatria ingestion"
first="$(
  docker compose run --rm tooling     python tools/ingest_cliopatria.py "${COMMON_ARGS[@]}"
)"
printf '%s\n' "$first"
grep -q '"action": "inserted"' <<<"$first"

echo "==> exact retry must be a no-op"
second="$(
  docker compose run --rm tooling     python tools/ingest_cliopatria.py "${COMMON_ARGS[@]}"
)"
printf '%s\n' "$second"
grep -q '"action": "noop"' <<<"$second"

echo "Cliopatria full-corpus raw/staging ingestion and retry reconciliation passed."
