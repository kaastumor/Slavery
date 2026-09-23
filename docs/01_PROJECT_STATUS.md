# Current Project Status

For execution order, use repository-root `BACKLOG.md`. GitHub `main`, open issues/PRs and current CI override this snapshot.

**Status date:** 2026-09-23  
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

Repository migrations currently run through `0029_claim_kind_function_privileges.sql`.

## Current gate

**M2 — semantic integration + complete geography backbone, issue #116.**

M1 completed after an explicit REVISE → corrective #112 → re-attack cycle. The accepted experimental target no longer treats P0–P4 as the future universal comparative ordinal and separates evidence pattern, interpretive basis, occurrence/institution/prevalence/structural significance, workflow/outcome, temporal applicability/precision and evidence locus/inference extent.

M2 must now prove those semantics in the real relational/query architecture while moving from polity-by-polity Cliopatria use to the complete pinned corpus as raw geography infrastructure. The current canonical v0.6.1 release and public preview remain unchanged during this gate.

M2 progress as of this snapshot:
- **#117 complete:** D-058 promotes the corrected M1 structure to the canonical **target** methodology/data model; schema draft is now draft-0.11 and explicitly not yet a claim of live relational implementation.
- **#118 complete:** D-059 resolves the Cliopatria v0.2.0 source-time and composite/RELATION handling needed for safe integration, while preserving source-native year zero/raw hierarchy.
- **#119 complete:** the exact pinned 44,231,317-byte Cliopatria asset loaded all 13,765 features into disposable raw/staging PostGIS, reconciled to the accepted corpus profile, preserved source-native years/type/hierarchy/geometry, and an exact second run was a verified no-op. No production schema/data or publication path changed.
- **#120 is now the highest-priority eligible task:** prototype the post-M1 claim semantics in disposable PostGIS without rewriting legacy v0.6.1 meaning.
- #121's #119 dependency is now satisfied but follows #120 in the M2 execution order; #122/#123 remain the integrated adversarial and health gates.

## Existing blockers

- **#43** — remaining protected staging/production boundary work requires sponsor/admin/credential action (including any paid Supabase development branch). Do not manufacture a workaround.
- **#26** — live migration-ledger metadata mismatch remains documented; do not replay already-live schema migrations or rewrite production history casually.

These blockers do not prevent M2.

## Canonical operating documents

- `docs/23_PROJECT_CHARTER.md`
- `docs/24_WAY_OF_WORKING.md`
- `docs/25_PROJECT_HEALTH.md`
- `docs/automation/hourly-worker.md`
- repository-root `BACKLOG.md`
- `docs/08_DECISIONS_LOG.md`

The older session handoff file is no longer an execution queue. A new session should inspect GitHub `main`, open PRs/issues, and `BACKLOG.md` before relying on this status snapshot.

## Important invariants

The atlas remains an evidence-synthesis/data-curation project. Territorial practice, legal regime, external participation, research coverage and geometry stay separate. Unknown is not absence. Raw/source-native values remain recoverable. Draft/reviewed/published/canonical are different states. Canonical releases are immutable.
