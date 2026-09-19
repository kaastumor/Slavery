$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path backups | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$file = "/workspace/backups/slavery_atlas_$stamp.dump"
docker compose exec -T db sh -lc "pg_dump -Fc -U \"`$POSTGRES_USER\" -d \"`$POSTGRES_DB\" -f '$file'"
Write-Host "Created backups/slavery_atlas_$stamp.dump"
