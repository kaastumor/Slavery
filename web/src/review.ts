import {
  LngLatBounds,
  Map,
  NavigationControl,
  setWorkerUrl,
  type GeoJSONSource,
} from "maplibre-gl";
import type { Feature, FeatureCollection, Geometry, GeoJsonProperties } from "geojson";
import "maplibre-gl/dist/maplibre-gl.css";
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url";
import "./review.css";

setWorkerUrl(workerUrl);

type ArtifactRecord = {
  path: string;
  size_bytes: number;
  sha256: string;
};

type ArtifactManifest = {
  schema_version: string;
  artifact_kind: string;
  git_sha: string | null;
  metadata?: Record<string, string>;
  inputs?: ArtifactRecord[];
  artifacts?: ArtifactRecord[];
  qc?: ArtifactRecord[];
};

type DecisionRow = {
  geometry_id: string | null;
  name?: string | null;
  status?: string;
  reasons?: string[];
  metrics?: {
    area_delta_pct?: number | null;
    symmetric_difference_pct?: number | null;
    hausdorff_m?: number | null;
    source_npoints?: number | null;
    render_npoints?: number | null;
  };
};

type DecisionPayload = {
  features?: DecisionRow[];
};

type LoadedFile = {
  fileName: string;
  sha256: string;
};

const PINNED_LAND_URL =
  "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/ca96624a56bd078437bca8184e78163e5039ad19/geojson/ne_10m_land.geojson";
const PINNED_LAND_SHA256 =
  "1ac90796408bc6ad6911d69448485d3c4dbf2190370080368a09976e1c9f7416";

const emptyCollection = (): FeatureCollection => ({
  type: "FeatureCollection",
  features: [],
});

const manifestInput = document.querySelector<HTMLInputElement>("#manifest-file")!;
const sourceInput = document.querySelector<HTMLInputElement>("#source-file")!;
const candidateInput = document.querySelector<HTMLInputElement>("#candidate-file")!;
const decisionInput = document.querySelector<HTMLInputElement>("#decision-file")!;
const landInput = document.querySelector<HTMLInputElement>("#land-file")!;
const geometrySelect = document.querySelector<HTMLSelectElement>("#geometry-select")!;
const fitSelectedButton = document.querySelector<HTMLButtonElement>("#fit-selected")!;
const fitWorldButton = document.querySelector<HTMLButtonElement>("#fit-world")!;
const showSource = document.querySelector<HTMLInputElement>("#show-source")!;
const showCandidate = document.querySelector<HTMLInputElement>("#show-candidate")!;
const manifestState = document.querySelector<HTMLElement>("#manifest-state")!;
const sourceState = document.querySelector<HTMLElement>("#source-state")!;
const candidateState = document.querySelector<HTMLElement>("#candidate-state")!;
const decisionState = document.querySelector<HTMLElement>("#decision-state")!;
const landState = document.querySelector<HTMLElement>("#land-state")!;
const reviewStatus = document.querySelector<HTMLElement>("#review-status")!;
const metrics = document.querySelector<HTMLElement>("#metrics")!;
const mapTitle = document.querySelector<HTMLElement>("#map-title")!;
const zoomLabel = document.querySelector<HTMLElement>("#zoom-label")!;

const map = new Map({
  container: "review-map",
  style: {
    version: 8,
    sources: {},
    layers: [
      {
        id: "background",
        type: "background",
        paint: { "background-color": "#d9e4e7" },
      },
    ],
  },
  center: [15, 24],
  zoom: 1.35,
  minZoom: 1,
  maxZoom: 10,
});

map.addControl(new NavigationControl({ showCompass: false }), "top-left");

let manifest: ArtifactManifest | null = null;
let sourceCollection: FeatureCollection | null = null;
let candidateCollection: FeatureCollection | null = null;
let landCollection: FeatureCollection | null = null;
let decisionRows = new globalThis.Map<string, DecisionRow>();
let selectedGeometryId: string | null = null;
let loadedSource: LoadedFile | null = null;
let loadedCandidate: LoadedFile | null = null;
let loadedDecision: LoadedFile | null = null;
let landVerified = false;

function setState(
  element: HTMLElement,
  text: string,
  state?: "ok" | "warn" | "error",
): void {
  element.textContent = text;
  element.classList.remove("ok", "warn", "error");
  if (state) element.classList.add(state);
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

function basename(path: string): string {
  const normalized = path.replaceAll("\\", "/");
  return normalized.split("/").at(-1) ?? normalized;
}

async function sha256Hex(buffer: ArrayBuffer): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", buffer);
  return [...new Uint8Array(digest)]
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

function parseFeatureCollection(value: unknown, label: string): FeatureCollection {
  if (
    typeof value !== "object" ||
    value === null ||
    (value as { type?: unknown }).type !== "FeatureCollection" ||
    !Array.isArray((value as { features?: unknown }).features)
  ) {
    throw new Error(label + " is not a GeoJSON FeatureCollection");
  }
  return value as FeatureCollection;
}

function geometryId(feature: Feature): string | null {
  const properties = feature.properties as GeoJsonProperties;
  const value = properties?.geometry_id;
  return value === null || value === undefined || value === "" ? null : String(value);
}

function featureName(feature: Feature): string {
  const properties = feature.properties as GeoJsonProperties;
  return String(properties?.name ?? geometryId(feature) ?? "Unnamed geometry");
}

function featureMap(collection: FeatureCollection | null): globalThis.Map<string, Feature> {
  const result = new globalThis.Map<string, Feature>();
  for (const feature of collection?.features ?? []) {
    const id = geometryId(feature);
    if (id) result.set(id, feature);
  }
  return result;
}

function singleFeatureCollection(feature: Feature | undefined): FeatureCollection {
  return {
    type: "FeatureCollection",
    features: feature ? [feature] : [],
  };
}

function findRecord(
  category: "inputs" | "artifacts" | "qc",
  fileName: string,
): ArtifactRecord | null {
  const records = manifest?.[category] ?? [];
  return records.find((record) => basename(record.path) === fileName) ?? null;
}

function verificationText(
  loaded: LoadedFile | null,
  category: "inputs" | "artifacts" | "qc",
): { text: string; state: "ok" | "warn" | "error" } {
  if (!loaded) return { text: "Not loaded", state: "warn" };
  if (!manifest) {
    return { text: loaded.fileName + " · manifest not loaded", state: "warn" };
  }

  const expected = findRecord(category, loaded.fileName);
  if (!expected) {
    return { text: loaded.fileName + " · not listed in manifest", state: "error" };
  }
  if (expected.sha256 !== loaded.sha256) {
    return { text: loaded.fileName + " · SHA-256 mismatch", state: "error" };
  }
  return { text: loaded.fileName + " · SHA-256 verified", state: "ok" };
}

function refreshVerificationStates(): void {
  const sourceVerification = verificationText(loadedSource, "inputs");
  setState(sourceState, sourceVerification.text, sourceVerification.state);

  const candidateVerification = verificationText(loadedCandidate, "artifacts");
  setState(candidateState, candidateVerification.text, candidateVerification.state);

  if (loadedDecision) {
    const decisionVerification = verificationText(loadedDecision, "qc");
    setState(decisionState, decisionVerification.text, decisionVerification.state);
  } else {
    setState(decisionState, "Optional", "warn");
  }

  if (manifest) {
    const landHash = manifest.metadata?.land_sha256;
    if (landHash && landHash !== PINNED_LAND_SHA256) {
      landVerified = false;
      setState(
        landState,
        "Manifest land SHA differs from the canonical pinned fabric: " + landHash,
        "error",
      );
    }
  }

  refreshReviewStatus();
}

function refreshReviewStatus(): void {
  const sourceRecord =
    loadedSource === null ? null : findRecord("inputs", loadedSource.fileName);
  const candidateRecord =
    loadedCandidate === null ? null : findRecord("artifacts", loadedCandidate.fileName);

  const sourceOk =
    loadedSource !== null &&
    sourceRecord !== null &&
    sourceRecord.sha256 === loadedSource.sha256;
  const candidateOk =
    loadedCandidate !== null &&
    candidateRecord !== null &&
    candidateRecord.sha256 === loadedCandidate.sha256;

  reviewStatus.classList.remove("ready", "blocked");

  if (!manifest || !sourceCollection || !candidateCollection || !landCollection) {
    reviewStatus.textContent =
      "Load the manifest, source and candidate. Canonical land must also verify.";
    return;
  }

  if (!sourceOk || !candidateOk || !landVerified) {
    reviewStatus.classList.add("blocked");
    reviewStatus.textContent =
      "Exact-artifact review blocked: a required SHA-256 check failed or is unverified.";
    return;
  }

  reviewStatus.classList.add("ready");
  const build = manifest.git_sha ? " · build " + manifest.git_sha.slice(0, 12) : "";
  reviewStatus.textContent =
    "Exact-artifact inputs verified" +
    build +
    ". Visual inspection may proceed; automated QC is not visual acceptance.";
}

async function readFile(
  file: File,
): Promise<{ buffer: ArrayBuffer; text: string; sha256: string }> {
  const buffer = await file.arrayBuffer();
  const sha256 = await sha256Hex(buffer);
  return {
    buffer,
    text: new TextDecoder().decode(buffer),
    sha256,
  };
}

async function loadManifest(file: File): Promise<void> {
  const loaded = await readFile(file);
  const parsed = JSON.parse(loaded.text) as ArtifactManifest;
  if (parsed.schema_version !== "atlas-artifact-manifest-v1") {
    throw new Error("Unsupported artifact manifest schema: " + parsed.schema_version);
  }
  manifest = parsed;
  const build = parsed.git_sha ? " · build " + parsed.git_sha.slice(0, 12) : "";
  setState(manifestState, file.name + build, "ok");
  refreshVerificationStates();
}

async function loadSource(file: File): Promise<void> {
  const loaded = await readFile(file);
  sourceCollection = parseFeatureCollection(JSON.parse(loaded.text), "Source file");
  loadedSource = { fileName: file.name, sha256: loaded.sha256 };
  refreshGeometryOptions();
  refreshVerificationStates();
}

async function loadCandidate(file: File): Promise<void> {
  const loaded = await readFile(file);
  candidateCollection = parseFeatureCollection(JSON.parse(loaded.text), "Candidate file");
  loadedCandidate = { fileName: file.name, sha256: loaded.sha256 };
  refreshGeometryOptions();
  refreshVerificationStates();
}

async function loadDecision(file: File): Promise<void> {
  const loaded = await readFile(file);
  const payload = JSON.parse(loaded.text) as DecisionPayload;
  decisionRows = new globalThis.Map(
    (payload.features ?? [])
      .filter((row): row is DecisionRow & { geometry_id: string } => Boolean(row.geometry_id))
      .map((row) => [String(row.geometry_id), row]),
  );
  loadedDecision = { fileName: file.name, sha256: loaded.sha256 };
  refreshVerificationStates();
  renderSelected();
}

async function applyLandBuffer(buffer: ArrayBuffer, label: string): Promise<void> {
  const digest = await sha256Hex(buffer);
  if (digest !== PINNED_LAND_SHA256) {
    landVerified = false;
    setState(
      landState,
      label + " · SHA-256 mismatch (" + digest.slice(0, 12) + "…)",
      "error",
    );
    refreshReviewStatus();
    throw new Error("Land fabric does not match the pinned Natural Earth 1:10m checksum");
  }

  const text = new TextDecoder().decode(buffer);
  landCollection = parseFeatureCollection(JSON.parse(text), "Land fabric");
  landVerified = true;
  setState(landState, label + " · SHA-256 verified", "ok");

  const landSource = map.getSource("land") as GeoJSONSource | undefined;
  landSource?.setData(landCollection);
  refreshReviewStatus();
}

async function loadPinnedLand(): Promise<void> {
  try {
    const response = await fetch(PINNED_LAND_URL);
    if (!response.ok) {
      throw new Error("Natural Earth fetch returned " + response.status);
    }
    await applyLandBuffer(await response.arrayBuffer(), "Pinned Natural Earth 1:10m");
  } catch (error) {
    console.error(error);
    landVerified = false;
    setState(
      landState,
      "Automatic load failed; select the exact pinned GeoJSON locally.",
      "warn",
    );
    refreshReviewStatus();
  }
}

function refreshGeometryOptions(): void {
  const sources = featureMap(sourceCollection);
  const candidates = featureMap(candidateCollection);
  const shared = [...sources.keys()]
    .filter((id) => candidates.has(id))
    .sort((a, b) => featureName(sources.get(a)!).localeCompare(featureName(sources.get(b)!)));

  geometrySelect.replaceChildren();

  if (shared.length === 0) {
    const option = document.createElement("option");
    option.textContent =
      sourceCollection && candidateCollection
        ? "No matching geometry_id values"
        : "Load source and candidate files";
    geometrySelect.append(option);
    geometrySelect.disabled = true;
    fitSelectedButton.disabled = true;
    selectedGeometryId = null;
    renderSelected();
    return;
  }

  for (const id of shared) {
    const option = document.createElement("option");
    option.value = id;
    option.textContent = featureName(sources.get(id)!) + " · " + id.slice(0, 8);
    geometrySelect.append(option);
  }

  geometrySelect.disabled = false;
  fitSelectedButton.disabled = false;

  if (!selectedGeometryId || !shared.includes(selectedGeometryId)) {
    selectedGeometryId = shared[0];
  }
  geometrySelect.value = selectedGeometryId;
  renderSelected();
}

function formatMetric(value: number | null | undefined, digits = 3): string {
  return value === null || value === undefined || !Number.isFinite(value)
    ? "n/a"
    : value.toFixed(digits);
}

function renderMetrics(row: DecisionRow | undefined): void {
  if (!selectedGeometryId) {
    metrics.innerHTML = '<div class="metric-empty">No geometry selected.</div>';
    return;
  }

  if (!row) {
    metrics.innerHTML =
      '<div class="metric-empty">No decision row loaded for this geometry.</div>';
    return;
  }

  const metric = row.metrics ?? {};
  const reasons = row.reasons?.length ? row.reasons.join(", ") : "—";
  const status = row.status ?? "unclassified";
  const hausdorffKm =
    metric.hausdorff_m === null || metric.hausdorff_m === undefined
      ? null
      : metric.hausdorff_m / 1000;

  metrics.innerHTML =
    '<span class="status-pill ' +
    escapeHtml(status) +
    '">' +
    escapeHtml(status) +
    "</span>" +
    '<div class="metric-row"><span>Area Δ</span><strong>' +
    escapeHtml(formatMetric(metric.area_delta_pct)) +
    "%</strong></div>" +
    '<div class="metric-row"><span>Symmetric diff</span><strong>' +
    escapeHtml(formatMetric(metric.symmetric_difference_pct)) +
    "%</strong></div>" +
    '<div class="metric-row"><span>Hausdorff</span><strong>' +
    escapeHtml(formatMetric(hausdorffKm)) +
    " km</strong></div>" +
    '<div class="metric-row"><span>Source vertices</span><strong>' +
    escapeHtml(metric.source_npoints ?? "n/a") +
    "</strong></div>" +
    '<div class="metric-row"><span>Render vertices</span><strong>' +
    escapeHtml(metric.render_npoints ?? "n/a") +
    "</strong></div>" +
    '<div class="metric-row"><span>Quarantine reasons</span><strong>' +
    escapeHtml(reasons) +
    "</strong></div>";
}

function renderSelected(): void {
  const sources = featureMap(sourceCollection);
  const candidates = featureMap(candidateCollection);
  const sourceFeature = selectedGeometryId ? sources.get(selectedGeometryId) : undefined;
  const candidateFeature = selectedGeometryId
    ? candidates.get(selectedGeometryId)
    : undefined;

  (map.getSource("source-geometry") as GeoJSONSource | undefined)?.setData(
    singleFeatureCollection(sourceFeature),
  );
  (map.getSource("candidate-geometry") as GeoJSONSource | undefined)?.setData(
    singleFeatureCollection(candidateFeature),
  );

  if (!sourceFeature || !candidateFeature || !selectedGeometryId) {
    mapTitle.textContent = "No geometry selected";
    renderMetrics(undefined);
    return;
  }

  mapTitle.textContent = featureName(sourceFeature);
  renderMetrics(decisionRows.get(selectedGeometryId));
  fitSelected();
}

function visitCoordinates(
  geometry: Geometry,
  visit: (lng: number, lat: number) => void,
): void {
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

function fitSelected(): void {
  if (!selectedGeometryId) return;
  const sources = featureMap(sourceCollection);
  const candidates = featureMap(candidateCollection);
  const sourceFeature = sources.get(selectedGeometryId);
  const candidateFeature = candidates.get(selectedGeometryId);
  if (!sourceFeature?.geometry || !candidateFeature?.geometry) return;

  const bounds = new LngLatBounds();
  let count = 0;
  for (const geometry of [sourceFeature.geometry, candidateFeature.geometry]) {
    visitCoordinates(geometry, (lng, lat) => {
      bounds.extend([lng, lat]);
      count += 1;
    });
  }

  if (count > 0) {
    map.fitBounds(bounds, { padding: 55, maxZoom: 6.5, duration: 250 });
  }
}

function setLayerVisible(layerId: string, visible: boolean): void {
  if (!map.getLayer(layerId)) return;
  map.setLayoutProperty(layerId, "visibility", visible ? "visible" : "none");
}

map.on("load", () => {
  map.addSource("land", {
    type: "geojson",
    data: emptyCollection(),
    tolerance: 0,
  });
  map.addLayer({
    id: "land-fill",
    type: "fill",
    source: "land",
    paint: { "fill-color": "#ece9e2", "fill-opacity": 1 },
  });
  map.addLayer({
    id: "land-line",
    type: "line",
    source: "land",
    paint: { "line-color": "#7f827f", "line-width": 0.8 },
  });

  map.addSource("source-geometry", {
    type: "geojson",
    data: emptyCollection(),
    tolerance: 0,
  });
  map.addLayer({
    id: "source-fill",
    type: "fill",
    source: "source-geometry",
    paint: { "fill-color": "#ad6b23", "fill-opacity": 0.08 },
  });

  map.addSource("candidate-geometry", {
    type: "geojson",
    data: emptyCollection(),
    tolerance: 0,
  });
  map.addLayer({
    id: "candidate-fill",
    type: "fill",
    source: "candidate-geometry",
    paint: { "fill-color": "#2f79aa", "fill-opacity": 0.34 },
  });
  map.addLayer({
    id: "candidate-line",
    type: "line",
    source: "candidate-geometry",
    paint: { "line-color": "#175c88", "line-width": 2.2 },
  });
  map.addLayer({
    id: "source-line",
    type: "line",
    source: "source-geometry",
    paint: {
      "line-color": "#a25d14",
      "line-width": 1.7,
      "line-dasharray": [3, 2],
    },
  });

  if (landCollection) {
    (map.getSource("land") as GeoJSONSource).setData(landCollection);
  }
  renderSelected();
});

map.on("zoom", () => {
  zoomLabel.textContent = "zoom " + map.getZoom().toFixed(2);
});

geometrySelect.addEventListener("change", () => {
  selectedGeometryId = geometrySelect.value || null;
  renderSelected();
});

fitSelectedButton.addEventListener("click", fitSelected);
fitWorldButton.addEventListener("click", () => {
  map.easeTo({ center: [15, 24], zoom: 1.35, duration: 250 });
});

showSource.addEventListener("change", () => {
  setLayerVisible("source-fill", showSource.checked);
  setLayerVisible("source-line", showSource.checked);
});

showCandidate.addEventListener("change", () => {
  setLayerVisible("candidate-fill", showCandidate.checked);
  setLayerVisible("candidate-line", showCandidate.checked);
});

manifestInput.addEventListener("change", async () => {
  const file = manifestInput.files?.[0];
  if (!file) return;
  try {
    await loadManifest(file);
  } catch (error) {
    console.error(error);
    manifest = null;
    setState(
      manifestState,
      error instanceof Error ? error.message : "Could not load manifest",
      "error",
    );
    refreshVerificationStates();
  }
});

sourceInput.addEventListener("change", async () => {
  const file = sourceInput.files?.[0];
  if (!file) return;
  try {
    await loadSource(file);
  } catch (error) {
    console.error(error);
    sourceCollection = null;
    loadedSource = null;
    setState(
      sourceState,
      error instanceof Error ? error.message : "Could not load source",
      "error",
    );
    refreshGeometryOptions();
    refreshReviewStatus();
  }
});

candidateInput.addEventListener("change", async () => {
  const file = candidateInput.files?.[0];
  if (!file) return;
  try {
    await loadCandidate(file);
  } catch (error) {
    console.error(error);
    candidateCollection = null;
    loadedCandidate = null;
    setState(
      candidateState,
      error instanceof Error ? error.message : "Could not load candidate",
      "error",
    );
    refreshGeometryOptions();
    refreshReviewStatus();
  }
});

decisionInput.addEventListener("change", async () => {
  const file = decisionInput.files?.[0];
  if (!file) return;
  try {
    await loadDecision(file);
  } catch (error) {
    console.error(error);
    decisionRows.clear();
    loadedDecision = null;
    setState(
      decisionState,
      error instanceof Error ? error.message : "Could not load decision file",
      "error",
    );
    renderSelected();
    refreshReviewStatus();
  }
});

landInput.addEventListener("change", async () => {
  const file = landInput.files?.[0];
  if (!file) return;
  try {
    await applyLandBuffer(await file.arrayBuffer(), file.name);
  } catch (error) {
    console.error(error);
  }
});

void loadPinnedLand();
