$ErrorActionPreference = "Stop"
& .\scripts\db-wait.ps1
& .\scripts\db-status.ps1
& .\scripts\verify-release.ps1
& .\scripts\db-test-schema.ps1
& .\scripts\test-python.ps1
& .\scripts\dry-run-v061.ps1
& .\scripts\db-test-v061.ps1
& .\scripts\db-test-non-atlantic.ps1
Write-Host "All development verification checks passed."
