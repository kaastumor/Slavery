#!/usr/bin/env bash
set -euo pipefail
./scripts/db-wait.sh
./scripts/db-status.sh
./scripts/verify-release.sh
./scripts/db-test-schema.sh
./scripts/test-python.sh
./scripts/dry-run-v061.sh
./scripts/db-test-v061.sh
./scripts/db-test-non-atlantic.sh
echo "All development verification checks passed."
