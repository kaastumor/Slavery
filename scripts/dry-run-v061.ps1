$ErrorActionPreference = "Stop"
$workbook = "data/releases/v0.6.1/Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx"
if (-not (Test-Path $workbook)) { throw "Canonical workbook not found at $workbook" }
docker compose run --rm tooling python tools/import_v061.py `
  --workbook "/workspace/$workbook" `
  --report /workspace/build/v061_dry_run_report.json
