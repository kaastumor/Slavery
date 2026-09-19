# atlas-web deployment adapter

Temporary static delivery adapter for the real `web/` MapLibre MVP.

This function exists only so the current frontend can be made publicly reachable without introducing another application framework or waiting for an external hosting account to be connected. It serves:

- HTML shell
- browser JavaScript
- CSS
- neutral world-land GeoJSON

The frontend still consumes the release-gated `atlas-data` API and uses MapLibre GL JS 6.10.0.

**Architectural boundary:** this function is hosting/delivery plumbing, not the canonical frontend source. Product development belongs in `web/`. When a normal static host (for example Vercel) is connected, deploy `web/` and retire this adapter.
