# COV-002 — Negative Controls

**Issue:** #151

## N1 — specialist depth

Deterministic selector:
`SHA-256("COV-002-N1|" + cell_id)`

Selected:
- **500:C — Alodia, 500 CE**
- digest: `0b60a0312b37c112c2e88b08675e0e81c0a09c8fb349a69b88ffe37888ed09ae`

Frozen question:

> Why does the known Alodian slave-sale evidence not establish slavery in Alodia at 500 CE, and what does the underlying source actually establish?

### Specialist source

Richard Holton Pierce, “A sale of an Alodian slave girl: A reexamination of papyrus Strassburg Inv. 1404,” *Symbolae Osloenses* 70 (1995), 148–166.  
DOI: https://doi.org/10.1080/00397679508590895

The article treats a papyrus dated to the late sixth century (with later scholarship proposing a still later date) as evidence about an African slave transaction/trade in Egypt and examines the possible role of Alodia/Makuria.

That is substantially later than the 500 CE anchor and is evidence of a bounded transaction/trade context, not proof that the sampled Alodian polity had the same condition at 500.

### Artifact comparison

F/R/M all correctly preserve the core abstention:
- target-specific source evidence postdates the anchor;
- it must not be back-projected.

But the specialist article provides the deeper legal/economic/source-history context that explains what the papyrus can and cannot bear.

**Result: PASS — specialist narrative > F/R/M for deep why/how interpretation.**

---

## N2 — specialized quantitative data

Reuse the fixed COV-001 capability question:

> For trans-Atlantic voyages disembarking enslaved people in Jamaica between 1750 and 1800, what does SlaveVoyages allow a researcher to inspect or quantify that the coverage corpus should not replace?

SlaveVoyages exposes voyage-level identifiers, vessels, routes, dates, embarkation/disembarkation, documented/imputed variables, persons/count estimates, mortality, resistance/outcomes, sources, filtering and downloads.

F/R/M are coverage artifacts. They can preserve the warning that voyage/network evidence is not territorial prevalence, but they cannot replace voyage-level quantitative analysis.

**Result: PASS — SlaveVoyages > F/R/M in its specialized unit of analysis.**

---

## N3 — single-cell reading

Deterministic selector:
`SHA-256("COV-002-N3|" + cell_id)`

Selected:
- **NP-02 — New Guinea Highlands, c. 1800 CE**
- digest: `27b4f6fd46c8c3716b495b08f5cac8e80734b2189640ff6612fe973d38e42e55`

Frozen question:

> What can we responsibly say about slavery in this sampled context at c.1800?

M already contains:
- `researched_inconclusive`;
- the bounded conclusion that later ethnography documents warfare/captivity but does not establish slavery at c.1800;
- the caveat not to back-project twentieth-century ethnography or equate captive incorporation with slavery;
- the source citation.

F/R add explicit coverage and access fields, but those do not materially improve this single-cell answer.

**Result: PASS — ordinary matrix M is competitive for a single-cell reading.**

## Negative-control gate

All three controls behave as expected:
- specialist scholarship remains superior for deep interpretation;
- specialized data remain superior for quantitative voyage research;
- a competent ordinary matrix remains competitive for simple single-cell use.

This constrains the corpus's value to repeated cross-cell coverage/retrieval tasks.
