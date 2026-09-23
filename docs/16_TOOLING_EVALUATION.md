# Tooling Evaluation — Phase 1

**Status:** historical evaluation snapshot. Current tooling eligibility and adoption triggers live in `docs/22_TOOLING_EVALUATION_TRIGGERS.md`.

Nothing in this document changes the canonical methodology, ontology, schema, release model or public architecture. Historical “strong candidate” wording records what was worth testing at the time; it is not current authorization to adopt a tool. Any architecture change still requires a demonstrated trigger and the normal Decisions Log process.

**Scope of this pass:** tools that can materially affect evidence quality or research reproducibility before frontend implementation.

## Evaluation criteria

A candidate tool is valuable only when it improves one or more of:

1. exact source-version identification;
2. provenance and reproducibility;
3. human-reviewable entity/place reconciliation;
4. preservation of uncertainty and raw values;
5. repeatable release reconstruction;
6. interoperability without creating a second canonical datastore.

A candidate is a poor fit when it:

- becomes a second source of truth for claims or identities;
- silently normalizes away raw values;
- encourages automatic acceptance of fuzzy matches;
- blurs research coverage with historical prevalence;
- creates provider lock-in before the query/application pattern is known.

---

## 1. Zotero — source-library workflow

### What the current official API supports

Zotero Web API v3 exposes items, collections and attachments and recommends explicit API-version pinning. The desktop client exposes a local API on `localhost:23119/api/`; read requests can operate locally/offline without rate limits, while Zotero 10+ local writes require explicit user authorization.

### Proposed atlas role

Use Zotero as the **researcher-facing bibliography and source library**, not as canonical historical evidence storage.

Candidate integration:

```text
Zotero item / attachment
        |
        v
atlas.SOURCE
        |
        +--> atlas.SOURCE_VERSION
        |
        +--> optional SOURCE_ASSET locator/checksum
```

Preserve Zotero library/item identifiers as external identifiers. A Zotero record may help initialize SOURCE metadata, but claim-specific provenance remains in PostgreSQL through CLAIM_SOURCE.

### Important boundary

Do not make a Zotero item or collection membership equivalent to a reviewed atlas claim. Zotero is a source-management interface; the atlas database remains authoritative for claim/evidence relationships.

### Current assessment

**Strong candidate for adoption.** Begin with a read-only proof before considering writes.

Official references:
- https://www.zotero.org/support/dev/web_api/v3/basics
- https://www.zotero.org/support/dev/web_api/v3/local_api

---

## 2. OpenRefine + World Historical Gazetteer — reconciliation workflow

### What the tools support

OpenRefine treats reconciliation as matching local data against an external identifier space and exposes candidate matches for review rather than assuming name equality.

World Historical Gazetteer exposes a reconciliation service compatible with OpenRefine/Reconciliation API v0.2. It can return historical-place candidates and enrich matched records with geometry, alternative names and temporal ranges.

### Proposed atlas role

Use this pair for **review-assisted place identity resolution** during ingestion/staging.

```text
source-native place text
        |
        v
OpenRefine candidate review
        |
        +--> WHG identifier / other authority ID
        +--> alternative names
        +--> temporal hints
        +--> geometry candidate
        |
        v
STAGING candidate
        |
        v
human-reviewed SPATIAL_ENTITY mapping
```

### Important boundaries

- Never auto-accept the highest reconciliation score as historical identity.
- A place match does not determine historical jurisdiction.
- WHG/GeoNames/TGN geometry does not automatically become the atlas historical polity geometry.
- Preserve the original source-native place string.
- Record authority/service/version information where possible so reconciliation can be audited.

### Current assessment

**Strong candidate for adoption.** It aligns directly with the current unknown-remains-unknown policy.

Official references:
- https://openrefine.org/docs/manual/reconciling
- https://docs.whgazetteer.org/content/technical/apis.html

---

## 3. Enslaved Ontology + JSDP — methodology and interoperability reference

### What the peer project demonstrates

The Enslaved Ontology was designed to integrate heterogeneous historical slave-trade datasets using historian-driven use cases, modular ontology design, provenance, and temporal/spatial modeling. Its published scope focuses particularly on historic persons and event records.

The Journal of Slavery and Data Preservation treats curated historical datasets and their documentation as scholarly outputs. Its workflow emphasizes data articles, review, supporting documentation/data dictionaries and durable repository deposit.

### Proposed atlas role

Use Enslaved/JSDP as **peer methodology**, not as a replacement canonical schema.

Specific concepts worth evaluating:

- competency-question-driven ontology/schema design;
- modular modeling;
- explicit provenance;
- dataset-level documentation as a first-class release artifact;
- scholarly/historical review of data construction, not just technical QC;
- durable release deposit and data dictionaries.

### Why not adopt the ontology wholesale

The Historical Slavery Atlas has a materially broader problem:

- territorial practice intensity;
- legal status/events;
- slavery-like and coerced-labour systems;
- research coverage/inconclusive states;
- external/network participation;
- historical political geometry and approximation;
- project-wide spatial/time uncertainty.

The current claim-centric relational model should therefore remain the working canonical model while we map selected concepts to external semantic standards where useful.

### Current assessment

**Adopt the design/review methodology selectively; do not migrate the database to this ontology.**

References:
- Shimizu et al., “The enslaved ontology: Peoples of the historic slave trade,” Journal of Web Semantics 63 (2020), DOI 10.1016/j.websem.2020.100567.
- https://msupress.org/journals/journal-of-slavery-and-data-preservation/
- https://ojs.msupress.org/index.php/JSDP/about/submissions

---

## 4. DVC — release-artifact/data versioning

### What DVC offers

DVC keeps data-version metadata in Git while storing actual large data in remote storage. It supports reconstructing dataset snapshots from Git-tracked metadata and remote object versions.

This resembles the repository boundary already established for v0.6.1: Git holds identity/checksum metadata, while canonical binaries remain external.

### Candidate atlas role

Potentially version:

- canonical workbook releases;
- imported source datasets;
- historical geometry packages;
- large generated release materializations;
- immutable publication bundles.

### Questions that must be answered before adoption

1. Is DVC materially better than our existing checksum manifest + immutable object-storage design?
2. Which remote storage provider should be used without prematurely locking production hosting?
3. Can a historical release remain understandable/recoverable without requiring DVC-specific tooling?
4. How do DVC metadata, release manifests and PostgreSQL release manifests interoperate without duplicating authority?
5. Does DVC complicate preservation/deposit workflows for external scholars or archives?

### Current assessment

**Trial required; no architecture decision yet.** A minimal proof should compare:
- plain immutable object storage + SHA-256 manifest;
- DVC metadata + the same object storage.

Reference:
- https://dvc.org/doc
- https://dvc.org/blog/cloud-versioning/

---

## Phase-1 outcome

| Candidate | Outcome |
|---|---|
| Zotero | proceed to read-only integration proof |
| OpenRefine + WHG | proceed to controlled reconciliation proof |
| Enslaved/JSDP | incorporate as methodology/design comparison; no schema replacement |
| DVC | run a bounded release-artifact experiment before deciding |

## Next tooling pass

1. Define source-ingestion lifecycle from discovery through reviewed CLAIM_SOURCE.
2. Prototype Zotero SOURCE/SOURCE_VERSION crosswalk.
3. Prototype OpenRefine/WHG place reconciliation with explicit candidate/review states.
4. Compare DVC versus plain object-storage manifests.
5. Convert key Enslaved/JSDP lessons into atlas competency questions and release-documentation requirements.
6. Then evaluate semantic-export standards: SKOS, PROV-O, CIDOC CRM / Linked Art, SHACL.
7. Only after the evidence/release flow is stable, move into API/search/frontend tooling.
