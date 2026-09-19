import { Map, NavigationControl, type GeoJSONSource, type MapGeoJSONFeature, type MapMouseEvent } from "maplibre-gl";
import type { Feature, FeatureCollection, Geometry } from "geojson";
import "maplibre-gl/dist/maplibre-gl.css";
import "./styles.css";

type SourceRef = {
  title: string;
  author_or_institution: string | null;
  source_type: string | null;
  source_classification: string | null;
  version_label: string | null;
  url: string | null;
  direction: "supports" | "challenges" | "qualifies" | "context" | string;
  locator: string | null;
};

type Claim = {
  claim_id: string;
  from_year: number | null;
  to_year: number | null;
  summary: string;
  review_status: string;
  publication_status: string;
  practice_type: string;
  practice_level: "P0" | "P1" | "P2" | "P3" | "P4" | null;
  coverage_state: string;
  classification_status: string | null;
  sources: SourceRef[];
};

type GeometryRecord = {
  geometry_id: string;
  from_year: number | null;
  to_year: number | null;
  accuracy_status: "exact" | "specialist" | "approximate_historical" | "modern_proxy" | "unresolved";
  resolution_method: string;
  source_native_id: string | null;
  geometry: Geometry | null;
  source_title: string | null;
  source_version: string | null;
  source_url: string | null;
};

type Place = {
  spatial_entity_id: string;
  name: string;
  display_name: string | null;
  entity_type_code: string;
  notes: string | null;
  claims: Claim[];
  geometries: GeometryRecord[];
};

type ApiResponse = {
  status: string;
  release_version: string;
  schema_version: string;
  canonical: boolean;
  data_boundary: string;
  date_model: string;
  places: Place[];
};

const API_URL =
  import.meta.env.VITE_ATLAS_API_URL ??
  "https://dilnayfllygkplsdymel.supabase.co/functions/v1/atlas-data";

const panel = document.querySelector<HTMLElement>("#panel")!;
const status = document.querySelector<HTMLElement>("#status")!;
const slider = document.querySelector<HTMLInputElement>("#year")!;
const yearLabel = document.querySelector<HTMLOutputElement>("#year-label")!;
const timelineRange = document.querySelector<HTMLElement>("#timeline-range")!;
const releaseBadge = document.querySelector<HTMLElement>("#release-badge")!;
const mapFallback = document.querySelector<HTMLImageElement>("#map-fallback")!;
const mapWarning = document.querySelector<HTMLElement>("#map-warning")!;

const map = new Map({
  container: "map",
  style: {
    version: 8,
    sources: {},
    layers: [{ id: "background", type: "background", paint: { "background-color": "rgba(0,0,0,0)" } }],
  },
  center: [15, 24],
  zoom: 1.35,
  minZoom: 1,
  maxZoom: 8,
});

map.addControl(new NavigationControl({ showCompass: false }), "top-left");

map.on("error", (event) => {
  console.error("MapLibre error", event.error);
  mapWarning.hidden = false;
});

let places: Place[] = [];
let selectedPlaceId: string | null = null;
let release: ApiResponse | null = null;

function activeInYear(fromYear: number | null, toYear: number | null, year: number): boolean {
  return (fromYear === null || year >= fromYear) && (toYear === null || year <= toYear);
}

function formatYear(year: number): string {
  return year <= 0 ? `${1 - year} BCE` : `${year} CE`;
}

function formatInterval(fromYear: number | null, toYear: number | null): string {
  const from = fromYear === null ? "unknown start" : formatYear(fromYear);
  const to = toYear === null ? "open-ended" : formatYear(toYear);
  return from === to ? from : `${from}–${to}`;
}

function escapeHtml(value: unknown): string {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;",
  })[char]!);
}

function readable(value: string): string {
  return value.replaceAll("_", " ");
}

function activeClaims(place: Place, year: number): Claim[] {
  return place.claims.filter((claim) => activeInYear(claim.from_year, claim.to_year, year));
}

function geometryForYear(place: Place, year: number): GeometryRecord | null {
  return place.geometries.find(
    (geometry) => geometry.geometry !== null && activeInYear(geometry.from_year, geometry.to_year, year),
  ) ?? null;
}

function unresolvedGeometryForYear(place: Place, year: number): GeometryRecord | null {
  return place.geometries.find(
    (geometry) =>
      geometry.accuracy_status === "unresolved" &&
      activeInYear(geometry.from_year, geometry.to_year, year),
  ) ?? null;
}

function highestPracticeLevel(claims: Claim[]): number {
  return claims.reduce((max, claim) => {
    if (!claim.practice_level) return max;
    return Math.max(max, Number(claim.practice_level.slice(1)));
  }, 0);
}

function featureState(claims: Claim[]): "supported" | "disputed" | "inactive" {
  if (claims.length === 0) return "inactive";
  return claims.some((claim) => claim.coverage_state !== "disputed") ? "supported" : "disputed";
}

function buildEvidenceCollections(year: number): { polygons: FeatureCollection; points: FeatureCollection } {
  const polygons: Feature[] = [];
  const points: Feature[] = [];

  for (const place of places) {
    const geometry = geometryForYear(place, year);
    if (!geometry?.geometry) continue;

    const claims = activeClaims(place, year);
    const feature: Feature = {
      type: "Feature",
      geometry: geometry.geometry,
      properties: {
        spatial_entity_id: place.spatial_entity_id,
        name: place.display_name || place.name,
        state: featureState(claims),
        p_level: highestPracticeLevel(claims),
        geometry_accuracy: geometry.accuracy_status,
      },
    };

    if (geometry.geometry.type === "Polygon" || geometry.geometry.type === "MultiPolygon") {
      polygons.push(feature);
    } else if (geometry.geometry.type === "Point" || geometry.geometry.type === "MultiPoint") {
      points.push(feature);
    }
  }

  return {
    polygons: { type: "FeatureCollection", features: polygons },
    points: { type: "FeatureCollection", features: points },
  };
}

function directionBadge(direction: string): string {
  const safe = ["supports", "challenges", "qualifies", "context"].includes(direction) ? direction : "context";
  return `<span class="badge ${safe}">${escapeHtml(direction)}</span>`;
}

function claimHtml(claim: Claim): string {
  const sources = claim.sources.length
    ? `<ul class="source-list">${claim.sources.map((source) => {
        const title = escapeHtml(source.title);
        const locator = source.locator ? ` · ${escapeHtml(source.locator)}` : "";
        const author = source.author_or_institution
          ? `<div class="meta source-meta">${escapeHtml(source.author_or_institution)}${locator}</div>`
          : locator
            ? `<div class="meta source-meta">${locator.slice(3)}</div>`
            : "";
        const link = source.url
          ? `<a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${title}</a>`
          : title;
        return `<li>${directionBadge(source.direction)} ${link}${author}</li>`;
      }).join("")}</ul>`
    : `<p class="meta">No claim-source link returned.</p>`;

  return `
    <article class="claim">
      <div class="claim-title-row">
        <h3>${escapeHtml(readable(claim.practice_type))}</h3>
        <span class="practice-level">${escapeHtml(claim.practice_level ?? "P-level unassigned")}</span>
      </div>
      <div class="badges">
        <span class="badge ${claim.coverage_state === "disputed" ? "disputed" : ""}">${escapeHtml(readable(claim.coverage_state))}</span>
        ${claim.classification_status ? `<span class="badge">${escapeHtml(readable(claim.classification_status))}</span>` : ""}
      </div>
      <p class="meta">${formatInterval(claim.from_year, claim.to_year)}</p>
      <p>${escapeHtml(claim.summary)}</p>
      <strong>Evidence package</strong>
      ${sources}
    </article>
  `;
}

function renderPlace(place: Place, year: number): void {
  selectedPlaceId = place.spatial_entity_id;
  const claims = activeClaims(place, year);
  const geometry = geometryForYear(place, year);
  const unresolved = unresolvedGeometryForYear(place, year);

  const geometrySource = geometry?.source_title
    ? geometry.source_url
      ? `<a href="${escapeHtml(geometry.source_url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(geometry.source_title)}</a>`
      : escapeHtml(geometry.source_title)
    : "";

  panel.innerHTML = `
    <button id="back-overview" class="back-button" type="button">← Year overview</button>
    <h2>${escapeHtml(place.display_name || place.name)}</h2>
    <div class="badges">
      <span class="badge">${escapeHtml(readable(place.entity_type_code))}</span>
      <span class="badge ${!geometry ? "disputed" : ""}">
        geometry: ${escapeHtml(readable(geometry?.accuracy_status ?? unresolved?.accuracy_status ?? "not resolved for year"))}
      </span>
    </div>
    <p class="meta">Selected year: <strong>${formatYear(year)}</strong></p>
    ${place.notes ? `<p class="meta">${escapeHtml(place.notes)}</p>` : ""}
    ${claims.length
      ? claims.map(claimHtml).join("")
      : `<div class="empty-state">No published territorial-practice claim is active here in ${formatYear(year)}.</div>`}
    <div class="geometry-note">
      <strong>Historical geometry</strong><br />
      ${escapeHtml(
        geometry?.resolution_method ??
        unresolved?.resolution_method ??
        "No defensible geometry has been attached for this place/year. This is not evidence of absence.",
      )}
      ${geometrySource ? `<br /><span class="meta">Source: ${geometrySource}</span>` : ""}
    </div>
  `;

  document.querySelector<HTMLButtonElement>("#back-overview")?.addEventListener("click", () => renderOverview(year));
}

function renderOverview(year: number): void {
  selectedPlaceId = null;
  const active = places
    .map((place) => ({ place, claims: activeClaims(place, year), geometry: geometryForYear(place, year) }))
    .filter(({ claims }) => claims.length > 0);

  const unresolvedCount = active.filter(({ geometry }) => geometry === null).length;
  const activeClaimCount = active.reduce((total, item) => total + item.claims.length, 0);

  const list = active.length
    ? active.map(({ place, claims, geometry }) => {
        const level = highestPracticeLevel(claims);
        const label = claims.map((claim) =>
          `${readable(claim.practice_type)}${claim.coverage_state === "disputed" ? " — disputed" : ""}`
        ).join(" · ");
        return `<button class="place-button" data-place-id="${escapeHtml(place.spatial_entity_id)}">
          <span class="row">
            <strong>${escapeHtml(place.display_name || place.name)}</strong>
            <span class="meta">${level ? `P${level}` : "—"}</span>
          </span>
          <span class="meta">${escapeHtml(label)}${geometry ? "" : " · geometry unresolved"}</span>
        </button>`;
      }).join("")
    : `<div class="empty-state">No published territorial-practice evidence is active in this release for ${formatYear(year)}.</div>`;

  panel.innerHTML = `
    <h2>${formatYear(year)}</h2>
    <div class="summary-lead">
      <strong>${active.length}</strong> place${active.length === 1 ? "" : "s"} ·
      <strong>${activeClaimCount}</strong> active claim${activeClaimCount === 1 ? "" : "s"}
      ${unresolvedCount ? ` · <strong>${unresolvedCount}</strong> unresolved map target${unresolvedCount === 1 ? "" : "s"}` : ""}
    </div>
    <p class="meta">
      This map shows published territorial-practice evidence only. Missing evidence remains unknown; it is never rendered as historical absence.
    </p>
    <div id="place-list">${list}</div>
    <div class="release-note">
      <strong>Release boundary</strong><br />
      ${release
        ? `${escapeHtml(release.release_version)} · schema ${escapeHtml(release.schema_version)} · ${release.canonical ? "canonical release" : "non-canonical research preview"}`
        : "Loading release metadata…"}
    </div>
  `;

  panel.querySelectorAll<HTMLButtonElement>("[data-place-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const place = places.find((candidate) => candidate.spatial_entity_id === button.dataset.placeId);
      if (place) renderPlace(place, year);
    });
  });
}

function updateMap(year: number): void {
  yearLabel.value = formatYear(year);
  yearLabel.textContent = formatYear(year);

  const collections = buildEvidenceCollections(year);
  const polygonSource = map.getSource("evidence-polygons") as GeoJSONSource | undefined;
  const pointSource = map.getSource("evidence-points") as GeoJSONSource | undefined;
  polygonSource?.setData(collections.polygons);
  pointSource?.setData(collections.points);

  const activePlaceCount = places.filter((place) => activeClaims(place, year).length > 0).length;
  const activeClaimCount = places.reduce((count, place) => count + activeClaims(place, year).length, 0);
  status.textContent = `${activeClaimCount} active claim${activeClaimCount === 1 ? "" : "s"} · ${activePlaceCount} place${activePlaceCount === 1 ? "" : "s"}`;

  if (selectedPlaceId) {
    const selected = places.find((place) => place.spatial_entity_id === selectedPlaceId);
    if (selected) renderPlace(selected, year);
    else renderOverview(year);
  } else {
    renderOverview(year);
  }
}

function currentYear(): number {
  return Number(slider.value);
}

function pickFeature(event: MapMouseEvent & { features?: MapGeoJSONFeature[] }): void {
  const feature = event.features?.[0];
  const id = feature?.properties?.spatial_entity_id as string | undefined;
  if (!id) return;
  const place = places.find((candidate) => candidate.spatial_entity_id === id);
  if (place) renderPlace(place, currentYear());
}

async function boot(): Promise<void> {
  try {
    const [apiResponse] = await Promise.all([
      fetch(API_URL).then(async (response) => {
        if (!response.ok) throw new Error(`Atlas API returned ${response.status}`);
        return (await response.json()) as ApiResponse;
      }),
      new Promise<void>((resolve) => map.once("load", () => resolve())),
    ]);

    release = apiResponse;
    places = apiResponse.places;
    releaseBadge.textContent = `${apiResponse.release_version}${apiResponse.canonical ? "" : " · preview"}`;
    releaseBadge.classList.toggle("preview", !apiResponse.canonical);
    releaseBadge.title = `Schema ${apiResponse.schema_version} · ${apiResponse.data_boundary}`;

    const years = places.flatMap((place) =>
      place.claims.flatMap((claim) =>
        [claim.from_year, claim.to_year].filter((year): year is number => year !== null),
      ),
    );
    if (years.length === 0) throw new Error("Published release contains no dated claims");

    const minYear = Math.min(...years);
    const maxYear = Math.max(...years);
    slider.min = String(minYear);
    slider.max = String(maxYear);
    slider.value = String(-499 >= minYear && -499 <= maxYear ? -499 : maxYear);
    timelineRange.innerHTML = `<span>${formatYear(minYear)}</span><span>${formatYear(maxYear)}</span>`;

    map.addSource("land", { type: "geojson", data: `${import.meta.env.BASE_URL}world-land.geojson` });
    map.once("idle", () => {
      if (map.isSourceLoaded("land")) {
        mapFallback.classList.add("loaded");
        mapWarning.hidden = true;
      }
    });
    map.addLayer({
      id: "land-fill",
      type: "fill",
      source: "land",
      paint: { "fill-color": "#e8dfd2", "fill-opacity": 1 },
    });
    map.addLayer({
      id: "land-line",
      type: "line",
      source: "land",
      paint: { "line-color": "#626762", "line-width": 0.95 },
    });

    const initialCollections = buildEvidenceCollections(currentYear());

    map.addSource("evidence-polygons", { type: "geojson", data: initialCollections.polygons });
    map.addLayer({
      id: "evidence-polygons",
      type: "fill",
      source: "evidence-polygons",
      paint: {
        "fill-color": [
          "match", ["get", "state"],
          "supported", "#9e493f",
          "disputed", "#c18a31",
          "#b8b7b2",
        ],
        "fill-opacity": [
          "case",
          ["==", ["get", "state"], "inactive"], 0.10,
          ["==", ["get", "state"], "disputed"], 0.55,
          ["match", ["get", "p_level"], 4, 0.72, 3, 0.58, 2, 0.44, 1, 0.30, 0.42],
        ],
        "fill-outline-color": "#4b302c",
      },
    });

    map.addSource("evidence-points", { type: "geojson", data: initialCollections.points });
    map.addLayer({
      id: "evidence-points",
      type: "circle",
      source: "evidence-points",
      paint: {
        "circle-radius": 9,
        "circle-color": [
          "match", ["get", "state"],
          "supported", "#9e493f",
          "disputed", "#c18a31",
          "#b8b7b2",
        ],
        "circle-opacity": ["case", ["==", ["get", "state"], "inactive"], 0.25, 0.92],
        "circle-stroke-width": 2.5,
        "circle-stroke-color": "#fffaf1",
      },
    });

    map.on("click", "evidence-polygons", pickFeature);
    map.on("click", "evidence-points", pickFeature);
    for (const layer of ["evidence-polygons", "evidence-points"]) {
      map.on("mouseenter", layer, () => { map.getCanvas().style.cursor = "pointer"; });
      map.on("mouseleave", layer, () => { map.getCanvas().style.cursor = ""; });
    }

    map.on("idle", () => {
      const currentClaims = places.reduce((count, place) => count + activeClaims(place, currentYear()).length, 0);
      if (currentClaims === 0) return;

      const sourceFeatureCount =
        map.querySourceFeatures("evidence-polygons").length +
        map.querySourceFeatures("evidence-points").length;

      const renderedFeatureCount = map.queryRenderedFeatures().filter((feature) =>
        feature.layer.id === "evidence-polygons" || feature.layer.id === "evidence-points"
      ).length;

      if (sourceFeatureCount > 0 && renderedFeatureCount === 0) {
        mapWarning.textContent =
          `Evidence loaded (${sourceFeatureCount} map feature${sourceFeatureCount === 1 ? "" : "s"}) but the browser rendered none. The side panel remains authoritative.`;
        mapWarning.hidden = false;
      } else if (renderedFeatureCount > 0) {
        mapWarning.hidden = true;
      }
    });

    slider.addEventListener("input", () => updateMap(currentYear()));
    updateMap(currentYear());
  } catch (error) {
    console.error(error);
    releaseBadge.textContent = "Load error";
    status.textContent = "Failed to load atlas data";
    panel.innerHTML = `<h2>Could not load the atlas</h2><p>${escapeHtml(error instanceof Error ? error.message : error)}</p>`;
  }
}

void boot();
