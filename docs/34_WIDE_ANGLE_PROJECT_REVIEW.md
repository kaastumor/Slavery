# Wide-angle Project Review — #123

**Project:** Historical Slavery Atlas  
**Repository:** `kaastumor/Slavery`  
**Review date:** 2026-09-23  
**Base main:** `5f1972eb5634461e8eb18386cff75ef40b73c849`  
**Status:** ACTIVE REVIEW — no direction chosen yet

This record is the durable evidence trail for issue #123. It is a horizon review, not a feature plan. Completion of any implementation gate does not imply continuation.

## Review method

Dependency-ordered chunks:

1. repository reality;
2. project thesis/value;
3. foundation/ownership;
4. GitHub/CI/automation/sanitation;
5. adversarial/evaluation quality;
6. external precedents/practice;
7. competing project identities;
8. shrinkage and repairs;
9. final direction.

Each chunk records evidence before a final disposition is allowed.

---

## Chunk 1 — Repository reality

### Snapshot

- canonical branch: `main` at review start `5f1972eb5634461e8eb18386cff75ef40b73c849`;
- open substantive issues: #123 (this review), parent #116, blocked #43, blocked #26;
- open pull requests: none at review start;
- latest M2 integration/adversarial work is merged;
- foundation CI and MVP availability monitor are green at review start;
- repository tree: 379 entries;
- no tracked large-file problem: largest tracked blob is ~363 KB;
- approximately 100 remote branches are visible; many are merged historical topic/auto branches;
- GitHub reports `main.protected=false`; the connected integration cannot read/administer the protected-branch endpoint and repository rulesets returned none.

### Canonical-owner agreement

After the preparatory conformance pass (#143/#144), the current owner documents agree on:

- v0.6.1 remains the immutable canonical historical data release;
- `mvp-preview-ancient-v2` remains non-canonical;
- M2 implementation/adversarial gate is complete;
- #123 is the sole current substantive boundary;
- no H2 expansion, production M2 migration, global geography publication or successor canonical release is authorized before this review.

No competing live project manifest remains.

### Stale / accumulated state

1. **Backlog history is too large for its stated role.**  
   `BACKLOG.md` is canonical execution order but retains long completed P0/P1 narratives. Historical evidence is useful, but much of this belongs in issues/decisions/audits rather than the live queue.

2. **Remote branch accumulation is real.**  
   Old `arch/*`, `auto/*`, `fix/*`, `docs/*`, `feat/*` branches substantially exceed what a short-lived-branch model implies. This is repository hygiene debt, not project knowledge.

3. **Frontend dependency resolution is not lockfile-reproducible.**  
   `web/package.json` pins direct versions, but no tracked `web/package-lock.json` exists. CI/deploy workflows run `npm install --package-lock-only` and then `npm ci`, which resolves transitive dependency state afresh per run.

4. **GitHub Actions are version-tag pinned, not commit-SHA pinned.**  
   This is ordinary practice but weaker supply-chain reproducibility than the project applies to historical datasets/QGIS/Natural Earth. Whether to harden must be proportional to actual project stakes.

5. **Only one scheduled workflow exists:** `MVP Availability Monitor`, every 15 minutes.  
   `MVP Self Heal` is event-triggered from monitor failure and can restart the Supabase project. These are operationally meaningful and must be judged against the current non-user-critical preview horizon, not retained automatically.

6. **No workflow writes commits to main.**  
   Workflows may deploy Pages, mutate external Supabase state in tightly scoped production-promotion/self-heal paths, or write incident issues. Production geometry promotion is triggered only by a specific execution-request path on main.

7. **Generated output is mostly artifact-scoped, not Git-scoped.**  
   Pages snapshots and browser/geometry review packs are retained as Actions artifacts; tracked geometry pilots/fixtures are bounded evidence rather than bulk generated build state.

### Repository-size / sanitation result

- no unexpectedly large tracked blob;
- canonical workbook binary is excluded;
- backups/build outputs are excluded except keep-files;
- sanitation blocks common secret/key/env/dump/cache/merge-marker failure modes;
- sanitation currently does **not** enforce a generic tracked-file size ceiling or local-user path pattern.

### Chunk-1 provisional pressure carried forward

- backlog should likely shrink after the final review;
- old branches should be pruned when an administrative path is available;
- frontend lockfile reproducibility deserves a concrete repair;
- 15-minute monitoring + automatic project restart may be disproportionate for a non-canonical preview with no meaningful user base;
- branch protection is not present according to the branch API and should not be assumed.

**Checkpoint:** repository reality established. No final project direction inferred from this chunk.


---

## Chunk 2 — Project thesis and value

### Problem

The project addresses a real and difficult problem:

Historical evidence about slavery/coercion is fragmented across time, place, terminology, source traditions and scholarship. A useful global comparison must preserve provenance, uncertainty, disagreement, research coverage, changing geography and distinctions such as law vs practice and territorial practice vs external participation.

That problem survives.

### Claimed contribution

The current claimed contribution is a **traceable comparison layer** that allows global place/time inspection while preserving those distinctions instead of collapsing them into one universal score.

This is stronger than the original “global slavery-intensity map” concept; M1 falsified that older concept.

### Current project/product form

The current artifact is larger than a map:

- curated claim/evidence research data;
- PostgreSQL/PostGIS normalized research system;
- time-aware geography/resolver;
- release/reconstruction machinery;
- API + MapLibre public preview;
- research/geometry/release validation workflows.

### Implementation

Current implementation choices include PostgreSQL/PostGIS, Supabase, MapLibre, GitHub Actions, Python/SQL/TypeScript, JSON/GeoJSON and QGIS/GEOS/GDAL tooling.

None is itself the contribution.

### Durable value-evidence classification

Existing ledger entries:

- **V-001** — geometry rendering: useful capability/correctness confirmation; ordinary QGIS/GIS remains a strong baseline competitor.
- **V-002** — static outage fallback: operational resilience evidence, not evidence for the historical-research thesis.
- **V-003** — more tooling/integration: **NO_VALUE / reject-for-now**; supports keeping the system lean.
- **V-004** — original P0–P4/coverage/time model: **CONTRADICTION**; falsified the original universal-ordinal direction.
- **V-005** — full Cliopatria ingestion: useful discovery/capability evidence; whole-corpus inspection exposes failures hidden by case-by-case use.
- **V-006** — first semantic redesign: **CONTRADICTION then correction**; component-green was insufficient.

M1/M2 add strong evidence for semantic correctness, abstention, provenance separation, temporal/spatial truth conditions and adversarial discipline.

### Important missing value evidence

There is currently **no durable head-to-head evidence that a researcher or reader solves a meaningful historical question materially better with the full atlas system than with the strongest boring baseline**.

This is the largest gap in the value ledger.

Current repository scale reinforces the need to test this before expansion:

- 29 database migrations;
- 12 GitHub workflows;
- 34 Python test files + 9 SQL test files;
- 19 tracked experiment files;
- only 4 current staged territorial research case files + 1 staged external-participation case in the active case lanes;
- public preview remains a small non-canonical demonstration rather than a demonstrated research-use product.

Earlier research JSON batches contain more evidence records, but quantity is not user-value evidence.

### Strongest boring baseline

A credible baseline is:

1. specialist literature + structured source notes;
2. a well-designed spreadsheet or ordinary relational claim/evidence table;
3. QGIS/static or simple interactive GIS for geography;
4. ordinary search plus a strong general-purpose model used competently;
5. small scripts/notebooks for selected-year filtering, provenance checks and reproducible exports.

Against that baseline:

- **semantic distinctions are not unique to the application stack**; a disciplined table/corpus can store them;
- **historical GIS rendering is not unique**; QGIS can perform the core transformations;
- **source/provenance discipline is not unique**; it can be represented in conventional research data management;
- **release reconstruction, machine-enforced integrity and fail-closed publication boundaries are stronger in the current system than a casual spreadsheet workflow**, but a smaller relational/tooling package could preserve much of that advantage;
- **global selected-year integration across raw historical geography + specialist overrides + claim truth is a genuine integrated capability**, but its practical research/user value has not yet been benchmarked against a simpler scripted/GIS workflow.

### If the project disappeared

Genuinely valuable things that would be lost:

- the accumulated methodological corrections and adversarial fixtures;
- claim-specific provenance/uncertainty conventions;
- global-balance research corpus;
- pinned complete Cliopatria profile and resolver semantics;
- release reconstruction/provenance machinery;
- curated geometry-source decisions and tested failure cases.

Things that appear comparatively replaceable:

- the current public preview as a product;
- much of the hosting/availability machinery;
- some application-specific release/deployment plumbing;
- the exact current frontend.

### Distinctiveness

The project is not currently justified by “nobody combines these components exactly this way.”

Its plausible distinctiveness is narrower:

> an auditable, globally scoped historical evidence corpus and comparison method that keeps claim truth, uncertainty, source lineage and historical geography coupled enough for place/time inspection without collapsing them into false equivalence.

That contribution remains plausible, but **the full product/system form has not yet been shown necessary to deliver it**.

### Falsified / weakened claims

- one universal P0–P4 comparative intensity scale — rejected;
- better wording alone could rescue that model — rejected;
- green component tests imply conceptual correctness — rejected;
- additional generic tooling/integration is inherently useful — rejected/parked;
- current full-stack public atlas form is the demonstrated source of user value — **not established**.

### When distinctiveness was last seriously re-tested

M1/M2 seriously re-tested internal semantics and architecture against real historical cases and simpler *internal* alternatives.

They did **not** perform a real external baseline/user-task comparison.

That missing comparison should weigh heavily in the final direction.

**Checkpoint:** the problem survives; the contribution survives only in a narrower corpus/methodology/integrated-query form; necessity of the current full product form remains unproven.


---

## Chunk 3 — Foundation and canonical ownership

### What survives strongly

The conceptual foundation is coherent and unusually explicit about ownership boundaries.

#### Source / provenance ownership

Distinct canonical concepts exist for:

- conceptual `SOURCE`;
- exact `SOURCE_VERSION`;
- optional exact `SOURCE_ASSET`;
- ingest run / raw source record;
- bounded source assertions / atlas claims;
- claim-source relationship and evidence direction;
- reviewed publication/release membership.

Source origin does not automatically determine authority. The source policy asks what proposition a source can support and uses specialist scholarship as interpretive context rather than a universal source-ranking scalar.

#### Identity / role ownership

The model separates:

- actor identity from historical role;
- source-native names from normalized identity;
- source-native IDs from internal UUIDs;
- spatial identity from historical political specialization;
- spatial identity from geometry;
- timeless identity from time-bounded jurisdiction/relations.

This directly addresses demonstrated historical failure modes.

#### Observation / interpretation ownership

The project distinguishes:

- source-native bounded evidence;
- specialist interpretation;
- atlas synthesis;
- evidence direction (supports/challenges/qualifies/context);
- research workflow state;
- classification outcome;
- publication state.

Contrary evidence is preserved without mechanically turning every conflict into `disputed`.

#### Time / space ownership

M1/M2 produced evidence-driven separations:

- outer query window vs positive selected-year applicability;
- temporal precision vs applicability;
- open terminus constraint vs indefinite continuity;
- evidence locus vs inference extent;
- historical source geometry vs cartographic render geometry;
- raw Cliopatria baseline vs reviewed atlas spatial identity;
- baseline geometry provenance vs chosen specialist provenance.

These were not invented for diagram elegance; integrated adversaries found real failures when they were collapsed.

#### Current state / historical state

Canonical release v0.6.1, mutable working research state, non-canonical preview, release candidates and disposable M2 prototypes are explicitly different.

Published/reconstructed release state is not inferred from whatever happens to be current in research tables.

### Derived views

The publish/API/map layers are derived consumers, not research-authoring authorities.

Existing production publication views do not consume the M2 raw resolver by accident, and public clients do not have direct access to internal research schemas.

This ownership boundary survives.

### Generality test

The universal CLAIM/provenance architecture has earned substantial generality:

- territorial-practice assertions;
- legal events;
- actor attributes;
- external participation;
- voyage relationships;
- competing/supporting/challenging evidence.

M1 did **not** justify a universal final slavery ontology. The faceted practice vocabulary remains deliberately evolving, which is the correct boundary.

The post-M1 dimensions were attacked with real Hittite, Baekje, Silla, Mauryan and Maya cases plus synthetic failures. That justifies a prototype abstraction, but not the claim that the vocabulary is globally final.

### Foundation not yet demonstrated

1. **Present-day/living-person coverage** remains unproven and privacy-blocked. Do not extend the current historical architecture into sensitive modern person-level data merely because the schema could hold it.

2. **Post-M1 semantics are not yet proven across a globally representative research corpus at production scale.** M1/M2 establish structure and integrity, not final vocabulary completeness.

3. **Broad Cliopatria source-row → atlas spatial-identity mapping remains intentionally unresolved.** Raw geography infrastructure is not reviewed map truth.

These are boundaries, not reasons to redesign the foundation today.

### Current-owner conflict discovered

Two adopted current workflow documents still preserve pre-M1 operational instructions:

- `docs/06_RESEARCH_WORKFLOW.md` step 18 says to assign a P-level when evidence supports an intensity assessment;
- `docs/17_SOURCE_EVIDENCE_LIFECYCLE.md` Stage 11 presents P0–P4 as a current classification step.

That conflicts with D-058/current methodology, where P0–P4 is **legacy release compatibility only** and new post-M1 claims should use independent reviewed dimensions.

This is a concrete semantic failure and should be repaired in Chunk 8.

### Architecture-vs-contribution pressure

The semantic ownership model survives much better than the current product/operations footprint.

There is no evidence here requiring an architecture reset. The harder question is whether all current serving/release/operations machinery is needed to deliver the demonstrated contribution.

**Checkpoint:** conceptual foundation survives; no semantic redesign justified. Repair stale P-level research instructions. Keep M2 production migration parked until value/form review is complete.
