# Source → Evidence → Claim → Release Lifecycle

**Status:** proposed research workflow for evaluation. This document does not yet change canonical methodology or schema. Any promoted change must be recorded in the Decisions Log.

## Purpose

Define one auditable path from discovering a source to exposing a historical statement in the public atlas.

The lifecycle is designed to prevent common failure modes:

- treating bibliography as evidence;
- treating OCR/LLM extraction as historical fact;
- collapsing source identity and source version;
- losing source-native wording during normalization;
- auto-accepting entity/place reconciliation;
- inferring actor nationality from indirect context;
- letting archive density determine P0–P4;
- confusing legal status, territorial practice, external participation and research coverage;
- publishing draft claims simply because they exist in the database.

---

## Stage 0 — research question / coverage target

**Input:** a bounded research target, not an arbitrary source.

Examples:

- territorial practice in a spatial entity during a period;
- legal status/event for a jurisdiction;
- external/network participation;
- identity/role of an actor;
- unresolved research-coverage cell;
- historical geometry for a selected year.

**Required output:**

- research target;
- temporal scope;
- spatial scope;
- claim dimension being investigated;
- known uncertainty;
- search/discovery strategy.

**Tool candidates:** Scite, library catalogues, archival finding aids, OpenAlex/Crossref, specialist bibliographies.

**Forbidden shortcut:** source abundance must not redefine the research target.

---

## Stage 1 — source discovery candidate

A search hit, bibliography entry, archive catalogue result, dataset record or recommendation is a **candidate**, not yet atlas evidence.

Capture at minimum:

- candidate title;
- author/institution;
- source type;
- discovery channel;
- stable identifier/URL where available;
- date discovered;
- why it may be relevant.

**Candidate tools:** Scite, Zotero, archive catalogues, OpenAlex/Crossref.

**Review gate:** relevance screening.

---

## Stage 2 — SOURCE identity

Create or reconcile the conceptual SOURCE only after confirming what the source actually is.

Examples:

- monograph;
- journal article;
- archival collection;
- manuscript/register;
- dataset;
- voyage database;
- legal instrument;
- institutional report.

A SOURCE is **not** the same thing as a particular edition, scan, snapshot, catalogue item or accessed web state.

**Candidate tool:** Zotero can help initialize bibliographic metadata.

**Canonical authority:** atlas database.

---

## Stage 3 — SOURCE_VERSION

Every evidence link should resolve to the exact source version actually reviewed.

Possible version distinctions:

- edition;
- article version;
- archive item;
- database snapshot;
- specific voyage page/record;
- web state/accessed resource;
- digitized scan;
- dataset release.

Capture:

- exact version label/date;
- persistent identifier or URL;
- access date when relevant;
- licence/redistribution status;
- version notes;
- relationship to conceptual SOURCE.

**Critical rule:** never silently replace an unavailable exact version with a related source.

---

## Stage 4 — SOURCE_ASSET / digital object

Optional binary/digital artifact associated with the source version.

Examples:

- PDF;
- IIIF manifest;
- image sequence;
- CSV;
- XLSX;
- TEI/XML;
- archived HTML;
- geometry package.

Capture:

- checksum;
- media type;
- storage locator;
- licence/redistribution status.

**Candidate tools:** IIIF, immutable object storage, later DVC if justified.

**Boundary:** the asset is not the source claim itself.

---

## Stage 5 — machine/human transcription or extraction layer

For scanned, manuscript or long-form material, produce a separate derivative.

Possible derivatives:

- OCR;
- HTR;
- corrected transcription;
- translated text;
- structured table extraction;
- LLM-assisted candidate extraction.

Capture:

- tool/model/version;
- source asset;
- page/canvas/locator;
- date;
- correction/review state;
- raw machine output where practical.

**Candidate tools:** Transkribus, GROBID, OCR/HTR, LLM extraction.

**Hard gate:** no machine-generated extraction becomes a reviewed historical claim automatically.

---

## Stage 6 — candidate historical assertion

Break source material into bounded assertions before normalization.

Examples:

- person X owned vessel Y in year Z;
- a law prohibited slave trading in jurisdiction J;
- debt bondage is documented in region R;
- a polity participated in captive export;
- a source is inconclusive about territorial practice.

Preserve:

- source wording;
- locator;
- assertion type;
- temporal wording;
- spatial wording;
- directness;
- uncertainty;
- whether the assertion supports, challenges, qualifies or merely contextualizes another claim.

**Rule:** one paragraph may generate multiple candidate claims; one claim may require multiple sources.

---

## Stage 7 — entity/place reconciliation

Resolve referenced identities without overwriting source-native strings.

### Actors

Possible authorities may include VIAF, Wikidata or specialist authorities, but matching remains review-assisted.

Never infer nationality/political identity from:

- vessel flag;
- port;
- residence;
- business base;
- surname;
- company jurisdiction.

### Places

Candidate workflow:

```text
raw place string
    ↓
OpenRefine reconciliation candidates
    ↓
WHG / authority identifiers + temporal/place context
    ↓
human judgment
    ↓
SPATIAL_ENTITY mapping
```

OpenRefine reconciliation is semi-automated and preserves the original string alongside reconciliation metadata. WHG can enrich candidates with geometry, alternative names and temporal bounds. These are candidate identity aids, not automatic historical-jurisdiction determinations.

---

## Stage 8 — normalized claim candidate

Map the assertion into the atlas claim model while preserving uncertainty.

Possible dimensions:

- TERRITORIAL_PRACTICE_CLAIM;
- LEGAL_EVENT;
- ACTOR_ATTRIBUTE_CLAIM;
- EXTERNAL_PARTICIPATION_CLAIM;
- voyage relationship claim;
- research-coverage assessment.

Required checks:

- correct claim dimension;
- source-native text still recoverable;
- temporal precision represented;
- spatial precision represented;
- claim/source relationship explicit;
- source independence considered;
- no derived nationality;
- no mechanical P-level;
- no false absence inference.

---

## Stage 9 — evidence-package review

Review the **claim plus its evidence package**, not merely one row.

Assess:

- directness of evidence;
- primary vs secondary role;
- independence between sources;
- chronological/spatial fit;
- competing interpretations;
- terminology/status ambiguity;
- specialist scholarship;
- whether additional sources are needed.

Primary sources are strongest for bounded events, transactions, terminology, law, dates and locations.

Specialist secondary scholarship is normally necessary for prevalence, continuity, classification and larger structural interpretation.

---

## Stage 10 — classification / P-level where appropriate

Only territorial-practice claims may receive P0–P4.

- P0 = explicit unknown/no usable classification, never absence;
- P1 = isolated direct attestation;
- P2 = repeated independent attestations;
- P3 = systemic/institutional practice strongly supported;
- P4 = widespread or structurally major practice supported by scholarship.

A claim may remain with **NULL practice_level** when an assessment has not been made.

Never derive the level mechanically from:

- document counts;
- voyage counts;
- archive size;
- citation count;
- number of imported rows.

---

## Stage 11 — review state

Suggested lifecycle:

```text
candidate
  → draft
  → reviewed
  → rejected / returned for research
```

Publication is a separate axis:

```text
unpublished
  → published
  → superseded / withdrawn
```

A reviewed claim is not automatically public.

---

## Stage 12 — QC / release membership

A release candidate must define exactly what it contains.

Required release outputs:

- exact source versions;
- exact included claims/entities/geometries;
- changelog;
- QC summary;
- unresolved-issues list;
- reproducible release manifest;
- data dictionary / codebook;
- methodology/version references.

JSDP's publication model is a useful peer precedent: research data are accompanied by supporting documentation such as data dictionaries/codebooks and deposited for long-term access after review.

---

## Stage 13 — publish layer

Only reviewed/published release material reaches public services.

Public consumers:

- JSON/API;
- vector/GeoJSON layers;
- PMTiles or Martin;
- map/timeline UI;
- evidence inspector;
- downloadable release materializations.

The public application must never query unrestricted draft research tables.

---

## Tool-boundary summary

| Tool | Allowed role | Must not become |
|---|---|---|
| Scite | literature discovery, citation context | automatic truth/ranking engine |
| Zotero | source library and bibliographic workflow | canonical claim datastore |
| IIIF | exact digital-object/canvas addressing | interpretation layer |
| Transkribus/GROBID | transcription/structure extraction | reviewed evidence |
| OpenRefine | reconciliation workbench | automatic identity authority |
| WHG | historical-place candidate authority | automatic polity/jurisdiction resolver |
| DVC/object store | artifact/version distribution | canonical historical interpretation |
| PostgreSQL/PostGIS | canonical reviewed research model after migration | opaque dump without provenance |
| ontology/RDF tools | interoperability/validation | mandatory replacement for relational core |
| MapLibre/API | publication/presentation | research-authoring authority |

---

## Immediate implementation implications

1. Add explicit candidate/review states to future research-ingestion tooling rather than inserting directly into canonical claims.
2. Keep external authority identifiers separate from internal UUIDs.
3. Preserve reconciliation candidates/decisions in staging or audit data.
4. Define release membership before database canonical cut-over.
5. Make exact source-version registration a prerequisite for reviewed CLAIM_SOURCE links.
6. Treat machine extraction as a derivative with tool/model provenance.
