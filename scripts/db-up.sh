#!/usr/bin/env bash
set -euo pipefail
[[ -f .env ]] || { echo "Missing .env; copy .env.example to .env first." >&2; exit 1; }
docker compose up -d db
docker compose ps db
