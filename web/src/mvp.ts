import { Map, NavigationControl, setWorkerUrl } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url";
import "./styles.css";

setWorkerUrl(workerUrl);

type CandidateTarget = {
  target_id: string;
  target_label: string;
  anchor: string | number;
  release_research_state: string;
  classification_outcome: string;
  interpretation: string;
};

type OverviewState = {
  id: string;
  label: string;
  description: string;
  count: number;
};

type CandidateBundle = {
  schema: string;
  candidate_id: string;
  canonical_historical_release: string;
  publication_state: string;
  review_scope: string;
  non_absence_rule: string;
  counts: { targets: number; reviewed_c1: number };
  overview_semantics: {
    rule: string;
    research_states: OverviewState[];
    geometry_states: OverviewState[];
    targets: Array<{ target_id: string; research_state: string; geometry_state: string }>;
  };
  targets: CandidateTarget[];
  reviewed_c1: unknown[];
};

const CANDIDATE_URL = new URL("./data/r1-mvp-candidate.json", window.location.href).toString();
const LAND_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson";

const panel = document.querySelector<HTMLElement>("#panel")!;
const status = document.querySelector<HTMLElement>("#status")!;
const releaseBadge = document.querySelector<HTMLElement>("#release-badge")!;
const slider = document.querySelector<HTMLInputElement>("#year")!;
const yearLabel = document.querySelector<HTMLOutputElement>("#year-label")!;
const timelineRange = document.querySelector<HTMLElement>("#timeline-range")!;
const fitWorldButton = document.querySelector<HTMLButtonElement>("#fit-world")!;
const fitActiveButton = document.querySelector<HTMLButtonElement>("#fit-active")!;
const researchStateLegend = document.querySelector<HTMLElement>("#research-state-legend")!;
const geometryStateLegend = document.querySelector<HTMLElement>("#geometry-state-legend")!;

const map = new Map({
  container: "map",
  style: { version: 8, sources: {}, layers: [{ id: "background", type: "background", paint: { "background-color": "#cfdcdf" } }] },
  center: [15, 24], zoom: 1.35, minZoom: 1, maxZoom: 8,
});
map.addControl(new NavigationControl({ showCompass: false }), "top-left");

function escapeHtml(value: unknown): string {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" })[char]!);
}

function formatYear(value: string | number): string {
  const year = typeof value === "number" ? value : /^-?\d+$/.test(value) ? Number(value) : Number.NaN;
  if (!Number.isFinite(year)) return String(value);
  return year <= 0 ? `${1 - year} BCE` : `${year} CE`;
}

function validateCandidate(value: unknown): CandidateBundle {
  if (!value || typeof value !== "object") throw new Error("Candidate bundle is not an object");
  const candidate = value as Partial<CandidateBundle>;
  if (candidate.schema !== "historical-slavery-atlas.r1-mvp-candidate.v1") throw new Error("Candidate bundle schema is missing or unsupported");
  if (!candidate.candidate_id || candidate.publication_state !== "candidate_not_published_not_canonical") throw new Error("Candidate publication boundary is missing or invalid");
  if (candidate.review_scope !== "internal_adversarial_review_only_not_independent_review") throw new Error("Candidate review scope is missing or invalid");
  if (!candidate.counts || candidate.counts.targets !== 77 || candidate.counts.reviewed_c1 !== 19) throw new Error("Candidate frozen counts do not match the R1.6 contract");
  if (!Array.isArray(candidate.targets) || candidate.targets.length !== candidate.counts.targets) throw new Error("Candidate target registry is missing or incomplete");
  if (!Array.isArray(candidate.reviewed_c1) || candidate.reviewed_c1.length !== candidate.counts.reviewed_c1) throw new Error("Candidate reviewed C1 packet is missing or incomplete");
  if (!candidate.overview_semantics || !Array.isArray(candidate.overview_semantics.research_states) || !Array.isArray(candidate.overview_semantics.geometry_states)) {
    throw new Error("Candidate overview semantics are missing");
  }
  const researchStateTotal = candidate.overview_semantics.research_states.reduce((sum, item) => sum + Number(item.count || 0), 0);
  const geometryStateTotal = candidate.overview_semantics.geometry_states.reduce((sum, item) => sum + Number(item.count || 0), 0);
  if (researchStateTotal !== candidate.counts.targets || geometryStateTotal !== candidate.counts.targets) {
    throw new Error("Candidate overview state counts do not cover the frozen target registry");
  }
  if (!Array.isArray(candidate.overview_semantics.targets) || candidate.overview_semantics.targets.length !== candidate.counts.targets) {
    throw new Error("Candidate per-target overview semantics are incomplete");
  }
  return candidate as CandidateBundle;
}

async function loadCandidate(): Promise<CandidateBundle> {
  const response = await fetch(CANDIDATE_URL, { cache: "no-store" });
  if (!response.ok) throw new Error(`Static R1 candidate returned ${response.status}`);
  return validateCandidate(await response.json());
}

function renderStateLegend(states: OverviewState[]): string {
  return states.map((state) => `
    <div class="state-legend-row">
      <span class="state-chip" data-state="${escapeHtml(state.id)}">${escapeHtml(state.label)}</span>
      <span class="state-count">${escapeHtml(state.count)}</span>
    </div>`).join("");
}

function renderOverviewCard(state: OverviewState): string {
  return `
    <article class="state-card" data-state="${escapeHtml(state.id)}">
      <div class="state-card-top"><strong>${escapeHtml(state.label)}</strong><span>${escapeHtml(state.count)}</span></div>
      <p>${escapeHtml(state.description)}</p>
    </article>`;
}

function renderCandidate(candidate: CandidateBundle): void {
  const anchors = [...new Set(candidate.targets.map((target) => Number(target.anchor)).filter(Number.isFinite))].sort((a, b) => a - b);
  const min = anchors[0] ?? -2000;
  const max = anchors.at(-1) ?? 1800;
  slider.min = String(min); slider.max = String(max); slider.value = String(max);
  yearLabel.value = formatYear(max); yearLabel.textContent = formatYear(max);
  timelineRange.innerHTML = `<span>${formatYear(min)}</span><span>${formatYear(max)}</span>`;

  releaseBadge.textContent = `${candidate.candidate_id} · candidate · non-canonical · internally reviewed`;
  releaseBadge.classList.add("preview");
  releaseBadge.title = `Canonical historical release remains ${candidate.canonical_historical_release}; review is internal adversarial review, not independent review.`;
  const unresolvedGeometry = candidate.overview_semantics.geometry_states.find((state) => state.id === "unresolved_no_geometry")?.count ?? 0;
  status.textContent = `${candidate.counts.targets} frozen targets · ${candidate.counts.reviewed_c1} reviewed · ${unresolvedGeometry} geometry unresolved`;

  researchStateLegend.innerHTML = renderStateLegend(candidate.overview_semantics.research_states);
  geometryStateLegend.innerHTML = renderStateLegend(candidate.overview_semantics.geometry_states);

  const researchCards = candidate.overview_semantics.research_states.map(renderOverviewCard).join("");
  const geometryCards = candidate.overview_semantics.geometry_states.map(renderOverviewCard).join("");
  panel.innerHTML = `
    <div class="panel-header">
      <div class="panel-kicker">R1 MVP candidate</div>
      <h2>Research-state overview</h2>
      <div class="panel-subhead">Static/read-only candidate data. Research state is not historical presence, absence or intensity.</div>
    </div>
    <div class="panel-body">
      <div class="overview-stats">
        <span><strong>${escapeHtml(candidate.counts.targets)}</strong><br>frozen targets</span>
        <span><strong>${escapeHtml(candidate.counts.reviewed_c1)}</strong><br>reviewed C1</span>
      </div>
      <p class="method-note">${escapeHtml(candidate.overview_semantics.rule)}</p>
      <section aria-labelledby="research-state-heading">
        <h3 id="research-state-heading" class="overview-heading">Research coverage</h3>
        <div class="state-grid">${researchCards}</div>
      </section>
      <section class="overview-section" aria-labelledby="geometry-state-heading">
        <h3 id="geometry-state-heading" class="overview-heading">Geometry representation</h3>
        <div class="state-grid">${geometryCards}</div>
      </section>
      <div class="empty-state map-truth-note"><strong>Map boundary:</strong> no unresolved target is drawn as historical territory. Neutral world land stays visible, and geometry availability does not alter any historical claim.</div>
      <p class="source-meta">${escapeHtml(candidate.non_absence_rule)}</p>
    </div>`;
}

async function boot(): Promise<void> {
  try {
    const [candidate] = await Promise.all([loadCandidate(), new Promise<void>((resolve) => map.once("load", () => resolve()))]);
    map.addSource("neutral-land", { type: "geojson", data: LAND_URL });
    map.addLayer({ id: "neutral-land-fill", type: "fill", source: "neutral-land", paint: { "fill-color": "#eee8dc", "fill-opacity": 1 } });
    map.addLayer({ id: "neutral-land-line", type: "line", source: "neutral-land", paint: { "line-color": "#777e78", "line-width": 0.75 } });
    renderCandidate(candidate);
    slider.addEventListener("input", () => { yearLabel.value = formatYear(Number(slider.value)); yearLabel.textContent = yearLabel.value; });
    fitWorldButton.addEventListener("click", () => map.easeTo({ center: [15, 24], zoom: 1.35, duration: 420 }));
    fitActiveButton.disabled = true;
    fitActiveButton.title = "No reviewed target geometry is materialized; unresolved targets are not drawn as territory";
  } catch (error) {
    console.error(error);
    releaseBadge.textContent = "R1 candidate load error";
    releaseBadge.classList.add("preview");
    status.textContent = "Static candidate unavailable or invalid";
    panel.innerHTML = `<div class="panel-body"><div class="empty-state"><strong>Could not load the R1 MVP candidate.</strong><br>${escapeHtml(error instanceof Error ? error.message : error)}<br>No live API fallback is attempted because it could silently substitute a different historical data product.</div></div>`;
  }
}

void boot();
