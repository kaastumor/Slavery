# Research Workflow

## A. Research a new region-period or spatial entity

1. Define the target spatial entity/region/polity and bounded or explicitly uncertain time interval.
2. Check current coverage state and existing claims before researching.
3. Identify source families in relevant languages and historiographies.
4. Look for both positive and limiting/counterevidence; do not search only for confirmation.
5. Separate direct practice evidence from captive-taking, hierarchy, inequality, legal terminology and trade participation.
6. Create one or more claim records rather than one narrative blob.
7. Register the exact source/source version used.
8. Attach evidence at claim level.
9. Assess independence of evidence.
10. Record temporal and spatial precision rather than inventing exactness.
11. Assign coverage state.
12. Assign P-level only when the evidence package supports it.
13. Resolve historical geometry independently.
14. Run QC before publication/merge into canonical research data.

## B. Ingest a bulk dataset or voyage/network record

1. Identify and register the exact source version/snapshot.
2. Preserve the source/raw identifier and source-native value.
3. If permissible, preserve the raw asset/snapshot and checksum it.
4. Load source-native data into the raw/staging layer before canonical normalization.
5. Preserve documented and imputed fields separately.
6. Normalize people/organizations to `ACTOR` without overwriting raw names.
7. Normalize ports/places to `SPATIAL_ENTITY` without assigning one timeless polity.
8. Create explicit voyage-role relationships, e.g. `VOYAGE_OWNER` and `VOYAGE_FINANCE`.
9. Leave ownership/finance shares unknown unless documented.
10. Enrich nationality/political identity only through an independent `ACTOR_ATTRIBUTE_CLAIM`.
11. Store residence, business base and corporate jurisdiction as distinct claims.
12. Preserve import lineage through an ingest-run identifier where applicable.
13. Never change territorial P-level directly because a voyage/network record exists.

## C. Legal-event research

1. Create a claim/legal-event identity.
2. Record legal instrument/event.
3. Record historical jurisdiction as a spatial entity.
4. Record enactment/effective date and temporal precision.
5. Record scope, exceptions and subnational variation.
6. Attach exact source version(s) and locators.
7. Keep implementation and continuing practice as separate claims.

## D. Publication workflow

Research and publication are separate states.

Preferred lifecycle:

1. draft
2. reviewed
3. published
4. superseded where later interpretation replaces it

The public web map must consume approved publish views/release materializations, not unrestricted draft research tables.

## E. Research batch completion criteria

A batch is not complete merely because sources were found. It is complete when:

- identities are normalized without discarding raw forms
- claims are normalized
- exact source versions are registered where applicable
- claim-source links and locators are explicit
- source roles and independence are explicit
- uncertainties are recorded
- temporal precision is recorded
- geography is resolved or explicitly unresolved
- raw/source values remain traceable for imported datasets
- QC passes
- changelog/decision log is updated where necessary
