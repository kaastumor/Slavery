#!/usr/bin/env bash
set -euo pipefail

echo "==> load and reconcile exact pinned Cliopatria corpus"
bash ./scripts/db-test-cliopatria-ingest.sh

echo "==> apply selected-year resolver and cheap adversarial fixtures"
bash ./scripts/db-test-cliopatria-resolver.sh

echo "==> emit real-corpus selected-year diagnostic"
docker compose exec -T db sh -lc \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < experiments/m2/cliopatria_selected_year_full_diagnostic.sql

echo "==> enforce frozen complete-corpus acceptance"
docker compose exec -T db sh -lc \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < experiments/m2/cliopatria_selected_year_full_acceptance.sql
