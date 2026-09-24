# EXP-01 — External expert audit crossover

**Issue:** #200  
**Parent:** #183  
**Decision basis:** D-082 / #198  
**Date:** 2026-09-24  
**Stage:** protocol preparation  
**Production implementation authorized:** no

## Question

Does the Atlas structured evidence packet materially improve external expert review of difficult slavery/coercion claims over a competent ordinary source-note/table baseline?

This experiment tests **transferable review value**, not UI novelty.

## Core hypothesis

For source-critical historical reviewers, the Atlas packet reduces safety-critical missed caveats / false inference and/or provenance reconstruction effort versus a strong ordinary baseline, despite added structure.

## Strong baseline

The baseline must be good enough that failure against it is meaningful.

Baseline packet:
- concise case question;
- same source list;
- same source locators;
- same relevant source summaries/excerpts permitted by citation limits;
- ordinary structured notes/table;
- no intentional omission of caveats present in the underlying evidence;
- no deliberately confusing layout.

It may use headings and bullets.

It may not use the Atlas-specific fields:
- bounded proposition;
- required abstention;
- evidence locus / inference extent;
- explicit temporal rendering state;
- source-family dependency label;
- formal review/access state.

## Atlas packet

Same underlying evidence, expressed through:
- bounded proposition;
- required abstention;
- evidence locus;
- inference extent;
- temporal applicability / precision;
- law/practice and network/territorial distinction where relevant;
- source version + locator;
- source-family dependency;
- review/access limitation.

No map or custom UI is required.

# Red team of the initial experiment design

## Attack 1 — self-scoring / rubric leakage

If the experiment scores participants on whether they notice exactly the distinctions explicitly named by the Atlas fields, the treatment is structurally advantaged.

### Correction

Use three outcome layers:

1. **Pre-registered reference hazards**
   - known failure modes from prior R1 adversarial review;
   - treated as a comparison reference, not historical ground truth.

2. **Open critique capture**
   - participants record any additional material concern, ambiguity or unsupported inference they see.

3. **Post-task adjudication**
   - external disagreements with the R1 reference are preserved;
   - a participant is never marked “wrong” solely for challenging the Atlas packet.

The experiment tests review performance, not obedience to the current ontology.

## Attack 2 — baseline crippling

A loose prose paragraph versus a structured Atlas packet would be unfair.

### Correction

Baseline receives:
- identical underlying evidence;
- clear source table;
- ordinary notes;
- readable structure;
- same source/version identifiers and locators.

The treatment advantage may come only from the **specific reasoning structure**, not from better typography or omitted baseline information.

## Attack 3 — order / learning effect

Seeing the Atlas packet first could teach participants the hazards and inflate performance on later baseline cases.

### Correction

Counterbalance:
- Group/order A: baseline case 1 → Atlas case 2 → baseline/Atlas case 3 according to randomized schedule;
- Group/order B: reversed treatment order.

No participant sees both formats for the same case before submitting their first answer.

## Attack 4 — domain expertise mismatch

Three globally different cases can punish participants for not being specialists rather than test the packet.

### Correction

The task is not “know the history from memory.”

Participants judge:
- what the **provided evidence** supports;
- what it does not support;
- what needs qualification;
- whether sources appear independent;
- what further evidence they would need.

Record:
- subject-area familiarity;
- period/region familiarity;
- digital-history/data experience.

Use familiarity as context, not as an exclusion criterion unless clearly inappropriate.

## Attack 5 — our internal R1 review is not independent truth

Using R1 as gold standard would circularly validate R1.

### Correction

Call R1 outputs **reference hazards**, not truth labels.

Any material external disagreement:
- is preserved verbatim;
- is adjudicated separately after the task;
- may trigger a new historical review issue;
- cannot be silently scored away.

## Attack 6 — stated reuse intent is weak evidence

“Would you use this?” is hypothetical enthusiasm.

### Correction

Ask for progressively stronger signals:
1. which format they would choose for the next analogous task;
2. whether they would keep/download the template;
3. whether they are willing to apply the packet to one of their own real claims/materials in a follow-up;
4. whether they are willing to introduce another relevant reviewer.

Only 3–4 are meaningful commitment signals.

## Attack 7 — time-on-task is noisy

Remote timing reflects reading speed, interruptions and domain familiarity.

### Correction

Treat time as a secondary measure.

Primary measures:
- safety-critical inference quality;
- provenance/dependency reconstruction;
- unsupported certainty;
- material caveats;
- burden/clarity observations.

## Attack 8 — public-repo contamination

The historical cases and R1 review are public.

### Correction

Participants are asked not to inspect the repository or search the cases during the timed comparison.

Record whether they already know the cases/project.

This experiment cannot guarantee laboratory blinding; do not overclaim it.

## Attack 9 — packet density may trade speed for safety

One composite score would hide the trade-off.

### Correction

Do not collapse outcomes into one score.

Report separately:
- correctness/safety;
- provenance recovery;
- effort/time;
- clarity;
- burden;
- reuse/commitment signal.

## Attack 10 — success would not validate a product

The test contains no map, search or platform.

### Correction

A positive result promotes only the **method/evidence-package hypothesis**.

It does not authorize:
- bespoke UI;
- platform revival;
- public launch;
- search/graph/timeline features.

# Revised design

## Candidate frozen cases

Use three existing R1 cases with different failure modes.

### Case A — Teotihuacan, 500 CE

Reference hazards:
- earlier Moon Pyramid sacrificial evidence projected to 500 CE;
- foreign-born / captive / sacrificed converted into slave status;
- site evidence generalized to citywide practice.

Why useful:
tests temporal projection + status translation + locus/extent.

### Case B — Portuguese Colonies, 1800

Reference hazards:
- constituent-colony evidence collapsed into one empire-wide territorial practice state;
- aggregate frame treated as a single historical territory;
- evidence from some possessions generalized to all.

Why useful:
tests aggregation + territorial inference.

### Case C — Lazica, 500 CE

Reference hazards:
- sixth-century slave-export evidence converted into exact selected-year 500 CE truth;
- modern discussion of Procopius counted as independent evidence from Procopius;
- export/network evidence converted into broad territorial prevalence.

Why useful:
tests temporal precision + source dependency + network/territorial separation.

These cases are already researched. No new subject research is authorized.

## Participant task

For each case, answer:

1. What is the strongest claim you think the provided evidence supports?
2. What must the final claim explicitly avoid or qualify?
3. What is the temporal scope you would permit?
4. What is the spatial/inference scope you would permit?
5. Which sources, if any, are not genuinely independent?
6. What additional evidence would you need before making a stronger claim?
7. How confident are you in your review, and why?

Treatment packet may answer some of these structurally; that is intentional. The question is whether the structure improves the quality/effort trade-off enough to matter.

## Measures

### Safety / inference

Record:
- unsupported exact-year assertion;
- unsupported slave-status assertion;
- target/context leakage;
- external/network → territorial leakage;
- aggregate → uniform territorial leakage;
- false source independence;
- other valid material caveat raised.

### Provenance

Record:
- source/version correctly identified;
- decisive vs contextual evidence understood where relevant;
- shared dependency noticed;
- further evidence need made explicit.

### Effort

Record where feasible:
- completion time;
- number of backtracks/questions;
- self-reported cognitive burden.

### Adoption signal

Record:
- next-task format choice;
- template keep/download;
- willingness to apply to own real case;
- willingness to refer another reviewer.

## Sample

Target a small purposive external sample.

Minimum useful start:
- 4 independent reviewers.

Preferred:
- 6–8 if accessible without turning recruitment into a project.

Do not calculate population-level effect estimates.

Participant profiles may include:
- historians working on slavery/coercion/dependency;
- historians with strong source-critical methods;
- experienced digital historians / research-data historians.

## Decision thresholds

No single scalar score.

### Encouraging

At least two independent reviewers show a **material safety/provenance advantage** with the structured packet that is not explained solely by extra information or presentation quality, and there is at least one stronger reuse signal (own-case follow-up or referral).

### Mixed

Packet improves one safety dimension but adds substantial burden, or advantage appears only for one reviewer/case.

Result:
- revise segment or packet;
- no promotion.

### Disconfirming

Strong baseline reaches practical parity on material inference/provenance while:
- Atlas packet is slower/more burdensome; and
- there is no stronger reuse signal.

Result:
- stop feature-oriented discovery;
- preserve method/benchmark artifacts;
- reconsider whether the packet itself needs to remain a product-facing artifact.

## External disagreement rule

If reviewers identify a credible flaw in the current R1 reference:
- do not alter R1 inside this experiment;
- open a separate historical-review issue;
- preserve the experiment response as evidence;
- canonical data remains unchanged until normal research/release review is complete.

## Current blocker

The protocol can be frozen now.

Execution requires real external participants.

The model/user/sponsor cannot stand in for the external sample.
