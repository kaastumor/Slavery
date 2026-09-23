# COV-004 Arm C — Historical Time-Split Result

**Cutoff:** 2015-12-31  
**Selected rows:** 6  
**Genuine accepted 2016–2026 evidence events:** **3/6**  
**Required:** >=2/6

| Target | Later event? | Class | Old -> new |
| --- | --- | --- | --- |
| Sabaeans | yes | changes_evidence_strength_and_qualifies | researched_inconclusive -> bounded_supported |
| Chámpa | yes | corroborates_and_qualifies | bounded_supported -> bounded_supported |
| Alodia | no | no_later_source_accepted | researched_inconclusive -> researched_inconclusive |
| Janapada of Aśmaka | no | no_later_source_accepted | researched_inconclusive -> researched_inconclusive |
| Cao | yes | corroborates_and_qualifies | researched_inconclusive -> researched_inconclusive |
| Janapada of Vatsa | no | no_later_source_accepted | researched_inconclusive -> researched_inconclusive |

## Result

**ARM C GATE: PASS.**

The point is not that every later source changes a classification.

- Sabaeans: later epigraphic scholarship materially changes the evidence state while adding terminology caution.
- Champa: later synthesis corroborates/qualifies without changing the bounded-supported outcome.
- Cao: later comparative scholarship improves regional context but correctly leaves the target-specific row inconclusive.
- Alodia, Aśmaka, Vatsa: no accepted later event in the bounded search.

All three genuine events are representable as **next-release row/source review tasks** without altering the immutable 2015-as-of snapshot.

No cross-cell query must silently mix 2015 and post-2015 states: query results must bind to a release/as-of state.

This is the first COV experiment to contain multiple real publication-time evidence updates rather than only same-day/no-change shocks.
