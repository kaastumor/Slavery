# COV-003 — Batch Source-Reuse Metrics

## Row-centric baseline: COV-002 expansion

- rows: 12
- cell-source links: 20
- unique sources: 20
- source-reuse factor: **1.00**
- repeated URLs: none

## COV-003 C1

- rows: 12
- cell-source links: **22**
- unique materially used sources: **10**
- source-reuse factor: **2.20**
- ratio to COV-002 baseline: **2.20x**
- target-specific follow-up searches: **12/12**

### Batch criterion

- **-500:F:** CN-YATES-2001 materially informs 4/4; CN-SCHEIDEL-2017 materially informs 4/4
- **1300:E:** no shared source materially informs >=3/4 C1 cells
- **-500:E:** IN-CHANANA-1960 materially informs 4/4; IN-KALB-2023 materially informs 4/4

## Strong batch-economy gate

1. reuse factor >=1.35x baseline: **PASS**
2. >=2/3 batches have a shared source informing >=3/4: **PASS**
3. <=9/12 targets require target-specific follow-up: **FAIL (12/12)**
4. no conclusion broadened merely to increase reuse: **PASS**

**Strong batch-economy gate: FAIL.**

The architecture nevertheless demonstrates real source reuse in the two coherent batches. The heterogeneous 1300:E batch correctly fails to manufacture a shared source.
