# Database Schema Implementation — Foundation v0.3

**Status:** executable migration package created; live PostgreSQL/PostGIS execution pending.  
**Schema draft:** draft-0.10.  
**Canonical data:** remains v0.6.1 workbook.

## What this implementation adds

The SQL package turns the architecture into enforceable database structures:

- UUID internal identities separated from source-native IDs;
- evolving controlled vocabularies as lookup tables;
- astronomical-year interval helper using `int4range`;
- source/version/asset provenance;
- actor identity plus source/raw actor names;
- generic spatial identity and time-bounded geometry;
- universal claims and exact claim-source links;
- claimable ownership, finance, voyage-stop and spatial relations;
- explicit missing-owner representation without a fake actor;
- raw/ingest lineage;
- separate research-coverage assessment table;
- review/publication views;
- v0.6.1 reconciliation crosswalk tables and acceptance tests;
- nullable P-level semantics (`NULL` = not yet assessed, distinct from explicit P0);
- rollback-only non-Atlantic acceptance fixtures based on existing workbook cases;
- research-coverage provenance bridge so RI/disputed assessments can cite exact reviewed source versions without becoming practice claims;
- full-workbook raw preservation for all 18 tabs / 288 non-empty rows;
- generic external-participation claims for non-voyage network evidence.

## Important migration correction discovered from v0.6.1

The legacy `OWNER_EVIDENCE` sheet is not equivalent to actor attributes. Some rows support business-base/nationality attributes, while others support ownership relationships or explicit missingness. Migration is therefore semantic and may be one-to-many.

Examples:

- E-001 business base → actor-attribute claim;
- E-004 ownership → evidence for the `VOYAGE_OWNER` relationship claim;
- E-008 missing owner → evidence for Orestes' missing-owner relationship/status;
- E-006 can support more than one target assertion if its legacy wording bundles corporate context and ship ownership.

This correction prevents a provenance model that would attach ownership facts to a person record instead of to the ownership relationship itself.

## Runtime validation still required

This environment has no PostgreSQL server, so the migrations have not been executed. Runtime validation must verify:

1. migrations 0001–0011 execute cleanly on the chosen PostgreSQL/PostGIS version;
2. `001_schema_smoke.sql` passes;
3. the v0.6.1 importer creates the expected crosswalks;
4. `002_v061_reconciliation.sql` passes;
5. non-Atlantic evidence fixtures pass before canonical cut-over.

## Technology basis

The implementation deliberately uses mature features available before PostgreSQL 18 (stored generated columns, UUIDs via `pgcrypto`, integer ranges, GiST indexes) rather than depending on newest-version-only capabilities. PostGIS geometry validity and GiST indexing are part of the acceptance model.

## Importer implementation checkpoint

The v0.2 importer was dry-run against the actual canonical workbook. It validates workbook identity by content invariants and SHA-256, preserves immediate-migration rows in `raw.raw_record`, and applies normalization only after those checks pass. The dry-run produced 8 voyages, 11 real actors, 12 voyage-owner/status relations, 17 registered sources, 11 legacy owner-evidence IDs, 17 semantic evidence-to-claim mappings, and 99 research-coverage cells.

The run also exposed a source-registry gap for the exact Fredensborg SlaveVoyages voyage URL. Because exact source identity is a project requirement, the importer creates a migration-generated source/version for that URL and records a QC warning; it does not replace the missing registry row with a related article or archive source.


## Non-Atlantic acceptance checkpoint

Before live execution, the schema was tested conceptually against existing non-Atlantic cases in v0.6.1. This exposed that `practice_level NOT NULL` would force unsupported P0–P4 values onto evidence that is merely reviewed, disputed, or researched-inconclusive. Migration `0009` therefore drops that NOT NULL constraint.

`db/tests/003_non_atlantic_acceptance.sql` is rollback-only and checks representability of:

- Carolingian slavery/unfree-status evidence without translating legacy S to P3/P4;
- Mycenaean direct terminology/purchase evidence without inventing intensity;
- disputed Shang captivity/slavery classification without coercing D to a P-level;
- Indus researched-inconclusive coverage without fabricating a positive practice claim;
- Ottoman practice and suppression/legal context as separate claims;
- c. 2130–2110 BCE astronomical-year handling for Anshan/Elam;
- a non-state Peruvian Amazon spatial target;
- unresolved geometry with no fabricated polygon;
- publish filtering for unpublished fixtures.

All fixture inserts are rolled back and do not become canonical data.


## Canonical-workbook completeness gate

The controlled importer initially normalized the Atlantic seed plus 99-cell coverage matrix but did not preserve the global evidence tabs row-by-row. That was insufficient for a future canonical switch. v0.3 now validates and raw-preserves all 18 workbook tabs / 288 non-empty rows.

The evidence tabs `v0.4.7 Evidence`, `v0.4.8 Evidence`, `v0.4.9 Evidence`, and `v0.5.0 Evidence` are deliberately marked by a blocking QC issue until their substantive assertions and source links are semantically migrated. Passing Atlantic reconciliation alone can therefore never make the database canonical.
