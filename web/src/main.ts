import {
  LngLatBounds,
  Map,
  NavigationControl,
  Popup,
  setWorkerUrl,
  type GeoJSONSource,
  type MapGeoJSONFeature,
  type MapMouseEvent,
} from "maplibre-gl";
import type { Feature, FeatureCollection, Geometry } from "geojson";
import "maplibre-gl/dist/maplibre-gl.css";
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url";
import "./styles.css";

setWorkerUrl(workerUrl);

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
  render_transform?: "land_clip" | "source_geometry" | "none" | string;
  render_land_mask_id?: string | null;
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

type CartographyFabric = {
  fabric_id: string;
  source_name: string;
  source_version: string;
  source_url: string;
  source_commit_sha: string;
  source_blob_sha: string;
  content_md5: string;
  content_sha256: string;
};

type ApiResponse = {
  status: string;
  release_version: string;
  schema_version: string;
  canonical: boolean;
  data_boundary: string;
  date_model: string;
  cartography: CartographyFabric | null;
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
const mapWarning = document.querySelector<HTMLElement>("#map-warning")!;
const fitActiveButton = document.querySelector<HTMLButtonElement>("#fit-active")!;
const fitWorldButton = document.querySelector<HTMLButtonElement>("#fit-world")!;

const map = new Map({
  container: "map",
  style: {
    version: 8,
    sources: {},
    layers: [{ id: "background", type: "background", paint: { "background-color": "#cfdcdf" } }],
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

const hoverPopup = new Popup({
  closeButton: false,
  closeOnClick: false,
  offset: 10,
});

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
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[char]!);
}

function labelize(value: string): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
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

function featureState(claims: Claim[]): "supported" | "disputed" {
  return claims.some((claim) => claim.coverage_state !== "disputed") ? "supported" : "disputed";
}

function buildEvidenceCollections(year: number): { polygons: FeatureCollection; points: FeatureCollection } {
  const polygons: Feature[] = [];
  const points: Feature[] = [];

  for (const place of places) {
    const claims = activeClaims(place, year);
    if (claims.length === 0) continue;

    const geometry = geometryForYear(place, year);
    if (!geometry?.geometry) continue;

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

function directionTag(direction: string): string {
  const safe = ["supports", "challenges", "qualifies", "context"].includes(direction)
    ? direction
    : "context";
  return `<span class="tag ${safe}">${escapeHtml(labelize(direction))}</span>`;
}

function claimHtml(claim: Claim): string {
  const sourceItems = claim.sources.length
    ? claim.sources.map((source) => {
        const title = escapeHtml(source.title);
        const link = source.url
          ? `<a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${title}</a>`
          : title;
        const details = [
          source.author_or_institution,
          source.locator,
        ].filter(Boolean).map((item) => escapeHtml(item)).join(" · ");

        return `
          <li>
            <div class="source-line">
              ${directionTag(source.direction)}
              <div class="source-link">
                ${link}
                ${details ? `<div class="source-meta">${details}</div>` : ""}
              </div>
            </div>
          </li>
        `;
      }).join("")
    : `<li>No source link returned.</li>`;

  return `
    <article class="claim-card">
      <div class="claim-heading">
        <h3>${escapeHtml(labelize(claim.practice_type))}</h3>
        <span class="practice-level">${escapeHtml(claim.practice_level ?? "P-level unassigned")}</span>
      </div>

      <div class="claim-tags">
        <span class="tag ${claim.coverage_state === "disputed" ? "disputed" : ""}">
          ${escapeHtml(labelize(claim.coverage_state))}
        </span>
        ${claim.classification_status
          ? `<span class="tag">${escapeHtml(labelize(claim.classification_status))}</span>`
          : ""}
      </div>

      <div class="claim-date">${formatInterval(claim.from_year, claim.to_year)}</div>
      <p class="claim-summary">${escapeHtml(claim.summary)}</p>

      <div class="evidence-title">Evidence</div>
      <ul class="source-list">${sourceItems}</ul>
    </article>
  `;
}

function renderPlace(place: Place, year: number): void {
  selectedPlaceId = place.spatial_entity_id;

  const claims = activeClaims(place, year);
  const geometry = geometryForYear(place, year);
  const unresolved = unresolvedGeometryForYear(place, year);
  const geometryStatus = geometry?.accuracy_status ?? unresolved?.accuracy_status ?? "unresolved";

  const geometrySource = geometry?.source_title
    ? geometry.source_url
      ? `<a href="${escapeHtml(geometry.source_url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(geometry.source_title)}</a>`
      : escapeHtml(geometry.source_title)
    : "";

  panel.innerHTML = `
    <div class="panel-header">
      <button id="back-overview" class="back-button" type="button">← Back to year overview</button>
      <div class="panel-kicker">${formatYear(year)}</div>
      <h2>${escapeHtml(place.display_name || place.name)}</h2>
      <div class="entity-tags">
        <span class="tag">${escapeHtml(labelize(place.entity_type_code))}</span>
        <span class="tag ${geometryStatus === "unresolved" ? "disputed" : ""}">
          Geometry · ${escapeHtml(labelize(geometryStatus))}
        </span>
      </div>
      ${place.notes ? `<p class="place-description">${escapeHtml(place.notes)}</p>` : ""}
    </div>

    <div class="panel-body">
      ${claims.length
        ? claims.map(claimHtml).join("")
        : `<div class="empty-state">No published territorial-practice claim is active here in ${formatYear(year)}.</div>`}

      <details class="geometry-details">
        <summary>Historical geometry</summary>
        <div class="geometry-body">
          ${escapeHtml(
            geometry?.resolution_method ??
            unresolved?.resolution_method ??
            "No defensible geometry has been attached for this place/year. This is not evidence of absence.",
          )}
          ${geometry?.render_transform === "land_clip"
  ? `<div class="source-meta">Display geometry is clipped to the same canonical 1:10m land fabric used by the basemap; the source historical geometry is preserved unchanged.</div>`
  : ""}
${geometrySource ? `<div class="source-meta">Source: ${geometrySource}</div>` : ""}
        </div>
      </details>
    </div>
  `;

  document.querySelector<HTMLButtonElement>("#back-overview")?.addEventListener("click", () => {
    selectedPlaceId = null;
    renderOverview(year);
  });
}

function renderOverview(year: number): void {
  selectedPlaceId = null;

  const active = places
    .map((place) => ({
      place,
      claims: activeClaims(place, year),
      geometry: geometryForYear(place, year),
    }))
    .filter(({ claims }) => claims.length > 0);

  const activeClaimCount = active.reduce((total, item) => total + item.claims.length, 0);
  const unresolvedCount = active.filter(({ geometry }) => geometry === null).length;

  const list = active.length
    ? active.map(({ place, claims, geometry }) => {
        const level = highestPracticeLevel(claims);
        const label = claims.map((claim) => {
          const suffix = claim.coverage_state === "disputed" ? " · disputed" : "";
          return `${labelize(claim.practice_type)}${suffix}`;
        }).join(" · ");

        return `
          <button class="place-card" data-place-id="${escapeHtml(place.spatial_entity_id)}" type="button">
            <span class="place-card-top">
              <span class="place-card-name">${escapeHtml(place.display_name || place.name)}</span>
              <span class="place-card-level">${level ? `P${level}` : "—"}</span>
            </span>
            <span class="place-card-meta">
              ${escapeHtml(label)}${geometry ? "" : " · geometry unresolved"}
            </span>
          </button>
        `;
      }).join("")
    : `<div class="empty-state">No published territorial-practice evidence is active for ${formatYear(year)}.</div>`;

  panel.innerHTML = `
    <div class="panel-header">
      <div class="panel-kicker">Year overview</div>
      <h2>${formatYear(year)}</h2>
      <div class="panel-subhead">Published territorial-practice evidence active in the selected year.</div>
    </div>

    <div class="panel-body">
      <div class="overview-stats">
        <span><strong>${active.length}</strong> place${active.length === 1 ? "" : "s"}</span>
        <span><strong>${activeClaimCount}</strong> claim${activeClaimCount === 1 ? "" : "s"}</span>
        ${unresolvedCount
          ? `<span><strong>${unresolvedCount}</strong> unmapped</span>`
          : ""}
      </div>

      <p class="method-note">Missing evidence remains unknown; it is never rendered as historical absence.</p>

      <div class="place-list">${list}</div>

      <div class="release-inline">
        ${release
          ? `${escapeHtml(release.release_version)} · schema ${escapeHtml(release.schema_version)} · ${release.canonical ? "canonical" : "non-canonical preview"}`
          : "Loading release metadata…"}
      </div>
    </div>
  `;

  panel.querySelectorAll<HTMLButtonElement>("[data-place-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const place = places.find((candidate) => candidate.spatial_entity_id === button.dataset.placeId);
      if (!place) return;
      renderPlace(place, year);
      focusPlace(place, year);
    });
  });
}

function visitCoordinates(geometry: Geometry, visit: (lng: number, lat: number) => void): void {
  if (geometry.type === "Point") {
    visit(geometry.coordinates[0], geometry.coordinates[1]);
  } else if (geometry.type === "MultiPoint" || geometry.type === "LineString") {
    for (const coordinate of geometry.coordinates) visit(coordinate[0], coordinate[1]);
  } else if (geometry.type === "MultiLineString" || geometry.type === "Polygon") {
    for (const line of geometry.coordinates) {
      for (const coordinate of line) visit(coordinate[0], coordinate[1]);
    }
  } else if (geometry.type === "MultiPolygon") {
    for (const polygon of geometry.coordinates) {
      for (const ring of polygon) {
        for (const coordinate of ring) visit(coordinate[0], coordinate[1]);
      }
    }
  } else if (geometry.type === "GeometryCollection") {
    for (const child of geometry.geometries) visitCoordinates(child, visit);
  }
}

function boundsForGeometry(geometry: Geometry): LngLatBounds | null {
  const bounds = new LngLatBounds();
  let count = 0;

  visitCoordinates(geometry, (lng, lat) => {
    bounds.extend([lng, lat]);
    count += 1;
  });

  return count > 0 ? bounds : null;
}

function focusPlace(place: Place, year: number): void {
  const geometry = geometryForYear(place, year)?.geometry;
  if (!geometry) return;

  if (geometry.type === "Point") {
    map.easeTo({
      center: [geometry.coordinates[0], geometry.coordinates[1]],
      zoom: Math.max(map.getZoom(), 4.2),
      duration: 420,
    });
    return;
  }

  const bounds = boundsForGeometry(geometry);
  if (bounds) {
    map.fitBounds(bounds, { padding: 80, maxZoom: 4.5, duration: 420 });
  }
}

function fitActiveEvidence(year: number): void {
  const bounds = new LngLatBounds();
  let count = 0;

  for (const place of places) {
    if (activeClaims(place, year).length === 0) continue;

    const geometry = geometryForYear(place, year)?.geometry;
    if (!geometry) continue;

    visitCoordinates(geometry, (lng, lat) => {
      bounds.extend([lng, lat]);
      count += 1;
    });
  }

  if (count > 0) {
    map.fitBounds(bounds, { padding: 70, maxZoom: 4.2, duration: 420 });
  }
}

function resetWorldView(): void {
  map.easeTo({ center: [15, 24], zoom: 1.35, duration: 420 });
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

  status.textContent =
    `${activeClaimCount} claim${activeClaimCount === 1 ? "" : "s"} · ${activePlaceCount} place${activePlaceCount === 1 ? "" : "s"}`;

  if (selectedPlaceId) {
    const selected = places.find((place) => place.spatial_entity_id === selectedPlaceId);
    selected ? renderPlace(selected, year) : renderOverview(year);
  } else {
    renderOverview(year);
  }
}

function currentYear(): number {
  return Number(slider.value);
}

function pickFeature(event: MapMouseEvent & { features?: MapGeoJSONFeature[] }): void {
  const id = event.features?.[0]?.properties?.spatial_entity_id as string | undefined;
  if (!id) return;

  const place = places.find((candidate) => candidate.spatial_entity_id === id);
  if (!place) return;

  renderPlace(place, currentYear());
  focusPlace(place, currentYear());
}

function attachLayerInteraction(layerId: string): void {
  map.on("click", layerId, pickFeature);

  map.on("mouseenter", layerId, (event) => {
    map.getCanvas().style.cursor = "pointer";
    const feature = event.features?.[0];
    const name = feature?.properties?.name as string | undefined;
    const level = Number(feature?.properties?.p_level ?? 0);
    const state = feature?.properties?.state as string | undefined;

    if (!name) return;

    const suffix = [
      level ? `P${level}` : "",
      state === "disputed" ? "disputed" : "",
    ].filter(Boolean).join(" · ");

    hoverPopup
      .setLngLat(event.lngLat)
      .setHTML(`<strong>${escapeHtml(name)}</strong>${suffix ? `<br>${escapeHtml(suffix)}` : ""}`)
      .addTo(map);
  });

  map.on("mousemove", layerId, (event) => {
    hoverPopup.setLngLat(event.lngLat);
  });

  map.on("mouseleave", layerId, () => {
    map.getCanvas().style.cursor = "";
    hoverPopup.remove();
  });
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

    releaseBadge.textContent =
      `${apiResponse.release_version}${apiResponse.canonical ? "" : " · preview"}`;
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
    timelineRange.innerHTML =
      `<span>${formatYear(minYear)}</span><span>${formatYear(maxYear)}</span>`;

    if (!apiResponse.cartography?.source_url) {
      throw new Error("No active canonical cartographic land fabric");
    }

    map.addSource("land", {
      type: "geojson",
      data: apiResponse.cartography.source_url,
    });
    map.addLayer({
      id: "land-fill",
      type: "fill",
      source: "land",
      paint: { "fill-color": "#eee8dc", "fill-opacity": 1 },
    });
    map.addLayer({
      id: "land-line",
      type: "line",
      source: "land",
      paint: { "line-color": "#777e78", "line-width": 0.75 },
    });

    const initialCollections = buildEvidenceCollections(currentYear());

    map.addSource("evidence-polygons", {
      type: "geojson",
      data: initialCollections.polygons,
    });
    map.addLayer({
      id: "evidence-polygons",
      type: "fill",
      source: "evidence-polygons",
      paint: {
        "fill-color": [
          "match", ["get", "state"],
          "supported", "#91473e",
          "disputed", "#b88632",
          "#9c9f9a",
        ],
        "fill-opacity": [
          "case",
          ["==", ["get", "state"], "disputed"], 0.56,
          ["match", ["get", "p_level"], 4, 0.78, 3, 0.65, 2, 0.52, 1, 0.38, 0.46],
        ],
        "fill-outline-color": "#59342f",
      },
    });

    map.addSource("evidence-points", {
      type: "geojson",
      data: initialCollections.points,
    });
    map.addLayer({
      id: "evidence-points",
      type: "circle",
      source: "evidence-points",
      paint: {
        "circle-radius": 8,
        "circle-color": [
          "match", ["get", "state"],
          "supported", "#91473e",
          "disputed", "#b88632",
          "#9c9f9a",
        ],
        "circle-opacity": 0.96,
        "circle-stroke-width": 2.5,
        "circle-stroke-color": "#fffdf8",
      },
    });

    attachLayerInteraction("evidence-polygons");
    attachLayerInteraction("evidence-points");

    slider.addEventListener("input", () => updateMap(currentYear()));
    fitActiveButton.addEventListener("click", () => fitActiveEvidence(currentYear()));
    fitWorldButton.addEventListener("click", resetWorldView);

    updateMap(currentYear());
  } catch (error) {
    console.error(error);
    releaseBadge.textContent = "Load error";
    status.textContent = "Failed to load atlas data";
    panel.innerHTML =
      `<div class="panel-body"><div class="empty-state">Could not load the atlas.<br>${escapeHtml(error instanceof Error ? error.message : error)}</div></div>`;
  }
}

void boot();
