import maplibregl, { type GeoJSONSource, type MapGeoJSONFeature } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import "./styles.css";

type SourceRef = {
  title: string;
  author_or_institution: string | null;
  source_type: string | null;
  source_classification: string | null;
  version_label: string | null;
  url: string | null;
  direction: string;
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
  geometry: GeoJSON.Geometry | null;
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

const map = new maplibregl.Map({
  container: "map",
  style: {
    version: 8,
    sources: {},
    layers: [
      {
        id: "background",
        type: "background",
        paint: { "background-color": "#dce3e5" },
      },
    ],
  },
  center: [15, 24],
  zoom: 1.35,
  minZoom: 1,
  maxZoom: 8,
  attributionControl: true,
});

map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-left");

let places: Place[] = [];
let selectedPlaceId: string | null = null;

function activeInYear(fromYear: number | null, toYear: number | null, year: number): boolean {
  return (fromYear === null || year >= fromYear) && (toYear === null || year <= toYear);
}

function formatYear(year: number): string {
  return year <= 0 ? `${1 - year} BCE` : `${year} CE`;
}

function formatInterval(fromYear: number | null, toYear: number | null): string {
  const from = fromYear === null ? "unknown start" : formatYear(fromYear);
  const to = toYear === null ? "open-ended" : formatYear(toYear);
  return `${from}–${to}`;
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

function activeClaims(place: Place, year: number): Claim[] {
  return place.claims.filter((claim) => activeInYear(claim.from_year, claim.to_year, year));
}

function geometryForYear(place: Place, year: number): GeometryRecord | null {
  return (
    place.geometries.find(
      (geometry) =>
        geometry.geometry !== null &&
        activeInYear(geometry.from_year, geometry.to_year, year),
    ) ?? null
  );
}

function unresolvedGeometryForYear(place: Place, year: number): GeometryRecord | null {
  return (
    place.geometries.find(
      (geometry) =>
        geometry.accuracy_status === "unresolved" &&
        activeInYear(geometry.from_year, geometry.to_year, year),
    ) ?? null
  );
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

function buildFeatureCollection(year: number): GeoJSON.FeatureCollection {
  const features: GeoJSON.Feature[] = [];

  for (const place of places) {
    const geometry = geometryForYear(place, year);
    if (!geometry?.geometry) continue;

    const claims = activeClaims(place, year);
    features.push({
      type: "Feature",
      id: place.spatial_entity_id,
      geometry: geometry.geometry,
      properties: {
        spatial_entity_id: place.spatial_entity_id,
        name: place.display_name || place.name,
        state: featureState(claims),
        p_level: highestPracticeLevel(claims),
        geometry_accuracy: geometry.accuracy_status,
      },
    });
  }

  return { type: "FeatureCollection", features };
}

function claimHtml(claim: Claim): string {
  const sources = claim.sources.length
    ? `<ul class="source-list">${claim.sources
        .map((source) => {
          const title = escapeHtml(source.title);
          const label = source.locator ? `${title} — ${escapeHtml(source.locator)}` : title;
          return source.url
            ? `<li><a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${label}</a></li>`
            : `<li>${label}</li>`;
        })
        .join("")}</ul>`
    : `<p class="meta">No claim-source link returned.</p>`;

  return `
    <article class="claim">
      <h3>${escapeHtml(claim.practice_type.replaceAll("_", " "))}</h3>
      <div class="badges">
        <span class="badge ${claim.coverage_state === "disputed" ? "disputed" : ""}">${escapeHtml(claim.coverage_state)}</span>
        <span class="badge">${escapeHtml(claim.practice_level ?? "P-level unassigned")}</span>
      </div>
      <p class="meta">${formatInterval(claim.from_year, claim.to_year)} · ${escapeHtml(claim.publication_status)}</p>
      <p>${escapeHtml(claim.summary)}</p>
      <strong>Evidence</strong>
      ${sources}
    </article>
  `;
}

function renderPlace(place: Place, year: number): void {
  selectedPlaceId = place.spatial_entity_id;
  const claims = activeClaims(place, year);
  const geometry = geometryForYear(place, year);
  const unresolved = unresolvedGeometryForYear(place, year);

  panel.innerHTML = `
    <h2>${escapeHtml(place.display_name || place.name)}</h2>
    <div class="badges">
      <span class="badge">${escapeHtml(place.entity_type_code)}</span>
      <span class="badge ${!geometry ? "disputed" : ""}">
        geometry: ${escapeHtml(geometry?.accuracy_status ?? unresolved?.accuracy_status ?? "not resolved for year")}
      </span>
    </div>
    <p class="meta">Selected year: <strong>${formatYear(year)}</strong></p>
    ${place.notes ? `<p class="meta">${escapeHtml(place.notes)}</p>` : ""}
    ${claims.length ? claims.map(claimHtml).join("") : "<p>No territorial-practice claim is active here in the selected year.</p>"}
    <div class="geometry-note">
      <strong>Geometry</strong><br />
      ${escapeHtml(
        geometry?.resolution_method ??
          unresolved?.resolution_method ??
          "No defensible geometry has been attached for this place/year. This is not evidence of absence.",
      )}
      ${geometry?.source_title ? `<br /><span class="meta">Source: ${escapeHtml(geometry.source_title)}</span>` : ""}
    </div>
  `;
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

  const unresolvedCount = active.filter(({ geometry }) => geometry === null).length;

  panel.innerHTML = `
    <h2>${formatYear(year)}</h2>
    <p>
      <strong>${active.length}</strong> researched places have active territorial-practice evidence.
      ${unresolvedCount ? `<strong>${unresolvedCount}</strong> currently lack a defensible map geometry.` : ""}
    </p>
    <p class="meta">
      Research coverage, law, network participation and territorial practice remain separate.
      Missing geometry or evidence is never interpreted as historical absence.
    </p>
    <div id="place-list">
      ${active
        .map(({ place, claims }) => {
          const label = claims
            .map((claim) => `${claim.practice_type.replaceAll("_", " ")}${claim.coverage_state === "disputed" ? " (?)" : ""}`)
            .join(", ");
          return `<button class="place-button" data-place-id="${escapeHtml(place.spatial_entity_id)}">
            <strong>${escapeHtml(place.display_name || place.name)}</strong><br />
            <span class="meta">${escapeHtml(label)}</span>
          </button>`;
        })
        .join("")}
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

  const source = map.getSource("evidence") as GeoJSONSource | undefined;
  source?.setData(buildFeatureCollection(year));

  const activeCount = places.reduce((count, place) => count + activeClaims(place, year).length, 0);
  status.textContent = `${activeCount} active claim${activeCount === 1 ? "" : "s"} · ${places.length} researched places`;

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

function pickFeature(event: maplibregl.MapMouseEvent & { features?: MapGeoJSONFeature[] }): void {
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

    places = apiResponse.places;

    const years = places.flatMap((place) =>
      place.claims.flatMap((claim) =>
        [claim.from_year, claim.to_year].filter((year): year is number => year !== null),
      ),
    );
    slider.min = String(Math.min(...years));
    slider.max = "2026";
    slider.value = String(years.some((year) => year <= -499) ? -499 : Math.max(...years));

    map.addSource("land", { type: "geojson", data: "/world-land.geojson" });
    map.addLayer({
      id: "land-fill",
      type: "fill",
      source: "land",
      paint: { "fill-color": "#efeee9", "fill-opacity": 1 },
    });
    map.addLayer({
      id: "land-line",
      type: "line",
      source: "land",
      paint: { "line-color": "#8f8b83", "line-width": 0.65 },
    });

    map.addSource("evidence", { type: "geojson", data: buildFeatureCollection(currentYear()) });
    map.addLayer({
      id: "evidence-fill",
      type: "fill",
      source: "evidence",
      filter: ["==", ["geometry-type"], "Polygon"],
      paint: {
        "fill-color": [
          "match",
          ["get", "state"],
          "supported", "#9e493f",
          "disputed", "#c18a31",
          "#b8b7b2",
        ],
        "fill-opacity": [
          "match",
          ["get", "state"],
          "supported", 0.66,
          "disputed", 0.62,
          0.1,
        ],
      },
    });
    map.addLayer({
      id: "evidence-line",
      type: "line",
      source: "evidence",
      filter: ["==", ["geometry-type"], "Polygon"],
      paint: {
        "line-color": [
          "match",
          ["get", "state"],
          "supported", "#6e2b24",
          "disputed", "#815914",
          "#8f8d88",
        ],
        "line-width": ["case", ["==", ["get", "state"], "inactive"], 0.7, 1.6],
      },
    });
    map.addLayer({
      id: "evidence-points",
      type: "circle",
      source: "evidence",
      filter: ["==", ["geometry-type"], "Point"],
      paint: {
        "circle-radius": ["case", ["==", ["get", "state"], "inactive"], 4, 7],
        "circle-color": [
          "match",
          ["get", "state"],
          "supported", "#9e493f",
          "disputed", "#c18a31",
          "#b8b7b2",
        ],
        "circle-opacity": ["case", ["==", ["get", "state"], "inactive"], 0.25, 0.85],
        "circle-stroke-width": 1.4,
        "circle-stroke-color": "#4f4841",
      },
    });

    map.on("click", "evidence-fill", pickFeature);
    map.on("click", "evidence-points", pickFeature);
    for (const layer of ["evidence-fill", "evidence-points"]) {
      map.on("mouseenter", layer, () => { map.getCanvas().style.cursor = "pointer"; });
      map.on("mouseleave", layer, () => { map.getCanvas().style.cursor = ""; });
    }

    slider.addEventListener("input", () => updateMap(currentYear()));
    updateMap(currentYear());
  } catch (error) {
    console.error(error);
    status.textContent = "Failed to load atlas data";
    panel.innerHTML = `<h2>Could not load the research preview</h2><p>${escapeHtml(error instanceof Error ? error.message : error)}</p>`;
  }
}

void boot();
