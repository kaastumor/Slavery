#!/usr/bin/env bash
set -euo pipefail

BUNDLE=/tmp/d054-full-state-bundle.json
CANDIDATE=/workspace/tests/fixtures/release_bundle_candidate.json

cleanup() {
  docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'     < db/tests/008_release_bundle_cleanup.sql >/dev/null || true
}
trap cleanup EXIT

cleanup

docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'   < db/tests/007_release_bundle_fixture.sql

docker compose run --rm tooling   python tools/release_bundle.py build "$CANDIDATE" "$BUNDLE" --source-git-sha ci-fixture

docker compose run --rm tooling python tools/release_bundle.py lint "$BUNDLE"
docker compose run --rm tooling python tools/release_bundle.py verify "$BUNDLE"

# Any historical-content drift between build and promotion must hard-block.
docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' <<'SQL'
update atlas.claim
set summary='D-054 deliberate bundle drift'
where claim_id='55555555-5555-4555-8555-555555555555'::uuid;
SQL

if docker compose run --rm tooling python tools/release_bundle.py verify "$BUNDLE"; then
  echo "Expected exact-bundle drift verification to fail" >&2
  exit 1
fi

docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' <<'SQL'
update atlas.claim
set summary='D-054 full-state bundle integration fixture'
where claim_id='55555555-5555-4555-8555-555555555555'::uuid;
SQL

docker compose run --rm tooling   python tools/release_bundle.py apply "$BUNDLE"     --storage-status workflow_artifact     --storage-locator ci://d054/full-state-bundle

# Typed captured-at-release membership, artifact registration and channel separation.
docker compose exec -T db sh -lc 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' <<'SQL'
do $$
declare
    release_status text;
    claim_status text;
    artifact_count integer;
    blocked boolean := false;
begin
    select status into release_status
    from audit.release_manifest
    where release_version='d054-bundle-fixture-release';

    if release_status <> 'published' then
        raise exception 'release status %, expected published', release_status;
    end if;

    select publication_status::text into claim_status
    from atlas.claim
    where claim_id='55555555-5555-4555-8555-555555555555'::uuid;

    if claim_status <> 'published' then
        raise exception 'claim status %, expected published', claim_status;
    end if;

    if not exists (
        select 1 from audit.release_claim
        where release_version='d054-bundle-fixture-release'
          and claim_id='55555555-5555-4555-8555-555555555555'::uuid
          and capture_status='captured_at_release'
          and object_sha256 is not null
    ) then
        raise exception 'captured release_claim membership missing';
    end if;

    if not exists (
        select 1 from audit.release_geometry
        where release_version='d054-bundle-fixture-release'
          and geometry_id='44444444-4444-4444-8444-444444444444'::uuid
          and capture_status='captured_at_release'
          and object_sha256 is not null
    ) then
        raise exception 'captured release_geometry membership missing';
    end if;

    if not exists (
        select 1 from audit.release_source_version
        where release_version='d054-bundle-fixture-release'
          and source_version_id='22222222-2222-4222-8222-222222222222'::uuid
          and capture_status='captured_at_release'
          and object_sha256 is not null
    ) then
        raise exception 'captured release_source_version membership missing';
    end if;

    select count(*) into artifact_count
    from audit.release_artifact
    where release_version='d054-bundle-fixture-release'
      and artifact_role='full_state_bundle'
      and capture_status='captured_at_release'
      and sha256 ~ '^[0-9a-f]{64}$';

    if artifact_count <> 1 then
        raise exception 'expected one registered full-state bundle, found %', artifact_count;
    end if;

    if exists(
        select 1 from audit.release_channel
        where release_version='d054-bundle-fixture-release'
    ) then
        raise exception 'bundle publication unexpectedly moved a serving channel';
    end if;

    begin
        update audit.release_artifact
        set storage_locator='ci://tamper'
        where release_version='d054-bundle-fixture-release'
          and artifact_role='full_state_bundle';
    exception when others then
        blocked := true;
    end;

    if not blocked then
        raise exception 'published release artifact provenance remained mutable';
    end if;
end $$;
SQL

# publication_status normalization makes the exact bundle verifiable after apply.
docker compose run --rm tooling python tools/release_bundle.py verify "$BUNDLE"

echo "D-054 full-state release bundle integration test passed"
