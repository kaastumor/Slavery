#!/usr/bin/env bash
set -euo pipefail
./scripts/db-wait.sh
./scripts/db-status.sh
./scripts/db-test-schema.sh
./scripts/test-python.sh
./scripts/db-test-non-atlantic.sh
./scripts/db-test-release-reconstruction.sh

workbook="data/releases/v0.6.1/Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx"
if [[ -f "$workbook" ]]; then
  ./scripts/verify-release.sh
  ./scripts/dry-run-v061.sh
  ./scripts/db-test-v061.sh
else
  echo "Release-specific verification skipped: canonical v0.6.1 artifact not present."
fi
echo "All available development verification checks passed."
