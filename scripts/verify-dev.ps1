$ErrorActionPreference = "Stop"
& .\scripts\db-wait.ps1
& .\scripts\db-status.ps1
& .\scripts\db-test-schema.ps1
& .\scripts\test-python.ps1
& .\scripts\db-test-non-atlantic.ps1
& .\scripts\db-test-release-reconstruction.ps1

$workbook = "data/releases/v0.6.1/Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx"
if (Test-Path $workbook) {
    & .\scripts\verify-release.ps1
    & .\scripts\dry-run-v061.ps1
    & .\scripts\db-test-v061.ps1
} else {
    Write-Host "Release-specific verification skipped: canonical v0.6.1 artifact not present."
}
Write-Host "All available development verification checks passed."
