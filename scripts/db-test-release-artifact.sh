#!/usr/bin/env bash
set -euo pipefail

ARTIFACT=/tmp/d054-release-artifact.json
CANDIDATE=/workspace/tests/fixtures/release_artifact_candidate.json

cleanup() {
  docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'     < db/tests/007_release_artifact_cleanup.sql >/dev/null || true
}
trap cleanup EXIT

cleanup

docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'   < db/tests/006_release_artifact_fixture.sql

docker compose run --rm tooling   python tools/release_artifact.py build "$CANDIDATE" "$ARTIFACT" --source-git-sha ci-fixture

docker compose run --rm tooling   python tools/release_artifact.py lint "$ARTIFACT"

docker compose run --rm tooling   python tools/release_artifact.py verify "$ARTIFACT"

# A one-field historical-content drift must make exact-artifact verification fail.
docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' <<'SQL'
update atlas.claim
set summary='D-054 fixture drift that must block promotion'
where claim_id='55555555-5555-4555-8555-555555555555'::uuid;
SQL

if docker compose run --rm tooling python tools/release_artifact.py verify "$ARTIFACT"; then
  echo "Expected drift verification to fail" >&2
  exit 1
fi

docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' <<'SQL'
update atlas.claim
set summary='D-054 exact-artifact integration fixture'
where claim_id='55555555-5555-4555-8555-555555555555'::uuid;
SQL

docker compose run --rm tooling   python tools/release_artifact.py apply "$ARTIFACT"

# Publication does not move the serving channel and preserves exact artifact provenance.
docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' <<'SQL'
do $$
declare
    m jsonb;
    status text;
    publication text;
begin
    select manifest, rm.status into m, status
    from audit.release_manifest rm
    where release_version='d054-fixture-release';

    if status <> 'published' then
        raise exception 'fixture release status %, expected published', status;
    end if;
    if m->>'purpose' <> 'public_mvp_preview' then
        raise exception 'fixture purpose mismatch';
    end if;
    if jsonb_array_length(m->'claim_ids') <> 1
       or m->'claim_ids'->>0 <> '55555555-5555-4555-8555-555555555555' then
        raise exception 'claim membership mismatch';
    end if;
    if coalesce(m#>>'{release_artifact,artifact_schema}','') <>
       'historical-slavery-atlas-release-artifact-v1' then
        raise exception 'artifact provenance missing';
    end if;
    if exists(select 1 from audit.release_channel where release_version='d054-fixture-release') then
        raise exception 'artifact publication unexpectedly moved a release channel';
    end if;

    select publication_status::text into publication
    from atlas.claim
    where claim_id='55555555-5555-4555-8555-555555555555'::uuid;
    if publication <> 'published' then
        raise exception 'claim was not published';
    end if;
end $$;
SQL

# Publication-status mutation is intentionally excluded from historical-content digests.
docker compose run --rm tooling   python tools/release_artifact.py verify "$ARTIFACT"

echo "D-054 exact release artifact integration test passed"
