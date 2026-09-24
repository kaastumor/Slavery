# EXP-05 adversarial review

Review type: internal same-operator/model attack. Not independent or blinded.

Assume the scoring conclusion is wrong:

> the portable package adds real task value, but the thin Atlas adds no material value
> beyond the package on the three frozen tasks.

## Attack 1 — the tasks are biased against a map

The three tasks emphasize temporal precision, scope, source dependency and category
mapping. Only T1/T2 have an obvious spatial component, and the current preview contains
navigation references rather than reviewed practice geometry.

A richer spatial task could make a map more useful.

**Response:** valid limitation, but it does not overturn the frozen result. EXP-05
tests the **current thin Atlas**, not a hypothetical richer geography product. Building
new geometry or a richer UI to create a task the current view could win would violate
the experiment. The result therefore says no **additional application investment is
earned yet**, not that maps are generally useless.

Disposition: **SURVIVES WITH NARROWER CLAIM.**

## Attack 2 — C is structurally downstream of B, so it cannot add information

The preview is an adapter over the portable package. It was never expected to invent
new historical facts.

**Response:** correct. The discriminating value available to C is reduced task burden,
better provenance recovery, safer comparison or a spatial insight. None reached the
preregistered material threshold. That is exactly the value question being tested.

Disposition: **SURVIVES.**

## Attack 3 — interaction count unfairly penalizes normal UI clicks

B's “two logical opens” hide substantial CSV scanning and joining, while C's six clicks
are cheap and visually guided. A human may prefer six clicks to reading raw CSV.

**Response:** this is the strongest measurement limitation. EXP-05 deliberately avoids
wall-clock claims because model/browser latency is noisy. Artifact/page count and
interaction count are crude proxies. C clearly has a readability/usability benefit,
also consistent with the sponsor's positive first glance.

But the material-advantage rule did not reward cosmetic readability alone. No task
showed a correctness, uncertainty or provenance result that B could not recover
directly. Therefore the experiment cannot claim that C is *worse UX*; it can only say
that C did not demonstrate a **material workflow advantage** under the frozen proxy.

Disposition: **SURVIVES WITH MEASUREMENT LIMIT.**

## Attack 4 — same-operator contamination creates a ceiling effect

The same model/operator saw lane A first, then B, then C. Knowledge from A could make
later lanes appear equally correct and suppress the chance for C to prevent mistakes.

**Response:** true. The frozen checklist prevents moving criteria, but it does not
create blindness. This weakens any strong claim about comparative error rates.

It does not explain the objective structural observation that B aligns the needed
fields in two artifacts and C exposes the same fields in target-detail UI. Nor can it
turn the sponsor's positive first-look feedback into external task evidence.

Disposition: **LIMITATION SURVIVES; NO INDEPENDENT-USER CLAIM.**

## Attack 5 — lane A is not a true external boring baseline

Lane A uses the project's own carefully written case packets and source table. A real
external researcher might instead use literature, notes, QGIS and a general model.

**Response:** correct. Lane A is a strong **internal boring representation baseline**,
not an end-to-end external research baseline. This makes EXP-05 a test of
representation/workflow value once evidence is already curated.

It cannot establish whether the corpus/method itself beats ordinary external research
for discovery. Earlier project evidence addressed that question only partially.

Disposition: **NARROW RESULT.**

## Attack 6 — source links integrated into C may be a material provenance gain

C puts source version, locator, claim fitness, independence family and dependency note
under the target, while B requires a target-id join across tables.

**Response:** this is a real presentation gain. The browser trace confirms it.

However, B exposes the same relationships explicitly with one source-table lookup,
and all three tasks recovered provenance correctly. C did not reduce the frozen
interaction proxy or recover otherwise-missed dependency. Under the preregistered
threshold, the gain is helpful but not material.

Disposition: **SURVIVES.**

## Attack 7 — sponsor first-look approval contradicts the no-value result

The sponsor said the live preview “looks (at first glance) great.”

**Response:** it does not contradict the experiment. That is positive lightweight
usability/readability evidence. EXP-05 asks a stricter question: whether the view
materially improves difficult comparative tasks over the portable package.

Both can be true:
- the preview is pleasant and useful to inspect;
- richer application investment is not yet justified.

Disposition: **SURVIVES.**

## Attack 8 — one new spatially dependent task could reverse the product conclusion

Yes. A future real task involving reviewed historical geometry, route comparison or
spatial intersection could provide a changed assumption and reopen the derived-view
question.

That is a valid reopening condition, not a reason to build speculative map features
now.

## Adversarial disposition

**SURVIVES, NARROWLY.**

The defensible conclusion is:

- portable package value is supported internally;
- current thin preview is a safe and useful inspection adapter;
- EXP-05 does **not** demonstrate material task advantage for the view over the package;
- therefore no richer application horizon is currently earned;
- do not infer that maps are useless, that users dislike the preview, or that external
  adoption is absent.

## Astra medium handoff

A deeper reasoning replay would be useful because task design and measurement are the
remaining weak points:

> Red-team EXP-05 without changing its preregistered criteria. Assume the conclusion
> “B materially beats A, while C adds no material task advantage beyond B” is wrong.
> Test whether the three frozen tasks, lane asymmetry, same-model contamination, and
> artifact/interaction effort proxy structurally bias against the thin map/table.
> Distinguish a true verdict reversal from a limitation that only narrows the claim.
> Return SURVIVE, REVISE, or VERDICT UNSUPPORTED with the smallest concrete
> counterexample.

This optional pass is not independent historical review and is not required to preserve
the internal EXP-05 result.
