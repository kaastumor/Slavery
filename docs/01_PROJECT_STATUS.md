# Current Project Status

For execution order, use repository-root `BACKLOG.md`. GitHub `main`, open issues/PRs and current CI override this snapshot.

**Status date:** 2026-09-22  
**Canonical historical data release:** v0.6.1 (unchanged)  
**Current public preview:** `mvp-preview-ancient-v2` (non-canonical)

## Current position

The atlas has a working end-to-end research, PostgreSQL/PostGIS, cartography, release, API and MapLibre path. The database is the working normalized research system; it has not silently replaced the immutable canonical v0.6.1 historical release.

Major product/infrastructure foundations already demonstrated include:
- claim/source-version provenance and separate research/publication states;
- normalized territorial-practice and external-participation lanes;
- historical geometry with specialist-source precedence and immutable source geometry;
- Natural Earth-backed cartographic render pipeline with quarantine/fallback;
- release-channel pointer, typed membership, immutable full-state bundles and static public fallback;
- private internal database schemas behind the public `atlas-data` Edge Function;
- public availability monitoring and guarded recovery;
- mobile/accessibility and evidence-inspector work.

Repository migrations currently run through `0027_release_artifact_immutability.sql`.

## Current gate

**M1 — methodology hardening, issue #100.**

The 2026-09-22 adversarial review found that the next major risk is semantic rather than infrastructural: the atlas must prove it can scale without turning evidence configuration into prevalence, uncertain dates into continuous duration, local evidence into polity-wide claims, events into statuses, or historically unlike systems into a misleading single ordinal comparison.

The short autonomous runway is #101–#106. #105 is the integrated gate adversary; #106 is the mandatory Project Health Check.

## Existing blockers

- **#43** — remaining protected staging/production boundary work requires sponsor/admin/credential action (including any paid Supabase development branch). Do not manufacture a workaround.
- **#26** — live migration-ledger metadata mismatch remains documented; do not replay already-live schema migrations or rewrite production history casually.

These blockers do not prevent M1.

## Canonical operating documents

- `docs/23_PROJECT_CHARTER.md`
- `docs/24_WAY_OF_WORKING.md`
- `docs/25_PROJECT_HEALTH.md`
- `docs/automation/hourly-worker.md`
- repository-root `BACKLOG.md`
- `docs/08_DECISIONS_LOG.md`

The older session handoff file is no longer an execution queue.

## Important invariants

The atlas remains an evidence-synthesis/data-curation project. Territorial practice, legal regime, external participation, research coverage and geometry stay separate. Unknown is not absence. Raw/source-native values remain recoverable. Draft/reviewed/published/canonical are different states. Canonical releases are immutable.
