#!/usr/bin/env bash
set -euo pipefail

SEED=/workspace/tests/fixtures/full_state_bundle_v2_seed.json
CANDIDATE=/workspace/build/gate3-full-state-candidate-v2.json
BUNDLE=/workspace/build/gate3-full-state-bundle-v2.json

cleanup() {
  rm -f build/gate3-full-state-candidate-v2.json build/gate3-full-state-bundle-v2.json
  docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
    < db/tests/013_full_state_bundle_v2_cleanup.sql >/dev/null || true
}
trap cleanup EXIT

cleanup

docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < db/tests/012_full_state_bundle_v2_fixture.sql

docker compose run --rm tooling \
  python tools/full_state_release_bundle.py freeze "$SEED" "$CANDIDATE" --source-git-sha ci-fixture

docker compose run --rm tooling \
  python tools/full_state_release_bundle.py build "$CANDIDATE" "$BUNDLE" --source-git-sha ci-fixture

docker compose run --rm tooling python tools/full_state_release_bundle.py lint "$BUNDLE"
docker compose run --rm tooling python tools/full_state_release_bundle.py verify "$CANDIDATE" "$BUNDLE"

python - <<'PY'
import json
from pathlib import Path
candidate=json.loads(Path("build/gate3-full-state-candidate-v2.json").read_text())
expected={
  "claim_ids":2,
  "actor_ids":1,
  "spatial_entity_ids":1,
  "geometry_ids":1,
  "voyage_ids":1,
  "coverage_assessment_ids":1,
  "source_version_ids":1,
  "research_target_result_ids":1,
}
actual={k:len(candidate["membership"][k]) for k in expected}
if actual != expected:
    raise SystemExit(f"unexpected v2 membership counts: {actual}")
bundle=json.loads(Path("build/gate3-full-state-bundle-v2.json").read_text())
if bundle["release"]["canonical"] is not False:
    raise SystemExit("Gate-3 proof bundle became canonical")
if set(bundle["objects"]) != {
    "claims","actors","spatial_entities","geometries","voyages",
    "coverage_assessments","source_versions","research_target_results"
}:
    raise SystemExit("full-state object groups incomplete")
PY

# Nested provenance drift must invalidate the exact bundle.
docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' <<'SQL'
update audit.research_target_source
set locator='fixture:tampered'
where research_target_source_id='71000000-0000-4000-8000-000000000010'::uuid;
SQL

if docker compose run --rm tooling python tools/full_state_release_bundle.py verify "$CANDIDATE" "$BUNDLE"; then
  echo "Expected nested research-source drift verification to fail" >&2
  exit 1
fi

docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' <<'SQL'
update audit.research_target_source
set locator='fixture:target'
where research_target_source_id='71000000-0000-4000-8000-000000000010'::uuid;
SQL

docker compose run --rm tooling python tools/full_state_release_bundle.py verify "$CANDIDATE" "$BUNDLE"

echo "Gate-3 full-state bundle v2 integration test passed"
