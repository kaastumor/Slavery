# COV-001 — Strongest Baseline Landscape

**Issue:** #148  
**Recorded:** 2026-09-23

This file defines the external resources the coverage-value experiment must beat or complement. It is intentionally subtractive: if an existing resource already solves the problem, the project should reuse or benchmark it rather than recreate it.

## 1. Cambridge World History of Slavery

Series:
https://www.cambridge.org/core/series/cambridge-world-history-of-slavery/23FA76D353956CE0B10BDAEAED4485B9

Observed role:
- four-volume scholarly survey;
- explicitly presents itself as surveying the history of slavery across the world from antiquity to the present;
- volumes are organized as specialist essays by period/region/theme;
- the medieval volume alone contains 23 specialist essays and explicitly addresses the relative neglect of medieval slavery.

**Disposition:** **benchmark**.

What it already does very well:
- authoritative global historical synthesis;
- specialist interpretation;
- thematic and chronological depth.

What COV-001 may test beyond it:
- explicit sampled place/time coverage state;
- machine/row-level visibility of gaps, uncertainty and source basis;
- repeated cross-cell retrieval without rereading many chapters.

The experiment may not claim value merely because Cambridge is narrative rather than tabular.

## 2. Palgrave Handbook of Global Slavery throughout History

Book:
https://link.springer.com/book/10.1007/978-3-031-13260-5

Observed role:
- open-access 2023 global/comparative handbook;
- 39 chapters;
- covers settings from ancient societies through the modern period;
- explicitly frames slavery as a global historical practice and encourages comparison.

**Disposition:** **benchmark / reuse**.

Why it is especially important:
- accessible without institutional subscription;
- strong regional entry points and bibliographies;
- already resembles a concise global starting index in narrative form.

COV-001 must demonstrate something beyond repackaging its table of contents.

## 3. Enslaved.org

Site:
https://enslaved.org/

Observed role:
- interconnected records of people, events, places and sources associated with historical slavery/slave trade;
- current site exposes hundreds of thousands of people/events and thousands of places/sources;
- data contribution is tied to the Journal of Slavery and Data Preservation;
- its stated dataset focus includes lives of enslaved Africans and descendants from fifteenth- to early-twentieth-century documentary material.

**Disposition:** **reuse / benchmark where in scope**.

It is a strong structured-data precedent, but it is not itself a deep-time all-societies territorial-practice coverage matrix.

## 4. SlaveVoyages

Site:
https://www.slavevoyages.org/

Observed role:
- mature structured databases centered on slaving voyages;
- trans-Atlantic and intra-American datasets have explicit methods, source records and imputed/documented distinctions;
- current site also exposes an Indian Ocean voyage category;
- the unit of analysis is fundamentally voyage/traffic oriented.

**Disposition:** **reuse / negative-control benchmark**.

COV-001 must never treat its voyage density as territorial prevalence. For questions inside SlaveVoyages' specialty, the specialized database should remain superior.

## 5. Ordinary specialist workflow

This is part of the baseline, not an inferior strawman:
- targeted specialist monographs/articles;
- source catalogues/editions;
- library/database/web search;
- citation manager or spreadsheet;
- static GIS when useful;
- strong general-purpose model;
- small scripts/notebooks.

**Disposition:** **benchmark**.

H2 already showed that a competent ordinary workflow can preserve many historical distinctions. COV-001 asks only whether **preassembled global coverage** adds a different kind of value.

## Baseline conclusion

There is no defensible claim that “nobody has made a global history of slavery.” Cambridge and Palgrave clearly have.

The unresolved niche is narrower:

> a systematic, auditable place/time **coverage index** that exposes what has been researched, what proposition is defensible, what remains uncertain, and where the major global syntheses do or do not provide direct coverage.

That niche is the object under test. It is not assumed to be valuable in advance.
