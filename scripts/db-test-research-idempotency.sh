#!/usr/bin/env bash
set -euo pipefail

case_key="example/ancient-site/slavery-v1"

first=$(docker compose run --rm tooling   python tools/add_research_case.py data/research_case_template.json --apply)
printf '%s
' "$first"

second=$(docker compose run --rm tooling   python tools/add_research_case.py data/research_case_template.json --apply)
printf '%s
' "$second"

grep -q "NO-OP: research case already applied unchanged" <<<"$second"

ledger_count=$(docker compose exec -T db sh -lc   "psql -At -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select count(*) from audit.research_case_ingest where case_key='$case_key';\"")
claim_count=$(docker compose exec -T db sh -lc   "psql -At -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select count(*) from atlas.claim c join audit.research_case_ingest r on r.claim_id=c.claim_id where r.case_key='$case_key';\"")

test "$ledger_count" = "1"
test "$claim_count" = "1"

echo "Research case idempotency passed: one ledger row, one claim, retry was a no-op."
