# Reconciliation candidate proof

This experiment models how OpenRefine/WHG-style reconciliation results should enter the atlas workflow.

The core rule is simple:

> A reconciliation score is a candidate ranking, not a historical identity decision.

Even a service-reported perfect/high-confidence match remains `unreviewed` until a human/research review accepts it.

The proof preserves:

- raw source-native text;
- reconciliation service/namespace;
- query context such as period or place type;
- every returned candidate;
- scores as service-native values;
- explicit review judgment;
- reviewer and review note when accepted/rejected.

A place identity match never determines historical jurisdiction or atlas geometry automatically.
