#!/usr/bin/env bash
set -euo pipefail
workbook="data/releases/v0.6.1/Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx"
[[ -f "$workbook" ]] || { echo "Canonical workbook not found at $workbook" >&2; exit 1; }
docker compose run --rm tooling python tools/import_v061.py \
  --workbook "/workspace/$workbook" \
  --report /workspace/build/v061_dry_run_report.json \
  --apply
