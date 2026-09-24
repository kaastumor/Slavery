import { LngLatBounds, Map, NavigationControl, Popup, setWorkerUrl } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url";
import "./styles.css";
import "./research-preview.css";

setWorkerUrl(workerUrl);

type PreviewSource = {
  source_id: string;
  source_version_ref: string;
  title: string;
  url?: string;
  locator?: string;
  source_classification?: string;
  evidence_role?: string;
  claim_fitness?: string;
  independence_group?: string;
  direction?: string;
  decisive?: string;
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

type PreviewTarget = {
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
  research_stage: "researched_internal" | "under_review";
  navigation_references: NavigationReference[];
  sources: PreviewSource[];
};

type PreviewBundle = {
  schema: "historical-slavery-atlas.exp04-research-preview.v1";
  preview_id: string;
  publication_state: string;
  canonical_historical_release: string;
  review_scope: string;
  method_disposition: string;
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
    researched_internal: number;
    under_review: number;
    independently_reviewed: number;
    source_relation_rows: number;
  };
  targets: PreviewTarget[];
};

const DATA_URL = new URL("./data/exp04-research-preview.json", window.location.href).toString();
const LAND_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson";

const panel = document.querySelector<HTMLElement>("#preview-panel")!;
const releaseBadge = document.querySelector<HTMLElement>("#release-badge")!;
const status = document.querySelector<HTMLElement>("#status")!;
const fitReferencesButton = document.querySelector<HTMLButtonElement>("#fit-references")!;
const fitWorldButton = document.querySelector<HTMLButtonElement>("#fit-world")!;

const hoverPopup = new Popup({ closeButton: false, closeOnClick: false, offset: 10 });
let bundle: PreviewBundle | null = null;
let selectedTargetId: string | null = null;

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

function validateBundle(value: unknown): PreviewBundle {
  if (!value || typeof value !== "object") throw new Error("Preview bundle is not an object");
  const candidate = value as Partial<PreviewBundle>;
  if (candidate.schema !== "historical-slavery-atlas.exp04-research-preview.v1") {
    throw new Error("Unsupported EXP-04 preview schema");
  }
  if (candidate.publication_state !== "experimental_non_canonical_research_preview") {
    throw new Error("Preview publication boundary is missing");
  }
  if (candidate.canonical_historical_release !== "v0.6.1") {
    throw new Error("Canonical release boundary drifted");
  }
  if (!candidate.counts || candidate.counts.targets !== 8) throw new Error("Expected eight frozen EXP-04 targets");
  if (candidate.counts.researched_internal !== 5 || candidate.counts.under_review !== 3) {
    throw new Error("EXP-04 research-stage counts drifted");
  }
  if (candidate.counts.independently_reviewed !== 0) throw new Error("Preview must not imply independent historical review");
  if (!Array.isArray(candidate.targets) || candidate.targets.length !== 8) throw new Error("Preview target membership is incomplete");
  if (!candidate.map_semantics?.neutral_world_land_always_visible) throw new Error("Neutral-land guard missing");
  if (!candidate.map_semantics?.navigation_references_are_not_historical_geometry) {
    throw new Error("Navigation-reference geometry guard missing");
  }
  if (candidate.map_semantics.practice_polygons_materialized) throw new Error("Practice polygons are outside preview scope");
  if (candidate.map_semantics.visual_intensity_from_source_counts) throw new Error("Source-count intensity is prohibited");
  return candidate as PreviewBundle;
}

async function loadBundle(): Promise<PreviewBundle> {
  const response = await fetch(DATA_URL, { cache: "no-store" });
  if (!response.ok) throw new Error(`EXP-04 preview bundle returned ${response.status}`);
  return validateBundle(await response.json());
}

function stageLabel(stage: PreviewTarget["research_stage"]): string {
  return stage === "researched_internal" ? "Internally researched" : "Under review";
}

function sourceHtml(source: PreviewSource): string {
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

function renderTable(data: PreviewBundle): void {
  const rows = data.targets.map((target) => `
    <tr data-target-row="${escapeHtml(target.target_id)}">
      <td><button class="table-target" type="button" data-target-id="${escapeHtml(target.target_id)}">${escapeHtml(target.target_label)}</button></td>
      <td>${escapeHtml(target.anchor)}</td>
      <td><span class="research-stage ${target.research_stage === "under_review" ? "under-review" : "researched"}">${escapeHtml(stageLabel(target.research_stage))}</span></td>
      <td>${escapeHtml(labelize(target.effective_frame_class))}</td>
      <td>${escapeHtml(labelize(target.temporal_state))}</td>
    </tr>
  `).join("");

  panel.innerHTML = `
    <div class="panel-header">
      <div class="panel-kicker">EXP-04 · eight frozen frontier cases</div>
      <h2>Research table</h2>
      <div class="panel-subhead">Presentation test only. Rows are not a canonical release and marker position does not define historical extent.</div>
    </div>
    <div class="panel-body">
      <div class="overview-stats">
        <span><strong>${data.counts.targets}</strong><br>targets</span>
        <span><strong>${data.counts.researched_internal}</strong><br>internally researched</span>
        <span><strong>${data.counts.under_review}</strong><br>under review</span>
        <span><strong>${data.counts.independently_reviewed}</strong><br>independently reviewed</span>
      </div>
      <div class="empty-state nonabsence-note"><strong>Non-absence rule:</strong> ${escapeHtml(data.non_absence_rule)}</div>
      <div class="table-scroll">
        <table class="preview-table">
          <thead><tr><th>Target</th><th>Anchor</th><th>Research stage</th><th>Frame</th><th>Temporal state</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
      <p class="method-note">${escapeHtml(data.map_semantics.rule)}</p>
      <div class="release-inline">Canonical historical release remains ${escapeHtml(data.canonical_historical_release)}. EXP-04 has no canonical data effect.</div>
    </div>`;

  panel.querySelectorAll<HTMLButtonElement>("[data-target-id]").forEach((button) => {
    button.addEventListener("click", () => selectTarget(button.dataset.targetId ?? null));
  });
}

function renderTarget(target: PreviewTarget): void {
  const sources = target.sources.length
    ? target.sources.map(sourceHtml).join("")
    : "<li>No source relation rows recorded.</li>";

  panel.innerHTML = `
    <div class="panel-header">
      <button class="back-button" id="preview-back" type="button">← Back to research table</button>
      <div class="panel-kicker">EXP-04 target · ${escapeHtml(target.anchor)}</div>
      <h2>${escapeHtml(target.target_label)}</h2>
      <div class="panel-subhead">${escapeHtml(stageLabel(target.research_stage))} · ${escapeHtml(labelize(target.effective_frame_class))}</div>
    </div>
    <div class="panel-body">
      <div class="claim-card ${target.research_stage === "under_review" ? "abstention-card" : ""}">
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
          ${escapeHtml(target.geometry_unresolved_note || "No historical practice geometry is materialized for this preview.")}
          <br><strong>Displayed markers are navigation references only.</strong> They do not create historical extent or strengthen the evidence.
        </div>
      </details>

      <div class="evidence-title">Source/version evidence</div>
      <ul class="source-list">${sources}</ul>

      <div class="release-inline">Internal research preview only · no independent historical review · no P-level or canonical promotion.</div>
    </div>`;

  panel.querySelector<HTMLButtonElement>("#preview-back")?.addEventListener("click", () => {
    selectedTargetId = null;
    if (bundle) renderTable(bundle);
    fitAllReferences();
    panel.focus();
  });
}

function featureCollection(data: PreviewBundle): GeoJSON.FeatureCollection<GeoJSON.Point> {
  return {
    type: "FeatureCollection",
    features: data.targets.flatMap((target) =>
      target.navigation_references.map((reference) => ({
        type: "Feature" as const,
        geometry: { type: "Point" as const, coordinates: [reference.lon, reference.lat] },
        properties: {
          target_id: target.target_id,
          target_label: target.target_label,
          anchor: target.anchor,
          research_stage: target.research_stage,
          reference_label: reference.label,
          reference_note: reference.note,
        },
      })),
    ),
  };
}

function fitTarget(target: PreviewTarget): void {
  const bounds = new LngLatBounds();
  target.navigation_references.forEach((reference) => bounds.extend([reference.lon, reference.lat]));
  if (target.navigation_references.length === 1) {
    const reference = target.navigation_references[0];
    map.easeTo({ center: [reference.lon, reference.lat], zoom: 4.3, duration: 350 });
  } else {
    map.fitBounds(bounds, { padding: 70, maxZoom: 4.1, duration: 350 });
  }
}

function fitAllReferences(): void {
  if (!bundle) return;
  const bounds = new LngLatBounds();
  let count = 0;
  bundle.targets.forEach((target) => target.navigation_references.forEach((reference) => {
    bounds.extend([reference.lon, reference.lat]);
    count += 1;
  }));
  if (count > 0) map.fitBounds(bounds, { padding: 45, maxZoom: 2.2, duration: 350 });
}

function selectTarget(targetId: string | null): void {
  if (!bundle || !targetId) return;
  const target = bundle.targets.find((item) => item.target_id === targetId);
  if (!target) return;
  selectedTargetId = targetId;
  renderTarget(target);
  fitTarget(target);
  panel.focus();
}

function attachMapInteractions(): void {
  map.on("click", "preview-references", (event) => {
    const id = event.features?.[0]?.properties?.target_id as string | undefined;
    if (id) selectTarget(id);
  });

  map.on("mouseenter", "preview-references", (event) => {
    map.getCanvas().style.cursor = "pointer";
    const feature = event.features?.[0];
    if (!feature) return;
    hoverPopup
      .setLngLat(event.lngLat)
      .setHTML(
        `<strong>${escapeHtml(feature.properties?.target_label)}</strong><br>` +
        `${escapeHtml(feature.properties?.reference_label)}<br>` +
        `<small>Navigation only · ${escapeHtml(stageLabel(feature.properties?.research_stage as PreviewTarget["research_stage"]))}</small>`,
      )
      .addTo(map);
  });
  map.on("mousemove", "preview-references", (event) => hoverPopup.setLngLat(event.lngLat));
  map.on("mouseleave", "preview-references", () => {
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

    releaseBadge.textContent = `${data.preview_id} · non-canonical`;
    releaseBadge.title = `Canonical historical release remains ${data.canonical_historical_release}; EXP-04 is internal research only.`;
    status.textContent = `${data.counts.targets} targets · ${data.counts.researched_internal} internally researched · ${data.counts.under_review} under review`;

    map.addSource("neutral-land", { type: "geojson", data: LAND_URL });
    map.addLayer({
      id: "neutral-land-fill",
      type: "fill",
      source: "neutral-land",
      paint: { "fill-color": "#eee8dc", "fill-opacity": 1 },
    });
    map.addLayer({
      id: "neutral-land-line",
      type: "line",
      source: "neutral-land",
      paint: { "line-color": "#777e78", "line-width": 0.75 },
    });

    map.addSource("preview-references", { type: "geojson", data: featureCollection(data) });
    map.addLayer({
      id: "preview-references",
      type: "circle",
      source: "preview-references",
      paint: {
        "circle-radius": 7,
        "circle-color": [
          "match",
          ["get", "research_stage"],
          "under_review", "#b88632",
          "#527a76",
        ],
        "circle-opacity": 0.95,
        "circle-stroke-width": 2,
        "circle-stroke-color": "#fffdf8",
      },
    });

    attachMapInteractions();
    renderTable(data);
    fitAllReferences();

    fitReferencesButton.addEventListener("click", fitAllReferences);
    fitWorldButton.addEventListener("click", () => map.easeTo({ center: [15, 24], zoom: 1.35, duration: 350 }));
  } catch (error) {
    console.error(error);
    releaseBadge.textContent = "EXP-04 preview load error";
    status.textContent = "Failed to load research preview";
    panel.innerHTML = `<div class="panel-body"><div class="empty-state">Could not load the EXP-04 preview.<br>${escapeHtml(error instanceof Error ? error.message : error)}</div></div>`;
  }
}

void boot();
