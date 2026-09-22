# Historical Slavery Atlas — Way of Working

## Default evidence loop

For consequential work use:

**Question → smallest useful proposal → adversarial attack → experiment/implementation → evidence → decision → sanitation → project-state reconciliation**

Do not substitute activity for progress.

## Adversarial dispositions

Every material adversarial finding receives exactly one disposition:

- **survives** — the proposal remains justified after a credible attack;
- **revise** — a real weakness changes the design;
- **reject** — the proposal is not justified;
- **park** — potentially useful, but not justified now;
- **experiment** — uncertainty is best resolved by a discriminating test.

An adversarial review that never changes anything is suspicious.

## Evidence classes

Keep epistemically different things explicit:

- **source evidence** — primary/source-native material;
- **specialist scholarship** — historical interpretation/synthesis;
- **deterministic observation** — reproducible code/database/GIS result;
- **statistical estimate** — quantified estimate with assumptions;
- **heuristic** — rule useful for operation but not historical fact;
- **model inference** — output from an AI/statistical model;
- **atlas interpretation** — reviewed project synthesis;
- **user/author assertion** — supplied claim not independently verified;
- **suggestion** — possible next step, not evidence.

Never silently promote one evidence class into another.

## Complexity rule

Use the smallest architecture that answers the current question.

A new dependency, service, database, queue, vector store, framework or provider needs a concrete failure of the simpler baseline recorded in the relevant issue/decision. Prefer existing repository capabilities first.

## Experiments

A non-trivial active experiment records:

- question;
- smallest discriminating test;
- strongest credible alternative;
- expected evidence;
- success signal;
- failure signal;
- state: **idea / active / survives / revise / reject / park**.

If an active experiment survives two Project Health Checks without new evidence, it must be accepted, rejected, parked, or given one concrete next discriminating test.

## Reproducibility contract

Once a run produces meaningful analytical/research output, it should be possible to identify, as applicable:

- source/data version;
- checksums;
- Git commit;
- tool/analyzer/model version;
- prompt/configuration version;
- parameters;
- ontology/methodology version;
- timestamp;
- output-schema version.

Do not build a separate experiment platform merely to satisfy this contract. Use Git, manifests, source-version records and existing audit tables until they demonstrably fail.

## Evaluation

Synthetic fixtures prove exact behavior. They do not prove historical usefulness.

Important changes should be evaluated against:
- synthetic known-behavior fixtures;
- independent/public real-world material when appropriate;
- the project's real data early enough to expose domain mismatch;
- the simpler baseline in the charter.

Where relevant test construct validity, perturbation behavior, temporal/spatial boundary behavior, source traceability, stability, and actual user value.

## Project Health Check

Run at meaningful gate/horizon boundaries and whenever a gate grows substantially beyond its expected scope.

A health check asks:
- Are we still serving the north star?
- What real value was demonstrated?
- Which assumptions changed?
- Which risks changed?
- Did complexity grow faster than capability?
- Is the backlog still the best next experiment?
- Are decisions/reproducibility/privacy current?
- Should we continue, redirect or stop?

Record decisions and deltas, not meeting transcripts.

## Governance deletion rule

Periodically attack the project-management system itself.

Delete or simplify governance that becomes duplicated, ceremonial, stale or more expensive than the failure it prevents. The repository-root `BACKLOG.md` remains the execution queue; GitHub issues hold durable task evidence; `docs/08_DECISIONS_LOG.md` remains the decision record. Do not create parallel systems.
