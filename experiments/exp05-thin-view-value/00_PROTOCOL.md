# EXP-05 — thin-view value discrimination

Issue: #223  
Primary gate: **product/workflow value**  
Status: preregistered / active  
Canonical historical release: **v0.6.1 unchanged**

## Question

Does the current thin EXP-04 Atlas preview materially improve difficult comparative
historical work over both:

A. ordinary case packets + source notes; and  
B. the portable package without the map?

This experiment tests **internal task/workflow value** only. It cannot establish
external demand, adoption, researcher preference, or independent historical validity.

## Why this experiment now

EXP-04 showed that D-089 can preserve heterogeneous evidence internally. #221 then
made that package viewable through an ordinary MapLibre map + table.

The largest remaining project-form uncertainty is therefore whether the derived view
adds practical value beyond the corpus/method itself.

Alternatives considered:
- **immediate broad research expansion:** adds rows but does not resolve the project-form
  question;
- **reopen Indus/Hadhramaut/Cuzco blockers:** lower information gain while access
  conditions are unchanged;
- **another representation-extension test:** weakly justified because EXP-04 found no
  missing repeated distinction.

EXP-05 therefore has the highest expected information gain.

## Frozen tasks

### T1 — temporal + spatial truth

Cases:
- Sumerian City-States — 2000 BCE
- Cuzco — 1300 CE
- Angkor — 1200 CE

Task:
1. state what is supported exactly at the anchor versus near-anchor/retrospective;
2. state the safest geographic/frame representation;
3. identify what must not be shown as a filled historical practice polygon.

### T2 — external/network versus territorial practice

Cases:
- Indus Valley Civilization — 2000 BCE
- Viking trade network — 900 CE
- Andaman Islands communities — 1800 CE

Task:
1. distinguish positive external/network/coercion evidence from territorial/internal
   practice;
2. identify supported, under-review and unresolved dimensions;
3. avoid converting external association into local slavery.

### T3 — category + dependency negative control

Cases:
- Sumerian City-States — 2000 BCE
- Angkor — 1200 CE
- Ethiopian Empire — 1800 CE

Task:
1. identify one historically specific term/status boundary per case that blocks generic
   “dependent = slave” normalization;
2. identify one important source-dependency or counting trap per case;
3. state what cannot be inferred about prevalence/intensity.

T3 is intentionally document-heavy and is **not expected** to benefit materially from
the map. If the thin view wins merely because presentation quality is rewarded, the
experiment is invalid.

## Lanes

### A — boring baseline

Permitted:
- individual EXP-04 case Markdown packets;
- `source_relations.csv` as an ordinary source-note table.

Prohibited:
- `targets_extended.csv`;
- generated preview JSON;
- preview UI;
- RESULT/audit summaries that pre-compose cross-case comparisons.

No new web research unless a frozen task is impossible from the existing evidence.
If so, record the gap rather than research until a desired answer appears.

### B — portable package

Permitted:
- `targets_extended.csv`;
- `source_relations.csv`;
- `manifest.json`;
- `RESULT.md`;
- `09_DEPENDENCY_CATEGORY_ACCESS_AUDIT.md`;
- `10_ADVERSARY.md`.

Prohibited:
- preview UI/generated preview JSON as a task surface.

### C — thin Atlas

Primary surface:
- live `research-preview.html`.

Source links opened from target detail are permitted because provenance recoverability
is part of the task. The UI must not be changed before all three C tasks are complete.

## Effort metric

Elapsed time is not scored.

Record:
- **distinct artifacts/pages opened**;
- **interaction steps** needed to obtain the answer.

One artifact opened once may support several facts within the same task.
A source link opened from the preview counts as one additional page.

Tool batching does not reduce the artifact count.

## Reference checklist

The following task-level elements are frozen **before lane execution** and are used
only for scoring correctness/scope and overclaim.

### T1 required distinctions

Sumer:
- near-anchor late Ur III evidence, not exact 2000 BCE;
- polity aggregate / transition, not one sovereign territory;
- no aggregate slavery polygon.

Cuzco:
- 1300 is incipient/local Killke-period Cuzco;
- mature Inca/colonial evidence is retrospective/later;
- no later-imperial Cuzco/Inca polygon back-projection.

Angkor:
- K.273 (1186) / K.908 (1191) are near-anchor, not exact 1200;
- node/site + linked institutional network;
- no automatic empire-wide practice polygon.

### T2 required distinctions

Indus:
- positive external Meluhhan association/status interpretation exists;
- territorial/local Indus slavery remains under review;
- acquisition geography/local enslavement unknown.

Viking:
- network frame itself legitimately supports capture/transport/sale;
- network evidence must not become one Viking territorial practice polygon;
- captive does not automatically equal sold slave.

Andaman:
- external British colonial captivity near anchor supported;
- indigenous internal practice unassessed;
- later penal-colony institutions cannot be backdated.

### T3 required distinctions

Sumer:
- `geme₂` context-dependent; `un-il₂` not slave in current specialist analysis;
- source/archive counts cannot establish prevalence;
- editions/lexical resources do not multiply underlying events.

Angkor:
- `khñum` not universally slave;
- K.273/K.908 personnel totals are not slave totals;
- later analyses reusing the inscriptions are dependency chains.

Ethiopia:
- `gabr/gäbbar` / servant / tributary terms require source-specific mapping;
- Bruce → later quotation/synthesis dependency must not be double-counted;
- traveler/market/export counts do not establish empire-wide prevalence.

## Evaluation dimensions

For each task/lane record:
1. correctness/scope against the frozen checklist;
2. uncertainty/abstention preservation;
3. provenance/source-family recoverability;
4. false-generalization/overclaim count;
5. artifact/page count;
6. interaction-step count;
7. any comparison/insight materially easier in that lane.

No new weighted composite score will be invented after seeing results.

## Material advantage rule

A lane earns a material task advantage only if it improves at least one of:
- correctness/scope;
- uncertainty preservation;
- provenance recoverability;
- materially lower interaction burden;

**without increasing overclaim**.

Cosmetic readability alone is not material.

## Decision rule

Compare B vs A and C vs the strongest of A/B.

- C materially improves **>=2/3 tasks** → thin Atlas earns continued derived-view
  investment.
- B improves but C does not → corpus/method survives; stop application expansion beyond
  maintenance.
- neither B nor C materially improves A → stop further Atlas expansion; preserve
  method/corpus/audit outputs.
- any dangerous presentation-induced overclaim may force REVISE regardless of wins.

## Contamination controls

This is one internal operator/model, so lane execution is **not independent or blinded**.

Controls:
- frozen tasks/checklist before lane answers;
- lane A executed first;
- lane outputs written before subsequent lane scoring;
- no UI changes during C;
- no new source research to repair a weak lane;
- final adversary must explicitly attack contamination and task selection.

## Complexity boundary

No new historical research tranche, schema/API/database work, geometry programme,
frontend changes, or scoring-rule change before result.

## Deeper-reasoning escalation

After the first complete scoring draft, a GPT-6 Astra medium-reasoning replay is
warranted if available. Focus only on whether the apparent lane advantage is real or
an artifact of task design, scoring or model contamination. It must not rewrite frozen
criteria.
