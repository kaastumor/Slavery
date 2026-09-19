$ErrorActionPreference = "Stop"
docker compose run --rm tooling python -m unittest discover -s tests -v
