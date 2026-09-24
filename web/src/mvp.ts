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
  absence_inference_prohibited?: boolean;
  qa_state?: string | null;
  effective_frame_class?: string | null;
  identity_limitation?: string | null;
  geometry_requirement?: string | null;
};

type ReviewedSource = {
  source_version_ref: string;
  title: string;
  author?: string | null;
  year?: string | number | null;
  url?: string | null;
  role?: string | null;
  direction?: string | null;
  decisive?: boolean;
  claim_fitness?: string | null;
  independence_group?: string | null;
  locator?: string | null;
  notes?: string | null;
};

type ReviewedC1 = {
  target_id: string;
  target_label: string;
  anchor: string | number;
  classification_outcome: string;
  bounded_proposition: string;
  required_abstention: string;
  evidence_locus: string;
  inference_extent: string;
  law_practice_note?: string | null;
  network_territorial_note?: string | null;
  review_state: string;
  language_access_limitations: string;
  coverage_confidence: string;
  sources: ReviewedSource[];
};

type OverviewState = {
  id: string;
  label: string;
  description: string;
  count: number;
};

type GeometryRow = {
  target_id: string;
  representation_state: string;
  expected_geometry_form?: string | null;
  representation_note?: string | null;
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
  reviewed_c1: ReviewedC1[];
  geometry_manifest: {
    policy: {
      unresolved_is_not_absence: boolean;
      neutral_world_land_always_visible: boolean;
    };
    rows: GeometryRow[];
  };
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
  if (!candidate.geometry_manifest || !Array.isArray(candidate.geometry_manifest.rows) || candidate.geometry_manifest.rows.length !== candidate.counts.targets) {
    throw new Error("Candidate geometry manifest is missing or incomplete");
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

function stateLabel(candidate: CandidateBundle, targetId: string): string {
  const overview = candidate.overview_semantics.targets.find((item) => item.target_id === targetId);
  const definition = candidate.overview_semantics.research_states.find((item) => item.id === overview?.research_state);
  return definition?.label ?? "Unknown research state";
}

function geometryFor(candidate: CandidateBundle, targetId: string): GeometryRow | undefined {
  return candidate.geometry_manifest.rows.find((row) => row.target_id === targetId);
}

function renderSource(source: ReviewedSource): string {
  const title = escapeHtml(source.title || source.source_version_ref);
  const linkedTitle = source.url
    ? `<a class="source-link" href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${title}</a>`
    : `<span class="source-link">${title}</span>`;
  const authorYear = [source.author, source.year].filter((value) => value !== null && value !== undefined && value !== "").map(escapeHtml).join(" · ");
  const family = source.independence_group ? `Source family: ${escapeHtml(source.independence_group)}` : "Source family not recorded";
  const roleFitness = [source.role, source.claim_fitness, source.decisive ? "decisive" : null].filter(Boolean).map(escapeHtml).join(" · ");
  return `
    <li>
      <div class="source-line">${linkedTitle}</div>
      ${authorYear ? `<div class="source-meta">${authorYear}</div>` : ""}
      <div class="source-meta">${escapeHtml(source.source_version_ref)}</div>
      ${source.locator ? `<div class="source-meta">Locator: ${escapeHtml(source.locator)}</div>` : ""}
      <div class="source-meta">${family}${roleFitness ? ` · ${roleFitness}` : ""}</div>
    </li>`;
}

function bindRegisterButtons(candidate: CandidateBundle): void {
  panel.querySelectorAll<HTMLButtonElement>("[data-target-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const targetId = button.dataset.targetId;
      if (targetId) renderTargetDetail(candidate, targetId);
    });
  });
}

function renderRegister(candidate: CandidateBundle): string {
  const ordered = [...candidate.targets].sort((a, b) => {
    const aYear = Number(a.anchor);
    const bYear = Number(b.anchor);
    if (Number.isFinite(aYear) && Number.isFinite(bYear) && aYear !== bYear) return aYear - bYear;
    return a.target_label.localeCompare(b.target_label);
  });

  return ordered.map((target) => {
    const geometry = geometryFor(candidate, target.target_id);
    return `
      <button class="place-card" type="button" data-target-id="${escapeHtml(target.target_id)}" aria-label="Open evidence record for ${escapeHtml(target.target_label)}">
        <span class="place-card-top">
          <span class="place-card-name">${escapeHtml(target.target_label)}</span>
          <span class="place-card-level">${escapeHtml(formatYear(target.anchor))}</span>
        </span>
        <span class="place-card-meta">${escapeHtml(stateLabel(candidate, target.target_id))} · geometry: ${escapeHtml(geometry?.representation_state ?? "unknown")}</span>
      </button>`;
  }).join("");
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
      <h2>Evidence register</h2>
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
      <section class="register-section" aria-labelledby="register-heading">
        <h3 id="register-heading" class="overview-heading">Frozen target register</h3>
        <p class="method-note">Open a target to inspect its permitted evidence/research state. Unresearched and held targets intentionally expose less information.</p>
        <div class="place-list">${renderRegister(candidate)}</div>
      </section>
      <p class="source-meta">${escapeHtml(candidate.non_absence_rule)}</p>
    </div>`;
  bindRegisterButtons(candidate);
}

function renderTargetDetail(candidate: CandidateBundle, targetId: string): void {
  const target = candidate.targets.find((item) => item.target_id === targetId);
  if (!target) return;
  const reviewed = candidate.reviewed_c1.find((item) => item.target_id === targetId);
  const geometry = geometryFor(candidate, targetId);
  const researchLabel = stateLabel(candidate, targetId);

  const geometryBlock = `
    <details class="geometry-details">
      <summary>Geometry representation</summary>
      <div class="geometry-body">
        <strong>${escapeHtml(geometry?.representation_state ?? "unknown")}</strong><br>
        ${escapeHtml(geometry?.representation_note ?? "No geometry note is available.")}
        ${geometry?.expected_geometry_form ? `<br>Expected form if later reviewed: ${escapeHtml(geometry.expected_geometry_form)}` : ""}
        <br>Geometry availability does not create or strengthen a historical claim.
      </div>
    </details>`;

  if (!reviewed) {
    panel.innerHTML = `
      <div class="panel-header">
        <button class="back-button" id="register-back" type="button">← Back to register</button>
        <div class="panel-kicker">Research-state record · no subject claim</div>
        <h2>${escapeHtml(target.target_label)}</h2>
        <div class="panel-subhead">${escapeHtml(formatYear(target.anchor))} · ${escapeHtml(researchLabel)}</div>
      </div>
      <div class="panel-body">
        <div class="claim-card">
          <div class="evidence-title">Permitted interpretation</div>
          <p class="claim-summary">${escapeHtml(target.interpretation)}</p>
        </div>
        <div class="detail-grid">
          <div><div class="evidence-title">QA state</div><p class="detail-text">${escapeHtml(target.qa_state ?? "not recorded")}</p></div>
          <div><div class="evidence-title">Frame</div><p class="detail-text">${escapeHtml(target.effective_frame_class ?? "not recorded")}</p></div>
        </div>
        ${target.identity_limitation ? `<div class="claim-card"><div class="evidence-title">Identity / frame limitation</div><p class="claim-summary">${escapeHtml(target.identity_limitation)}</p></div>` : ""}
        <div class="empty-state nonabsence-note"><strong>No historical absence inference.</strong><br>This target has no reviewed C1 subject packet in the candidate. Its research state must not be rendered as evidence that slavery/coercion was absent.</div>
        ${geometryBlock}
        <div class="release-inline">Candidate / non-canonical. No independent historical review is claimed.</div>
      </div>`;
  } else {
    const sources = reviewed.sources.map(renderSource).join("");
    const extraNotes = [
      reviewed.law_practice_note ? `<div><div class="evidence-title">Law / practice note</div><p class="detail-text">${escapeHtml(reviewed.law_practice_note)}</p></div>` : "",
      reviewed.network_territorial_note ? `<div><div class="evidence-title">Network / territorial note</div><p class="detail-text">${escapeHtml(reviewed.network_territorial_note)}</p></div>` : "",
    ].filter(Boolean).join("");

    panel.innerHTML = `
      <div class="panel-header">
        <button class="back-button" id="register-back" type="button">← Back to register</button>
        <div class="panel-kicker">Reviewed C1 evidence record</div>
        <h2>${escapeHtml(reviewed.target_label)}</h2>
        <div class="panel-subhead">${escapeHtml(formatYear(reviewed.anchor))} · ${escapeHtml(researchLabel)} · ${escapeHtml(reviewed.classification_outcome)}</div>
      </div>
      <div class="panel-body">
        <div class="claim-card">
          <div class="evidence-title">Strongest bounded proposition</div>
          <p class="claim-summary">${escapeHtml(reviewed.bounded_proposition)}</p>
        </div>
        <div class="claim-card abstention-card">
          <div class="evidence-title">Required abstention</div>
          <p class="claim-summary">${escapeHtml(reviewed.required_abstention)}</p>
        </div>
        <div class="detail-grid">
          <div><div class="evidence-title">Evidence locus</div><p class="detail-text">${escapeHtml(reviewed.evidence_locus)}</p></div>
          <div><div class="evidence-title">Inference extent</div><p class="detail-text">${escapeHtml(reviewed.inference_extent)}</p></div>
          ${extraNotes}
        </div>
        <div class="claim-card">
          <div class="evidence-title">Research limitations</div>
          <p class="claim-summary">${escapeHtml(reviewed.language_access_limitations)}</p>
          <div class="source-meta">Coverage confidence: ${escapeHtml(reviewed.coverage_confidence)} · Review: ${escapeHtml(reviewed.review_state)} (internal adversarial review only; not independent review)</div>
        </div>
        <div class="evidence-title">Source/version evidence</div>
        <ul class="source-list">${sources}</ul>
        ${geometryBlock}
        <div class="release-inline">Candidate / non-canonical. Source-family labels expose shared evidentiary dependencies; publication count is not independent support.</div>
      </div>`;
  }

  panel.querySelector<HTMLButtonElement>("#register-back")?.addEventListener("click", () => {
    renderCandidate(candidate);
    panel.focus();
  });
  panel.focus();
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
