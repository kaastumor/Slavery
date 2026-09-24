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

type CandidateBundle = {
  schema: string;
  candidate_id: string;
  canonical_historical_release: string;
  publication_state: string;
  review_scope: string;
  non_absence_rule: string;
  counts: { targets: number; reviewed_c1: number };
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
  return candidate as CandidateBundle;
}

async function loadCandidate(): Promise<CandidateBundle> {
  const response = await fetch(CANDIDATE_URL, { cache: "no-store" });
  if (!response.ok) throw new Error(`Static R1 candidate returned ${response.status}`);
  return validateCandidate(await response.json());
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
  status.textContent = `${candidate.counts.targets} frozen targets · ${candidate.counts.reviewed_c1} reviewed C1`;

  const rows = candidate.targets.slice(0, 12).map((target) => `
    <li><strong>${escapeHtml(target.target_label)}</strong> · ${escapeHtml(formatYear(target.anchor))}<br><span class="source-meta">${escapeHtml(target.release_research_state)} · ${escapeHtml(target.classification_outcome)}</span></li>`).join("");
  panel.innerHTML = `<div class="panel-header"><div class="panel-kicker">R1 MVP candidate</div><h2>Frozen evidence package</h2><div class="panel-subhead">Static/read-only candidate data. ${escapeHtml(candidate.non_absence_rule)}</div></div><div class="panel-body"><p><strong>${candidate.counts.targets}</strong> targets are loaded from the generated R1 candidate bundle. The live Atlas API is not used for core evidence data.</p><ul class="source-list">${rows}</ul><p class="source-meta">Target-state map semantics and compact evidence detail are completed in the next bounded MVP issues.</p></div>`;
}

async function boot(): Promise<void> {
  try {
    const [candidate] = await Promise.all([loadCandidate(), new Promise<void>((resolve) => map.once("load", resolve))]);
    map.addSource("neutral-land", { type: "geojson", data: LAND_URL });
    map.addLayer({ id: "neutral-land-fill", type: "fill", source: "neutral-land", paint: { "fill-color": "#eee8dc", "fill-opacity": 1 } });
    map.addLayer({ id: "neutral-land-line", type: "line", source: "neutral-land", paint: { "line-color": "#777e78", "line-width": 0.75 } });
    renderCandidate(candidate);
    slider.addEventListener("input", () => { yearLabel.value = formatYear(Number(slider.value)); yearLabel.textContent = yearLabel.value; });
    fitWorldButton.addEventListener("click", () => map.easeTo({ center: [15, 24], zoom: 1.35, duration: 420 }));
    fitActiveButton.disabled = true;
    fitActiveButton.title = "Historical target geometry is not yet promoted in the R1 candidate";
  } catch (error) {
    console.error(error);
    releaseBadge.textContent = "R1 candidate load error";
    releaseBadge.classList.add("preview");
    status.textContent = "Static candidate unavailable or invalid";
    panel.innerHTML = `<div class="panel-body"><div class="empty-state"><strong>Could not load the R1 MVP candidate.</strong><br>${escapeHtml(error instanceof Error ? error.message : error)}<br>No live API fallback is attempted because it could silently substitute a different historical data product.</div></div>`;
  }
}

void boot();
