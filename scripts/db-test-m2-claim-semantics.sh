#!/usr/bin/env bash
set -euo pipefail

docker compose exec -T db sh -lc \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /workspace/experiments/m2/post_m1_claim_semantics.sql'

docker compose exec -T db sh -lc \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /workspace/experiments/m2/post_m1_claim_semantics_acceptance.sql'

echo "M2 post-M1 claim semantics prototype passed."
