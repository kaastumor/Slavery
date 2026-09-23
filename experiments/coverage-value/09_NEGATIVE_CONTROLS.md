# COV-001 — Negative Controls

**Issue:** #148

## N1 — deep specialist context

Deterministic selection rule:
SHA-256 of `COV-001-N1|cell_id`, lexicographically smallest eligible polity cell.

Selected:
- cell: **500:F**
- target: **Chámpa, c. 500 CE**
- digest: `0d53b7b558366b52e65ba40326310e369f3cabab01cb5b141147e0c894191968`
- first specialist secondary source in frozen row: Don J. Wyatt, *Slavery in East Asia*.

Frozen question:

> **Why is later medieval evidence of Cham enslavement insufficient to establish a slavery institution in Champa c. 500 CE, and what source limitations create that boundary?**

### Specialist narrative

Wyatt's specialist synthesis explains that medieval Vietnamese slavery is much better visible from the Đại Cồ Việt/Lý/Trần periods onward. It notes that Chams were frequently enslaved as regional outsiders/captives of war, while also stressing how little is known about the conditions of the earliest medieval slaves and even less about their precursors.

That source-history explanation matters. It distinguishes:
- evidence about **Chams enslaved in Vietnam** from evidence about **slavery inside Champa**;
- later medieval documentation from the c.500 anchor;
- absence of accessible early evidence from historical absence.

Source:
https://www.cambridge.org/core/books/slavery-in-east-asia/69CDDD5E84C9CC20EF4E67ECB832BD17

### Mini-index

The frozen index correctly says:
- later medieval evidence exists;
- it is centuries too late;
- it must not be back-projected to c.500.

But it does not reproduce the specialist narrative's historiographical explanation or wider Vietnamese source context.

**Control result: PASS. Specialist narrative > mini-index for the deep why/how question.**

This is desirable. The coverage corpus is not a replacement for specialist interpretation.

---

## N2 — specialized quantitative-data control

Frozen question:

> For trans-Atlantic voyages disembarking enslaved people in Jamaica between 1750 and 1800, what does SlaveVoyages allow a researcher to inspect or quantify that a global coverage index should not pretend to replace?

### SlaveVoyages capability

The Trans-Atlantic Slave Trade Database uses the voyage as a unit of analysis and exposes:
- voyage IDs;
- vessel and ownership fields;
- dates;
- embarkation/disembarkation places and regions;
- numbers embarked/disembarked;
- mortality;
- resistance/outcomes;
- source citations;
- documented versus imputed variables;
- searchable time/place filters;
- tabular, timeline, map and downloadable data/estimate outputs.

Its methodology explicitly distinguishes data variables from imputed variables, and the estimates interface supports date ranges and Jamaica as a disembarkation region.

Sources:
- https://legacy.slavevoyages.org/voyage/about
- https://legacy.slavevoyages.org/blog/variable-list
- https://legacy.slavevoyages.org/blog/methodology-trans-atlantic
- https://legacy.slavevoyages.org/assessment/estimates
- https://www.slavevoyages.org/documents/download/VoyagesGuide.pdf

### Mini-index capability

The COV-001 mini-index can say that:
- voyage/trade evidence is a distinct network layer;
- such evidence must not mechanically determine territorial prevalence;
- specialized structured data are relevant to some rows.

It cannot responsibly supply:
- voyage counts;
- route distributions;
- ship/owner records;
- embarkation/disembarkation estimates;
- documented/imputed voyage variables;
- detailed Jamaica 1750–1800 quantitative analysis.

**Control result: PASS. SlaveVoyages > mini-index for voyage-level and quantitative research.**

The control also confirms an important project invariant: voyage density is network evidence, not territorial-practice intensity.

## Negative-control gate

Both controls behave as preregistered:
- specialist narrative remains better at deep explanation;
- specialist database remains better at its quantitative unit of analysis.

The mini-index is useful only as a global coverage/navigation/synthesis layer.
