# Historical Slavery Atlas web MVP

This is the first durable web client for the atlas.

## Architecture

- **Map client:** MapLibre GL JS
- **Build tool:** Vite
- **Language:** TypeScript
- **Research store:** PostgreSQL + PostGIS
- **Current API host:** Supabase Edge Function, configured through `VITE_ATLAS_API_URL`
- **Neutral land:** static GeoJSON
- **Current evidence delivery:** GeoJSON assembled from reviewed `atlas.*` records

The frontend is intentionally not coupled to Supabase. Replacing the API host should require changing the configured URL, not the map model.

The current endpoint is a **research preview** over reviewed records. It is not a canonical published data release. The production publication boundary remains the `publish` schema / release materialization described in the project architecture.

## Run

From `web/`:

1. install dependencies
2. start the Vite development server
3. optionally set `VITE_ATLAS_API_URL` to another compatible API

## MVP behavior

- neutral world land is always visible
- astronomical integer years are converted to BCE/CE labels in the UI
- time-bounded claims and geometries are resolved independently
- exact, specialist, approximate historical, modern proxy and unresolved geometry states remain explicit
- disputed classifications are visually distinct
- unresolved geometry remains visible in the evidence list rather than becoming map absence
- claim detail includes exact source-version links returned by the API
