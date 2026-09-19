param([Parameter(Mandatory=$true)][string]$Backup)
$ErrorActionPreference = "Stop"
if (-not (Test-Path $Backup)) { throw "Backup not found: $Backup" }
$resolved = (Resolve-Path $Backup).Path
$repo = (Resolve-Path ".").Path
if (-not $resolved.StartsWith($repo)) { throw "Backup must be inside this repository, preferably backups/." }
$relative = $resolved.Substring($repo.Length).TrimStart('\') -replace '\\','/'
Write-Warning "This replaces the contents of the LOCAL development database."
$answer = Read-Host "Type RESTORE to continue"
if ($answer -ne "RESTORE") { Write-Host "Cancelled"; exit 0 }
docker compose exec -T db sh -lc 'dropdb --if-exists -U "$POSTGRES_USER" "$POSTGRES_DB" && createdb -U "$POSTGRES_USER" "$POSTGRES_DB"'
docker compose exec -T db sh -lc "pg_restore -U \"`$POSTGRES_USER\" -d \"`$POSTGRES_DB\" --no-owner --no-privileges '/workspace/$relative'"
Write-Host "Restore complete."
