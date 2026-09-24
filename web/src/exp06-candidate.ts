import { LngLatBounds, Map, NavigationControl, Popup, setWorkerUrl } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url";
import "./styles.css";
import "./research-preview.css";
import "./exp06-candidate.css";

setWorkerUrl(workerUrl);

type SourceRow = {
  source_id: string;
  source_version_ref: string;
  title: string;
  url?: string;
  locator?: string;
  evidence_role?: string;
  claim_fitness?: string;
  independence_group?: string;
  access_limitation?: string;
  dependency_note?: string;
};

type NavigationReference = {
  label: string;
  lat: number;
  lon: number;
  role: "navigation_reference_only";
  geometry_claim_role: "none";
  note: string;
};

type DisplayState = "researched_bounded" | "researched_inconclusive" | "under_review";

type TargetRow = {
  target_id: string;
  target_label: string;
  anchor: string;
  research_outcome: string;
  effective_frame_class: string;
  bounded_proposition: string;
  required_abstention: string;
  evidence_locus: string;
  inference_extent: string;
  temporal_state: string;
  law_practice_note: string;
  network_territorial_note: string;
  historical_terms: string;
  category_mapping_status: string;
  category_mapping_note: string;
  language_access_limitations: string;
  coverage_confidence: string;
  geometry_resolved_form: string;
  geometry_claim_role: string;
  geometry_unresolved_note: string;
  research_stage: string;
  display_state: DisplayState;
  navigation_references: NavigationReference[];
  sources: SourceRow[];
};

type CandidateBundle = {
  schema: "historical-slavery-atlas.exp06-candidate.v1";
  candidate_id: string;
  publication_state: string;
  canonical_historical_release: string;
  source_historical_commit: string;
  review_scope: string;
  non_absence_rule: string;
  map_semantics: {
    neutral_world_land_always_visible: boolean;
    navigation_references_are_not_historical_geometry: boolean;
    practice_polygons_materialized: boolean;
    visual_intensity_from_source_counts: boolean;
    rule: string;
  };
  counts: {
    targets: number;
    researched_bounded: number;
    researched_inconclusive: number;
    under_review: number;
    independently_reviewed: number;
    source_relation_rows: number;
  };
  targets: TargetRow[];
};

const DATA_URL = new URL("./data/exp06-candidate.json", window.location.href).toString();
const LAND_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson";

const panel = document.querySelector<HTMLElement>("#candidate-panel")!;
const releaseBadge = document.querySelector<HTMLElement>("#release-badge")!;
const status = document.querySelector<HTMLElement>("#status")!;
const fitReferencesButton = document.querySelector<HTMLButtonElement>("#fit-references")!;
const fitWorldButton = document.querySelector<HTMLButtonElement>("#fit-world")!;

const hoverPopup = new Popup({ closeButton: false, closeOnClick: false, offset: 10 });
let bundle: CandidateBundle | null = null;

const map = new Map({
  container: "map",
  style: {
    version: 8,
    sources: {},
    layers: [{ id: "background", type: "background", paint: { "background-color": "#cfdcdf" } }],
  },
  center: [25, 15],
  zoom: 1.15,
  minZoom: 1,
  maxZoom: 8,
});
map.addControl(new NavigationControl({ showCompass: false }), "top-left");

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
  return value.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function stateLabel(state: DisplayState): string {
  if (state === "under_review") return "Under review";
  if (state === "researched_inconclusive") return "Researched inconclusive";
  return "Internally researched · bounded";
}

function validateBundle(value: unknown): CandidateBundle {
  if (!value || typeof value !== "object") throw new Error("Candidate bundle is not an object");
  const data = value as Partial<CandidateBundle>;
  if (data.schema !== "historical-slavery-atlas.exp06-candidate.v1") throw new Error("Unexpected candidate schema");
  if (data.candidate_id !== "exp06-candidate-v1") throw new Error("Unexpected candidate identity");
  if (data.publication_state !== "candidate_noncanonical_pending_gate") throw new Error("Candidate publication boundary missing");
  if (data.canonical_historical_release !== "v0.6.1") throw new Error("Canonical release boundary drifted");
  if (!data.counts || data.counts.targets !== 6) throw new Error("Expected six frozen candidate targets");
  if (data.counts.researched_bounded !== 3 || data.counts.researched_inconclusive !== 1 || data.counts.under_review !== 2) {
    throw new Error("Candidate research-state counts drifted");
  }
  if (data.counts.independently_reviewed !== 0) throw new Error("Candidate must not imply independent review");
  if (!Array.isArray(data.targets) || data.targets.length !== 6) throw new Error("Candidate target membership incomplete");
  if (!data.map_semantics?.neutral_world_land_always_visible) throw new Error("Neutral-land guard missing");
  if (!data.map_semantics?.navigation_references_are_not_historical_geometry) throw new Error("Navigation-reference guard missing");
  if (data.map_semantics.practice_polygons_materialized) throw new Error("Practice polygons are outside candidate scope");
  if (data.map_semantics.visual_intensity_from_source_counts) throw new Error("Source-count intensity is prohibited");
  return data as CandidateBundle;
}

async function loadBundle(): Promise<CandidateBundle> {
  const response = await fetch(DATA_URL, { cache: "no-store" });
  if (!response.ok) throw new Error(`Candidate bundle returned ${response.status}`);
  return validateBundle(await response.json());
}

function sourceHtml(source: SourceRow): string {
  const title = escapeHtml(source.title || source.source_id);
  const linked = source.url
    ? `<a class="source-link" href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${title}</a>`
    : `<span class="source-link">${title}</span>`;

  const meta = [
    source.evidence_role ? labelize(source.evidence_role) : "",
    source.claim_fitness || "",
    source.independence_group ? `family: ${source.independence_group}` : "",
  ].filter(Boolean).map(escapeHtml).join(" · ");

  return `<li>
    <div class="source-line">${linked}</div>
    <div class="source-meta">${escapeHtml(source.source_version_ref)}</div>
    ${source.locator ? `<div class="source-meta">Locator: ${escapeHtml(source.locator)}</div>` : ""}
    ${meta ? `<div class="source-meta">${meta}</div>` : ""}
    ${source.access_limitation ? `<div class="source-meta">Access: ${escapeHtml(source.access_limitation)}</div>` : ""}
    ${source.dependency_note ? `<div class="source-meta">Dependency: ${escapeHtml(source.dependency_note)}</div>` : ""}
  </li>`;
}

function renderOverview(data: CandidateBundle): void {
  const rows = data.targets.map((target) => `
    <tr>
      <td><button class="table-target" type="button" data-target-id="${escapeHtml(target.target_id)}">${escapeHtml(target.target_label)}</button></td>
      <td>${escapeHtml(target.anchor)}</td>
      <td><span class="candidate-state ${escapeHtml(target.display_state)}">${escapeHtml(stateLabel(target.display_state))}</span></td>
      <td>${escapeHtml(labelize(target.effective_frame_class))}</td>
      <td>${escapeHtml(labelize(target.temporal_state))}</td>
    </tr>
  `).join("");

  panel.innerHTML = `
    <div class="panel-header">
      <div class="panel-kicker">Issue #227 · publish / hold / rework gate</div>
      <h2>EXP-06 evidence register</h2>
      <div class="panel-subhead">Exact non-canonical candidate from historical commit ${escapeHtml(data.source_historical_commit.slice(0, 7))}. Marker position is navigation only.</div>
    </div>
    <div class="panel-body">
      <div class="overview-stats candidate-stats">
        <span><strong>${data.counts.targets}</strong><br>targets</span>
        <span><strong>${data.counts.researched_bounded}</strong><br>bounded internal</span>
        <span><strong>${data.counts.researched_inconclusive}</strong><br>inconclusive</span>
        <span><strong>${data.counts.under_review}</strong><br>under review</span>
      </div>
      <div class="empty-state nonabsence-note"><strong>Non-absence rule:</strong> ${escapeHtml(data.non_absence_rule)}</div>
      <div class="table-scroll">
        <table class="preview-table">
          <thead><tr><th>Target</th><th>Anchor</th><th>Research state</th><th>Frame</th><th>Temporal state</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
      <p class="method-note">${escapeHtml(data.map_semantics.rule)}</p>
      <div class="release-inline"><strong>Candidate only.</strong> Canonical historical release remains ${escapeHtml(data.canonical_historical_release)}. Independent historical review: ${data.counts.independently_reviewed}.</div>
    </div>`;

  panel.querySelectorAll<HTMLButtonElement>("[data-target-id]").forEach((button) => {
    button.addEventListener("click", () => selectTarget(button.dataset.targetId ?? ""));
  });
}

function renderTarget(target: TargetRow): void {
  panel.innerHTML = `
    <div class="panel-header">
      <button class="back-button" id="candidate-back" type="button">← Back to evidence register</button>
      <div class="panel-kicker">EXP-06 candidate · ${escapeHtml(target.anchor)}</div>
      <h2>${escapeHtml(target.target_label)}</h2>
      <div class="panel-subhead"><span class="candidate-state ${escapeHtml(target.display_state)}">${escapeHtml(stateLabel(target.display_state))}</span> · ${escapeHtml(labelize(target.effective_frame_class))}</div>
    </div>
    <div class="panel-body">
      <div class="claim-card ${target.display_state !== "researched_bounded" ? "abstention-card" : ""}">
        <div class="evidence-title">Research outcome</div>
        <p class="claim-summary">${escapeHtml(labelize(target.research_outcome))}</p>
        <div class="source-meta">Temporal state: ${escapeHtml(labelize(target.temporal_state))}</div>
      </div>

      <div class="claim-card">
        <div class="evidence-title">Strongest bounded proposition</div>
        <p class="claim-summary">${escapeHtml(target.bounded_proposition)}</p>
      </div>

      <div class="claim-card abstention-card">
        <div class="evidence-title">Required abstention</div>
        <p class="claim-summary">${escapeHtml(target.required_abstention)}</p>
      </div>

      <div class="detail-grid">
        <div><div class="evidence-title">Evidence locus</div><p class="detail-text">${escapeHtml(target.evidence_locus)}</p></div>
        <div><div class="evidence-title">Inference extent</div><p class="detail-text">${escapeHtml(target.inference_extent)}</p></div>
        <div><div class="evidence-title">Law / practice</div><p class="detail-text">${escapeHtml(target.law_practice_note)}</p></div>
        <div><div class="evidence-title">Network / territory</div><p class="detail-text">${escapeHtml(target.network_territorial_note)}</p></div>
      </div>

      <div class="claim-card">
        <div class="evidence-title">Historical terms / category mapping</div>
        <p class="claim-summary">${escapeHtml(target.historical_terms)}</p>
        <div class="source-meta">${escapeHtml(labelize(target.category_mapping_status))}</div>
        <p class="detail-text">${escapeHtml(target.category_mapping_note)}</p>
      </div>

      <div class="claim-card">
        <div class="evidence-title">Coverage and access limitations</div>
        <p class="claim-summary">${escapeHtml(target.language_access_limitations)}</p>
        <div class="source-meta">Coverage: ${escapeHtml(labelize(target.coverage_confidence))}</div>
      </div>

      <details class="geometry-details" open>
        <summary>Map / geometry boundary</summary>
        <div class="geometry-body">
          ${escapeHtml(target.geometry_unresolved_note || "No historical practice geometry is materialized.")}
          <br><strong>Displayed markers are navigation references only.</strong>
        </div>
      </details>

      <div class="evidence-title">Source/version evidence · ${target.sources.length} rows</div>
      <ul class="source-list">${target.sources.map(sourceHtml).join("")}</ul>

      <div class="release-inline">Non-canonical candidate · internal research only · no independent historical review · no P-level or canonical promotion.</div>
    </div>`;

  panel.querySelector<HTMLButtonElement>("#candidate-back")?.addEventListener("click", () => {
    if (bundle) renderOverview(bundle);
    fitAllReferences();
    panel.focus();
  });
}

function collection(data: CandidateBundle): GeoJSON.FeatureCollection<GeoJSON.Point> {
  return {
    type: "FeatureCollection",
    features: data.targets.flatMap((target) => target.navigation_references.map((reference) => ({
      type: "Feature" as const,
      geometry: { type: "Point" as const, coordinates: [reference.lon, reference.lat] },
      properties: {
        target_id: target.target_id,
        target_label: target.target_label,
        display_state: target.display_state,
        reference_label: reference.label,
      },
    }))),
  };
}

function fitTarget(target: TargetRow): void {
  const bounds = new LngLatBounds();
  target.navigation_references.forEach((reference) => bounds.extend([reference.lon, reference.lat]));
  if (target.navigation_references.length === 1) {
    const ref = target.navigation_references[0];
    map.easeTo({ center: [ref.lon, ref.lat], zoom: 4.2, duration: 300 });
  } else {
    map.fitBounds(bounds, { padding: 70, maxZoom: 3.5, duration: 300 });
  }
}

function fitAllReferences(): void {
  if (!bundle) return;
  const bounds = new LngLatBounds();
  bundle.targets.forEach((target) => target.navigation_references.forEach((reference) => bounds.extend([reference.lon, reference.lat])));
  map.fitBounds(bounds, { padding: 45, maxZoom: 1.9, duration: 300 });
}

function selectTarget(targetId: string): void {
  const target = bundle?.targets.find((row) => row.target_id === targetId);
  if (!target) return;
  renderTarget(target);
  fitTarget(target);
  panel.focus();
}

function wireMap(): void {
  map.on("click", "candidate-references", (event) => {
    const id = event.features?.[0]?.properties?.target_id as string | undefined;
    if (id) selectTarget(id);
  });
  map.on("mouseenter", "candidate-references", (event) => {
    map.getCanvas().style.cursor = "pointer";
    const feature = event.features?.[0];
    if (!feature) return;
    hoverPopup
      .setLngLat(event.lngLat)
      .setHTML(
        `<strong>${escapeHtml(feature.properties?.target_label)}</strong><br>` +
        `${escapeHtml(feature.properties?.reference_label)}<br>` +
        `<small>Navigation only · ${escapeHtml(stateLabel(feature.properties?.display_state as DisplayState))}</small>`,
      )
      .addTo(map);
  });
  map.on("mousemove", "candidate-references", (event) => hoverPopup.setLngLat(event.lngLat));
  map.on("mouseleave", "candidate-references", () => {
    map.getCanvas().style.cursor = "";
    hoverPopup.remove();
  });
}

async function boot(): Promise<void> {
  try {
    const [data] = await Promise.all([
      loadBundle(),
      new Promise<void>((resolve) => map.once("load", () => resolve())),
    ]);
    bundle = data;

    releaseBadge.textContent = `${data.candidate_id} · pending gate`;
    releaseBadge.title = `Non-canonical candidate. Canonical historical release remains ${data.canonical_historical_release}.`;
    status.textContent = `${data.counts.researched_bounded} bounded · ${data.counts.researched_inconclusive} inconclusive · ${data.counts.under_review} under review`;

    map.addSource("neutral-land", { type: "geojson", data: LAND_URL });
    map.addLayer({ id: "neutral-land-fill", type: "fill", source: "neutral-land", paint: { "fill-color": "#eee8dc", "fill-opacity": 1 } });
    map.addLayer({ id: "neutral-land-line", type: "line", source: "neutral-land", paint: { "line-color": "#777e78", "line-width": 0.75 } });

    map.addSource("candidate-references", { type: "geojson", data: collection(data) });
    map.addLayer({
      id: "candidate-references",
      type: "circle",
      source: "candidate-references",
      paint: {
        "circle-radius": 7,
        "circle-color": [
          "match", ["get", "display_state"],
          "under_review", "#b88632",
          "researched_inconclusive", "#6f7681",
          "#527a76",
        ],
        "circle-opacity": 0.95,
        "circle-stroke-width": 2,
        "circle-stroke-color": "#fffdf8",
      },
    });

    wireMap();
    renderOverview(data);
    fitAllReferences();
    fitReferencesButton.addEventListener("click", fitAllReferences);
    fitWorldButton.addEventListener("click", () => map.easeTo({ center: [25, 15], zoom: 1.15, duration: 300 }));
  } catch (error) {
    console.error(error);
    releaseBadge.textContent = "Candidate load error";
    status.textContent = "Candidate unavailable";
    panel.innerHTML = `<div class="panel-body"><div class="empty-state">Could not load EXP-06 candidate.<br>${escapeHtml(error instanceof Error ? error.message : error)}</div></div>`;
  }
}

void boot();
