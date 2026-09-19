#!/usr/bin/env bash
set -euo pipefail
docker compose run --rm tooling python tools/migrate.py status
