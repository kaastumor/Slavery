# #370 connected SQL transport - preparation only

The sponsor approved merge #401 and continuation with #370 preparation. This
does not authorize a #370 production write or the new transport PR's merge.

Fresh read-only preflight on 2026-10-01 at 22:40:01 UTC matched the frozen three
claim/spatial identities and intervals. Goryeo/956 and Taghaza/1352 have no
geometry; Dahomey/1727 retains reviewed/unresolved NULL geometry
`bdab64f1-cc36-4771-8224-00b199d16c15`. All three claims remain unpublished with
zero release memberships/locus links; territorial P-levels are NULL. Jakin
identity and all four new source URLs have zero collisions. Serving remains
`v0.8.1-public-mvp-v2`. This snapshot must be refreshed before an authorized write.

`tools/export_geometry_closure_tranche_01_sql.py` reuses the existing insertion
collector and calls the exact reviewed #370 Python helpers. It does not execute
SQL or connect to a database. Default exports raise before INSERTs. Executable
export requires original `ISSUE-370-EXPLICIT`, `ATLAS_GEOMETRY_WRITE_AUTHORIZED=1`
and exact checked-out revision authority. Review, plan and rehearsal receipt are
bound to exact Git blobs; input drift is rejected.

The single atomic DO block locks affected/protected tables with timeouts,
checks claim kinds and identities (including the Goryeo legal event), states,
collisions and the exact unresolved Dahomey row. Expected delta: +1 Jakin spatial
identity, +4 sources/versions, +3 modern-proxy navigation/context points, +1 Law
historical-place context relation, +1 Dahomey-Jakin evidence locus. Goryeo and
Taghaza use existing target entities; Goryeo gains no physical event locus.
Dahomey's target geometry remains unresolved. Points do not define historical
practice extent or increase claim strength. Taghaza coordinate conflict remains
in its reviewed resolution method.

Complete snapshots preserve claim/territorial/legal-event state, ingestion
ledger, release membership and serving channels. The unresolved geometry's full
row must remain identical. The receipt returns real geometry/locus/source IDs
and exact before/after counts. A repeat submission fails closed; on ambiguous
responses read back state independently before any retry.

The existing foundation CI runs
`tools/test_geometry_closure_tranche_01_sql.py --disposable-test-db` in Compose
PostGIS with CI=true, always rolling back. Controls cover absent authority,
wrong claim/unresolved IDs, failure after all INSERTs, same-count changes to the
unresolved row or legal event, existing Python exact no-op replay, independently
matching generated IDs, duplicate submission rejection and restored counts.
The unchanged #374 export/rehearsal also remains tested. No workflow, dependency,
service, schema, historical claim or release change is added. Local focused unit
tests pass; real SQL evidence must be read from the exact-head CI result.

Before any live write: accept the transport PR, verify merged implementation
and pinned inputs/green CI, obtain scoped sponsor authority specifically for
#370's three-case manifest, refresh preflight, submit once through connected
Supabase, independently verify full metadata and preserve the production receipt.
No local DATABASE_URL is needed for that route. This preparation leaves #370,
#379, five-case admission, D-121 and public serving/release gates unchanged.
