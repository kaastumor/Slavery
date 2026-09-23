# COV-002 — Maintenance-Shock Metrics

## Update accounting

| Row | F atoms touched | R atoms touched | M atoms touched | R/F | Downstream task state |
| --- | ---: | ---: | ---: | ---: | --- |
| COV2:1300:C | 2 | 2 | 2 | 100.0% | T6 source recovery |
| COV2:-500:A | 0 | 0 | 0 | neutral 0/0 | none |
| -500:E | 0 | 0 | 0 | neutral 0/0 | none |
| -500:A | 0 | 0 | 0 | neutral 0/0 | none |
| 1300:C | 2 | 2 | 2 | 100.0% | T6 source recovery |
| COV2:500:F | 2 | 2 | 1 | 100.0% | T3 handbook coverage, T6 source recovery |

### Strict preregistered maintenance-economy gate

- Material update rows: **3**
- No-change rows: **3**
- Material rows where R touched <=70% as many review atoms as F: **0/3**
- Required by protocol: **>=4/6 update rows**

**Result: FAIL.**

The three `0/0` searches are not counted as cost savings. Counting them as “R is cheaper” merely because neither representation changed would be mathematically convenient but experimentally misleading.

## Interpretation

Static compression remains strong: R is about 60% of F's review surface at N=37. But when genuinely new evidence changed a row, the compact register did **not** require materially fewer local conceptual edits than F in this small shock sample.

This means COV-002 has evidence for **smaller resting representation**, but not for **lower evidence-maintenance cost**.
