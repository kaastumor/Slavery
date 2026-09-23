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


---

## Chunk 4 — GitHub, CI, automation and sanitation

### GitHub project-system result

**Main is canonical in practice, but not technically protected.**

- repository API reports `main.protected=false`;
- repository rulesets returned none;
- the connected integration cannot read/administer the protected-branch endpoint;
- substantive autonomous work has nevertheless used short-lived branches + PR + green CI discipline.

Do not describe branch protection as existing.

### Autonomous execution

The ChatGPT-side **Slavery Atlas Build Loop is disabled**. The old ChatGPT Atlas availability watch is also disabled.

Therefore there is no hidden active autonomous project executor continuing #123 in the background.

The repository-versioned worker runbook remains useful as an execution contract if automation is intentionally re-enabled later.

### Workflow inventory

12 repository workflows remain.

Distinct responsibilities mostly survive:

- foundation deterministic CI;
- web PR build;
- Pages deployment + static snapshot;
- research-case validation;
- release-candidate validation;
- geometry candidate build;
- geometry browser review;
- geometry promotion gate;
- production geometry promotion;
- public live/fallback browser review;
- live availability monitor;
- event-triggered self-heal.

### Deterministic CI vs live probes

The separation is conceptually good:

- `foundation-ci` is deterministic/local PostGIS and does not depend on public network availability;
- browser/live monitoring uses separate workflows;
- external availability does not determine ordinary branch-green.

### Duplicate/overlapping execution

`web-mvp.yml` runs on both PR and main push, while `deploy-pages.yml` also rebuilds the web application on main web changes.

The PR validation role is distinct; the second main build is redundant. A small consolidation is justified: retain web build on PR, let deployment own main-build/deploy.

### Scheduled/live operations

Only one repository workflow is scheduled:

- `MVP Availability Monitor` every **15 minutes**, plus every main push/manual dispatch.

On monitor failure, `MVP Self Heal` may:

- probe twice;
- inspect Supabase project state;
- use a management credential;
- automatically restart the Supabase project;
- write incident/recovery comments.

This was sensible while proving outage handling, but the current preview is non-canonical, has static fallback, and has no demonstrated user-critical availability requirement.

**Assessment:** 15-minute monitoring and automatic external-project restart have outlived the current horizon. Availability observation may remain useful at a much lower cadence; automatic self-heal does not currently justify its mutation authority.

### Workflows that can mutate meaningful state

No workflow commits to `main`.

External/project mutations include:

- Pages deployment;
- production geometry promotion to Supabase from a specific execution request on main;
- self-heal project restart;
- incident issue create/update/close.

Production geometry promotion currently lacks verified GitHub environment protection because #43 is blocked and main itself is unprotected. Its exact-artifact gate is strong, but automatic push-triggered external mutation should be reduced while no promotions are authorized.

### Git is not being used as an operational research database

Research state is stored in structured files/database/release artifacts; Git stores source, fixtures, manifests, reviewed public-safe research cases and decisions.

Actions artifacts carry generated browser/release/geometry evidence with bounded retention.

No large generated-output accumulation exists in Git.

### Sanitation

Current sanitation correctly rejects:

- tracked `.env`;
- canonical XLSX release binaries;
- backups/cache directories;
- dump/sql.gz;
- PEM/private-key extensions;
- common secret token patterns;
- merge markers;
- missing canonical project-system files.

Gaps:

- no generic maximum tracked-file threshold;
- no explicit `.pfx/.p12` block;
- no machine-specific local-user-path scan despite the project runbook prohibiting local paths.

These can be strengthened cheaply without a new security system.

### Dependency/reproducibility assessment

Positive:

- Python runtime dependency is exact-version pinned;
- direct web dependencies are exact-version pinned;
- QGIS production candidate container is digest-pinned;
- Natural Earth input is exact commit/checksum pinned.

Weaker:

- no tracked npm lockfile; CI resolves transitive packages afresh with `npm install --package-lock-only`;
- standard GitHub Actions use mutable major-version tags rather than commit SHAs;
- local PostGIS compose image uses a version tag rather than digest.

For current stakes, action/Docker SHA pinning is a **low-to-medium hardening opportunity**, not a reason to add enterprise supply-chain infrastructure.

The missing npm lockfile is the clearest reproducibility defect and is worth fixing.

### Project-system repair candidates for Chunk 8

- retire automatic Supabase self-heal;
- reduce live monitor from every 15 minutes to a modest demonstration cadence;
- make production geometry promotion explicit/manual while environment protection remains unavailable;
- eliminate duplicate main web build;
- track an npm lockfile;
- strengthen sanitation for file size, local paths and PFX/P12;
- prune merged remote branches when an administrative path exists.

**Checkpoint:** GitHub/CI design is basically sound, but operations are over-provisioned relative to demonstrated public value. Simplification is justified without weakening research correctness.


---

## Chunk 5 — Adversarial and evaluation quality

### Adversarial quality

This is a project strength.

The adversarial fixtures/gates attack real semantic assumptions rather than cosmetic edge cases:

- Silla possible-date window vs continuous truth;
- Silla local evidence vs whole-polity inference;
- Baekje bounded enslavement event vs enduring territorial practice;
- Hittite simultaneous status/function/property/transmission dimensions;
- Mauryan supporting/challenging/qualifying evidence;
- Maya unresolved geometry vs map-first pressure;
- reverse mutation of relational state;
- baseline vs chosen specialist geometry provenance;
- open terminus vs indefinite continuity.

M1 and M2 both produced **REVISE** outcomes after apparently successful component work. That is strong evidence that adversarial review is not ceremonial.

### Negative/fail-closed behavior

Negative controls are substantial:

- wrong-kind claim subtype inserts are rejected;
- claim kind cannot be casually mutated;
- direct canonical preview promotion is rejected;
- research staging cannot self-publish;
- unresolved geometry cannot smuggle in a shape;
- external/network cases reject territorial P-level leakage;
- nationality inference guardrails fail closed;
- exact-retry vs changed-content behavior is tested;
- release drift and provenance mismatches fail closed;
- resolver ambiguity remains unresolved rather than guessed.

### Real/orthogonal cases

The conceptual abstractions were not frozen from one region alone.

Real cases span at least:

- Anatolia / Hittite;
- Korea / Silla and Baekje;
- Mauryan South Asia;
- Maya;
- additional non-Atlantic research fixtures.

This is sufficient to justify the **structural separations** discovered in M1, though not a final global vocabulary.

### Abstention / ambiguity

The project can represent:

- unknown/no claim;
- unresolved geometry;
- disputed classification;
- inconclusive completed review;
- unassessed semantic dimensions;
- ambiguous hierarchy;
- quarantined geometry;
- source-native uncertainty.

Ambiguity is generally preserved instead of converted into a forced answer.

### Implementation success vs analytical validation

The repository repeatedly states that green CI is not historical/editorial approval, and M1/M2 behavior supports that claim.

However, **project-value evaluation remains much weaker than correctness evaluation**.

The tests can answer “does the architecture preserve this distinction?” but not yet “does this project materially improve a historian/researcher/user task over the strongest simple workflow?”

That is the missing adversary.

### Method-maturity reconciliation

| Capability / method | Maturity after this review | Reason |
| --- | --- | --- |
| P0–P4 as universal target comparison | **RETIRED** | M1 falsified the construct; retain only historical-release compatibility. |
| Current P0–P4 preview | **VALIDATED_FOR_VIEW only as a frozen legacy/non-canonical demonstration** | Operationally tested, but its ordinal rhetoric is not the target methodology. |
| Post-M1 semantic model | **EXPERIMENTAL** | Strong real/synthetic adversarial evidence and disposable relational implementation; not yet broad production research/public view. |
| Post-M1 temporal applicability / locus-extent semantics | **EXPERIMENTAL** | Correctness is well tested; user/research scaling is not. |
| Complete Cliopatria raw ingestion | **VALIDATED_FOR_AUTOMATION as raw ingestion** | Exact corpus/checksum, idempotency and no-publication boundaries tested. |
| Cliopatria selected-year atlas resolver | **EXPERIMENTAL** | Full corpus behavior is frozen, but broad source→atlas identity resolution/publication remains unresolved. |
| Geometry candidate generation/QC | **VALIDATED_FOR_AUTOMATION for candidate production** | Reproducible toolchain, quantitative QC, quarantine and artifact manifests. |
| Geometry publication choice | **VALIDATED_FOR_VIEW with reviewed promotion boundary** | Human/explicit accepted override remains required. |
| Research-case structural ingestion | **VALIDATED_FOR_AUTOMATION for package integrity only** | Idempotency/schema checks do not validate historical interpretation. |
| Historical evidence synthesis | **human-reviewed method, not automation** | Specialist interpretation remains the authority boundary. |
| Release reconstruction / public serving boundary | **VALIDATED_FOR_AUTOMATION within current release contract** | Exact membership/bundle, rollback/fallback and CI are exercised. |
| Automatic MVP self-heal | **RETIRED candidate** | Works operationally, but current value/risk no longer justifies automatic external restart. |

### Acceptance-boundary quality

Where execution required unavailable admin/cost/private capability, the project generally preserved the real criterion instead of weakening it:

- protected environment/staging boundary remains blocked in #43;
- live migration-history mutation remains blocked in #26;
- canonical workbook is externally supplied by exact checksum rather than replaced with a synthetic proxy;
- visual geometry review is captured as explicit review evidence.

This is healthy.

### Evaluation gap that should determine the next direction

A new integrated test should **not** be another schema or resolver test.

The missing discriminating experiment is a real research/user task performed with:

A. the strongest boring baseline, and  
B. the smallest atlas-derived evidence package/interface necessary to express the same question.

Measure:

- time/effort to reach an inspectable answer;
- provenance recoverability;
- uncertainty/abstention preservation;
- cross-place/time comparison quality;
- error/overclaim rate;
- what the atlas exposes that the baseline misses;
- what the baseline does just as well.

Do this before productionizing M2 or resuming broad H2 expansion.

**Checkpoint:** adversarial correctness survives strongly. Method maturity is now explicitly bounded. Project-value validation remains the critical missing test.


---

## Chunk 6 — External precedents and practice

External review is used subtractively. The project should not become a generic digital-humanities platform, gazetteer, ontology platform or scholarly repository.

### 1. nodegoat — **BENCHMARK + REMOVE FROM OUR SCOPE**

Official project:
- https://nodegoat.net/about
- https://nodegoat.net/faq

nodegoat already provides:

- custom humanities data models;
- source references at object/description level;
- temporal and spatial attributes;
- diachronic maps/timelines;
- relational/network analysis;
- data import/export and API access;
- configurable public research interfaces;
- collaborative research environments.

This is a substantially stronger baseline than “spreadsheet + static GIS.”

**Consequence:** do not build generic:

- collaborative research database UI;
- arbitrary data-model designer;
- generic temporal/spatial visualization platform;
- generic network-analysis workbench;
- generic humanities publication interface.

If the Atlas cannot demonstrate value beyond nodegoat + domain methodology/data, it should shrink/redirect rather than reproduce that platform class.

### 2. Enslaved.org / Enslaved Ontology — **BENCHMARK + LEARN FROM + REMOVE FROM SCOPE**

Sources:
- https://enslaved.org/
- Shimizu et al. 2020, DOI 10.1016/j.websem.2020.100567

Enslaved.org already searches/interconnects very large record collections across People, Events, Places and Sources, with visual exploration.

The Enslaved Ontology was explicitly developed from historian use cases to integrate heterogeneous historic slave-trade datasets, using modular ontology design.

**Learn from:**
- historian/use-case-driven ontology work;
- modularity;
- explicit person/event/place/source separation;
- ethics and stewardship;
- interoperability.

**Remove from scope:**
- becoming another generic person/event search repository for the historical slave trade;
- duplicating large Atlantic/African record integration where Enslaved/other specialist projects already provide it.

The Atlas should reference/import bounded evidence where needed for its distinct comparative questions, not compete on record count.

### 3. Journal of Slavery and Data Preservation — **REUSE + BENCHMARK + REMOVE FROM SCOPE**

Source:
- https://ojs.msupress.org/index.php/JSDP

JSDP treats curated slavery datasets and their documentation as scholarly outputs and deposits data/supporting documentation in durable repositories.

**Consequence:**
- benchmark release documentation against scholarly data-publication expectations;
- later deposit suitable stable datasets in established scholarly repositories;
- do **not** build a custom journal, peer-review system or long-term preservation institution.

The Atlas's exact release bundles may support reproducibility, but should not be mistaken for a complete archival/publishing ecosystem.

### 4. World Historical Gazetteer + OpenRefine reconciliation — **REUSE**

Source:
- https://docs.whgazetteer.org/content/technical/apis.html

WHG exposes Linked Places Format and an OpenRefine-compatible reconciliation API, and explicitly describes reconciliation as **candidate suggestion for human review**, not adjudication.

This matches the Atlas's identity rules almost exactly.

**Consequence:** use/reuse candidate reconciliation when a real workload trigger appears; do not build a historical gazetteer or fuzzy-place-matching authority.

WHG's source-specific licensing/attribution behavior is also a useful precedent for preserving source-native licensing rather than assigning one blanket licence to aggregated data.

### 5. W3C PROV-O — **LEARN FROM / interoperability benchmark**

Source:
- https://www.w3.org/TR/prov-o/

PROV-O provides a stable provenance interchange model around Entity / Activity / Agent and qualified derivation/attribution relationships.

The Atlas already has domain-specific source/version/asset/ingest/claim/release provenance.

**Consequence:** do not rewrite the relational core into RDF/OWL. If a real interoperability consumer appears, map representative provenance to PROV-O and test for loss.

### 6. CIDOC CRM / ISO 21127:2023 — **BENCHMARK + LEARN FROM**

Sources:
- https://cidoc-crm.org/
- https://cidoc-crm.org/node/8920

CIDOC CRM is explicitly intended to mediate heterogeneous cultural-heritage information and now includes robust spatiotemporal/chronological modeling concerns.

**Consequence:** use CIDOC CRM as a semantic adversary for events, actors, time, places, source/document relationships and interoperability.

Do not create an ISO compliance program and do not migrate the internal model merely for standards alignment.

### 7. Linked Art — **LEARN FROM**

Source:
- https://linked.art/model/

Linked Art is a usability-oriented application profile over cultural-heritage standards and includes people, places, events, documents, provenance and specific assertions.

**Consequence:** useful future export/interface precedent; no internal-model rewrite without a real consumer.

### 8. Seshat / existing historical datastores — **REUSE + BENCHMARK**

Source:
- https://seshat-global-history-databank.readthedocs.io/

Seshat demonstrates a mature global-history databank and reproducible research practices.

The Atlas already correctly treats external historical datasets as sources rather than trying to become the authoritative global database for every historical variable.

**Consequence:** continue to reuse/pin source datasets; do not expand into generic global-history data collection unrelated to the Atlas's slavery/coercion evidence question.

### External-review synthesis

The strongest external precedents materially narrow the Atlas contribution.

The project should **not** justify itself as:

- a digital-humanities database;
- a temporal GIS;
- a collaborative historical-research workbench;
- a generic graph/network explorer;
- a historical gazetteer;
- an ontology platform;
- a slave-trade person/event repository;
- a scholarly preservation platform.

Existing projects already cover those categories well.

The remaining plausible contribution is domain-specific:

> a globally/deep-time, claim-specific evidence corpus and comparison protocol for slavery/coercion that explicitly separates evidentiary structure, historical characterization, research coverage, uncertainty and historical geography, with a map as one derived inspection view.

This makes **domain corpus + methodology + discriminating queries** more central and makes generic platform/UI expansion less defensible.

**Checkpoint:** external practice strengthens the case for a narrower identity and removes multiple possible future feature families from scope.


---

## Chunk 7 — Competing project identities

No identity receives sunk-cost preference.

### Identity A — Incumbent: integrated Historical Slavery Atlas platform

**Definition:** a full end-to-end research/database/release/API/web system whose primary public form is an interactive global time-aware atlas.

**Evidence for:**
- complete research → reviewed publication → public map path works;
- temporal/spatial/provenance problems genuinely benefit from integrated queries;
- selected-year geography and source lineage have strong correctness controls;
- map can expose geographic comparison in a way prose alone cannot.

**Evidence against:**
- actual user/research value of the full application has not been benchmarked;
- current preview is still legacy semantics and small;
- generic research database/time-map/publication capabilities overlap heavily with nodegoat and other DH platforms;
- 29 migrations / 12 workflows / deployment/monitoring/release machinery are substantial relative to demonstrated public use;
- the map has repeatedly exerted pressure toward false precision/ordinal rhetoric.

**Maintenance cost:** high.  
**Research potential:** high.  
**Uniqueness:** medium-low as a platform; potentially high only in domain semantics/corpus.  
**Falsifiability:** user-task comparison possible, but not yet performed.  
**Current standing:** plausible but not justified as the default identity.

### Identity B — Smaller: auditable evidence corpus + thin atlas

**Definition:** the project is primarily a curated, versioned global/deep-time evidence corpus and comparison methodology. A thin map/timeline/evidence inspector is one derived query surface, not a continuously operated product platform.

Core artifacts:

- domain methodology and vocabulary;
- claim/source/version provenance;
- difficult-case fixtures and negative controls;
- reviewed global research corpus;
- historical geography resolution rules and selected-year query logic;
- reproducible data releases;
- minimal static or low-operations atlas view/download/query tooling.

**Evidence for:**
- preserves nearly every strong M1/M2 contribution;
- directly reflects the charter's strongest surviving thesis;
- avoids competing with nodegoat as a generic workbench;
- makes the public map subordinate to evidence instead of allowing map rhetoric to drive ontology;
- can keep PostgreSQL/PostGIS as research tooling without requiring heavy public operations;
- easier to preserve/deposit as scholarly data.

**Evidence against:**
- may provide less immediate public “wow” than a fully dynamic application;
- must prove that a thin derived atlas still adds useful geographic reasoning rather than merely decorating a dataset.

**Maintenance cost:** medium-low.  
**Research potential:** high.  
**Uniqueness:** medium-high if the corpus/method genuinely covers global deep-time comparison.  
**Falsifiability:** strong; compare thin atlas/corpus tasks against baseline.  
**Current standing:** strongest fit to accumulated evidence.

### Identity C — Adjacent: Historical Slavery Evidence Method / benchmark corpus

**Definition:** the most valuable artifact is the methodology, adversarial fixture corpus, evaluation protocol and curated reference cases. The “atlas” becomes secondary or optional.

Potential outputs:

- claim/evidence modeling conventions;
- benchmark cases for false equivalence, false temporal/spatial precision, contradictory evidence and abstention;
- source/provenance/release protocol;
- reusable test/evaluation corpus for digital-history systems and AI-assisted historical synthesis.

**Evidence for:**
- adversarial/methodological work is the strongest demonstrated contribution;
- M1/M2 generated real semantic discoveries;
- low operational burden;
- can be published/deposited independently of a web product;
- value is highly inspectable and falsifiable.

**Evidence against:**
- risks abandoning the original global-atlas research ambition before testing whether the map/corpus combination adds value;
- methodology without sustained real research data may become sterile;
- existing standards/peer projects already cover parts of provenance and cultural-heritage modeling.

**Maintenance cost:** low.  
**Research potential:** medium-high, but shifts toward methods.  
**Uniqueness:** medium; strongest in the slavery/coercion-specific adversarial cases rather than generic provenance.  
**Falsifiability:** strong through new orthogonal historical cases.  
**Current standing:** credible fallback/adjacent identity, but not yet clearly superior to B.

### Identity D — Negative control: generic digital-history evidence platform

**Definition:** generalize the architecture beyond slavery/coercion into a reusable humanities research platform.

**Evidence for:** technical architecture could be generalized.

**Evidence against:**
- nodegoat already provides generic humanities data modeling, source links, spatial/temporal visualisation, API and publication;
- CIDOC CRM/Linked Art/PROV already supply broad semantic standards;
- no project evidence demonstrates a cross-domain need;
- this would turn implementation generality into a new product thesis.

**Maintenance cost:** very high.  
**Research potential:** broad but speculative.  
**Uniqueness:** low.  
**Falsifiability:** vague without a new project.  
**Current standing:** **REJECT**.

### Comparative result

| Criterion | A — full platform | B — corpus + thin atlas | C — method/benchmark | D — generic platform |
| --- | --- | --- | --- | --- |
| Fits strongest value evidence | medium | **high** | high | low |
| Beats external baseline | weak/unproven | **plausible, domain-specific** | plausible | poor |
| Maintenance burden | high | **medium-low** | low | very high |
| Preserves research ambition | high | **high** | medium | diffuse |
| Distinctiveness | integration-heavy | **domain corpus/method** | method cases | low |
| Falsifiability | medium | **high** | high | low |
| User/research need proven | no | not yet, testable cheaply | partial scholarly need | no |

### Plausible survivors

**B and C survive.**

A is not rejected as an eventual delivery form, but it loses default status: the project has not earned the right to maintain/expand a full application platform merely because one exists.

D is rejected.

### Experiment that distinguishes B from C (and can re-earn A)

Choose a small set of real, difficult cross-place/time historical questions.

Run them through:

1. strongest external/simple baseline (literature + structured notes/table + QGIS/nodegoat/general model as appropriate);
2. the domain corpus/method with no custom atlas interaction;
3. the **smallest thin atlas/query view** needed to expose place/time/evidence differences.

If the thin atlas repeatedly improves correct, inspectable cross-place/time reasoning, Identity B is justified and a richer A may later be earned.

If the corpus/method produces the same practical value without the map/product layer, Identity C should dominate.

**Checkpoint:** Identity B is the best current hypothesis; C remains a serious competitor. Full-platform A must re-earn its cost through user/research evidence rather than momentum.


### Bounded baseline challenge — Silla and Hittite

To avoid leaving the strongest-baseline comparison entirely hypothetical, this review ran two existing methodology-driving cases through ordinary targeted web/literature discovery.

#### Silla Village Register

A simple targeted search readily recovers:

- the National Institute of Korean History synthesis reporting 25 `nobi` among 462 persons in four villages;
- specialist date disagreement, including a 695 CE argument and a separate 818/819 reconstruction.

The difficult historical facts are therefore **not unique Atlas discoveries**.

What the Atlas adds is structured restraint:

- it records the date range as disagreement rather than 125 years of continuous truth;
- it keeps the four-village evidence target narrower than all Unified Silla;
- it preserves the conflicting date interpretations as qualifiers rather than choosing a false exact year;
- unresolved geometry remains legitimate.

#### Hittite central Anatolia

A simple specialist search readily recovers:

- the broader ancient-Near-East warning that slavery/dependency categories do not map cleanly onto one modern category;
- Hittite legal evidence for potentially chattel slaves;
- status flexibility in mixed-status marriage;
- frequent use of slaves as herdsmen.

Again, discovery of these facts does not require the Atlas.

What the Atlas adds is a persistent comparative representation in which:

- attestation pattern does not equal prevalence;
- institutional features may be supported while prevalence/structural significance remain unassessed;
- status/function/property/transmission facets coexist;
- normative law is evidence without becoming a mechanical prevalence claim.

#### Baseline result

**PARITY on bounded fact discovery.**

Ordinary targeted research + a strong general model can recover the core Silla/Hittite facts and major caveats quickly.

**Plausible Atlas advantage on durable comparison semantics.**

The project makes it harder to lose those caveats when the evidence is later queried across place/time, especially temporal truth, spatial generalization and orthogonal dimensions.

This benchmark therefore **weakens the case for a large discovery/application platform** while strengthening the case for a domain corpus/method with a thin comparative query surface.

It is still not a real external-user evaluation and must not be overstated.

