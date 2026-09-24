# EXP-04 — integrated adversarial review

Issue: #213. Scope: method/representation attack after all eight frozen cases.
Review type: internal adversarial pass by the same assistant, **not independent review**.

The attack target is not “is slavery real in these places?” It is narrower:

> Can D-089's portable contract preserve the distinctions exposed by the eight cases
> without silently strengthening claims, converting missing evidence into absence, or
> forcing unlike coerced-labour/status systems into one category?

## Attack 1 — one target outcome hides simultaneous dimensions

**Attack:** The Andaman case has a supported external colonial-captivity dimension and
an unassessed indigenous-internal-practice dimension. A single target-level outcome
could flatten those into either positive or unknown.

**Evidence:** The target row uses a compound bounded outcome, while
bounded_proposition, required_abstention, inference_extent and network_territorial_note
state the two dimensions separately.

**Disposition:** **SURVIVES, with boundary.**

For EXP-04's preservation test, the distinction remains explicit and recoverable. The
row does not force one territorial verdict. A future product requiring machine filtering
of each historical dimension independently might justify dimension-level structured
fields, but that is a query/interface requirement not demonstrated by this experiment.

**Consequence:** no contract extension now; make the Research Preview visually expose
the two dimensions rather than compressing the outcome to one color.

## Attack 2 — under_review is merely a disguised P0 / absence

**Attack:** Indus, Hadhramaut and Cuzco have no positive territorial conclusion. A
flat table may make “unassessed / under_review” look like no slavery.

**Evidence:** Each row carries a positive statement of what is known, an explicit
required abstention, coverage/access limits and a research_stage distinct from
research_outcome. Packets retain exact reopening triggers.

**Disposition:** **SURVIVES.**

The representation preserves unresolved research as a first-class state. It would fail
only if a consumer ignores those fields and maps missing/under-review to absence.

**Consequence:** the preview must render under-review/unresolved explicitly and must
not use an absence color for these rows.

## Attack 3 — historical terms are still being normalized through English prose

**Attack:** Even with category notes, labels such as slave, servant, captive,
dependent, yanacona, khñum, a-ru-a and gäbbar could be collapsed by the English
bounded proposition.

**Evidence:** Every difficult case required explicit historical_terms,
category_mapping_status/note and source-level claim_fitness. Positive outcomes were
narrowed when the original-language category was ambiguous.

**Disposition:** **SURVIVES provisionally.**

No case required one historical term to be assigned one universal modern category.
The contract preserved “text-specific mapping” and “mapping disputed/context-dependent.”

**Consequence:** the preview should show category notes on demand and never generate a
single normalized “slave type” field from these experimental rows.

## Attack 4 — source dependency is recorded but still double-counted rhetorically

**Attack:** A packet can list many sources while several are editions, translations or
interpretations of one artifact. Human readers may mistake source count for
corroboration.

**Evidence:** source_relations.csv explicitly records independence_group,
evidence_role, claim_fitness and dependency_note. The integrated audit identifies the
main repeated chains.

**Disposition:** **SURVIVES.**

The data preserves the dependency relation. Nothing in EXP-04 derives confidence or
prevalence from row counts.

**Consequence:** any preview source count must either use independence groups or avoid
presenting a count as evidentiary strength.

## Attack 5 — temporal anchors manufacture exactness

**Attack:** A map/table organized at 2000 BCE, 500 BCE, 900 CE, etc. can imply that all
evidence is exactly contemporaneous.

**Evidence:** Sumer explicitly separates late-Ur-III predecessor and Isin-Larsa
continuity; Hadhramaut preserves dating disagreement; Cuzco separates later imperial
evidence; Viking and Ethiopia use near-anchor predecessor/succeeding evidence; Angkor
uses 1186/1191 for the 1200 anchor.

**Disposition:** **SURVIVES.**

The temporal_state and packet notes preserve exact/near-anchor/transition distinctions.

**Consequence:** the Research Preview must display temporal precision/state next to the
selected anchor. A timeline point alone is not enough.

## Attack 6 — frame labels quietly become territorial claims

**Attack:** Terms such as Sumerian City-States, Indus, Viking, Andaman, Angkor and
Ethiopian Empire invite polygon filling even where the frame is aggregate, cultural,
networked, communal, nodal or politically fragmented.

**Evidence:** effective_frame_class and geometry notes distinguish polity aggregate,
civilization region, mobile network, region community, node/site and fragmented
sovereignty. No positive packet selected a practice polygon.

**Disposition:** **SURVIVES, visualization-critical.**

The portable contract preserves the difference, but an ordinary choropleth could still
destroy it.

**Consequence:** the preview must use neutral land and only bounded point/route/reference
geometry where defensible. No automatic polygon fill from target labels.

## Attack 7 — positive evidence is over-promoted to prevalence

**Attack:** Sumer, Angkor, Viking and Ethiopia are source-rich and could acquire a
stronger visual/intensity treatment than their evidence supports.

**Evidence:** each packet explicitly rejects archive counts, personnel totals, dirham
flows, traveler counts or citation counts as prevalence estimators. coverage_confidence
separates presence from prevalence/uniformity.

**Disposition:** **SURVIVES.**

No target result derives scale from documentation density.

**Consequence:** the preview may distinguish research/result state but must not rank or
shade positive cases by source volume.

## Attack 8 — Angkor still overstates slavery by translating temple personnel

**Attack:** The phrase “institutionalized unfree/slavery evidence” may inherit older
translations of khñum/personnel lists as slaves. Later Angkor scholarship explicitly
questions universal slave translations.

**Evidence:** The packet does not turn K.273/K.908 headcounts into slave totals and
uses Lustig/Lustig's broad inscriptional analysis to preserve heterogeneous status.
The bounded proposition says specific contexts support slavery/property status while
other personnel require broader dependency/labor labels.

**Disposition:** **SURVIVES after re-reading; no claim expansion needed.**

The positive proposition is institutional unfree/bonded labor with source-specific
slavery/property contexts, not “all temple personnel were slaves.”

**Consequence:** maintain that exact wording in any preview; do not shorten the result
to “Angkor: slavery — 12,640+ people.”

## Attack 9 — Ethiopia's nominal empire makes regional evidence look empire-wide

**Attack:** A target named Ethiopian Empire plus a positive result can visually imply
uniform 1800 imperial practice even though Zemene Mesafint sovereignty was fragmented.

**Evidence:** effective_frame_class is imperial_title_fragmented_sovereignty;
inference_extent and geometry notes reject uniformity and later borders.

**Disposition:** **SURVIVES.**

The distinction is representable; the main risk moves to presentation.

**Consequence:** no one solid 1800 empire polygon should be colored from these results.

## Attack 10 — method “success” is circular because the same assistant authored and reviewed

**Attack:** Internal authorship, source selection, synthesis and adversarial review can
all share the same blind spots. A clean packet may reflect self-consistency rather than
method validity.

**Evidence:** EXP-04 was ex-ante frozen before subject search, contains contrary cases
and retained unresolved outcomes instead of forcing success. But there is no
independent historical reviewer and no independent model review.

**Disposition:** **LIMITATION SURVIVES; does not falsify the internal portability test.**

The experiment can support an internal representation result, not independent
historical validation or external usefulness.

**Consequence:** final result must say “internal method success,” keep historical cases
at their actual review stage, and preserve the optional deeper-model/independent-review
boundary.

## Attack 11 — the flat format only works because difficult nuance is buried in prose

**Attack:** If every distinction survives only because long prose is stuffed into cells,
the “portable contract” has not actually demonstrated useful structure.

**Evidence:** Repeated distinctions map to stable fields: frame class; temporal state;
bounded proposition vs abstention; evidence locus vs inference extent; law/practice;
network/territorial; historical terms/category mapping; source role/claim fitness;
independence group; access limits; research stage; geometry role. Prose is used for
case-specific content, not to invent a new field for every case.

**Disposition:** **SURVIVES.**

The Andaman two-dimensional outcome is the closest pressure point. It remains
structured enough for preservation but should be tested in the preview before claiming
excellent query ergonomics.

**Consequence:** use the Research Preview as a presentation test: if ordinary map/table
cannot expose these distinctions without misleading compression, treat that as a new
representation failure rather than “fixing” it with hidden UI logic.

## Integrated result

No attack demonstrates a repeated material distinction that D-089 cannot preserve.

**Method/representation disposition: SUCCESS / PORTABLE CONTRACT SURVIVES EXP-04.**

This means:
- no D-089 extension is required by the eight frozen cases;
- the boring portable package remains viable;
- three historical cases remain under review;
- five internally researched cases retain their bounded conclusions;
- no canonical schema/data/publication decision follows automatically.

It does **not** mean:
- the eight histories have independent scholarly approval;
- the current fields are final for all future cases;
- a map/table can safely omit qualifiers;
- public value or adoption has been demonstrated.

## Focused deeper-reasoning handoff

A GPT-6 Astra medium-reasoning pass is warranted if available because the remaining
question is a subtle representation-failure question rather than routine evidence
collection:

> Red-team EXP-04's final claim that D-089 needs no extension. Look only for a
> material distinction in the eight frozen cases that the flat contract appears to
> preserve but actually loses or strengthens for a competent downstream reader or
> machine consumer. Pay special attention to Andaman's simultaneous external-positive/
> internal-unassessed state, Angkor's contested khñum mapping, Sumer's transition
> aggregate, and Ethiopia's fragmented sovereignty. Do not reward added complexity.
> Return survive, revise, or extension-required with the smallest concrete
> counterexample.

This optional pass is not required to continue to the already-authorized
non-canonical Research Preview.
