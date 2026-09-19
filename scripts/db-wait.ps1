$ErrorActionPreference = "Stop"
$deadline = (Get-Date).AddMinutes(2)
while ((Get-Date) -lt $deadline) {
    $cid = docker compose ps -q db
    if ($cid) {
        $status = docker inspect --format '{{.State.Health.Status}}' $cid 2>$null
        if ($status -eq "healthy") { Write-Host "Database is healthy."; exit 0 }
    }
    Start-Sleep -Seconds 2
}
throw "Database did not become healthy within 2 minutes. Run 'docker compose logs db'."
