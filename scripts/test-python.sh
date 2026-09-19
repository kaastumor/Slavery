#!/usr/bin/env bash
set -euo pipefail
docker compose run --rm tooling python -m unittest discover -s tests -v
