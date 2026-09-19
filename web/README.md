# Historical Slavery Atlas web MVP

This is the durable MapLibre web client for the atlas.

## Architecture

- **Map client:** MapLibre GL JS
- **Build tool:** Vite
- **Language:** TypeScript
- **Research store:** PostgreSQL + PostGIS
- **Current API host:** Supabase Edge Function, configured through `VITE_ATLAS_API_URL`
- **Neutral land:** static GeoJSON
- **Current evidence delivery:** explicit published release via `atlas-data`

The frontend is intentionally not coupled to Supabase. Replacing the API host should require changing the configured URL, not the map model.

## Hosting

The production MVP is a static Vite build deployed through GitHub Pages.

- source: `web/`
- build command: `npm run build`
- output: `web/dist`
- deployment workflow: `.github/workflows/deploy-pages.yml`

The Vite base is relative so the same artifact can be hosted at a GitHub Pages project path, a custom domain, Cloudflare Pages, Netlify, Vercel, or another ordinary static host without rebuilding the frontend architecture.

## Run locally

From `web/`:

1. `npm ci`
2. `npm run dev`
3. optionally set `VITE_ATLAS_API_URL` to another compatible API

## MVP behavior

- neutral world land is always visible
- astronomical integer years are converted to BCE/CE labels
- time-bounded claims and geometries are resolved independently
- P1–P4 affect territorial-practice intensity; source counts never do
- exact, specialist, approximate historical, modern proxy and unresolved geometry states remain explicit
- genuinely disputed classifications are visually distinct
- unresolved geometry remains visible in the evidence list rather than becoming map absence
- source evidence exposes support/challenge/qualification/context direction
- claim detail includes exact source-version links returned by the API
- release identity and canonical/non-canonical status are visible in the UI
