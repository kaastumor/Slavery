#!/usr/bin/env bash
set -euo pipefail

POSTGIS_SCHEMA="$(
  docker compose exec -T db sh -lc \
    'psql -At -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT n.nspname FROM pg_extension e JOIN pg_namespace n ON n.oid=e.extnamespace WHERE e.extname='\''postgis'\''"'
)"

if [[ -z "$POSTGIS_SCHEMA" ]]; then
  echo "PostGIS extension schema not found" >&2
  exit 1
fi

PGOPTIONS_VALUE="-c search_path=${POSTGIS_SCHEMA},pg_catalog,public,extensions,staging,raw,atlas,audit"

run_sql() {
  local file="$1"
  docker compose exec -T -e PGOPTIONS="$PGOPTIONS_VALUE" db sh -lc \
    'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < "$file"
}

run_sql experiments/m2/cliopatria_raw_staging.sql
run_sql experiments/m2/cliopatria_selected_year_resolver.sql
run_sql experiments/m2/cliopatria_selected_year_resolver_acceptance.sql

echo "M2 Cliopatria selected-year resolver synthetic acceptance passed."
