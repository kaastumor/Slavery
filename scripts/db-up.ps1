$ErrorActionPreference = "Stop"
if (-not (Test-Path ".env")) {
    throw "Missing .env. Copy .env.example to .env and set POSTGRES_PASSWORD first."
}
docker compose up -d db
docker compose ps db

