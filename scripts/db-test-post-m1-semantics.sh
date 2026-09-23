#!/usr/bin/env bash
set -euo pipefail

docker compose exec -T db sh -lc   'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'   < experiments/m2/post_m1_relational_prototype.sql

docker compose exec -T db sh -lc   'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'   < experiments/m2/post_m1_relational_acceptance.sql
