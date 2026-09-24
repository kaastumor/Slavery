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
| A-009 | A systematically assembled global historical coverage corpus may have value distinct from Atlas representation/UI | survives narrowly / scale economics unresolved | COV-001 found robust material value on 4/6 cross-cell tasks after adversarial downgrade, while specialist narrative and SlaveVoyages remained superior in their domains. The value lives in a flat coverage corpus, not Atlas infrastructure. |
| A-010 | The value of the flat coverage corpus compounds faster than review/update burden as it scales | current row-by-row workflow not demonstrated; broader systematic-coverage economics remain open | COV-002 found persistent reuse and strong static compression, but its maintenance gate does not discriminate the economics of tiered/versioned/batch-curated coverage. ADV-001 limits the stop to the tested workflow. |
| A-011 | Tiering breadth, compact evidence and selective depth can make systematic coverage methodologically viable without default deep research for every target | survives with stronger QC | COV-004: escalation replay passed at 1/6 false negatives only after adding source-quality failure as a C2/review trigger; non-polity challenge and real update mechanics also survived. |
| A-012 | A bespoke Atlas evidence inspector adds material value beyond a competent conventional map + tiered register | rejected at current scale | COV-004 Arm D: 0/4 material gains with identical frozen evidence/geometry; no misleading Atlas inferences. Ordinary map/register presentation remains valid. |
| A-013 | A real bounded release programme can harden the surviving method better than further miniature architecture experiments | survives subject-research phase / release QC next | 19 C1 rows completed with 19/19 replay and 4 C2 packets; closure tranche changed legacy Pandya positive to inconclusive and legacy Chimú inconclusive to a narrower corvée positive. Frozen polity balance reaches A2/B1/C3/D2/E1/F3 without quota-fill. | Stop subject expansion. Test the assembled candidate package at release level; preserve remaining queue as research-state, not absence. |

## Standing risk register

| ID | Risk | State | Current control / next pressure |
| --- | --- | --- | --- |
| R-001 | False equivalence across unlike coercive systems | medium-high / controlled experimentally | Post-M1 dimensions and adversarial fixtures reduce the risk, but remain experimental for broad publication. No production migration or bulk expansion is authorized. |
| R-002 | False temporal/spatial precision from map UI | high / controlled experimentally | COV-004 non-polity map test preserved points/routes/fuzzy/unresolved framing without false territorialization. Bespoke map semantics failed the value gate; ordinary map/register remains the safer default. |
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
| V-013 | Does preassembled global coverage itself create value beyond narrative handbooks + ordinary research/matrices? | **NARROW VALUE / survives** | COV-001: 4/6 fixed cross-cell tasks retained material value after result adversary; basic overview reached matrix parity; terminology advantage was downgraded; specialist narrative and SlaveVoyages won the negative controls. | Preserve the flat coverage-corpus thesis; do not reopen Atlas product expansion. Next uncertainty is reuse/maintenance economics at larger scale. |
| V-014 | Does corpus reuse value grow faster than research/review/update burden, and can a compact register preserve the gain? | **MIXED / STOP TESTED WORKFLOW** | COV-002: reuse survives at N=37 and compact R is ~60.5% of F's static review surface, but the maintenance gate failed under its frozen metric. ADV-001 shows that failure cannot be generalized to all systematic-coverage architectures. | Preserve compact register pattern; no automatic scaling. |
| V-015 | Does COV-002 justify rejecting systematic comprehensive coverage as a project direction? | **NO — inference overreach** | ADV-001/#153: scope mismatch, non-discriminating 4/6 update gate after three neutral shocks, atom-granularity sensitivity, unmeasured batch/versioned economics and demand-bias risk. | Keep project idle unless a new explicit hypothesis is authorized. |
| V-016 | Can a C0/C1/C2 tiered, batch-curated, versioned architecture improve the systematic-coverage case? | **TIERED VALUE / survives narrowly** | COV-003: C0 and C1 survive with review controls; C2 materially improved 2/3 escalations; systematic selection retained difficult/non-direct-handbook targets. Strong batch-economy gate failed because 12/12 C1 targets required follow-up. | Preserve tiered architecture; do not infer cheap comprehensive ingestion. |
| V-017 | Does the tiered method survive direct falsification, non-polity targets, real later scholarship, and a renewed Atlas comparison? | **METHOD SURVIVE** | COV-004: A passed narrowly (1/6 FN), B passed, C passed with 3/6 real updates, bespoke Atlas D failed 0/4 versus strong ordinary map/register. | Move only to preservation or an explicitly authorized lean research/release programme; no more architecture experiments by default. |
| V-018 | Can R1 freeze a balanced, non-evidence-selected real release frame without turning programme ceilings into quotas or hiding source-frame gaps? | **PASS / frame frozen** | 65 new C0, 24 new C1, 12 legacy C1 re-review; sector-B new-polity gap preserved rather than substituted; full planned C1 still covers all six neutral sectors. | Proceed to C0/identity QA; do not treat frame membership as historical evidence. |
| V-019 | Can neutral target QA prevent wasted/misattached subject research in the first real programme? | **PASS / 2 holds + 16 frame limitations** | R1.3 reviewed all 36 planned C1 targets before slavery research; French Louisiana 1800 and Duchy of Bavaria 1800 are held with no substitution. | Proceed with only the frozen 34-row queue; retain limitations as release metadata. |

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


### HC-005 — COV-001 coverage-value boundary — 2026-09-23

Decision: **NARROW SURVIVE — COVERAGE CORPUS THESIS SURVIVES; ATLAS PRODUCT EXPANSION REMAINS STOPPED.**

Durable experiment: `experiments/coverage-value/` / issue #148.  
Direction decision: D-065.

#### Sample and research

- exact deterministic Cliopatria sampling frame frozen before slavery/coercion research;
- 21/24 polity-year strata valid;
- 3 sampling gaps preserved;
- 4 preregistered non-polity challenge contexts added;
- 25 research rows frozen as plain JSON/CSV/Markdown;
- outcomes: 8 bounded-supported, 2 materially disputed, 15 researched-inconclusive;
- no inconclusive/gap state treated as historical absence.

The sample also exposed a source-frame failure: the selected `1300:C` Mahdids row conflicts with its supplied Wikidata identity/date. It remains unresolved rather than silently substituted.

#### Fixed-query result

Preliminary: 5/6 material tasks.

Result adversary downgraded the terminology/category task because a competent ordinary spreadsheet could reproduce most of that gain with one added column.

Robust final:
- Q1 basic overview — parity;
- Q2 law vs practice — material;
- Q3 network vs territorial inference — material;
- Q4 terminology/category — marginal/not counted;
- Q5 global-handbook coverage — material, bounded;
- Q6 unresolved/gap map — material.

**4/6 robust material tasks — PASS** against the preregistered >=3/6 rule.

#### Negative controls

- deep Champa why/how question: specialist narrative > index;
- Jamaica 1750–1800 voyage/traffic capability: SlaveVoyages > index.

Both controls pass and constrain the contribution.

#### Interpretation

The evidence supports a smaller identity than the Atlas:

> a curated, auditable, explicitly incomplete global coverage corpus recording what can be said, what cannot, why, and from which sources.

No evidence from COV-001 supports Postgres/API/MapLibre/frontend expansion.

The project remains **IDLE / preservation** after COV-001. A future bounded scale test is a candidate only, not authorized.

#### Next unresolved value question

Does corpus reuse/value grow faster than research, review and update burden at materially larger scale?

Any future experiment must test that directly rather than maximizing record count.


### HC-006 — COV-002 scale/reuse boundary — 2026-09-23

Decision: **STOP FURTHER AUTOMATIC SCALING; PRESERVE COMPACT COVERAGE-REGISTER PATTERN.**

Durable experiment: `experiments/coverage-scale/` / issue #151.  
Direction decision: D-067.

#### Expansion

- 12 deterministic rank-2 polity-year targets frozen before slavery/coercion research;
- combined corpus size increased from 25 to 37 researched rows;
- expansion outcomes: 4 bounded-supported, 8 researched-inconclusive;
- three expansion targets failed at identity/time validation before slavery classification:
  - New Netherland at 1800;
  - medieval Kingdom of Georgia at 1800;
  - Western Regions protectorate at 500 CE.

No successor polity was silently substituted.

#### Reuse result

At N=37:
- T1 law/practice — F/R materially better than M;
- T2 network/territorial inference — F/R materially better than M;
- T3 global-handbook coverage — F/R materially better than M;
- T4 unresolved research — parity with stronger M;
- T5 overview — parity;
- T6 decisive source recovery — practical parity; F retains richer source-role metadata.

R matched F on all six fixed tasks.

The 3/4 cross-cell scaling threshold therefore passed.

#### Static review-surface result

At N=37:
- F total review atoms: 547;
- R total: 331;
- R/F: 60.5%;
- F median: 15;
- R median: 9;
- median R/F: 60.0%.

Static <=70% compactness threshold passed.

The 12-row information-loss audit found no safety-critical omitted field under the fixed tasks.

#### Maintenance result

Six deterministic update rows were frozen before search.

- 3 searches produced genuine new/contextual specialist evidence;
- 3 produced no acceptable new source;
- every material update touched 2 F atoms and 2 R atoms;
- 0/0 no-change rows were treated as neutral.

Required: R <=70% of F update surface in >=4/6 rows.

Observed: **0 qualifying material rows — FAIL.**

No widespread stale/contradictory outputs appeared, but lower evidence-maintenance cost was not demonstrated.

#### Negative controls

- specialist Alodia source interpretation > F/R/M;
- SlaveVoyages > F/R/M for voyage-level quantitative research;
- ordinary matrix M remained competitive for single-cell New Guinea Highlands reading.

All controls pass.

#### Interpretation

The project has learned enough to stop generating its own growth justification.

A compact coverage register is useful for real comparative work, but systematic global expansion has not earned its maintenance burden.

The project returns to **IDLE / preservation**.

Future expansion requires a concrete external use case, consumer or research question that pays for the curation burden. “Completeness” alone is not sufficient.


### HC-007 — Completeness-inference correction — 2026-09-23

Decision: **NARROW THE COV-002 STOP — DO NOT TREAT IT AS A REJECTION OF SYSTEMATIC COVERAGE IN GENERAL.**

Durable audit: `experiments/coverage-scale/14_COMPLETENESS_INFERENCE_ADVERSARY.md` / issue #153.  
Direction correction: D-068.

#### What the audit attacked

The post-COV-002 statement:

> “Systematically researching all known history purely in pursuit of completeness is not justified by the evidence we have.”

#### Result

That formulation overstates what COV-002 tested.

COV-002 legitimately supports:
- no automatic continuation of its row-by-row expansion workflow;
- no default global F-style detailed row;
- preservation of the compact register pattern.

It does not establish that:
- tiered global target/research coverage is uneconomic;
- versioned/as-of reference releases are uneconomic;
- batch/source-centric research cannot reduce marginal cost;
- comprehensive coverage has no option/reference/bias-correction value.

#### Maintenance-gate problem

The preregistered maintenance requirement was R <=70% of F update surface in >=4/6 shocks.

Three shocks yielded no acceptable new source and were later treated as neutral 0/0 rather than savings wins.

Under that interpretation, at most three rows could qualify, so the 4/6 gate became impossible to pass.

Further, each rich F source object and each bare R source link counted as one source/citation atom, making the observed 2-vs-2 updates sensitive to atom granularity.

This does not prove R has favorable long-run maintenance economics. It does mean the maintenance FAIL cannot settle the broader completeness thesis.

#### Bias correction

Requiring an external consumer/funded use case as the only future trigger is not methodologically neutral. It can favor already-visible, well-funded, well-digitized histories and recreate a demand-density analogue of the archive-density bias the project seeks to resist.

#### Corrected state

Project remains **IDLE / preservation**.

No new corpus-growth experiment is authorized.

A future evaluation may be triggered by:
- a concrete external user/consumer/research task; or
- an explicitly authorized methodological hypothesis such as bias-resistant systematic coverage.

Any such evaluation must use a new cost/value model rather than repeat COV-002.


### HC-008 — COV-003 tiered-coverage boundary — 2026-09-23

Decision: **TIERED SURVIVE — PRESERVE C0/C1/SELECTIVE-C2 ARCHITECTURE; DO NOT AUTHORIZE COMPREHENSIVE INGESTION.**

Durable experiment: `experiments/coverage-tiered/` / issue #155.  
Direction decision: D-070.

#### C0

24 deterministic targets were registered before subject research.

Only 12 were assigned C1 research.

Every C0-only target explicitly remains:
> Registered target; historical slavery/coercion research not yet performed.

Six preregistered identity/time probes:
- four valid at anchor;
- Later Zhou at -500 — mismatch;
- Xu at -500 — ambiguous.

C0 therefore demonstrates research-state coverage and pre-research target QA without creating a slavery inference.

#### C1

12 researched rows:
- 4 bounded-supported;
- 8 researched-inconclusive.

The compact tier preserves:
- bounded proposition and abstention;
- law/practice distinction;
- network/territorial warning;
- handbook coverage;
- unresolved reason;
- recoverable source references.

Source reuse:
- row-centric COV-002 baseline: 1.00;
- COV-003 C1: 2.20;
- two of three batches reused shared specialist sources across all four C1 targets.

But 12/12 C1 targets still required target-specific follow-up.

Therefore the strong batch-economy gate fails.

#### C2

Three frozen escalations:
- Zhu — material correctness/temporal/category gain;
- Hanthawaddy — material legal-status/law-practice gain;
- Pañcāla — no material gain.

2/3 threshold passes.

Selective deep evidence is justified; deep evidence by default is not.

#### Versioning and source dependencies

The three deterministic post-freeze source searches found no genuinely new accepted source, so positive update economics remain untested.

C2 nevertheless created a real quality event: the early-China shared packet requires review, affecting four dependent C1 rows.

The experiment therefore adds a required control:

> shared source packets must maintain explicit source-to-row dependencies and propagate next-release review state to their dependents.

Frozen releases remain immutable.

#### Coverage / bias

None of the 12 C1 targets had direct Cambridge or Palgrave coverage, yet four yielded bounded-supported results and eight yielded meaningful researched abstentions.

A direct-handbook easy-evidence rule would omit every C1 target.

This supports systematic selection as a bias-resistance function, not as proof that every target deserves equal research depth.

#### Adversarial corrections

- the 2.20 reuse factor is source/context reuse, not a 2.20x historian-effort saving;
- the heterogeneous 1300:E batch shows longitude sector is not a good universal batching unit;
- one Chandela event citation is below production-grade specialist-source expectations and remains a next-release review item;
- identity triage used some general reference sources and is not publication-grade identity evidence;
- the polity frame still does not solve non-polity human-history coverage.

#### Boundary

**STRONG SURVIVE rejected. TIERED SURVIVE accepted.**

No comprehensive-ingestion, successor experiment, production migration or Atlas product horizon follows automatically.

Future validation, if explicitly authorized, should test non-polity frames, historiographically coherent batching, independent/multi-reviewer evaluation, a real positive post-release evidence update and stronger source-quality gates.


### HC-009 — COV-004 falsification boundary — 2026-09-23

Decision: **METHOD SURVIVE; RETAIN BORING MAP/REGISTER ATLAS; DO NOT REOPEN BESPOKE ATLAS PLATFORM.**

Durable experiment: `experiments/falsification-atlas/` / issue #157.  
Direction decision: D-072.

#### Arm A — escalation
- 1/6 material false negatives among previously non-escalated C1 rows;
- 2/3 prior C2 escalations remain materially useful;
- pass at boundary.

Mandatory repair:
**source-quality failure is an explicit C2/review trigger.**

Independent/multi-reviewer calibration remains required before broad public C1 publication.

#### Arm B — non-polity
- 12/12 registered without false territorialization;
- 8/8 researched C1 rows represented without polity pretense;
- sites, institutions, mobile networks and fuzzy community/region frames all fit experimentally;
- 0 silent geometry proxies.

This is representability evidence, not a canonical non-polity ontology.

#### Arm C — time-split updates
Six 2015-as-of rows were frozen before later-literature reveal.

Three genuine 2016–2026 evidence events:
- Sabaeans — material strengthening/qualification;
- Champa — corroboration/qualification;
- Cao — contextual corroboration.

Gate passed.

Versioned release/review mechanics therefore survive a real update test. Maintenance labour economics remain unmeasured.

#### Arm D — Atlas
Strong conventional map/register baseline versus bespoke semantic Atlas:
- D1–D4 material bespoke gains: 0/4;
- D5 parity;
- no new misleading Atlas inference.

Bespoke Atlas re-entry fails.

But baseline B is already a legitimate thin atlas:
- world map;
- points/routes/fuzzy frames;
- C0 research coverage;
- evidence register;
- citations.

Therefore the project does not abandon maps. It abandons the assumption that custom Atlas interaction is itself the contribution.

#### Boundary

The architecture-falsification sequence is complete.

The next decision is not another experiment by default.

Choose:
- preservation; or
- explicitly authorize a real lean systematic coverage programme with releases/QC using C0/C1/selective-C2 and ordinary map/GIS presentation.

No comprehensive ingestion or production platform follows automatically.


### HC-010 — R1.4 tranche 01 calibration checkpoint — 2026-09-24

Decision: **CORE SURVIVES AFTER MATERIAL CORRECTION; RETAIN REVIEW FLOOR; PAUSE BEFORE TRANCHE 02.**

Durable tranche:
- `programmes/r1/c1_tranche_01_final.json`
- `programmes/r1/12_C1_TRANCHE_01_ADVERSARIAL_REPLAY.md`
- issue #163.

#### Why this is useful evidence

This is the first use of Core Contract v1 on a real frozen research queue rather than an architecture experiment.

The initial synthesis was already cautious, yet 100% replay still found four material correctness risks:
- temporal leakage at Teotihuacan;
- context-to-target inference at Shaolin;
- external/captive relation leakage plus temporal projection for Inuit;
- temporal/status overreach at Cahokia.

The corrections changed release-safe semantics, not merely wording.

#### C2

Two of ten rows earned C2:
- Portuguese Colonies — resolved by refusing one territorial-practice state for the dispersed aggregate;
- Cahokia — resolved by changing preliminary `disputed` slave status to `inconclusive` and refusing selected-year 1200 continuity.

Both deeper packets materially affected the safe release result.

#### What cannot be inferred

The tranche intentionally over-sampled difficult/frame-limited cases.

Therefore:
- 3/10 classified is not prevalence;
- 7/10 inconclusive is not evidence of absence;
- 4 material corrections do not estimate the error rate of the remaining queue;
- the tranche does not estimate long-run historian labour.

#### Control decision

Do not weaken:
- selected-year applicability review;
- evidence-locus/inference-extent review;
- claim-specific source fitness;
- dimension separation;
- selective C2;
- minimum 50% C1 adversarial replay.

No new schema or ontology is justified by this tranche.

#### Boundary

#163 ends at tranche 01.

The next tranche is not automatically authorized. R1/#159 remains active, but continuation should deliberately choose a more ordinary operational tranche if it proceeds, so the project next tests repeatability/cost rather than stacking another stress sample.


### HC-011 — R1.5 tranche 02 operational checkpoint — 2026-09-24

Decision: **ORDINARY TRANCHE SURVIVES; 100% REPLAY REMAINS ACTIVE; ENTER MIDPOINT STOP REVIEW.**

Durable tranche:
- `programmes/r1/c1_tranche_02_final.json`;
- `programmes/r1/15_C1_TRANCHE_02_ADVERSARIAL_REPLAY.md`;
- issue #166.

#### Why this is useful evidence

Tranche 02 deliberately preferred ordinary `validated` frames rather than another stress-heavy cohort.

Six frozen rows were researched and all six were adversarially replayed:
- Kingdom of Kush 500 BCE;
- Cai 500 BCE;
- Lazica 500 CE;
- Nālandā 700 CE;
- Mali 1300 CE;
- United States 1800 CE.

Final outcomes:
- 1 classified/bounded-supported;
- 5 inconclusive for the exact frozen target/year/frame question;
- 1 C2 packet completed;
- 0 target substitutions.

#### Replay result

Unlike tranche 01, no row required a post-synthesis semantic release correction.

Replay still found two provenance/dependency issues worth correcting:
- Lazica — Procopius and modern discussion of Procopius cannot be counted as independent sixth-century attestations;
- Nālandā — modern target discussions materially reuse the same Yijing-centered seventh-century evidentiary base for this question.

The tranche therefore supports operational repeatability without showing that replay has become redundant.

#### C2

Mali 1300 earned C2 because Sākūra's status combines Arabic `mawlā`, later Mande servile terminology, reconstructed chronology and overlapping source traditions.

C2 resolves to inconclusive:
- preserve a possible servile/client origin as a historical status question;
- do not publish an unqualified “former slave” fact;
- do not infer a Mali-wide territorial-practice state;
- do not project better-attested later-fourteenth-century slavery backward to 1300.

#### Review setting

Core Contract v1 §19 is applied at 100% C1 replay for remaining R1 candidate work because tranche 01 exceeded the contract's 10% material-error trigger.

This is not a new ontology or source rule.

#### What cannot be inferred

- 1/6 classified is not prevalence;
- 5/6 inconclusive is not absence;
- 0 semantic corrections in six ordinary rows does not establish a general error rate;
- source-recovery burden and language/access limits still vary sharply by historical context.

#### Boundary

Combined R1 subject research now covers 16 C1 rows across two bounded tranches.

R1 therefore enters its mandatory midpoint stop review before any tranche 03. The review must decide whether to stop smaller, continue one bounded tranche, or change course. No new schema, ontology, platform feature or production migration is justified by tranche 02.


### HC-012 — R1 mandatory midpoint stop review — 2026-09-24

Decision: **CONTINUE ONCE — THREE-ROW BALANCE CLOSURE; THEN RELEASE QC.**

Durable review: programmes/r1/16_MIDPOINT_STOP_REVIEW.md / issue #168.

#### Evidence at midpoint

Sixteen C1 rows have been researched under Core Contract v1:
- 4 classified/bounded-supported;
- 12 inconclusive;
- 3 C2 packets completed;
- 16/16 internally adversarially replayed.

Tranche 01 required four semantic corrections. Tranche 02 required none after fresh synthesis but still required two dependency/provenance normalizations.

Language/access confidence across the 16 rows ranges from high to limited. Gaps are material in several contexts but do not dominate the entire release. Source/version recovery is functioning and dependency grouping is repeatedly useful.

#### Balance pressure

Current researched polity-sector counts are A2/C3/D2/F2; B and E are absent.

Adding only B and E produces 11 polity rows with C=3/11 (27.3%), failing the <=25% balance rule.

The deterministic minimum closure from the frozen queue is:
- Tamna (F);
- Pandya Empire (E);
- Chimu Empire (B).

Projected counts: A2/B1/C3/D2/E1/F3 = 12 polity rows, maximum 25%.

#### Burden/value judgment

One three-row closure is proportionate because it buys a concrete declared-frame property. Continuing toward the 36-row ceiling is not justified by row count, completeness desire or current evidence.

The repeated cross-history value remains methodological/release structural: selected-year applicability, bounded inference, dimension separation, source fitness/dependency and explicit abstention.

No feature-friction threshold has been crossed; no bespoke Atlas/platform work is authorized.

#### Boundary

Authorize one closing C1 tranche of Tamna, Pandya and Chimu only. Freeze membership before subject research, prohibit substitution and replay 100%. Afterward, proceed to R1.6 release QC unless a new hold/rework condition emerges.


### HC-013 — R1 closing C1 tranche and subject-research stop — 2026-09-24

Decision: **CLOSURE PASSES; STOP SUBJECT EXPANSION; ENTER RELEASE QC.**

Durable tranche:
- `programmes/r1/c1_tranche_03_final.json`;
- `programmes/r1/19_C1_TRANCHE_03_ADVERSARIAL_REPLAY.md`;
- issue #170.

#### Final closure result

Three midpoint-authorized rows were researched and replayed:

- **Tamna 500 CE** — inconclusive;
- **Pandya Empire 1300 CE** — inconclusive after C2;
- **Chimú Empire 1300 CE** — bounded-supported for state labor service/corvée.

No target was substituted.

No post-synthesis semantic correction was required, though source fitness/search-provenance handling was tightened during replay.

#### Legacy reversal test

The two legacy promotions move in opposite directions:
- Pandya: legacy bounded-supported → Core-v1 inconclusive;
- Chimú: legacy researched-inconclusive → Core-v1 bounded-supported corvée/labor service.

This is evidence that fresh rereview is not mechanically conservative or permissive. The claim shape changes when source-to-target fit changes.

#### R1 subject-research totals

Across three tranches:
- 19 researched C1;
- 5 classified;
- 14 inconclusive;
- 0 final disputed;
- 4 C2 packets completed;
- 19/19 internally adversarially replayed.

These counts are not prevalence.

Researched polity-sector counts:
A2 / B1 / C3 / D2 / E1 / F3.

With 12 researched polity rows, the maximum sector share is 25%. The midpoint balance gap is closed.

#### Research-stop judgment

D-078 was satisfied by exactly three rows. No evidence justifies continuing toward the 36-row ceiling.

The remaining frozen queue is valuable as research-state coverage and unresolved/planned scope. It must not be silently converted into absence or dropped from the release package.

#### Next boundary

Proceed to R1.6 release-level QC:
- cross-row Core-v1 validation;
- source/version and dependency audit;
- selected-year/target/dimension guard audit;
- C2 closure audit;
- geometry/release-surface checks;
- manifest/changelog/QC/unresolved-issues assembly;
- candidate research release only.

No subject-research tranche follows automatically. No new software feature has met the friction threshold.


### HC-014 — R1.6 release-level QC — 2026-09-24

Decision: **PASS WITH EXPLICIT LIMITATIONS; CRYSTALLIZE TO MVP.**

R1.6 audits the complete 19-row subject-research package at release level and finds no blocking internal-contract failure.

The surviving core is smaller than the historical project:
- immutable reviewed evidence rows;
- explicit unresearched/held research state;
- source-version/dependency reconstruction;
- temporal/inference guards;
- a neutral geographic navigation surface.

That core is now strong enough to justify a small technical MVP, but not a return to broad platform building.

#### What survives

- C0/C1/selective-C2 release semantics;
- bounded proposition + abstention;
- selected-year/period/near-anchor distinction;
- target/context and network/territorial separation;
- source quality + source-family dependency;
- immutable candidate inputs;
- research coverage as a visible non-historical layer;
- ordinary map/register as the Atlas form.

#### What remains unresolved

- concrete geometry materialization;
- independent historical review;
- uneven language/access coverage;
- public-surface implementation;
- final R1.8 publication/canonical decision.

#### MVP consequence

R1.7 should implement only the smallest read-only Atlas that makes this core inspectable.

Feature discovery resumes **after** that MVP exists. New feature candidates must begin as baseline comparisons with kill rules; discovery evidence does not authorize implementation.

No production migration or new service architecture is justified.


### HC-015 — MVP crystallization and delivery/discovery split — 2026-09-24

Decision: **DELIVER THE SMALL CORE; KEEP FEATURE CURIOSITY IN DISCOVERY.**

D-080 gives the project a bounded product form after R1.6:

> immutable R1 candidate package + neutral world map + explicit geometry/research states + compact evidence register.

The delivery plan deliberately reuses the existing Vite/TypeScript/MapLibre frontend and adds no new backend/service by default.

Operational controls:
- WIP=1;
- fixed serial MVP queue #175–#182;
- explicit dependencies;
- Definition of Ready / Definition of Done;
- short-lived PRs and green CI;
- technical MVP gate before discovery;
- discovery #184–#187 produces evidence/dispositions only.

This setup is not new feature-value evidence. It is project-control evidence intended to stop the small core from regrowing into the discarded platform.

Kill/shrink rule:
if the MVP requires backend/platform expansion, invented geometry precision or loss of the R1 evidence contract, shrink/hold rather than rebuilding the old architecture.


### HC-016 — Technical MVP gate — 2026-09-24

Decision: **TECHNICAL_MVP_CANDIDATE; DO NOT CONFUSE TECHNICAL COMPLETION WITH PUBLICATION.**

The R1.7 delivery queue #175–#182 has materially produced the small Atlas core defined by D-080.

#### What now exists

- reproducible locked Vite/TypeScript/MapLibre build;
- deterministic static R1 candidate generated from immutable R1.6 inputs;
- 77-target research-state registry;
- explicit geometry representation state for every target;
- neutral world map context;
- compact evidence register with bounded proposition + abstention + provenance;
- source-family / independence-group visibility;
- language/access + internal-review labels;
- discrete frozen research anchors;
- exact/period/near-anchor/unknown/aggregate temporal rendering guards;
- no live evidence API requirement.

#### Adversarial findings during MVP delivery

The MVP work found and corrected real issues rather than merely wrapping the data:
- CI caught a MapLibre listener type/build defect before merge;
- old P-level-first overview semantics were removed from the MVP path;
- unresolved target geometry was retained instead of manufacturing map precision;
- unresearched/held/C0 targets expose less information rather than simulated evidence;
- the old numeric BCE display path would render source-native -500 as 501 BCE; R1.7 now separates source/display anchors from Atlas astronomical internal years.

#### What remains deliberately weak

- all 77 target geometries remain unresolved;
- the neutral Natural Earth land layer is still an external static runtime dependency;
- no independent historical review;
- no full sponsor/browser/screen-reader usability acceptance;
- the candidate is not yet the public/canonical release.

These are visible release limitations, not reasons to rebuild backend/platform infrastructure.

#### Product judgment

The MVP still looks like the intended nugget:
**evidence package + boring map + register**, not a revived research platform.

No backend, database migration, auth, search service, graph infrastructure, frontend framework rewrite or new historical research was required.

#### Boundary

Open the post-MVP discovery lane for evidence-only experiments.

In parallel, require sponsor usability review before R1.8 makes an explicit **PUBLISH / HOLD / REWORK** decision.

A discovery result does not authorize production implementation.


### HC-017 — DISC-01 richer timeline vs discrete-anchor baseline — 2026-09-24

Disposition: **REJECT.**

The first post-MVP discovery run tested whether a richer timeline materially improves temporal interpretation over the technical MVP's discrete frozen anchors plus per-record precision labels.

#### Evidence

The frozen candidate has:
- 77 targets across 17 discrete research anchors;
- 19 reviewed C1 rows across 11 anchors;
- only 1 exact cross-section;
- 3 period-level positives;
- 1 near-anchor positive;
- 13 reviewed selected-year-unknown rows;
- 1 aggregate with no single territorial selected-year state.

The release does not contain reviewed continuous validity intervals for most claims.

External precedent review reinforces the mismatch:
- TimelineJS is strongest for short chronological narratives and visible spans require start/end dates;
- kepler.gl playback assumes timestamped observations and rolling time windows;
- digital-humanities uncertainty research warns that visually objective displays can hide historical uncertainty.

#### Baseline comparison

Task A — triage reviewed rows at one anchor:
the existing register already exposes exact / unknown / aggregate temporal state inline. A richer timeline adds no material information or operation reduction.

Task B — compare temporal precision across several anchors:
a one-screen overview can reduce navigation, but the useful part is cross-case comparison. A simple table exposes the same distinction without invented intervals or timeline machinery.

#### Adversarial result

- period bars would require unsupported start/end inference;
- point-only timeline marks collapse toward the current anchor/badge baseline;
- playback suggests continuity/density that the sparse R1 frame does not possess;
- the only surviving friction belongs more naturally to #187 cross-case comparison.

#### Consequence

Do not create a production timeline delivery issue.

Keep:
- discrete frozen anchors;
- temporal precision states;
- per-record temporal display rules;
- source-native BCE vs Atlas-internal-year separation.

New evidence could reopen this only if reviewed validity intervals become explicit data or users repeatedly fail a temporal task that discrete anchors plus ordinary comparison cannot solve.

Durable discovery: `docs/discovery/DISC_01_TIMELINE.md`.


### HC-018 — Discovery reset: novelty/competition inference correction — 2026-09-24

Decision: **RE-RUN WIDE-LENS VALUE DISCOVERY BEFORE MORE FEATURE-FIRST EXPERIMENTS.**

The prior wide-angle review remains useful evidence, but its competitor/novelty logic needs a narrower correction.

#### What survives from the old review

- full-platform expansion is not justified by current value evidence;
- generic DH platform expansion has no demonstrated cross-domain user need;
- ordinary map/register baselines are strong;
- the method/corpus contains stronger demonstrated value than bespoke interface complexity;
- maintenance/operations burden matters;
- real user/value evidence remains the central uncertainty.

Those conclusions were supported by more than competitor overlap.

#### What needs correction

- overlap with nodegoat/standards cannot itself invalidate an opportunity;
- “not unique” and “not valuable” must be separated;
- a feature queue cannot substitute for a user/job/alternative map;
- external-user demand/adoption remains unproven and must not be implied by the phrase “proven core”;
- commercial frameworks should not manufacture a customer model where none exists.

#### Current external landscape signal

Official materials confirm substantial generic capability overlap:
- nodegoat: configurable humanities data models, source-linked data, spatial/temporal and network visualisation, API/publication;
- Heurist: flexible humanities databases, Zotero sync, maps/timelines/networks, publishing/API;
- WHG: historical place data, reconciliation, collections and APIs;
- Enslaved.org: slavery-specific search across people/events/places/sources plus visualisation;
- SlaveVoyages: specialized quantitative tables/timelines/maps for Atlantic slave-trade data;
- Seshat: global systematic historical databank with expert review, snapshots, API and reproducible research outputs.

This establishes alternatives and substitutes. It does **not** establish that Atlas value is absent.

#### Active uncertainty

The key question is now:

> **For which concrete research/review job, if any, does the Atlas’s domain-specific evidence/abstention/research-state system create enough relative advantage over these alternatives and competent modular workflows to change behaviour?**

#198 is active. #185–#187 are blocked until that question is reassessed.

Durable standard: `docs/discovery/DISCOVERY_STANDARD_V2.md`.


### HC-019 — R1.8 sequencing red team — 2026-09-24

Decision: **FINISH THE R1 RELEASE/NO-RELEASE BOUNDARY BEFORE RUNNING EXTERNAL CASE TASKS.**

The proposed post-reset sequence was attacked before implementation.

#### What survived

- R1 still needs an explicit end-state because #159 requires a release/no-release gate.
- #200 remains the highest-information external-value experiment.
- no feature queue should restart before that external-value uncertainty is reduced.

#### What changed

The initial plan was too serial and too easy to misread.

Corrections:
- sponsor usability is only a release-coherence gate, not user validation;
- #200 protocol is frozen now rather than waiting;
- recruitment feasibility may proceed in parallel;
- participant execution waits for #203 so the tested packet cannot be silently superseded;
- PUBLISH became PUBLISH_CANDIDATE to prevent canonical-release ambiguity;
- HOLD_NO_RELEASE is an acceptable completed R1 outcome;
- REWORK keeps R1 open;
- “method/package” remains a working hypothesis, not a frozen project identity.

#### Why #203 is now the active boundary

R1 has:
- completed subject research;
- passed release QC with limitations;
- produced a green technical MVP candidate;
- not yet completed its sponsor release/no-release gate.

Closing that programme boundary before external task execution prevents the project from testing an artifact whose own sponsor-level coherence is still unresolved.

#### Why #200 remains prepared

The external expert audit attacks the most important remaining value hypothesis:
whether the structured evidence packet transfers its internal review value to independent reviewers.

The experiment is preserved, not postponed by indecision.

Only participant execution is sequenced after R1.8.

Durable gate: `docs/mvp/r1.8-sponsor-review.md`.


### HC-020 — Internal-only path and R1.8 stale-artifact finding — 2026-09-24

Decision: **DEFER EXTERNAL INVOLVEMENT; REWORK R1 RELEASE INTEGRITY; PREPARE SUBTRACTIVE INTERNAL DISCOVERY.**

#### Sponsor constraint

No external people should be involved yet.

This is treated as a real project constraint, not as permission to simulate external validation internally.

#200 remains preserved but deferred.

#### Internal release adversary result

A real R1.8 defect was found:

the committed `web/public/data/r1-mvp-candidate.json` was stale and lacked the current:
- research-state overview semantics;
- temporal-navigation contract;
- geometry manifest.

The Web MVP workflow masked this because it regenerated the candidate before running its stale check.

#### Bounded repair

- refresh committed candidate;
- check freshness before any CI regeneration;
- add a committed-byte reconstruction regression.

No historical claim or product feature changes.

#### Next internal discovery

#205 / EXP-02 asks whether the R1 evidence packet can be reduced while preserving:
- proposition vs abstention;
- temporal precision;
- evidence locus vs inference extent;
- law/practice and network/territorial boundaries;
- exact provenance and source dependency;
- review/access limits;
- non-absence research states.

It will also test whether ordinary Markdown / flat tables preserve the same internal contract.

This experiment cannot establish user value.

#### Boundary

Finish #203 first.

Then run #205.

Stop and re-evaluate again after #205.

No automatic successor.
