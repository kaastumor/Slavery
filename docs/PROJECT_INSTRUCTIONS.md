# Suggested Project Instructions

Use the files in this Project as the canonical methodological and architectural context for the Historical Slavery Atlas.

Before extending the dataset or changing schema, read `00_START_HERE.md`, `01_PROJECT_STATUS.md`, `02_METHOD_AND_ONTOLOGY.md`, `03_SOURCE_POLICY.md`, `04_DATA_MODEL.md`, `05_GEOGRAPHY_AND_MAP.md`, `08_DECISIONS_LOG.md`, `11_SYSTEM_ARCHITECTURE.md`, `13_DATABASE_SCHEMA_IMPLEMENTATION.md`, `14_LOCAL_DATABASE_DEVELOPMENT.md`, `15_DEVELOPMENT_ENVIRONMENT.md`, and `17_SOURCE_EVIDENCE_LIFECYCLE.md`.

Preserve the current canonical data release unless explicitly creating and validating a new version. Do not overwrite historical releases. A schema draft, newer database state, or public preview does not become canonical merely because it is newer.

The atlas is an **evidence-synthesis and data-curation project**, not an independent historical research institute. Its normal role is to collect, normalize, reconcile and digest existing historical evidence and specialist scholarship. Do not invent novel historical interpretations where relevant specialist historiography already exists.

Treat slavery and related coerced-labour systems as a multidimensional evidence problem, not a binary yes/no field. Keep territorial practice, legal status, external/network participation, research coverage, and historical geometry separate.
Use generic external-participation claims for non-voyage network evidence rather than forcing such records into territorial-practice intensity.

If no defensible territorial-practice claim exists for a place/time, the atlas state is **unknown**. Do not infer absence from missing evidence, no claim, P0, researched-inconclusive status, or unresolved geometry.

Never infer actor/owner nationality or political identity from vessel flag, registration, port, residence, business base, surname, or company jurisdiction. Unknown must remain unknown unless independently evidenced.

Never let archive density, voyage counts, document counts, captive counts, or citation counts mechanically determine territorial practice intensity. P0–P4 must be based on the interpreted evidence package and relevant specialist scholarship.

Use primary/source-native evidence mainly for bounded events, transactions, terminology, law, inscriptions, dates, locations and other directly recorded facts. Use specialist secondary scholarship to interpret classification, prevalence, continuity, representativeness and wider structure.

When sources conflict, do **not** automatically set the atlas designation to `disputed` or blank the P-level. Preserve the contrary evidence, apply ordinary historical source criticism, and follow the treatment of the issue in relevant specialist historiography. Record the best-supported working designation when a defensible synthesis exists.

Use `disputed` only when credible specialist scholarship remains materially divided over the historical classification after synthesis. A `CLAIM_SOURCE` link marked `challenges` or `qualifies` does not automatically negate the claim.

Evidence is claim-specific. Keep person/organization identity separate from historical roles; keep spatial identity separate from historical jurisdiction; preserve temporal and spatial uncertainty.
Keep research-coverage provenance separate from historical claim evidence: sources reviewed for RI/disputed coverage may be linked to the coverage assessment without implying a positive territorial-practice claim.

For imported datasets, preserve exact source version, source-native identifiers/values, documented versus imputed distinctions, and ingestion lineage. Never silently normalize away the only copy of a raw value.
For canonical workbook migration, preserve every non-empty workbook row in raw lineage and do not declare a canonical database switch until substantive evidence sheets are semantically migrated, not merely archived raw.

Do not coerce disputed, researched-inconclusive, or merely reviewed evidence to P0. A NULL P-level means no P0–P4 intensity assessment has yet been recorded; P0 is an explicit reviewed unknown/no-usable-classification assessment. A positive historical designation may still have a NULL P-level if intensity has not yet been assessed.

Always retain a neutral world land outline. Resolve historical geometries using the documented hierarchy and mark approximate or modern-proxy geometry explicitly. Do not enlarge a narrow evidence target to a whole polity merely because a convenient polygon exists.

Keep draft research separate from public/published data. Public services must consume reviewed/published views or release materializations rather than unrestricted draft tables.

Any methodology, ontology or schema change must be added to the Decisions Log before becoming canonical. Every data release must include a changelog, QC summary and unresolved-issues list.

Never create a fake historical entity merely to represent missingness (for example an unknown owner). Preserve source-native IDs separately from internal database IDs.
