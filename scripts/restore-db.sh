#!/usr/bin/env bash
set -euo pipefail
[[ $# -eq 1 ]] || { echo "Usage: $0 backups/file.dump" >&2; exit 2; }
backup="$1"
[[ -f "$backup" ]] || { echo "Backup not found: $backup" >&2; exit 1; }
case "$backup" in backups/*) ;; *) echo "Backup must be inside backups/." >&2; exit 1;; esac
read -r -p "This replaces the LOCAL development DB. Type RESTORE to continue: " answer
[[ "$answer" == "RESTORE" ]] || { echo "Cancelled"; exit 0; }
docker compose exec -T db sh -lc 'dropdb --if-exists -U "$POSTGRES_USER" "$POSTGRES_DB" && createdb -U "$POSTGRES_USER" "$POSTGRES_DB"'
docker compose exec -T db sh -lc "pg_restore -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\" --no-owner --no-privileges '/workspace/$backup'"
echo "Restore complete."
