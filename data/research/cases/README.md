# Research Case Staging

This directory stores reviewable claim-centric research case specifications before database ingestion.

Rules:

- one bounded research case per JSON file where practical;
- preserve exact source/version identifiers and claim-specific evidence;
- cases here are **not published data**;
- validation uses `tools/add_research_case.py` in dry-run mode;
- database ingestion remains a separate action;
- publication remains a separate release gate;
- do not store copyrighted source assets here unless redistribution is permitted.

A file passing CI means that its structure and mandatory methodological fields validate. It does **not** mean that its historical interpretation, P-level or geometry has been editorially approved.
