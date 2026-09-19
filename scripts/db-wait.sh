#!/usr/bin/env bash
set -euo pipefail
for _ in $(seq 1 60); do
  cid="$(docker compose ps -q db)"
  if [[ -n "$cid" ]]; then
    status="$(docker inspect --format '{{.State.Health.Status}}' "$cid" 2>/dev/null || true)"
    if [[ "$status" == "healthy" ]]; then
      echo "Database is healthy."
      exit 0
    fi
  fi
  sleep 2
done
echo "Database did not become healthy within 2 minutes. Run 'docker compose logs db'." >&2
exit 1
