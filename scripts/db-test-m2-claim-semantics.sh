#!/usr/bin/env bash
set -euo pipefail

run_sql() {
  local file="$1"
  docker compose exec -T db sh -lc \
    'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < "$file"
}

run_sql experiments/m2/post_m1_claim_semantics.sql
run_sql experiments/m2/post_m1_claim_semantics_correction.sql

# Existing Hittite/Baekje/Silla/legacy acceptance must survive the correction.
run_sql experiments/m2/post_m1_claim_semantics_acceptance.sql

# New reverse-direction/open-terminus attacks.
run_sql experiments/m2/post_m1_claim_semantics_correction_acceptance.sql

echo "M2 post-M1 claim semantics + #135 integrity correction passed."
