# Production population preparation — 2026-09-29

Follow-up: `source_review_followup.json` records four further locator proposals
(Nepal 1998 preface, Pakistan, Peru publisher summary, Brazil 2005 Global Report)
and one explicit Nepal 2001 hold. `batch_1_gate_manifest.json` records the first-batch
source gates and accepted/held dispositions. The clean review history retains only
public-safe structured source-gate summaries and rechecked public source locators;
private worker-chat transcripts, identifiers and rendered-text digests are excluded.
Missing original scheduler packet revisions remain unknown rather than reconstructed.
These files remain candidate evidence in the same #360/PR #367 workstream, not a second queue.

This is a fixed preflight observation for #360, not a second queue or a release-ready historical dataset. Active work remains in root BACKLOG.md and #360.

The sponsor accepted #366's map candidate with known limitations and deferred further visual refinement. This removes map perfection as a prerequisite for population preparation, not historical or technical integrity checks.

`preflight.json` records two explicit read-only Supabase queries at 00:16:50 and 00:19:14 UTC. The first enumerated off-v0.8.1 territorial claims, ingest lineage, locators and directly attached temporal-overlap geometry; the second checked the 23 planned subject names/aliases and counted tracked off-release claims. Native database responses are the observation basis. Digest fields are values observed in the ingest ledger, not independently recomputed source-file hashes.

Result: 11 tracked reviewed/unpublished current-method claims already exist and must not be inserted again; all have NULL practice level and no non-null overlapping geometry directly attached to the target entity. Six have one or more blank source-locator fields requiring review. All 23 planned subject names lacked matches under the checked aliases; exact identity, full packet recovery and evidence review remain pending. Separate evidence-locus relations were not audited.

## Immediate data work

Start with the first mixed five-subject set already named in #360: Hamadab, Goryeo, Dahomey, Mexica and Bagan/Pagan. The morning inventory is only a summary, not the full packets. Recover exact packets or explicitly prepare fresh source-backed revisions; never invent old packet bytes or citations. In parallel within this same batch deliverable, reuse the 11 existing IDs and complete source/geometry dependencies where defensible. Do not use broad country shapes simply to make every entry appear on the map.

The eventual deployable package needs accepted-ID and dependency manifests, exact import/replay results, a candidate map demonstrating the actual added places/years, changelog, QC, exclusions, staged rollout and rollback. This preflight establishes none of those completion claims.

## Verification performed

The two production reads used BEGIN READ ONLY / COMMIT. The local expanded observation was checked for 11 unique existing claim IDs, 23 unique target names, 5/5/5/4/4 grouping, six locator-follow-up rows, and 64-character recorded ingest hashes. No historical acceptance, database mutation, migration, public cutover or paid CI sweep occurred during this preflight. Normal repository CI applies to this proposed checkpoint.


## Accepted staging subset

`accepted_subset_manifest.json` freezes Goryeo's bounded 956 legal event and
Dahomey's bounded 1727 sale-process claim as the first two candidates ready for
an explicit production-ingest approval. Exact-head foundation CI run 36581157387
proved first insert + unchanged replay/no-op for both in disposable PostGIS.

A fresh connected read-only production preflight at
2026-09-29T15:55:03.576502+00:00 found no matching candidate entity, case-key,
candidate source-version URL, Goryeo research target, or release-claim collision.
The public preview baseline is now `v0.8.1-public-mvp-v2`.

The accepted staging subset now also includes **Angkor 1296–1297**. Exact-head
foundation CI run 36595321724 proved first insert + unchanged replay/no-op and
one reviewed `modern_proxy` point sourced to UNESCO component 668-001. The
point is a navigation/evidence-locus proxy for the capital-core claim, **not**
the historical labor-system extent or Khmer Empire extent.

The combined accepted staging subset is therefore Goryeo + Dahomey + Angkor:
three new claims, of which exactly **one** would create a visible point geometry
if later selected into a release/materialization. Hamadab, Mexica and Bagan
remain explicit HOLD exclusions.
Production ingestion, release membership and serving-channel movement remain
separate explicit gates.


## Asante staging addition

Asante 1807–1895 is now a reviewed staging candidate grounded principally in
Gareth Austin's specialist economic history, which treats slavery/slave trading
as widespread and economically important across nineteenth-century Asante.
Pawnship remains analytically separate. Exact-head foundation CI run
36596741744 proved first insert + unchanged replay/no-op with NULL P-level.

A fresh live read-only preflight at 2026-09-29T16:20:19.934488+00:00 found
no Asante/Ashanti entity alias, case-key, exact source-version URL, or release
collision. The candidate uses the Seshat Kumasi capital coordinate only as a
reviewed `modern_proxy` navigation point while the exact pinned Cliopatria
polity row remains unresolved. It is not the historical slavery extent or an
Ashanti boundary polygon.

The accepted staging subset is now **Goryeo + Dahomey + Angkor + Asante**:
four new claims, two reviewed point proxies (Angkor and Kumasi), zero new
shaded practice polygons, and no release/publication changes.
