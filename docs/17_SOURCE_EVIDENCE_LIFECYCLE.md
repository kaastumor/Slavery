# Source → Evidence → Claim → Release Lifecycle

**Status:** adopted research workflow guidance. Methodological authority comes from the core methodology/source-policy documents and the Decisions Log.

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
- treating any contradiction as an automatic `disputed` classification;
- attempting to replace specialist historiography with ad hoc project interpretation;
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

**Forbidden shortcut:** source abundance must not redefine the research target.

---

## Stage 1 — specialist historiography discovery

Before attempting broad classification, identify the relevant historical scholarship.

Look for:

- current or authoritative specialist syntheses;
- dedicated monographs/articles on the institution or status category;
- major historiographical disagreements;
- scholarship identifying the primary/source-native evidence base;
- newer work that materially revises older interpretations.

A general encyclopedia, search snippet or isolated article can help discovery, but should not substitute for specialist historiography where the question is historically complex.

**Output:** candidate interpretive literature and known controversies.

---

## Stage 2 — source discovery candidate

A search hit, bibliography entry, archive catalogue result, dataset record or recommendation is a **candidate**, not yet atlas evidence.

Capture at minimum:

- candidate title;
- author/institution;
- source type;
- discovery channel;
- stable identifier/URL where available;
- date discovered;
- why it may be relevant.

**Review gate:** relevance screening.

---

## Stage 3 — SOURCE identity

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

**Canonical authority:** atlas database.

---

## Stage 4 — SOURCE_VERSION

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

## Stage 5 — SOURCE_ASSET / digital object

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

**Boundary:** the asset is not the historical claim itself.

---

## Stage 6 — machine/human transcription or extraction layer

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

**Hard gate:** no machine-generated extraction becomes a reviewed historical claim automatically.

---

## Stage 7 — candidate historical assertions

Break source material into bounded assertions before synthesis.

Examples:

- person X owned vessel Y in year Z;
- a law prohibited slave trading in jurisdiction J;
- debt bondage is documented in region R;
- a polity participated in captive export;
- a source claims slavery was absent;
- a specialist argues that a historical status should not be classified as slavery.

Preserve:

- source wording;
- locator;
- assertion type;
- temporal wording;
- spatial wording;
- directness;
- uncertainty;
- whether the assertion supports, challenges, qualifies or merely contextualizes another claim.

**Rule:** one paragraph may generate multiple candidate assertions; one atlas claim may require multiple sources.

---

## Stage 8 — entity/place reconciliation

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
authority/reconciliation candidates
    ↓
temporal/place context
    ↓
human judgment
    ↓
SPATIAL_ENTITY mapping
```

External authorities can enrich candidates with geometry, alternative names and temporal bounds. They are candidate identity aids, not automatic historical-jurisdiction determinations.

---

## Stage 9 — normalized claim candidate

Map the bounded assertions into the atlas claim model while preserving uncertainty.

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

## Stage 10 — evidence-package synthesis

Review the **historical question plus the full evidence package**, not merely one row.

Assess:

- directness of evidence;
- role of primary/source-native evidence;
- role of specialist interpretation;
- independence between sources;
- chronology and transmission;
- genre and purpose;
- geographic/spatial fit;
- representativeness;
- competing interpretations;
- terminology/status ambiguity;
- whether newer scholarship revises older interpretations;
- whether additional sources are needed.

### Normal synthesis rule

The atlas should record the **best-supported designation reflected in the evidence package and specialist historiography**.

Contrary evidence remains attached as `challenges` or `qualifies`.

The atlas does not become blank or `disputed` merely because contradictory evidence exists.

### Genuine dispute rule

Use `disputed` only where credible specialist scholarship remains materially divided over a classification after the evidence has been synthesized.

If historians broadly resolve the contradiction, follow the best-supported interpretation and preserve the losing/limiting evidence as provenance.

### Project-role boundary

The atlas is a collector and synthesizer of historical evidence and scholarship.

It should not independently attempt to settle major philological, archaeological or historiographical controversies from primary material where specialist scholarship already addresses them.

---

## Stage 11 — classification / P-level where appropriate

Only territorial-practice claims may receive P0–P4.

- P0 = explicit reviewed assessment that no usable P1–P4 classification is currently available; never absence;
- P1 = isolated direct attestation;
- P2 = recurrent/repeatedly evidenced practice;
- P3 = systemic/institutional practice strongly supported;
- P4 = widespread or structurally major practice supported by scholarship.

A positive historical designation may remain with **NULL practice_level** when intensity has not yet been assessed.

Never derive the level mechanically from:

- document counts;
- voyage counts;
- archive size;
- citation count;
- number of imported rows;
- number of captives in one event.

---

## Stage 12 — unknown / no-claim handling

If no defensible territorial-practice claim can be produced, the atlas remains **unknown** for that place/time.

Do not create a negative historical assertion from:

- missing sources;
- unresearched coverage;
- inconclusive research;
- unresolved geometry;
- P0;
- failure to locate a source during one research pass.

Research coverage records what the project has reviewed; it does not convert missing claims into historical absence.

---

## Stage 13 — review state

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

## Stage 14 — QC / release membership

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

QC should verify that source conflicts have been synthesized rather than converted mechanically into `disputed`, and that challenging evidence remains linked where relevant.

---

## Stage 15 — publish layer

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
| literature/citation search | discovery, citation context | automatic truth/ranking engine |
| bibliographic manager | source library and bibliographic workflow | canonical claim datastore |
| IIIF/digital object systems | exact digital-object/canvas addressing | interpretation layer |
| OCR/HTR/LLM extraction | transcription/structure/candidate extraction | reviewed evidence or historical authority |
| reconciliation tools | candidate entity/place matching | automatic identity authority |
| historical place authorities | candidate geography/identifier source | automatic polity/jurisdiction resolver |
| object/version storage | artifact/version distribution | canonical historical interpretation |
| PostgreSQL/PostGIS | normalized reviewed research model | opaque dump without provenance |
| MapLibre/API | publication/presentation | research-authoring authority |

---

## Immediate implementation implications

1. Research tooling should preserve candidate/review states rather than publishing directly.
2. Exact source-version registration remains a prerequisite for reviewed CLAIM_SOURCE links.
3. Evidence direction must distinguish support, challenge, qualification and context.
4. Research templates should encourage specialist-historiography capture for broad classification claims.
5. QC should flag unsupported use of `disputed` where no actual historiographical dispute is documented.
6. Public claims should expose contrary evidence where materially relevant.
7. External authority identifiers remain separate from internal UUIDs.
8. Machine extraction remains a derivative with tool/model provenance.
