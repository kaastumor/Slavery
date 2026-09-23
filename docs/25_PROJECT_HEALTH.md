# Historical Slavery Atlas — Project Health

This file holds the **live assumptions register, standing material risks, value evidence and gate-health decisions**. It is not a second backlog.

## Initial foundation audit — 2026-09-22

Canonical repository inspected: `kaastumor/Slavery`, `main` at `f766ab9`.

### What already works

- end-to-end research → database → reviewed publication → API → MapLibre path;
- PostgreSQL/PostGIS schema/migrations through 0027 in the repository;
- immutable/reconstructible release machinery and static public fallback;
- cartographic build/QC/promotion separation;
- research-case idempotency;
- claim-level provenance and source/version separation;
- external participation kept separate from territorial practice;
- public API security boundary and availability monitoring;
- CI is green on current `main`.

### Audit findings and dispositions

| Finding | Disposition | Consequence |
| --- | --- | --- |
| Existing backlog/decision/QC structures are adequate | survives | Reuse them; no second PM system. |
| `docs/01_PROJECT_STATUS.md` and `docs/20_CURRENT_HANDOFF.md` can become stale and were directing work to completed #27 | revise | Make them state snapshots/pointers, not competing queues. |
| `SECURITY.md` says the repository is private while GitHub reports it public | revise | Correct the threat/privacy model immediately. |
| ~100 old topic branches remain | revise | Sanitation should flag branch hygiene; delete confirmed merged branches when tooling/admin path permits. |
| Current open execution queue is blocked/parked after completed P0/P1 work | revise | Start M1 methodology-hardening gate #100 rather than manufacture maintenance work. |
| Current P0–P4/coverage/time/space semantics face credible false-equivalence/false-precision attacks | experiment | M1 #100 with a short AUTO runway #101–#106. |
| Existing database/GIS stack is already justified by live requirements | survives | No architecture reset. |
| Generic tooling shopping was parked | survives | Issue #2 closed as not planned; reopen only for a concrete trigger. |
| Scheduled build-loop prompt encoded the old backlog model and was disabled | revise | Replace with repository-versioned runbook before re-enabling. |

## Assumptions register

| ID | Assumption | Status | Strongest pressure / discriminating evidence |
| --- | --- | --- | --- |
| A-001 | Global comparison can be useful without implying equivalence | not demonstrated at the H2 project-value threshold | H2 found one material corpus-method gain but not the required repeatable advantage across two cases. Preserve the comparison discipline; do not scale the Atlas on this assumption. |
| A-002 | P0–P4 can remain the target universal public summary | rejected | M1 shows the scale mixes evidentiary configuration with different historical structures. Preserve it only as legacy compatibility until a post-M1 interface exists. |
| A-003 | Cliopatria is the best open global deep-time fallback backbone | survives for raw infrastructure | Exact 13,765-feature ingestion and selected-year behavior survive M2. The resolver remains experimental Atlas truth; specialist overrides and reviewed source→atlas identity remain necessary. |
| A-004 | PostgreSQL/PostGIS is justified over files/spreadsheets for the working research/integrity system | survives with boundary | Time/spatial joins, provenance, release reconstruction and integrity are demonstrated. This does not prove that the public product needs an always-on database/API platform. |
| A-005 | MapLibre + current API/GeoJSON delivery is sufficient at current scale | survives / freeze | It is sufficient for the existing non-canonical demonstration. Do not expand serving/render infrastructure until the thin-atlas value hypothesis is demonstrated. |
| A-006 | The project can responsibly cover the present as well as antiquity | unproven / blocked for sensitive person-level expansion | Living-person/sensitive-data policy remains insufficient; do not let H2 modern expansion outrun this. |
| A-007 | A serial issue-driven autonomous worker can create value without roadmap drift | survives only as a bounded gate mechanism / idle | M1/M2/H2 produced useful corrections, but H2 triggered the stop rule. No autonomous execution runway is justified in preservation state. |
| A-008 | The full interactive Atlas platform is the best form for the demonstrated contribution | rejected for active expansion | H2 did not show a repeatable material advantage for the corpus/method over a strong baseline, and the thin view did not materially beat the corpus in any case. Preserve existing artifacts; do not expand the platform. |

## Standing risk register

| ID | Risk | State | Current control / next pressure |
| --- | --- | --- | --- |
| R-001 | False equivalence across unlike coercive systems | medium-high / controlled experimentally | Post-M1 dimensions and adversarial fixtures reduce the risk, but remain experimental for broad publication. No production migration or bulk expansion is authorized. |
| R-002 | False temporal/spatial precision from map UI | high / active | M2 prototypes solve key truth conditions, but the public preview remains legacy/non-canonical. The next question is whether a thin atlas adds value without reintroducing map rhetoric. |
| R-003 | Archive/research-density bias mistaken for prevalence | high / controlled | Global-balance strategy; coverage kept separate; no count-derived P-level. |
| R-004 | Governance/document drift | medium / controlled | Root backlog, gate issues, sanitation and health checks remained synchronized through M1; continue deleting stale state rather than adding parallel systems. |
| R-005 | Public-repository leakage of secrets/private/sensitive source material or derivatives | high / controlled | SECURITY classification, .gitignore, sanitation, synthetic/public-safe CI fixtures. |
| R-006 | Production/cloud dependence or outage erases public state | low-medium / controlled | Static release fallback and explicit release pointer preserve published preview state. Weekly liveness is enough; automatic cloud restart was retired. |
| R-007 | Automation creates activity rather than evidence | medium / controlled | M1/M2 produced discriminating evidence, but HC-003 intentionally leaves no execution runway. Disabled/idle automation is the correct state. |
| R-008 | Branch/workflow/experiment accumulation increases cognitive load | medium / active | DVC and self-heal workflows were retired and duplicate main web build removed; ~100 historical remote branches still need admin-capable pruning. |
| R-009 | Public preview is mistaken for canonical historical release | medium / controlled | explicit non-canonical release identity and immutable v0.6.1 baseline. |
| R-010 | No repository license creates ambiguity if outside contribution/reuse begins | low / parked | Decide only when external contribution/distribution needs make it material. |
| R-011 | Research/platform effort grows faster than demonstrated value over the strongest baseline | controlled by stop decision | H2 failed the pre-registered value threshold. D-063 stops active Atlas expansion; reopening requires new external evidence rather than more internal build-out. |

## Value evidence

Record meaningful outcomes, including no-value results.

| ID | Question / capability | Outcome | Baseline comparison | What changed |
| --- | --- | --- | --- | --- |
| V-001 | Can coarse historical geometry be rendered against a modern physical coastline without rewriting source geometry? | useful confirmation | Raw Cliopatria polygon/render was visibly worse | QGIS/Natural Earth render pipeline adopted; Achaemenid pilot visually accepted with bounded area change. |
| V-002 | Can an already-published preview survive live API/database failure? | useful confirmation | API-only serving would disappear during outage | Checksummed static fallback added and outage-tested. |
| V-003 | Do we currently need another major tooling/integration layer? | no value / reject-for-now | Existing stack already covers demonstrated needs | Tooling-shopping lane parked and issue #2 closed until a real trigger exists. |
| V-004 | Does the original P0–P4 / coverage / time model survive a serious cross-period attack? | contradiction / redesign | Better labels on the old model would not change query truth or simultaneous categories | M1 rejected P0–P4 as the target universal ordinal and split the overloaded semantics. |
| V-005 | Is complete Cliopatria ingestion worth pursuing instead of polity-by-polity geometry acquisition? | useful confirmation + blocker discovery | On-demand resolution hides corpus-wide failure modes | Exact v0.2.0 corpus profile found 13,765 features and explicit year-zero endpoints; whole-corpus integration proceeds, silent calendar normalization does not. |
| V-006 | Did the first M1 semantic redesign actually solve the adversarial findings? | contradiction then correction | Green component tests alone would have accepted an overloaded v1 prototype | Integrated gate found three displaced overloads; #112 corrected them and the re-attack survived. |
| V-007 | Does integrated adversarial review add value beyond ordinary green CI? | value | Component tests repeatedly missed semantic/integrity defects later found by M1/M2 integrated attacks | Preserve the adversarial fixture/re-attack method as a core project artifact. |
| V-008 | Does the Atlas uniquely discover the core facts in the Silla/Hittite benchmark cases? | parity | Targeted literature/search + strong general model recovered the core facts and major caveats quickly | Factual discovery is not the differentiator; durable comparison semantics may still be. |
| V-009 | Is a generic historical database/timeline/map/research platform a distinctive project contribution? | contradiction / remove scope | nodegoat and adjacent DH/cultural-heritage systems already provide generic modeling, sources, temporal/spatial views and publication | Do not generalize into a DH platform; narrow to slavery/coercion corpus + method. |
| V-010 | Does the non-canonical unused preview justify 15-minute monitoring and automatic cloud restart? | no value / retire | Static fallback preserves the demonstration and no user-critical availability need is evidenced | Retire self-heal and reduce liveness to weekly. |
| V-011 | Has the current full application/platform form earned its maintenance cost? | unproven / simplify | Strong correctness evidence exists, but no external user-task evidence shows the full product materially outperforms a simpler corpus/method + GIS/model workflow | Make corpus + thin atlas the working identity; full platform must re-earn expansion. |
| V-012 | Does the corpus/method, then a minimal thin view, materially outperform the strongest competent baseline on difficult historical reasoning? | **PARITY / threshold failure** | Three preregistered cases: B materially improved A only for the Mexica category case; repaired C did not materially improve B in any case under the fixed rule | Trigger D-062 kill rule: stop active Atlas expansion; preserve methodology/corpus/audit artifacts. |

## Health-check history

### HC-001 — Foundation operating-system check — 2026-09-22

Decision: **continue, with M1 as the next substantive gate**.

Rationale:
- the working product/release architecture demonstrates real capability and should not be reset;
- the largest current risk is semantic overclaiming at scale, not missing infrastructure;
- two production/release tasks remain genuinely blocked by sponsor/admin prerequisites and should not consume autonomous runs;
- the smallest useful next experiment is the methodology-hardening gate #100.

Next mandatory health check: #106 after the integrated M1 adversary #105.


## Foundation setup adversary — 2026-09-22

| Attack | Disposition | Result |
| --- | --- | --- |
| Governance can become the project instead of supporting it | survives with constraint | Only four operating documents plus the existing backlog/decision system; no board, sprint system or parallel roadmap. |
| New documents can create competing sources of truth | revise | Root BACKLOG is still the only execution queue; health file explicitly is not a backlog; stale handoff is reduced to a pointer. |
| AUTO issues can turn a speculative roadmap into busywork | revise | Only #101–#106 exist; #105/#106 are dependency-gated; no next-gate queue may be pre-generated. |
| Two autonomous workers can overlap | revise | Reuse the existing disabled Slavery Atlas Build Loop rather than create a second executor; availability monitoring is not an executor. |
| Green CI can create false confidence | survives with constraint | Runbook requires adversarial evidence and real atlas cases; gate success is not inferred from CI. |
| Synthetic fixtures can overfit the model | revise | #101–#103 require real existing atlas cases alongside synthetic fixtures. |
| Roadmap creates sunk-cost pressure | survives with constraint | Charter horizons are hypotheses; #106 must choose continue/redirect/stop. |
| Public repository can leak private/restricted material | revise | SECURITY now classifies source/derived data and CI is constrained to public-safe fixtures; sanitation checks common repository leaks. |
| Architecture inflation follows “serious project” setup | reject | No new service/database/framework introduced. Existing PostgreSQL/PostGIS/Supabase/MapLibre stack remains because it already serves demonstrated requirements. |
| Experiments can become zombies | survives with constraint | Way of Working adds experiment states and a two-health-check kill rule. |
| Old branches/workflows can accumulate | revise / park cleanup | Branch accumulation is recorded as R-008; do not create a new cleanup system, but prune confirmed merged branches when an available admin/tool path supports it. |
| Scheduled worker can execute stale instructions | revise | Stable scheduler prompt points to the versioned runbook and repository decisions override old AUTO issue text. |

Foundation conclusion: **survives after revision**. The project operating system is small enough to merge, and the next action is substantive M1 work rather than more setup.


### HC-002 — M1 methodology-hardening boundary — 2026-09-23

Decision: **CONTINUE, with H1/M2 as the next substantive gate.**

#### What M1 actually proved

- The pre-M1 P0–P4 model is not a defensible target universal ordinal for global deep-time comparison.
- A smaller additive model can keep attestation pattern, interpretive basis, occurrence, institutionalization, prevalence, structural significance, workflow state, epistemic outcome, assertion form and practice facets separable.
- Temporal applicability can be modeled separately from dating precision; evidence locus can be modeled separately from inference extent.
- Those distinctions survive synthetic fixtures and real Hittite, Baekje, Silla, Mauryan and Maya cases at prototype level.
- Complete Cliopatria profiling is practical and preferable to polity-by-polity source acquisition as the raw global baseline, while source-native calendar and RELATION semantics still require explicit resolution.
- The project operating system produced a real correction rather than just green CI: #105 returned REVISE, #112 repaired the model, and the gate was re-attacked before promotion.

#### What M1 did not prove

- The new semantics are not yet canonical methodology/schema.
- They are not yet represented in the live relational/query path.
- The current public preview still uses legacy P-level opacity and simple from/to selected-year filtering.
- Cliopatria year-zero, RELATION/composite and selected-year resolver behavior are not yet integrated.
- Real end-user value versus literature + notes + ordinary GIS/search remains only partially evidenced.
- Modern/living-person privacy handling remains insufficient for unrestricted present-day expansion.

#### Simpler-baseline check

**Continue.** A spreadsheet/static GIS could store many of the new fields, but it would not by itself solve the already-demonstrated needs for:
- exact release reconstruction;
- claim/source-version lineage;
- spatial/temporal joins and selected-year resolution;
- whole-corpus historical geometry with specialist overrides;
- reviewed/publication boundaries;
- reproducible public serving and rollback.

No new service, framework, queue, vector database or ontology platform was needed during M1. Complexity stayed below the failure threshold.

#### Stop / redirect test

**Do not stop.** M1 found correctable semantic defects rather than invalidating the central thesis.  
**Redirect:** yes, narrowly. Do **not** resume bulk historical research yet. The next uncertainty is integration, not source volume.

#### Next gate

**M2 / H1 — semantic integration + complete geography backbone (#116).**

Short runway:
- #117 canonicalize only the M1 semantics that survived;
- #118 resolve Cliopatria calendar + RELATION semantics;
- #119 ingest the complete pinned corpus into raw staging;
- #120 prototype post-M1 claim semantics in disposable PostGIS;
- #121 build the complete selected-year resolver;
- #122 integrated adversarial gate;
- #123 Project Health Check.

Blocked operational work #43 and #26 remains blocked and does not displace M2.

Next mandatory health check: #123 after #122.


### M2 progress delta — 2026-09-23

This is a state reconciliation, not a horizon health check.

- **#117 / D-058 complete:** the M1 v2 structure is now the canonical **target** methodology/data model. It is not yet the live relational implementation. P0–P4 and legacy coverage fields remain historical-release compatibility only.
- **#118 / D-059 complete:** pinned Cliopatria v0.2.0 source intervals are inclusive; atlas BCE selected-year lookup uses the documented source translation; source integer 0 stays preserved and receives no invented independent historical label; POLITY/RELATION/composite hierarchy is preserved and type-aware.
- **Next discriminating test:** #119 must prove that all 13,765 pinned Cliopatria features can be ingested reproducibly into raw/staging PostGIS without flattening hierarchy, rewriting source-native years, conflating source identity with atlas spatial identity, or exposing raw rows to publication.
- **No gate promotion:** bulk historical research remains paused until M2 #122 and #123.
- **Operational blockers unchanged:** #43 and #26 remain blocked and do not displace M2.

No new assumption is promoted by this note beyond D-058/D-059. The next mandatory Project Health Check remains #123.


## Project-system conformance delta — 2026-09-23

This is a **project-system reconciliation**, not the #123 horizon health decision.

The repository was checked against a lean long-lived-project standard emphasizing repository-first state, strongest-baseline comparison, canonical ownership, adversarial evidence, resumability, sanitation, workflow discipline and explicit health boundaries.

### Survives

- GitHub `main` is the implementation/methodology source of truth.
- Root `BACKLOG.md` is the single execution queue; issues/PRs hold durable task evidence.
- `23_PROJECT_CHARTER.md` already carries a real north star, simpler baseline, success/failure conditions and non-goals.
- This file remains the single owner of assumptions, material risks, value evidence and health decisions; separate duplicate ledgers are not justified.
- `24_WAY_OF_WORKING.md` already uses question → adversary → experiment → evidence → decision → reconciliation rather than feature throughput.
- M1/M2 demonstrate real revise/correct/re-attack behavior rather than ceremonial adversarial review.
- Canonical historical releases, database working state, previews and experiments remain distinct.
- Repository sanitation, release reconstruction, security boundaries and source-version provenance are already fail-closed in CI.
- Persistent workflows mostly have distinct responsibilities: foundation, research-case validation, release candidate validation, geometry build/review/promotion, web build/deploy, availability/recovery.

### Revised in this conformance pass

- root `README.md` no longer points at completed M1;
- `01_PROJECT_STATUS.md` now reflects the #123 stopping point instead of directing work to #120;
- `20_CURRENT_HANDOFF.md` no longer carries a mutable gate snapshot;
- `docs/README.md` is now an ownership/index document rather than a stale architecture-status narrative;
- `23_PROJECT_CHARTER.md` now separates **problem / contribution / project form / implementation architecture**, strengthens the boring baseline, and makes shrinkage/parity explicit kill pressure;
- `24_WAY_OF_WORKING.md` now makes canonical ownership, method maturity, discovery lanes, capability-bound acceptance, resumable chunks, competing identities, strongest-baseline comparison and shrinkage mandatory where relevant;
- stale `docs/project_manifest.yaml` was removed because it duplicated current state and had drifted materially (repository visibility, migration count, schema draft and milestone);
- the completed DVC evaluation remains as evidence but its dedicated persistent workflow was removed because no current adoption trigger exists.

### Explicitly not created

No new standalone assumptions register, value-evidence ledger, audit directory, roadmap, experiment platform or project-management database was added. Existing canonical owners already cover those responsibilities.

### Remaining project-system pressure

- The remote repository still contains a large number of old topic branches. This is already R-008; prune confirmed merged branches when an administrative/tooling path is available rather than inventing a new tracking system.
- `main` is currently reported unprotected. Treat branch protection as repository-administration hardening when available; do not weaken PR/CI discipline because protection is absent.
- Some historical numbered documents intentionally contain old phase/status language. They are historical evidence, not current-state owners. Do not churn them merely for cosmetic freshness.
- The decisive unanswered questions are now project-value questions, not project-system setup questions. They belong to #123: baseline parity, competing identities, artifact shrinkage, demonstrated value, and continue/simplify/redirect/stop.

No new development horizon is authorized by this reconciliation.


### HC-003 — M2 wide-angle project review — 2026-09-23

Decision: **CONTINUE + SIMPLIFY.**

Durable review: `docs/34_WIDE_ANGLE_PROJECT_REVIEW.md`.

#### What survives

- the global/deep-time evidence problem;
- claim-specific source/provenance discipline;
- uncertainty, disagreement and abstention;
- post-M1 structural separations at experimental maturity;
- raw Cliopatria global geography infrastructure;
- PostgreSQL/PostGIS as research/integrity tooling;
- exact release reconstruction;
- adversarial fixtures and revise/correct/re-attack discipline;
- a thin map/query surface as a hypothesis worth testing.

#### What does not survive as the default direction

- the full interactive application platform as the presumed project identity;
- generic digital-humanities platform expansion;
- broad H2 research expansion merely because M2 passed;
- M2 production migration as the next task;
- production-like preview operations;
- new P0–P4 assignment in current research.

#### Baseline result

A bounded Silla/Hittite challenge reached **parity on core fact discovery** with targeted literature/search + a strong general model. The Atlas's remaining plausible advantage is durable comparative semantics: preserving temporal/spatial truth, provenance, orthogonal historical dimensions and abstention when evidence is later queried across place/time.

External precedent review also shows that nodegoat and adjacent projects already cover generic DH platform functions.

#### Working identity

Preferred: **auditable evidence corpus + thin atlas**.

Fallback if the thin atlas adds no material value: **methodology / adversarial benchmark corpus**.

The full platform may only be re-earned through evidence.

#### Repairs authorized and completed in the review branch

- active research workflow/lifecycle aligned with post-M1 legacy-only P0–P4 rule;
- automatic Supabase self-heal retired;
- preview monitor reduced to weekly;
- production geometry promotion made explicit/manual;
- duplicate main web build removed;
- sanitation strengthened for key containers, machine-local paths and >5 MB tracked files.

#### Remaining bounded debt

- real npm lockfile must be generated/committed in a networked environment before substantive frontend expansion;
- remote historical branches should be pruned when admin-capable tooling is available;
- main currently reports unprotected; branch/environment protection remains an administrative hardening boundary.

#### Candidate next experiment — NOT AUTHORIZED BY THIS REVIEW

A three-question value-discrimination pilot comparing:

1. strongest boring/external workflow;
2. corpus/method without custom map interaction;
3. smallest thin atlas/query view.

The project remains execution-idle until that pilot is explicitly authorized.

#### Kill rule

A richer Atlas product earns no further application/infrastructure horizon unless at least two independent tasks from different historical contexts show a repeatable practical advantage over the strongest baseline in inspectable cross-place/time reasoning, provenance recovery or uncertainty preservation without increased overclaim.

If the corpus/method adds the value but the thin atlas does not, collapse to the methodology/corpus identity and stop application expansion.

If neither adds material value, stop further Atlas expansion and preserve the methodology/corpus/audit artifacts as the final project result.


### HC-004 — H2 value-discrimination boundary — 2026-09-23

Decision: **STOP ACTIVE ATLAS EXPANSION; PRESERVE METHOD/CORPUS/AUDIT ARTIFACTS.**

Durable experiment: `experiments/h2-value-discrimination/` / issue #146.  
Direction decision: D-063.

#### What H2 tested

Three frozen evidence packets were evaluated through:
1. a deliberately strong conventional baseline;
2. the Atlas post-M1 corpus/method representation;
3. the smallest dependency-free thin query/visual artifact.

The setup adversary returned **REVISE** before research and replaced the original Andes case with a map-hostile Mexica category negative control. The result adversary later found and repaired an unfair provenance loss in the thin view before final evaluation.

#### Result

- Mexica: corpus/method materially improved claim-specific provenance/scope recovery; thin view did not add material value.
- India 1843: the conventional baseline already preserved law/practice/jurisdiction boundaries; thin interaction made the legal/practice discontinuity more salient but did not meet the materiality threshold.
- Genoese Black Sea: the conventional proposition/evidence/scope table already prevented network→territorial-prevalence inference; thin interaction made the 1475 Caffa boundary more salient but did not meet the materiality threshold.

Project-level requirement was a repeatable material advantage in at least two independent cases.

**Corpus/method over baseline: 1/3 material cases — FAIL.**  
**Thin view over corpus/method: 0/3 material cases — FAIL.**

#### Interpretation

The methodology is worth preserving. The bespoke Atlas expansion thesis is not supported strongly enough to justify further active development.

This is not a universal claim that maps, relational claims, PostGIS or structured provenance have no value. It is a decision that **this project has not earned another expansion horizon** against its own strongest-baseline rule.

#### State after HC-004

- v0.6.1 remains canonical and immutable;
- current preview remains frozen/non-canonical;
- H2 evidence remains experimental/non-canonical;
- M2 production migration stays parked;
- bulk research and product/platform growth stay parked;
- no H3/H4 or AUTO runway exists;
- repository moves to **IDLE / preservation**.

A future development horizon requires new external evidence or a concrete simpler-baseline failure; internal desire to continue building is not a trigger.
