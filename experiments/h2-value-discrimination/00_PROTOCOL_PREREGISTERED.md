# H2 Value-Discrimination Pilot — Pre-registered Protocol

**Issue:** #146  
**Authorized:** 2026-09-23  
**State:** active — setup only until adversarial review passes  
**Canonical historical release:** v0.6.1 unchanged  
**Base commit:** `ce6c23ceec3b0ed1c9ef54b67eae1b1ff8b734e2`

## Purpose

Test the remaining project-value hypothesis after HC-003 / D-062:

> Does the Atlas corpus/method, and then the smallest thin atlas/query representation, materially improve difficult historical reasoning over the strongest competent boring baseline?

This is a value experiment, not a data-release batch and not an application-development horizon.

## Pre-registered cases

### Q1 — Andes: continuity / temporal truth

To what extent is it defensible to treat pre-Hispanic Inca `mit'a` and the Spanish colonial Potosí `mita` as a continuous institution rather than related but materially transformed coercive-labour regimes?

Stress:
- terminology and category continuity;
- selected-year truth across regime change;
- evidence scope vs generalization;
- forced labour / corvée / slavery distinction.

### Q2 — British India: law / practice

What can a selected-year historical view defensibly say around Act V of 1843 when the legal enforceability/status of slavery changed but social/economic dependency and coerced labour did not necessarily vanish on that date?

Stress:
- law is not practice;
- abolition date is not disappearance date;
- jurisdiction and subregional variation;
- legal evidence vs social-practice evidence.

### Q3 — Genoese Black Sea network: participation / territorial inference

What does Genoese participation in the Black Sea slave trade c. 1260–1500 establish about Caffa/other trade nodes, network participation, and territorial practice in Genoa itself—and what does it not establish?

Stress:
- network participation is not territorial practice;
- port/site evidence locus vs wider territorial inference;
- historical political/spatial relations;
- trade volume is not prevalence.

## Arms

### A — strongest boring baseline

Use a competent conventional workflow:
- specialist scholarship;
- bounded primary/source-native material where it adds direct evidence;
- structured prose notes + ordinary source table;
- ordinary search and a strong general-purpose model;
- no Atlas ontology imposed during the first synthesis.

### B — Atlas corpus/method

Use the **same frozen evidence packet** as A. Re-represent it using the project's surviving method:
- claim-specific provenance;
- explicit evidence class and supports/challenges/qualifies/context direction;
- temporal applicability separated from dating precision;
- evidence locus separated from inference extent;
- law / practice / participation / coverage / geometry separated;
- unsupported dimensions remain unassessed;
- no new P0–P4 assignment.

### C — smallest thin atlas/query representation

Use only the information in B.

No production database migration, new service, package, framework or deploy target is allowed. The default implementation is a static experiment artifact generated from the structured case representation. Add spatial/temporal interaction only where it is necessary to test the hypothesis.

## Evidence packet rule

For each question:
1. discover and review the source package;
2. freeze a source/evidence log;
3. write the baseline synthesis;
4. only then translate the same package into Atlas structure;
5. the thin view may consume only the structured Atlas artifact.

Do not let B or C gain better sources than A.

## Evaluation

Do not produce one aggregate score.

For each arm record:
- **provenance recovery:** can a reader recover the exact evidentiary basis for a proposition?
- **uncertainty / abstention:** are unsupported or disputed dimensions visibly left unresolved?
- **temporal truth:** are dates/ranges distinguished from positive applicability?
- **spatial discipline:** is evidence locus distinguished from inference extent?
- **layer separation:** are law, practice and external participation prevented from silently substituting for one another?
- **comparison quality:** can relevant similarities/differences be inspected without implying full equivalence?
- **overclaim:** what false generalization becomes easy or hard?
- **representation overhead:** what additional authoring/maintenance structure is required?
- **unique practical gain:** what can a competent reader do materially better?
- **parity / no-value:** where does a smaller arm already perform as well?

## Probe questions

After all three artifacts exist, evaluate them against fixed probes without changing the artifacts to fit the probes:

1. What proposition is strongest, and what proposition must remain unasserted?
2. What date/range is evidence date versus positive historical applicability?
3. What geographic locus is directly evidenced, and how far may the claim extend?
4. Which evidence is legal/normative, which concerns observed practice, and which concerns participation/network?
5. Which source supports the decisive proposition and where can it be recovered?
6. What contrary/qualifying evidence would a reader most easily miss?
7. Can the artifact compare the case with another pilot case without implying equivalence?
8. Does the visual/query surface reveal something materially harder to recover from the corpus artifact alone?

## Success / failure signals

### Corpus/method survives as value

At least two independent cases must show a repeatable practical gain over A in one or more of:
- provenance recovery;
- preservation of uncertainty/abstention;
- inspectable cross-place/time reasoning;

and must not increase overclaim.

A difference that exists only because B contains more documentation does not count unless that documentation changes recoverability or error behavior.

### Thin atlas survives as value

At least two independent cases must show a practical gain of C over B. Visual novelty, attractiveness or faster scanning alone is insufficient unless it changes correct understanding or recovery of the evidence.

### Failure

If A performs materially as well as B, record parity.

If B performs better but C does not, prefer methodology/corpus and stop application expansion.

If neither B nor C materially improves the strongest baseline, stop further Atlas expansion and preserve the method/corpus/audit artifacts.

## Explicit exclusions

This pilot does not authorize:
- changing canonical v0.6.1;
- adding experiment cases to published/canonical research tables;
- M2 production migration;
- bulk research expansion;
- frontend redesign;
- new monitoring or infrastructure;
- a successor horizon.

## Reproducibility

Record:
- repository base/head commit;
- issue/PR;
- access date for web sources;
- exact source titles/URLs/identifiers where available;
- source role and relevant locator/quoted proposition;
- experiment artifact versions;
- protocol revision caused by the setup adversary.

The adversarial setup review must occur before historical execution.
