#!/usr/bin/env bash
set -euo pipefail

case_key="example/ancient-site/slavery-v1"

first=$(docker compose run --rm tooling   python tools/add_research_case.py data/research_case_template.json --apply)
printf '%s\n' "$first"

second=$(docker compose run --rm tooling   python tools/add_research_case.py data/research_case_template.json --apply)
printf '%s\n' "$second"

grep -q "NO-OP: research case already applied unchanged" <<<"$second"

ledger_count=$(docker compose exec -T db sh -lc   "psql -At -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select count(*) from audit.research_case_ingest where case_key='$case_key';\"")
claim_count=$(docker compose exec -T db sh -lc   "psql -At -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select count(*) from atlas.claim c join audit.research_case_ingest r on r.claim_id=c.claim_id where r.case_key='$case_key';\"")

test "$ledger_count" = "1"
test "$claim_count" = "1"

echo "Research case idempotency passed: one ledger row, one claim, retry was a no-op."

# #360: existing production packages are replayed ONLY in this disposable database.
# The script itself rejects external hosts and has no commit path.
docker compose run --rm -e CI=true tooling \
  python tools/test_population_replay.py --disposable-test-db

goryeo="data/research/recovery/production_batch_2026_09_29/candidates/01_goryeo_0956_legal_event.json"
legal_key="production-batch-2026-09-29/goryeo/nobi-status-review-0956-v1"
legal_first=$(docker compose run --rm tooling python tools/add_legal_event_case.py "$goryeo" --apply)
printf '%s\n' "$legal_first"
legal_second=$(docker compose run --rm tooling python tools/add_legal_event_case.py "$goryeo" --apply)
printf '%s\n' "$legal_second"
grep -q "NO-OP: legal-event case already applied unchanged" <<<"$legal_second"

legal_counts=$(docker compose exec -T db sh -lc "psql -At -F '|' -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select
 (select count(*) from audit.research_case_ingest where case_key='$legal_key'),
 (select count(*) from atlas.claim c join audit.research_case_ingest r using(claim_id) where r.case_key='$legal_key' and c.claim_kind_code='legal_event'),
 (select count(*) from atlas.legal_event le join audit.research_case_ingest r using(claim_id) where r.case_key='$legal_key'),
 (select count(*) from audit.research_target_result rr where rr.target_key='production-batch-2026-09-29/goryeo/nobi-0956'),
 (select count(*) from audit.research_target_review rv join audit.research_target_result rr using(research_target_result_id) where rr.target_key='production-batch-2026-09-29/goryeo/nobi-0956' and rv.admitted);
\"")
test "$legal_counts" = "1|1|1|1|1"

dahomey="data/research/recovery/production_batch_2026_09_29/candidates/02_dahomey_1727_sale_process.json"
dahomey_key="production-batch-2026-09-29/dahomey/royal-captive-allocation-sale-1727-v1"
dahomey_first=$(docker compose run --rm tooling python tools/add_research_case.py "$dahomey" --apply)
printf '%s\n' "$dahomey_first"
dahomey_second=$(docker compose run --rm tooling python tools/add_research_case.py "$dahomey" --apply)
printf '%s\n' "$dahomey_second"
grep -q "NO-OP: research case already applied unchanged" <<<"$dahomey_second"

dahomey_counts=$(docker compose exec -T db sh -lc "psql -At -F '|' -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select
 (select count(*) from audit.research_case_ingest where case_key='$dahomey_key'),
 (select count(*) from atlas.claim c join audit.research_case_ingest r using(claim_id) where r.case_key='$dahomey_key' and c.claim_kind_code='territorial_practice'),
 (select count(*) from atlas.territorial_practice_claim t join audit.research_case_ingest r using(claim_id) where r.case_key='$dahomey_key'),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key='$dahomey_key' and g.geom is not null);
\"")
test "$dahomey_counts" = "1|1|1|0"

echo "Population candidate ingestion passed: Goryeo legal-event + research result idempotent; Dahomey bounded practice idempotent; no resolved Dahomey geometry."


angkor="data/research/recovery/production_batch_2026_09_29/candidates/04_angkor_1296_1297_household_slavery.json"
angkor_key="production-batch-2026-09-29/angkor/household-slavery-1296-1297-v1"
angkor_first=$(docker compose run --rm tooling python tools/add_research_case.py "$angkor" --apply)
printf '%s\n' "$angkor_first"
angkor_second=$(docker compose run --rm tooling python tools/add_research_case.py "$angkor" --apply)
printf '%s\n' "$angkor_second"
grep -q "NO-OP: research case already applied unchanged" <<<"$angkor_second"

angkor_counts=$(docker compose exec -T db sh -lc "psql -At -F '|' -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select
 (select count(*) from audit.research_case_ingest where case_key='$angkor_key'),
 (select count(*) from atlas.claim c join audit.research_case_ingest r using(claim_id) where r.case_key='$angkor_key' and c.claim_kind_code='territorial_practice'),
 (select count(*) from atlas.territorial_practice_claim t join audit.research_case_ingest r using(claim_id) where r.case_key='$angkor_key' and t.practice_level is null),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key='$angkor_key' and g.geom is not null and GeometryType(g.geom)='POINT'),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key='$angkor_key' and g.accuracy_status='modern_proxy');
\"")
test "$angkor_counts" = "1|1|1|1|1"

echo "Angkor candidate ingestion passed: bounded 1296-1297 claim idempotent with one modern-proxy point and no P-level."


asante="data/research/recovery/production_batch_2026_09_29/candidates/05_asante_1807_1895_slavery.json"
asante_key="production-batch-2026-09-29/asante/slavery-1807-1895-v1"
asante_first=$(docker compose run --rm tooling python tools/add_research_case.py "$asante" --apply)
printf '%s\n' "$asante_first"
asante_second=$(docker compose run --rm tooling python tools/add_research_case.py "$asante" --apply)
printf '%s\n' "$asante_second"
grep -q "NO-OP: research case already applied unchanged" <<<"$asante_second"

asante_counts=$(docker compose exec -T db sh -lc "psql -At -F '|' -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select
 (select count(*) from audit.research_case_ingest where case_key='$asante_key'),
 (select count(*) from atlas.claim c join audit.research_case_ingest r using(claim_id) where r.case_key='$asante_key' and c.claim_kind_code='territorial_practice'),
 (select count(*) from atlas.territorial_practice_claim t join audit.research_case_ingest r using(claim_id) where r.case_key='$asante_key' and t.practice_level is null),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key='$asante_key' and g.geom is not null and GeometryType(g.geom)='POINT'),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key='$asante_key' and g.accuracy_status='modern_proxy');
\"")
test "$asante_counts" = "1|1|1|1|1"

echo "Asante candidate ingestion passed: reviewed 1807-1895 slavery claim idempotent with Kumasi navigation proxy and no P-level."


sitka="data/research/recovery/production_batch_2026_09_29/candidates/06_sitka_sah_quah_1886_slavery.json"
sitka_key="production-batch-2026-09-29/sitka/sah-quah-slavery-1886-v1"
sitka_first=$(docker compose run --rm tooling python tools/add_research_case.py "$sitka" --apply)
printf '%s\n' "$sitka_first"
sitka_second=$(docker compose run --rm tooling python tools/add_research_case.py "$sitka" --apply)
printf '%s\n' "$sitka_second"
grep -q "NO-OP: research case already applied unchanged" <<<"$sitka_second"

sitka_counts=$(docker compose exec -T db sh -lc "psql -At -F '|' -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select
 (select count(*) from audit.research_case_ingest where case_key='$sitka_key'),
 (select count(*) from atlas.claim c join audit.research_case_ingest r using(claim_id) where r.case_key='$sitka_key' and c.claim_kind_code='territorial_practice'),
 (select count(*) from atlas.territorial_practice_claim t join audit.research_case_ingest r using(claim_id) where r.case_key='$sitka_key' and t.practice_level is null),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key='$sitka_key' and g.geom is not null and GeometryType(g.geom)='POINT'),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key='$sitka_key' and g.accuracy_status='modern_proxy');
\"")
test "$sitka_counts" = "1|1|1|1|1"

echo "Sitka candidate ingestion passed: bounded Sah Quah 1886 claim idempotent with one modern-proxy navigation point and no P-level."
