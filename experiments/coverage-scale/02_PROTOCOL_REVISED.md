# COV-002 — Revised Protocol After Setup Adversary

**Issue:** #151  
**Setup adversary:** `01_SETUP_ADVERSARY.md`  
**State:** cleared for sample freeze; historical research not yet started

## Experiment target

Test whether COV-001's value:
1. remains reusable as the corpus grows from 25→31→37 rows;
2. can be preserved in a smaller compact register;
3. remains maintainable under six bounded evidence updates.

The experiment is about **artifact form and reuse economics**, not world-history representativeness.

## Artifacts

### F — full row
Use the COV-001 detailed row schema.

### R — compact register
Fields:
- cell ID;
- target/year;
- research outcome;
- bounded conclusion;
- required abstention;
- law/practice divergence;
- network/territorial warning;
- Cambridge coverage;
- Palgrave coverage;
- unresolved/gap reason;
- source links;
- access/language warning.

### M — strongest ordinary matrix
Fields:
- cell ID;
- target/year;
- research status;
- concise conclusion;
- caveat/notes;
- citations.

M is intentionally competent and is allowed to retain a status column.

## Expansion sample

Add 12 deterministic rank-2 polity cells from the original COV-001 strata.

Exact upstream source:
- Cliopatria commit `ad28a691b7c07c1fca89d0e0636d324667d2a258`
- SHA-256 `d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370`

Selection:
1. reproduce COV-001 eligibility/ranking;
2. keep strata with >=2 eligible candidates;
3. rank strata by SHA-256 `COV-002-STRATUM|cell_id`;
4. take first 12;
5. select candidate rank 2 in each;
6. freeze before slavery/coercion research.

If fewer than 12 valid expansion cells are produced, stop and revise.

## Research

Research only the 12 frozen expansion cells.

Use COV-001 source ladder/budget and outcome states.

Do not improve COV-001 rows except during the later deterministic update shock.

## Reuse tests

Run T1–T6 from the preregistered protocol at:
- N=25;
- N=31;
- N=37.

Evaluate F, R and M.

Record:
- direct / traceable / reconstructive / unavailable / misleading;
- rows inspected;
- notes/fields interpreted;
- external source openings;
- manual classifications needed.

T5 bounded overview is treated as a likely parity control.

## Review-surface proxy

For each representation, per row count:
- populated reviewable scalar/narrative fields;
- citation/source objects;
- manually distinct notes;
- duplicated propositions.

Also record the number of distinct concepts a reviewer must understand.

Do not translate this to hours.

## Information-loss audit

For each new row, compare F→R.

Every omitted F field is classified:
- duplicated;
- unused by demonstrated tasks;
- potentially safety-critical;
- uniquely valuable.

Compression fails if R omits a safety-critical boundary without an equivalent representation.

## Maintenance shock

After N=37 freeze:

1. deterministically select six rows by SHA-256 `COV-002-UPDATE|cell_id`;
2. freeze selected row IDs;
3. for each row execute one bounded query:
   `<exact target> <anchor period> slavery slave unfree dependency`;
4. accept the first credible genuinely new specialist source materially addressing the target;
5. if none appears in the bounded search, record `no_source_found`;
6. freeze the update packet;
7. apply it independently to F/R/M.

Record:
- row atoms touched;
- citations touched;
- concepts revisited;
- downstream tasks stale;
- whether update is local;
- handbook/source-version staleness.

## Negative controls

- N1 specialist depth;
- N2 specialized quantitative data;
- N3 single-cell reading where M should remain competitive.

## Gates

### R retains value if
- R matches F on >=5/6 tasks at N=37;
- no critical task becomes misleading;
- T1–T4 source recovery stays direct/traceable.

### R is materially smaller if
- median review atoms/row <=70% F;
- total review atoms at N=37 <=70% F;
- in >=4/6 maintenance shocks, R touches <=70% of F review atoms;
- no dropped field forces extra general research.

### Scale value survives if
- at least 3/4 of T1–T4 materially beat M at N=37;
- the advantage does not shrink from N=25→37 on >1 task;
- M's rereading burden materially grows with N while F/R remain direct;
- updates do not create widespread stale/contradictory outputs.

### Outcome
- **STOP** — no compounding value;
- **REDIRECT** — compact register keeps value with materially lower review surface;
- **NARROW SUSTAIN** — full row earns its extra complexity on >=2 independent correctness/provenance/uncertainty gains.

No outcome creates an Atlas product horizon or automatic corpus expansion.
