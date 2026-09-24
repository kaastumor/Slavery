# DISC-01 — Timeline interaction versus discrete-anchor baseline

**Issue:** #184  
**Parent:** #183  
**Stage:** completed discovery  
**Date:** 2026-09-24  
**Production implementation authorized:** no

## Question

Does a richer timeline materially improve a real Historical Slavery Atlas task over the technical MVP's current discrete frozen-anchor navigation plus per-record temporal precision guard?

## Concrete task

A user wants to answer:

> **Across several historically different reviewed cases, what can I safely say at the selected research anchor, and which apparent time differences are only period-level / near-anchor / unknown rather than exact-year evidence?**

The task is deliberately about temporal interpretation, not visual spectacle.

Test cases must include at least:
- Middle Kingdom of Egypt — period-level support;
- Carthage — period-level support;
- Gao — near-anchor / approximate;
- United States 1800 — exact cross-section;
- Chimú — period-level support;
- one selected-year-unknown row such as Teotihuacan.

## Strongest boring baseline

The existing MVP:

1. discrete navigation over frozen research anchors only;
2. target register filtered to the selected anchor;
3. each reviewed target displays one explicit temporal state:
   - exact cross-section;
   - period-level support;
   - near-anchor / approximate;
   - unknown;
   - aggregate / not-applicable;
4. each detail record displays the human-readable temporal guard;
5. source-native BCE display remains separate from Atlas astronomical internal year.

This baseline is intentionally strong. A richer timeline must beat it rather than merely look richer.

## Candidate richer interaction

The smallest candidate concept is **not** a production timeline.

For the experiment only, consider a horizontal temporal overview that could show:
- frozen anchors as discrete positions;
- reviewed targets attached to those anchors;
- temporal-support category encoded directly on each item;
- optional period/near-anchor extents only when already present in reviewed evidence.

No inferred continuous interval may be created from an anchor alone.

## Predeclared kill rule

**REJECT** richer timeline interaction if any of the following holds:

1. it does not materially reduce interpretation/navigation burden on at least **two independent test tasks** compared with the boring baseline;
2. its main benefit is aesthetic or “seeing time” rather than a concrete correctness/comparison gain;
3. it requires fabricating start/end dates or continuous validity intervals not present in R1;
4. it makes period-level or near-anchor evidence look more exact than the baseline;
5. it needs a new timeline library/service/data model merely to reproduce information already clear in the register.

A small result may be **REVISE** rather than reject only if one narrower temporal affordance clearly solves a repeated task while the full timeline does not.

## Evidence collection plan

1. inspect a small set of external timeline/map precedents for interaction patterns and known precision risks;
2. derive the actual frozen anchor/temporal-state distribution from the MVP candidate;
3. run two or more concrete comparison tasks against:
   - A: current discrete-anchor/register baseline;
   - B: a non-production paper/data prototype of richer timeline semantics;
4. record:
   - steps/operations;
   - temporal distinctions exposed;
   - new ambiguity introduced;
   - extra data assumptions required;
5. attack the provisional result for false precision and feature attraction.

## Allowed dispositions

Exactly one final disposition:
- ADOPT_FOR_EXPERIMENT
- REVISE
- REJECT
- PARK

Even ADOPT_FOR_EXPERIMENT does not authorize production implementation.


# Discovery evidence

## Corpus shape

The current frozen candidate is unusually sparse in time:

- 77 frozen targets;
- 17 distinct frozen research anchors;
- 19 reviewed C1 rows;
- reviewed C1 appears at 11 of those anchors.

Reviewed temporal states are:

- exact cross-section: 1;
- period-level support: 3;
- near-anchor / approximate: 1;
- selected-year unknown: 13;
- aggregate / no single territorial state: 1.

The remaining 58 targets are unassessed because C1 subject research was not performed.

This matters because the candidate does **not** contain normalized continuous validity intervals for most historical claims.

## External precedent review

### Knight Lab TimelineJS

Official documentation:
- https://timeline.knightlab.com/
- https://timeline.knightlab.com/docs/json-format.html
- https://timeline.knightlab.com/docs/using-spreadsheets.html

Useful observations:

- TimelineJS is designed around events/slides with a required start date and optional end date.
- End dates create visible time spans.
- A separate display-date field can soften how uncertain dates are written, but the event still needs a position/date for layout.
- Knight Lab recommends relatively short timelines and says the tool works best for a strong chronological narrative rather than stories that need to jump around.

Subtractive implication for the Atlas:

R1 has frozen research anchors and epistemic precision states, not defensible start/end intervals for most claims. Populating timeline spans would therefore require new temporal inference. Rendering every row as a point avoids that inference but largely reproduces the existing discrete-anchor navigation.

### kepler.gl time playback

Official documentation:
- https://docs.kepler.gl/docs/user-guides/h-playback
- https://docs.kepler.gl/docs/user-guides/e-filters

Useful observations:

- time playback operates on time-related fields/timestamps;
- it uses a rolling window and distribution/time-series controls;
- its interaction model assumes observations distributed through time.

Subtractive implication for the Atlas:

Playback suggests continuity and event density that R1 does not possess. The Atlas has sparse frozen research anchors and many selected-year-unknown results. A playback control would therefore be a poor semantic fit even if technically easy.

### Digital-humanities uncertainty literature

Panagiotidou et al., *Communicating Uncertainty in Digital Humanities Visualization Research*, IEEE TVCG 29(1), 2023:
- DOI: https://doi.org/10.1109/TVCG.2022.3209436
- PubMed: https://pubmed.ncbi.nlm.nih.gov/36166561/

The paper's motivating problem is directly relevant: humanistic data contain multiple uncertainties, while visualizations can appear overly objective when uncertainty is not visibly communicated.

Subtractive implication for the Atlas:

A visually continuous timeline should be presumed risky unless its uncertainty encoding improves a concrete task. Visual smoothness is not neutral here.

# Smallest discriminating experiment

No production UI was built.

The experiment compared the current MVP with the smallest plausible richer-timeline semantics on two tasks.

## Task A — anchor-local temporal triage

Question:

> At 1800, which reviewed candidate rows have exact selected-year support, which are unknown, and which cannot receive one territorial selected-year state?

Actual reviewed 1800 cases:

| Target | R1 temporal state |
| --- | --- |
| United States of America | exact cross-section |
| Inuit Arctic communities | selected-year unknown |
| Portuguese Colonies | aggregate / no single territorial state |

### Baseline

The MVP user selects the discrete 1800 anchor.

The register already exposes the temporal category inline for each target, and the detail view exposes the full display rule.

No inferred interval is required.

### Rich timeline concept

A richer timeline can place the same three items at 1800 and encode the same three states.

It does not reduce the essential operation count or expose a distinction unavailable in the baseline. If it draws intervals or playback, it adds unsupported semantics.

**Result:** no material task advantage.

## Task B — cross-anchor precision comparison

Question:

> Compare temporal precision for Middle Kingdom, Carthage, Teotihuacan, Chimú, Gao and U.S. 1800 without accidentally treating their anchors as equivalent exact observations.

Frozen result:

| Target | Anchor | R1 temporal state |
| --- | ---: | --- |
| Middle Kingdom of Egypt | 2000 BCE | period-level |
| Carthage | 500 BCE | period-level |
| Teotihuacan | 500 CE | selected-year unknown |
| Chimú Empire | 1300 CE | period-level |
| Gao | 1500 CE | near-anchor / approximate |
| United States | 1800 CE | exact cross-section |

### Baseline

The discrete-anchor register requires moving between anchors to inspect all six cases.

That is somewhat cumbersome, but every transition preserves the correct temporal label and never implies continuity between anchors.

### Rich timeline concept

A single overview can place all six cases on one horizontal axis and expose their categories together.

This reduces navigation for this one comparison task.

However:

- drawing period bars would require start/end values that the frozen release does not provide;
- drawing only anchor points plus category labels collapses the “rich timeline” into a simple temporal-state overview;
- the actual benefit is **cross-case comparison**, not continuous temporal navigation;
- a plain comparison table exposes the same six distinctions with lower ambiguity and no timeline-specific machinery.

**Result:** a narrow comparison benefit exists, but it does not justify richer timeline interaction.

# Adversarial replay

## Attack 1 — are we rejecting a feature merely because the corpus is small?

Partly small scale matters, but the stronger objection is semantic.

Even at larger row counts, a playback/continuous timeline remains unsafe unless claim-validity intervals become explicit reviewed data. Scale alone would not make inferred intervals legitimate.

## Attack 2 — could TimelineJS display only points and custom display dates?

Yes.

That removes much of the false-precision risk, but then it duplicates the existing frozen-anchor navigation and temporal badges. The distinctive timeline value disappears.

## Attack 3 — does cross-anchor comparison prove timeline value?

No.

It proves a possible future need to compare several temporal states at once. That need belongs more naturally to the separately registered cross-case-comparison question (#187), where a boring table is the correct baseline.

## Attack 4 — are we ignoring narrative/pedagogical value?

A narrative timeline could be useful for a curated story, but R1 is a research-state/evidence product, not a single chronological narrative. Knight Lab's own guidance is strongest for short chronological stories. Narrative presentation is not the task tested here.

# Kill-rule result

The predeclared threshold is **not met**.

- Task A: no material gain.
- Task B: one real navigation gain, but it is reproduced more safely by a simple cross-case table/overview.
- A continuous or playback timeline would require temporal semantics the candidate does not currently contain.
- A point-only timeline collapses back toward the boring baseline.

# Final disposition

## **REJECT**

Reject a richer timeline/playback interaction as a post-MVP feature candidate on current evidence.

This does **not** mean time is unimportant.

Keep:
- discrete frozen-anchor navigation;
- explicit temporal precision categories;
- per-record display rules;
- source-native BCE / Atlas-internal-year separation.

Do not create:
- inferred validity intervals;
- continuous playback;
- a new timeline library;
- a production timeline delivery issue.

If future reviewed data acquire explicit claim-validity intervals, or real users repeatedly fail a temporal task that the discrete anchors and a plain comparison table cannot solve, that would be new evidence and could reopen discovery.

The small cross-anchor comparison friction should be tested under #187 rather than smuggled into a timeline feature.
