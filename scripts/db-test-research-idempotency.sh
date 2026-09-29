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

# #360: rehearse the full accepted 12-case subset as one atomic transaction.
# In disposable mode the tool always rolls back after verifying exact deltas.
docker compose run --rm -e CI=true tooling \
  python tools/ingest_population_subset.py --apply --disposable-test-db


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


bukhara="data/research/recovery/production_batch_2026_09_29/candidates/07_bukhara_persian_slavery_1820.json"
bukhara_key="production-batch-2026-09-29/bukhara/persian-slavery-1820-v1"
bukhara_first=$(docker compose run --rm tooling python tools/add_research_case.py "$bukhara" --apply)
printf '%s\n' "$bukhara_first"
bukhara_second=$(docker compose run --rm tooling python tools/add_research_case.py "$bukhara" --apply)
printf '%s\n' "$bukhara_second"
grep -q "NO-OP: research case already applied unchanged" <<<"$bukhara_second"
bukhara_counts=$(docker compose exec -T db sh -lc "psql -At -F '|' -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select
 (select count(*) from audit.research_case_ingest where case_key='$bukhara_key'),
 (select count(*) from atlas.territorial_practice_claim t join audit.research_case_ingest r using(claim_id) where r.case_key='$bukhara_key' and t.practice_level is null),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key='$bukhara_key' and g.geom is not null and GeometryType(g.geom)='POINT' and g.accuracy_status='modern_proxy');
\"")
test "$bukhara_counts" = "1|1|1"

taghaza="data/research/recovery/production_batch_2026_09_29/candidates/08_taghaza_slave_salt_mining_1352.json"
taghaza_key="production-batch-2026-09-29/taghaza/slave-salt-mining-1352-v1"
taghaza_first=$(docker compose run --rm tooling python tools/add_research_case.py "$taghaza" --apply)
printf '%s\n' "$taghaza_first"
taghaza_second=$(docker compose run --rm tooling python tools/add_research_case.py "$taghaza" --apply)
printf '%s\n' "$taghaza_second"
grep -q "NO-OP: research case already applied unchanged" <<<"$taghaza_second"
taghaza_counts=$(docker compose exec -T db sh -lc "psql -At -F '|' -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select
 (select count(*) from audit.research_case_ingest where case_key='$taghaza_key'),
 (select count(*) from atlas.territorial_practice_claim t join audit.research_case_ingest r using(claim_id) where r.case_key='$taghaza_key' and t.practice_level is null),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key='$taghaza_key');
\"")
test "$taghaza_counts" = "1|1|0"

echo "Batch 3 candidate ingestion passed: Bukhara modern-proxy point + Taghaza unresolved site claim are idempotent with no P-levels."


for candidate in   "09_imerina_slavery_1790_1861.json"   "10_zanzibar_slave_based_production_1859_1871.json"   "11_kongo_slavery_transformation_1491_1800.json"   "12_khiva_slavery_1873.json"
do
  path="data/research/recovery/production_batch_2026_09_29/candidates/$candidate"
  first=$(docker compose run --rm tooling python tools/add_research_case.py "$path" --apply)
  printf '%s\n' "$first"
  second=$(docker compose run --rm tooling python tools/add_research_case.py "$path" --apply)
  printf '%s\n' "$second"
  grep -q "NO-OP: research case already applied unchanged" <<<"$second"
done

batch4_counts=$(docker compose exec -T db sh -lc "psql -At -F '|' -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select
 (select count(*) from audit.research_case_ingest where case_key in (
  'production-batch-2026-09-29/imerina/slavery-1790-1861-v1',
  'production-batch-2026-09-29/zanzibar/slave-based-plantation-production-1859-1871-v1',
  'production-batch-2026-09-29/kongo/slavery-transformation-1491-1800-v1',
  'production-batch-2026-09-29/khiva/slavery-1873-v1')),
 (select count(*) from atlas.territorial_practice_claim t join audit.research_case_ingest r using(claim_id) where r.case_key in (
  'production-batch-2026-09-29/imerina/slavery-1790-1861-v1',
  'production-batch-2026-09-29/zanzibar/slave-based-plantation-production-1859-1871-v1',
  'production-batch-2026-09-29/kongo/slavery-transformation-1491-1800-v1',
  'production-batch-2026-09-29/khiva/slavery-1873-v1') and t.practice_level is null),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key in (
  'production-batch-2026-09-29/imerina/slavery-1790-1861-v1',
  'production-batch-2026-09-29/zanzibar/slave-based-plantation-production-1859-1871-v1',
  'production-batch-2026-09-29/kongo/slavery-transformation-1491-1800-v1',
  'production-batch-2026-09-29/khiva/slavery-1873-v1') and g.geom is not null and GeometryType(g.geom)='POINT' and g.accuracy_status='modern_proxy');
\"")
test "$batch4_counts" = "4|4|4"

echo "Batch 4 candidate ingestion passed: Imerina, Zanzibar, Kongo and Khiva are idempotent, NULL-P-level claims with modern-proxy navigation points only."


istanbul="data/research/recovery/production_batch_2026_09_29/candidates/13_istanbul_slavery_1590_1710.json"
istanbul_key="production-batch-2026-09-29/istanbul/slavery-1590-1710-v1"
istanbul_first=$(docker compose run --rm tooling python tools/add_research_case.py "$istanbul" --apply)
printf '%s\n' "$istanbul_first"
istanbul_second=$(docker compose run --rm tooling python tools/add_research_case.py "$istanbul" --apply)
printf '%s\n' "$istanbul_second"
grep -q "NO-OP: research case already applied unchanged" <<<"$istanbul_second"
istanbul_counts=$(docker compose exec -T db sh -lc "psql -At -F '|' -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c \"select
 (select count(*) from audit.research_case_ingest where case_key='$istanbul_key'),
 (select count(*) from atlas.territorial_practice_claim t join audit.research_case_ingest r using(claim_id) where r.case_key='$istanbul_key' and t.practice_level is null),
 (select count(*) from atlas.geometry g join atlas.territorial_practice_claim t using(spatial_entity_id) join audit.research_case_ingest r on r.claim_id=t.claim_id where r.case_key='$istanbul_key' and g.geom is not null and GeometryType(g.geom)='POINT' and g.accuracy_status='modern_proxy');
\"")
test "$istanbul_counts" = "1|1|1"
echo "Batch 5 Istanbul candidate ingestion passed: bounded archival urban claim idempotent with modern-proxy navigation point and no P-level."


# #370: rehearse three reviewed case-linked mapped representations only after
# the full #367 population set exists in this disposable database. The tool
# has no production commit path and rolls back all closure amendments.
docker compose run --rm -e CI=true tooling \
  python tools/rehearse_geometry_closure_tranche_01.py --apply --disposable-test-db

echo "100/100 geometry closure tranche 1 rehearsal passed: Goryeo, Jakin/Godomey and Taghaza mapped roles are idempotent and rolled back."
