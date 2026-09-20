# Research Workflow

## A. Research a new region-period or spatial entity

1. Define the target spatial entity/region/polity and bounded or explicitly uncertain time interval.
2. Check current coverage state and existing claims before researching.
3. Identify the relevant specialist historiography, including current or authoritative syntheses and any recognized historiographical disagreements.
4. Identify the primary/source-native evidence that anchors the historical question where accessible: inscriptions, transactions, law, registers, administrative documents, chronicles, archaeological records, or other bounded evidence.
5. Determine what each source can actually support. Separate law, terminology, captive-taking, social hierarchy, trade participation and observed territorial practice.
6. Look for limiting and challenging evidence, not only confirmation.
7. Determine how specialist historians have interpreted the evidence package.
8. Record the **best-supported historical designation** rather than mechanically mirroring individual source statements.
9. Preserve contrary or limiting evidence through claim-source directions such as `challenges` and `qualifies`.
10. Use `disputed` only when relevant specialist scholarship remains materially divided after synthesis.
11. If no defensible historical claim can be made, leave the territorial condition unknown and record the appropriate research-coverage state. Do not invent a negative claim.
12. Create one or more claim records rather than one narrative blob.
13. Register the exact source/source version used.
14. Attach evidence at claim level.
15. Assess source dependence and independence.
16. Record temporal and spatial precision rather than inventing exactness.
17. Assign coverage state.
18. Assign P-level only when the interpreted evidence package supports an intensity assessment. A positive designation may still have `practice_level = NULL` if intensity remains unassessed.
19. Resolve historical geometry independently from the slavery/coercion evidence.
20. Run QC before publication/merge into canonical research data.

### Research-role rule

The project normally **synthesizes existing scholarship**. It should not attempt to become the primary scholarly authority on a historical controversy.

When specialist scholarship exists, the project should capture and digest that scholarship rather than independently adjudicating difficult philological, archaeological or historiographical questions from raw evidence alone.

When specialist scholarship is genuinely absent, the project may preserve bounded primary evidence as such, but should avoid turning that evidence into a broad structural interpretation unsupported by scholarship.

## B. Resolving conflicting evidence

When sources disagree:

1. confirm that they actually address the same proposition
2. distinguish primary evidence from later interpretation
3. assess chronology, provenance, transmission, genre, terminology and scope
4. identify whether the sources are independent
5. consult specialist scholarship on the contradiction
6. determine whether historians generally resolve the contradiction, qualify it, or remain divided
7. record the best-supported atlas designation
8. retain the contrary evidence in `CLAIM_SOURCE`
9. use `disputed` only if the historical classification itself remains genuinely unresolved

Do not use disagreement between two source rows as an automatic reason to blank a classification.

## C. Ingest a bulk dataset or voyage/network record

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

## D. Legal-event research

1. Create a claim/legal-event identity.
2. Record legal instrument/event.
3. Record historical jurisdiction as a spatial entity.
4. Record enactment/effective date and temporal precision.
5. Record scope, exceptions and subnational variation.
6. Attach exact source version(s) and locators.
7. Keep implementation and continuing practice as separate claims.
8. Do not infer prevalence from legal recognition alone.
9. Where law is used to interpret a status category, use specialist scholarship to establish how historians understand that category.

## E. Publication workflow

Research and publication are separate states.

Preferred lifecycle:

1. draft
2. reviewed
3. published
4. superseded where later interpretation replaces it

The public web map must consume approved publish views/release materializations, not unrestricted draft research tables.

A claim should not be published merely because sources exist. Publication requires that the atlas designation reflects the reviewed evidence synthesis, including relevant counterevidence and historiography.

## F. Research batch completion criteria

A batch is not complete merely because sources were found. It is complete when:

- identities are normalized without discarding raw forms
- claims are normalized
- exact source versions are registered where applicable
- claim-source links and locators are explicit
- evidence direction is explicit
- source roles and independence are explicit
- relevant specialist interpretation has been identified where available
- contrary/limiting evidence has been checked
- conflicts have been synthesized rather than automatically marked disputed
- uncertainties are recorded
- temporal precision is recorded
- geography is resolved or explicitly unresolved
- raw/source values remain traceable for imported datasets
- QC passes
- changelog/decision log is updated where necessary

## G. Direct PostgreSQL research entry

New hand-researched cases should normally enter the atlas database directly rather than being staged in a new Excel workbook.

Use `data/research_case_template.json` as the claim-centric input shape and validate it first:

```bash
python tools/add_research_case.py data/research_case_template.json
```

The loader creates or reuses the exact `SOURCE_VERSION`, resolves/creates the `SPATIAL_ENTITY`, creates the base `CLAIM`, `TERRITORIAL_PRACTICE_CLAIM`, `CLAIM_SOURCE` rows, and optional geometry. It always creates the claim as `unpublished`; publication is a separate operation.

To apply after review:

```bash
DATABASE_URL=... python tools/add_research_case.py path/to/case.json --apply
```

A public preview/release is created separately with `tools/publish_release.py`. That gate checks that every selected claim is reviewed, has claim-level evidence, and that territorial-practice targets have reviewed geometry coverage or an explicit unresolved-geometry record. The publication tool cannot declare a canonical release.

This workflow does not alter the requirement to preserve raw/source-native records for bulk imported datasets.

## H. Stable research-case identity and retry safety

Every new claim-centric research case must have a stable top-level `case_key`.

The case key identifies one immutable ingested research package. The loader computes a SHA-256 hash from canonical JSON serialization and records it in `audit.research_case_ingest` together with the created claim ID, source path and optional Git revision.

Retry behavior is deliberately strict:

- same `case_key` + same content hash → no-op, returning the original claim;
- same `case_key` + different content hash → reject;
- materially revised historical interpretation → create a new case key and use the normal review/supersession model rather than mutating an already-ingested case in place.

This protects automated and retried ingestion from silently creating duplicate claims while preserving a transparent history of substantive research revisions.

A case passing structural CI is still only a valid research package. It does not become reviewed or published merely because its schema/hash checks pass.
