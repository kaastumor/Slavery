$ErrorActionPreference = "Stop"
Write-Warning "This deletes the LOCAL development database volume. Canonical project files are not touched."
$answer = Read-Host "Type RESET to continue"
if ($answer -ne "RESET") { Write-Host "Cancelled"; exit 0 }
docker compose down -v
docker compose up -d db
Write-Host "Database recreated. Run scripts/db-migrate.ps1 and scripts/db-test-schema.ps1 next."

