#!/usr/bin/env bash
set -euo pipefail

docker compose exec -T db sh -lc \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < experiments/m2/cliopatria_raw_staging.sql

docker compose exec -T db sh -lc \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < experiments/m2/cliopatria_selected_year_resolver.sql

docker compose exec -T db sh -lc \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < experiments/m2/cliopatria_selected_year_resolver_acceptance.sql

echo "M2 Cliopatria selected-year resolver synthetic acceptance passed."
