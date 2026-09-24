# DISC-07 analysis — cross-dimensional coverage audit

**Issue:** #245  
**Frozen universe:** 77 R1.6 registry targets  
**Registry blob:** `cec379246221d166db3830845566311077596862`  
**Historical subject research:** none

## Disposition

**SURVIVES — as a narrow target-frame QA rule, not as an evidence-gap map or product feature.**

The joint matrices expose one material research-design blind spot that the existing
marginal gates do not state explicitly:

> **Chronology coverage and frame-class coverage both pass separately, but they are not
> jointly balanced.**

The current R1 balance summary says:
- all frozen source-anchor bands are represented;
- multiple frame classes are represented;
- all six release polity sampling sectors are represented;
- no release polity sector exceeds the cap.

Those marginal checks are true. They do not imply that structurally different frame
types are represented across the same chronological bands.

Matrix A shows that early chronology is dominated by polity-like frames:
- **2000 BCE:** 4 rows — historical-period polity, polity aggregate, polity, civilization region;
- **500 BCE:** 9 rows — 8 polity + 1 dynastic polity;
- **500 CE:** 11 rows — 9 polity + 1 island polity + 1 urban-polity/site.

The recurring non-polity frame families enter unevenly:
- institution/estate: 1000 BCE, 700, 800, 1000, 1100;
- mobile network: 100 BCE, 900, 1300, 1400;
- node/site: 1200, 1400, 1500;
- region/community: 1600, 1700, 1800.

This is not a historical “gap.” It is a **target-frame design concentration**.

## Why this is material

A future programme could satisfy the current marginal gates while still making its
earliest comparison almost entirely through polity/civilization frames and its later
comparison through sites, networks, institutions and communities.

That matters because the project has repeatedly shown that frame class changes the
permitted inference:
- site ≠ polity territory;
- network ≠ territorial practice;
- aggregate ≠ uniform jurisdiction;
- community frame ≠ one polity.

Therefore future claims such as “chronologically broad and structurally diverse target
coverage” require a **joint chronology × broad-frame-family audit**, not just separate
marginal checks.

This finding would materially qualify future target-frame design. It does **not**
authorize filling empty cells or choosing cases because evidence is likely positive.

## Matrix B — sector × chronology

Matrix B mostly confirms a known limitation rather than discovering a new one.

Sector B appears only at the 1300 anchor in the frozen full registry, and the R1 target
freeze already explicitly records the new-polity sector-B gap and the role of legacy
South American rows.

**Result:** useful verification, not new decision evidence.

No named modern region labels were invented.

## Matrix C — frame × QA/research state

Matrix C adds two QA observations but does not independently meet the SURVIVES bar.

1. The registry contains **10 singleton effective frame labels**:
   `civilization_region`, `dynastic_polity`, `historical_period_polity`, `imperial_title_fragmented_sovereignty`, `invalid_label_at_anchor`, `island_polity`, `jurisdiction_aggregate`, `jurisdiction_title_transition`, `node_or_incipient_polity`, `urban_polity_site`.
2. Recurring broad classes are concentrated in a few families:
   `institution_estate` 7; `mobile_network` 7; `node_site` 7; `polity` 37; `polity_aggregate` 2; `region_community` 7.

This shows that `effective_frame_class` serves both broad structural grouping and
case-specific frame limitation. A future balance audit should therefore use a stable
**broad selection-frame family** for coverage checks and keep the more specific
effective frame for historical interpretation.

Do not mechanically merge the singleton labels here; D-092 compression/first-refusal
would require a separate semantics test.

## Immutable registry versus live project state

The R1.6 registry intentionally remains frozen. It still marks later EXP-04/06/08
research targets according to their R1.6 release state.

Therefore Matrix A/C are valid for **R1.6 target/release design**, not a live “what has
the project researched by today?” dashboard.

A future live-coverage view, if ever needed, must be a derived overlay that preserves
the immutable release state rather than rewriting it.

This prevents a serious category error:
- frozen release state ≠ current experimental research state;
- unresearched in R1.6 ≠ unresearched forever;
- neither state implies historical absence.

## Anchor-normalization note

The registry stores anchors in more than one source-preserving representation:
numeric values and display strings such as `2000 BCE` / `1300 CE`.

The audit normalized these **only for grouping**. No registry value was changed.

A naïve numeric cast would have placed 41 polity rows into an artificial missing-anchor
bucket. That is a tooling hazard, not a historical coverage finding.

## Frozen discriminator

SURVIVES required:
> at least one material cross-dimensional blind spot not already explicit in the
> baseline that would change or materially qualify a future target-frame/horizon
> decision.

Observed:
- chronology × frame interaction: **material and not explicit in current pass/fail gates**;
- sector × chronology: already explicit/known;
- frame × state/QA: useful QA/semantics warning, not a second independent decision win.

**Threshold met by one material joint-balance blind spot.**

## Method consequence

For future target-frame programmes that make broad-coverage claims:
1. keep marginal gates;
2. add a non-visual **chronology × broad-frame-family** cross-check before subject research;
3. preserve empty/sparse cells rather than automatically filling them;
4. state whether sparsity reflects the candidate universe, deliberate design or
   unresolved access—not historical absence;
5. keep polity neutral-sector checks separate;
6. never use the matrix to infer prevalence or to reward archive-rich areas.

No change to frozen R1, EXP-08, canonical v0.6.1 or current ontology follows.
