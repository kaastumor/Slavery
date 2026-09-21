# Tooling evaluation triggers

**Status:** operational guidance for issue #2; not an architecture decision  
**Date:** 2026-09-21

Issue #2 is intentionally a toolbox, not an implementation queue. A named tool is evaluated only when a concrete atlas workflow has a demonstrated need that the existing stack does not already satisfy. Evaluation does not authorize a schema, methodology, release, hosting, or canonical-data change; those still require the normal decision process where applicable.

## Default rule

Do not add infrastructure for novelty. Prefer the smallest reversible experiment that answers a measured workflow question. Keep PostgreSQL/PostGIS canonical, historical source geometry immutable, research claims human-reviewed, and published releases reconstructible.

## Trigger matrix

| Workflow need | Candidate(s) worth evaluating | Trigger evidence | Minimum acceptance evidence | Do not do |
| --- | --- | --- | --- | --- |
| Bibliography/source-library friction | Zotero API/local API | repeated manual duplicate metadata entry or inability to preserve stable bibliography identifiers | round-trip sample preserves source/version identity, locators and licensing metadata without becoming a second canonical store | migrate canonical claims into Zotero |
| Scholarly discovery/citation context | Scite, OpenAlex, Crossref | a bounded research batch needs systematic literature discovery beyond ordinary targeted search | benchmark on a real research question; record useful recall, false leads, provenance and manual-review burden | treat citation counts or model summaries as historical evidence |
| Archive/manuscript image access | IIIF | target archive exposes IIIF and image-level citation/transcription is materially useful | stable manifest/canvas identifiers and reproducible source locators | mirror restricted images by default |
| PDF structure/reference extraction | GROBID | a batch of accessible secondary-literature PDFs makes manual bibliography extraction a bottleneck | compare extraction accuracy against hand-checked sample; preserve original source asset/version | promote extracted text to reviewed claims automatically |
| Manuscript OCR/HTR | Transkribus or archive-native OCR/HTR | a research question depends on handwritten/poorly OCRed material at sufficient volume | hand-checked character/word error sample and page-level provenance | treat transcript as the primary source itself |
| Vocabulary/RDF interoperability | SKOS, PROV-O, CIDOC CRM/Linked Art, SHACL | a real export/integration consumer requires interoperable RDF/vocabularies | lossless mapping of a representative claim/evidence/provenance sample and validation fixtures | rewrite the canonical relational model merely to produce RDF |
| Human-reviewed reconciliation | OpenRefine, WHG | a batch has enough unresolved entities/places that manual one-by-one reconciliation is the bottleneck | candidate generation remains review-only; accepted links retain source and decision provenance | auto-accept reconciliation |
| Historical geometry QA | QGIS LTR / established GEOS/GDAL tooling | geometry requires bounded specialist comparison or render preprocessing | immutable input, reproducible transform, quantitative + visual QC, quarantine/fallback on failure | hand-edit polity coastlines or weaken QC |
| Large immutable artifacts | DVC + object storage | repository/Actions artifact size, retention, or reproducibility becomes an observed constraint | content-addressed immutable retrieval, checksum verification, documented recovery and cost model | add paid storage without approval or create a second canonical datastore |
| Search/API complexity | PostgreSQL FTS/trigram, then FastAPI only if needed | measured user/product need exceeds current `atlas-data` contract | benchmark real queries; preserve release-bound serving semantics and private-schema boundary | add a search engine or service tier pre-emptively |
| Large stable map layers | PMTiles / Martin | the Stage C triggers in `docs/21_PERFORMANCE_STRATEGY.md` are repeatedly observed | release-bound immutable tiles, provenance/QC, fallback and browser benchmark | tile rewrite merely because the technology is available |
| High-volume routes/networks | deck.gl | real network/flow layer exceeds MapLibre's practical rendering envelope | representative browser benchmark including mobile/accessibility impact | adopt for ordinary polygon/point layers |
| Component regression/accessibility | Storybook, Vitest, Playwright + axe | component count or regressions make current tests insufficient | catches a demonstrated regression class without duplicating existing CI | add a framework solely for coverage optics |
| Map-style authoring | Maputnik | style iteration becomes error-prone in source JSON | reproducible style artifact and reviewable diff | let style tooling redefine data semantics |

## Current disposition (2026-09-21)

No candidate currently has a trigger strong enough to justify a new infrastructure commitment:

- The published preview is below the vector-tile/PMTiles adoption gate defined in `docs/21_PERFORMANCE_STRATEGY.md`.
- QGIS/GEOS/GDAL already satisfy the demonstrated historical-geometry preprocessing need; issue #27 was resolved without a new platform.
- PostgreSQL/PostGIS plus the existing `atlas-data` boundary satisfy current API/search needs.
- Current release artifacts fit the existing GitHub/Pages recovery path; no observed large-artifact storage failure justifies DVC/object storage yet.
- Research tooling should be benchmarked against the next bounded research question that actually needs it, rather than evaluated abstractly.

Therefore issue #2 should remain an evaluation register and be treated as **PARKED until a trigger fires**. When a trigger fires, open a bounded child issue naming the workflow problem, corpus/sample, comparison baseline, acceptance metrics, provenance/licensing constraints, cost implications, and rollback/removal path.

## Evaluation record template

For each future experiment record:

1. **Problem:** concrete workflow bottleneck or capability gap.
2. **Baseline:** how the atlas handles it today.
3. **Candidate:** tool/version/deployment mode being tested.
4. **Sample:** bounded real atlas corpus or workload.
5. **Metrics:** quality, reproducibility, review burden, performance, cost, licensing and preservation as relevant.
6. **Result:** adopt, reject, or defer, with evidence.
7. **Architecture impact:** none, or link the required Decisions Log entry before implementation.
8. **Exit path:** how to remove/replace the tool without losing canonical data or provenance.
