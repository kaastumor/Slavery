# ADV-001 — Adversarial Audit of the COV-002 Completeness-Stop Inference

**Issue:** #153  
**Date:** 2026-09-23  
**Target conclusion:** “Systematically researching all known history purely in pursuit of completeness is not justified by the evidence we have.”  
**Scope:** inference audit only; no new historical cells  
**Preliminary verdict:** **THE BROAD CONCLUSION OVERREACHES THE EXPERIMENT. THE OPERATIONAL STOP SURVIVES ONLY IN A NARROWER FORM.**

## 1. What must be separated

COV-002 can support at least three different statements:

1. **A — Current-workflow continuation:** the project should not automatically continue adding detailed rows after N=37.
2. **B — Current compact-register economics:** the experiment demonstrated favorable long-run research/review/update economics for R.
3. **C — Comprehensive-coverage thesis:** a systematic, versioned, globally scoped coverage program is not worth pursuing absent an external use case.

A is an operational governance decision.

B is an empirical claim about the tested artifact/workflow.

C is a much broader strategic claim.

COV-002 clearly supports **A**. It does not establish **B**. The central question of this audit is whether failure to establish B supports C.

It does not.

---

# 2. Attack matrix

| ID | Attack | Severity | Effect on broad completeness-stop inference |
| --- | --- | --- | --- |
| X1 | Scope mismatch: protocol says artifact form/reuse economics, not world-history representativeness | critical | prevents generalization from COV-002 to comprehensive coverage |
| X2 | N=25→37 is a 48% expansion, not a long-run scale curve | high | cannot identify economies/diseconomies at hundreds/thousands of targets |
| X3 | 4/6 maintenance gate became mathematically unreachable after three neutral no-change shocks | critical | maintenance FAIL is partly a denominator-design artifact |
| X4 | “Source object” and “source link” each count as one update atom | critical | maintenance metric suppresses F→R complexity difference |
| X5 | Research/search cost was not measured as cost, only bounded procedurally | critical | cannot conclude total maintenance/research economics |
| X6 | Row-local update shocks do not test batch/source reuse across many cells | high | systematic research may have different marginal costs |
| X7 | Fixed tasks were inherited from COV-001 | high | larger-corpus emergent/option value was not tested |
| X8 | External-use-case-first rule can reintroduce demand/archive-density bias | high | conflicts with global-balance motivation |
| X9 | Target-frame failures were treated primarily as scaling cost | medium-high | they are also a demonstrated corpus-quality benefit |
| X10 | Negative controls constrain substitution, not completeness value | medium | irrelevant to whether a global index is worthwhile |
| X11 | Continuous-maintenance assumption was not compared to versioned/as-of releases | high | overstates need for perpetual currentness |
| X12 | “All known history” conflates target completeness with evidence completeness | critical | strategic object being rejected was never operationally defined |

---

# 3. Critical attack X1 — COV-002 explicitly disclaims the inference later drawn from it

The revised protocol states:

> “The experiment is about artifact form and reuse economics, not world-history representativeness.”

It freezes a 12-cell rank-2 expansion and asks whether:
- value remains reusable from 25→31→37;
- R can preserve F's fixed-task value;
- six bounded updates are maintainable.

D-067 later says:

> “Do not continue systematic/global coverage-corpus expansion from project momentum alone.”

That narrower operational consequence is defensible.

But the user-facing summary escalated this to:

> “Systematically researching all known history purely in pursuit of completeness: not justified by the evidence we have.”

That sounds like COV-002 evaluated the value/economics of a comprehensive historical reference corpus.

It did not.

The tested object was a **37-row sample using a specific row-by-row research/update workflow**.

A comprehensive project could differ on:
- coverage granularity;
- batch research;
- source reuse;
- update cadence;
- review architecture;
- contributor distribution;
- target frame;
- versioning;
- query repertoire.

**Finding:** the strategic completeness claim is outside the experiment's declared scope.

---

# 4. Critical attack X3 — the maintenance threshold stopped being discriminating

Preregistered requirement:

> R touches <=70% as many review atoms as F in at least **4/6** maintenance shocks.

Observed:
- 3 shocks produced material evidence updates;
- 3 produced `no_source_found`;
- the result adversary correctly refused to count `0/0` as a compact-register savings win.

Once that interpretation was chosen, **at most three rows could qualify**.

The gate still required four.

Therefore the maintenance economy gate was mathematically impossible to pass after the update outcomes, regardless of how cheap R might have been on every row that actually changed.

Example counterfactual:
- all three changed rows: F=100 atoms, R=1 atom;
- all three no-change rows: F=0, R=0 and treated neutral.

Qualifying rows under the adopted rule: 3/6.

Result: FAIL.

That is not a discriminating test of R's update efficiency.

The setup should have preregistered one of:
- >=4/6 including a rule for 0/0;
- >=X% of **material-change** rows;
- or a two-part gate separating search-yield from representation-update cost.

It did not.

**Finding:** the maintenance FAIL cannot bear the strategic weight placed on it.

---

# 5. Critical attack X4 — update “atom” granularity suppresses compactness by construction

The static metric counts a `source/citation object` as one review atom.

In F, a new source object contains fields such as:
- title;
- author;
- year;
- URL/identifier;
- source role;
- evidence direction;
- locator.

In R, the corresponding source representation is a bare source link.

During all three material update shocks, the final metric reports:
- F = 2 atoms touched;
- R = 2 atoms touched.

Example conceptual accounting:
- F: one changed historical/coverage field + one **rich source object**;
- R: one changed compact field + one **URL**.

Calling both “2 atoms” is consistent with the frozen metric, but it does not demonstrate equal review work.

### Sensitivity illustration — not a protocol re-score

If source metadata scalars were counted individually:

Typical F update:
- 1 historical field;
- ~7 source metadata fields;
- total ~8 reviewable scalars.

Typical R update:
- 1 compact historical field;
- 1 source URL;
- total ~2.

Illustrative R/F ratio: ~25%.

That does **not** prove R is 75% cheaper in labour. It proves only that the maintenance result is highly sensitive to the atom unit.

The experiment therefore cannot use “2 vs 2” as strong evidence that compact and full forms cost the same to maintain.

---

# 6. Critical attack X5 — the experiment did not measure the dominant research cost

The central COV-002 question includes:

> research, review and update burden.

But the experiment explicitly avoids wall-clock claims and does not measure:
- historian search time;
- reading time;
- source-access effort;
- language effort;
- expert consultation;
- target identity validation time;
- bibliography reuse;
- duplicated source retrieval across cells.

It measures representation surface and local edits.

That was appropriate for a bounded artifact experiment.

It is insufficient to conclude **total corpus economics**.

In particular, the update packet's source search was performed once, then applied to F/R/M. The largest shared cost was deliberately outside the representation comparison.

**Finding:** “we did not demonstrate cheaper maintenance representation” is valid; “the corpus does not earn its research/maintenance cost” is not directly measured.

---

# 7. Attack X6 — row-by-row research is not necessarily the efficient systematic workflow

COV-002 researches each expansion row as an independent bounded packet.

A real systematic corpus can amortize work.

Examples:
- one specialist monograph can cover multiple adjacent polity/time cells;
- one global synthesis can populate direct/adjacent/none coverage judgments across many cells;
- one regional bibliography can support several targets;
- one upstream identity correction can repair multiple derived cells;
- source metadata can be stored once and referenced many times;
- experts can review batches rather than isolated rows.

COV-002 does not measure marginal cost under source-centric or region-centric batching.

This matters because “systematically researching history” implies a **research program**, not 1,000 independent copies of COV-002's one-row search ladder.

**Finding:** no long-run marginal cost curve was established.

---

# 8. Attack X2 — 37 rows are too few to infer the shape of a corpus network effect

The experiment grows 25→37 rows: +12 rows, or +48%.

That is enough to test whether a known effect immediately disappears.

It is not enough to establish whether value or cost behaves:
- linearly;
- sublinearly;
- superlinearly;
- with thresholds;
- with saturation.

The observed positive fact is actually important:
- 3/4 cross-cell reuse mechanisms still materially beat M at N=37;
- the advantage did not collapse.

That is evidence **for persistence of corpus value**.

The experiment contains no observation at N=100, 500, 1,000, etc., and no empirical scaling model.

**Finding:** COV-002 supports “value persists through 37,” not “value stops compounding beyond 37.”

---

# 9. Attack X7 — the value function was closed before scale could create new questions

T1–T6 were fixed from the mechanisms already discovered in COV-001.

This is excellent for preventing post-hoc success.

But it creates a blind spot when the hypothesis under attack is **reference-corpus value**.

Large reference corpora can support questions that are not meaningful at N=25:
- where do certain evidence gaps cluster geographically or chronologically?
- which historiographies repeatedly conflate network and territorial evidence?
- where do the global handbooks systematically lose direct coverage?
- which historical-geography sources show recurring identity/time defects?
- which terminology problems recur across unrelated source traditions?
- what combinations of law/practice/network evidence recur?

COV-002 intentionally does not allow emergent tasks to count.

Therefore it cannot estimate the **option value of future cross-corpus questions**.

This does not invalidate the fixed-task result. It limits its use as a verdict on comprehensive-reference value.

---

# 10. Attack X8 — “external use case first” risks recreating the bias the project was designed to resist

D-002's project rationale deliberately rejects letting unusually dense Atlantic/Western documentation dominate the project.

A rule saying:

> expand only when an external consumer, funded question or concrete use case pays for the curation

can create a parallel **demand-density bias**.

Likely external demand is not evenly distributed across:
- periods;
- languages;
- regions;
- literatures;
- archival accessibility;
- institutional funding.

The most documented and institutionally visible histories are also more likely to generate:
- funded projects;
- users;
- digitization;
- partnerships.

A coverage project driven only by external pulls can therefore reproduce the same imbalance the project's non-Atlantic-first rule was meant to counter.

Systematic sampling/completeness can have methodological value precisely because it **refuses demand-weighted selection**.

**Finding:** an external-trigger rule is not methodologically neutral.

---

# 11. Attack X9 — three “bad targets” are both cost and value

COV-002 surfaced:
- New Netherland at 1800;
- medieval Kingdom of Georgia at 1800;
- Western Regions protectorate at 500.

The final result counts these as evidence that scaling incurs target-validation cost.

Correct.

But systematic coverage also **discovered upstream errors that would otherwise remain latent**.

That is a corpus-quality function:
- broad validation finds defects;
- defects can propagate into maps, joins, derived datasets and historical claims;
- a systematic pass can improve the shared geographic/identity substrate.

The correct accounting is:
- target validation = cost;
- defect discovery = benefit.

COV-002 records the cost but never assigns value to defect discovery.

---

# 12. Attack X10 — negative controls do not argue against systematic coverage

COV-002 correctly shows:
- specialist narrative > index for deep interpretation;
- SlaveVoyages > index for voyage-level quantitative work;
- ordinary matrix competitive for a single row.

These are strong controls against **replacement claims**.

But a comprehensive index does not have to replace:
- monographs;
- specialist datasets;
- single-case research.

Its value can be:
- discovery;
- orientation;
- gap visibility;
- comparison;
- routing users to specialist sources.

The controls constrain the product claim; they do not discriminate the completeness thesis.

---

# 13. Attack X11 — maintenance strategy was assumed rather than varied

Historical evidence is not a live operational feed.

A defensible reference corpus can publish:
- versioned releases;
- “reviewed through” dates;
- immutable snapshots;
- scheduled rather than continuous refresh;
- issue queues for corrections;
- explicit stale/needs-review states.

COV-002 asks whether an update can be applied cheaply now.

It does not compare:
- continuous updating;
- annual/periodic releases;
- update-on-citation;
- update-on-research-use;
- frozen scholarly editions.

A systematic corpus can remain useful even when some rows are “as reviewed in 2026,” provided that provenance and review date are explicit.

**Finding:** failure to show cheap continuous maintenance is not equivalent to failure of a versioned reference-work model.

---

# 14. Attack X12 — “completeness” was not defined

There are at least four different completeness claims:

### C0 — target-frame completeness
Every target in a declared geography/time frame exists in the register, even if unresearched.

### C1 — research-coverage completeness
Every target has a status: unresearched / researched-inconclusive / supported / disputed / access-limited.

### C2 — source-direction completeness
Every researched target has at least a bounded bibliography/source direction and abstention.

### C3 — evidence completeness
Every target receives a deep, continuously maintained evidence packet.

COV-002 mostly attacks the economics of C2/C3-style rows.

The user-facing phrase “all known history” sounds like C0/C1/C2.

Those are not the same project.

A global C0/C1 register might be much cheaper and still deliver a large portion of the demonstrated gap/coverage value.

**Finding:** the rejected strategic object is underdefined.

---

# 15. External precedent — counterexamples to “no consumer, no broad data”

These do not prove this project should scale. They show the stop logic is not a general law of historical-data projects.

## Seshat: Global History Databank

Seshat explicitly exists to gather systematic historical information across societies so hypotheses can be tested comparatively. Its published methodology began with a stratified global sample and long time series rather than waiting for one consumer per society.

The Seshat architects also argued that as the databank grows, accumulated variables can make new questions cheaper because existing coded information can be reused.

Relevant:
- https://seshatdatabank.info/how-we-work
- https://www.digitalhumanities.org/dhq/vol/10/4/000272.html
- Turchin et al., *Cliodynamics* 6:1 (2015)

This is a direct countermodel to purely task-pull curation.

## Pleiades and World Historical Gazetteer

Pleiades operates as a continuously published scholarly reference work for ancient places, with stable identifiers and open bulk/API reuse.

As of June 2026, Pleiades reported 23,417 place resources with 43,556 inbound links from 21 external datasets/sites.

World Historical Gazetteer reports more than 2 million place records and over 70 datasets/collections, designed to improve discovery by connecting historical place information across time and language.

Relevant:
- https://pleiades.stoa.org/
- https://pleiades.stoa.org/help/linked-data-sidebar
- https://pleiades.stoa.org/news/blog/world-historical-gazetteer

The value here is partly **network/reuse value that emerges because the reference infrastructure exists at scale**.

## Enslaved.org / Journal of Slavery and Data Preservation

In this domain, JSDP explicitly treats curated slavery datasets as scholarly outputs and integrates them into Enslaved.org, a searchable repository intended for preservation and discovery.

An NEH award for Enslaved.org expansion described adding ten collections and increasing the linked-data platform toward approximately 1.3 million records, alongside stakeholder and sustainability work.

Relevant:
- https://ojs.msupress.org/index.php/JSDP
- https://awardsearch.neh.gov/AwardDetail.aspx?gn=PW-277479-21

This does not validate a global deep-time slavery ontology. It is evidence that **aggregation, preservation and discoverability themselves can be legitimate scholarly products**.

## SlaveVoyages

The COV negative control itself supplies a historical counterexample.

Voyage-level data were accumulated over decades; later scholars could reaggregate that broad corpus by route and decade to produce analyses not identical to the original data-entry purpose.

The lesson is not “copy SlaveVoyages globally.” It is that reference-corpus option value can emerge after sustained accumulation.

---

# 16. Attack the attack

A serious adversary must also attack the countercase.

## AA1 — precedent projects have institutions, funding and contributor networks

Correct.

Seshat, Pleiades, WHG and Enslaved.org are not evidence that one small project can sustainably reproduce their scale.

This preserves a strong resource/governance objection.

## AA2 — Seshat is hypothesis-driven, not completeness for completeness's sake

Correct.

Seshat is actually evidence against a naive “research everything” plan. It uses structured sampling and research programs.

This means the best countercase is **systematic coverage as research infrastructure**, not literal totality without a question.

## AA3 — Enslaved.org's scope is narrower and source-rich relative to global deep-time coercion

Correct.

Its existence does not remove the category/translation/temporal problems that make this project harder.

## AA4 — the compact register still requires historians

Correct.

No schema eliminates the intellectual cost of:
- interpreting categories;
- locating specialist scholarship;
- preserving disagreement;
- avoiding temporal back-projection.

## AA5 — broad coverage can become a graveyard of stale superficial rows

Correct.

A C0/C1/C2 coverage program needs:
- explicit review dates;
- provenance;
- release versions;
- “needs review” states;
- no pretense of completeness of evidence.

## AA6 — “completeness” can become a psychologically attractive but scientifically empty target

Correct.

Record count is not research progress.

The project should never use “we covered more cells” as the value metric.

### Attack-the-attack result

These objections defeat **unbounded completeness as a goal in itself**.

They do **not** restore the stronger COV-002 inference that systematic global coverage is currently shown not to be worth doing.

---

# 17. Final adversarial verdict

## Claim 1
> COV-002 does not justify another automatic row-by-row expansion using the current workflow.

**SURVIVES.**

## Claim 2
> The full F row should not be the default global representation.

**SURVIVES strongly.**

## Claim 3
> A compact coverage register is useful for cross-cell reasoning.

**SURVIVES strongly.**

## Claim 4
> COV-002 demonstrated that systematic comprehensive historical coverage is not economically justified.

**FAILS.**

COV-002 did not test the right object, scale or cost model for that conclusion.

## Claim 5
> “Completeness alone” is not enough to justify any global coverage program.

**TOO VAGUE TO ACCEPT.**

Literal evidence completeness is impossible and is a bad target.

But declared-frame target/research coverage (C0/C1), with explicit unknown/inconclusive states, can itself have methodological value:
- reduces demand-weighted selection;
- reveals gaps;
- enables future questions;
- exposes upstream data defects;
- improves discoverability.

---

# 18. Narrow correction

Replace the broad statement:

> “Systematically researching all known history purely in pursuit of completeness is not justified by the evidence we have.”

with:

> **COV-002 does not justify automatically extending the current row-by-row research workflow toward global completeness. It does not resolve whether a tiered, versioned, batch-curated global coverage register is worth building. That broader completeness thesis remains open.**

And replace:

> “Future substantive expansion requires a new external use case…”

with:

> **Future substantive expansion requires a new explicit value hypothesis and bounded cost model. An external consumer is one valid trigger, but a preregistered methodological objective such as bias-resistant systematic coverage may also be a valid trigger.**

This preserves the anti-momentum discipline while avoiding demand-density bias.

---

# 19. What a real completeness test would need to test

Do not immediately research hundreds of new cells.

First test the **architecture of completeness**.

A discriminating follow-up would compare:

1. **C0 target register** — target + validated identity/time + research state only.
2. **C1 compact coverage** — add bounded conclusion/abstention + source direction.
3. **C2 deep packet** — full F only for selected high-value/disputed cases.

It should then test:
- source-centric batch research across multiple cells;
- regional/synthesis reuse;
- fixed periodic release rather than continuous updating;
- cost per newly enabled query, not atom count alone;
- independent generation of *new* corpus-level questions after coverage expands;
- sampling bias under external-demand selection versus stratified systematic coverage;
- target-validation defect discovery as both cost and benefit.

Only that experiment could support a strong verdict on whether broad systematic coverage is worth pursuing.
