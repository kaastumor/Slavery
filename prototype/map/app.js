import * as maplibregl from 'https://unpkg.com/maplibre-gl@6.10.0/dist/maplibre-gl.mjs';

const [land, brazil, slice] = await Promise.all([
  fetch('./data/world-land.geojson').then(r => r.json()),
  fetch('./data/brazil-modern-proxy.geojson').then(r => r.json()),
  fetch('./data/slice.json').then(r => r.json())
]);

const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: {},
    layers: [
      {
        id: 'background',
        type: 'background',
        paint: {'background-color': '#dce6ea'}
      }
    ]
  },
  center: [-52, -12],
  zoom: 2.2,
  minZoom: 1
});

map.addControl(new maplibregl.NavigationControl({showCompass: false}), 'top-right');

const yearInput = document.querySelector('#year');
const yearValue = document.querySelector('#year-value');
const panel = document.querySelector('#panel');

function activeForYear(year) {
  const from = slice.claim.from_year ?? Number.NEGATIVE_INFINITY;
  const to = slice.claim.to_year ?? Number.POSITIVE_INFINITY;
  return year >= from && year <= to;
}

function renderPanel() {
  const c = slice.claim;
  const g = slice.geometry;
  panel.replaceChildren();

  const kicker = document.createElement('p');
  kicker.className = 'panel-kicker';
  kicker.textContent = `${c.spatial_name} · ${c.claim_kind.replaceAll('_', ' ')}`;

  const title = document.createElement('h2');
  title.textContent = c.practice_label;

  const summary = document.createElement('p');
  summary.textContent = c.summary;

  const facts = document.createElement('dl');
  const rows = [
    ['Selected year', yearValue.textContent],
    ['Coverage', `${c.coverage_state} (legacy ${c.legacy_coverage})`],
    ['P-level', c.practice_level ?? 'Not yet assigned'],
    ['Geometry', g.accuracy_status.replaceAll('_', ' ')],
    ['Geometry method', g.resolution_method]
  ];
  for (const [label, value] of rows) {
    const dt = document.createElement('dt');
    dt.textContent = label;
    const dd = document.createElement('dd');
    dd.textContent = value;
    facts.append(dt, dd);
  }

  const sourceTitle = document.createElement('h3');
  sourceTitle.textContent = 'Evidence source';

  const source = document.createElement('a');
  source.href = c.source.exact_url;
  source.target = '_blank';
  source.rel = 'noreferrer';
  source.textContent = c.source.title;

  const caveat = document.createElement('p');
  caveat.className = 'caveat';
  caveat.textContent = slice.caveats.join(' ');

  panel.append(kicker, title, summary, facts, sourceTitle, source, caveat);
}

function updateYear() {
  const year = Number(yearInput.value);
  yearValue.textContent = String(year);
  const visible = activeForYear(year);
  map.setLayoutProperty('practice-fill', 'visibility', visible ? 'visible' : 'none');
  map.setLayoutProperty('practice-outline', 'visibility', visible ? 'visible' : 'none');
  if (!visible) {
    panel.innerHTML = '<p class="panel-kicker">No active claim in this prototype</p><h2>Choose 1900 or later</h2><p>The world land outline remains visible even when the selected claim is outside its evidence interval.</p>';
  } else if (panel.dataset.open === 'true') {
    renderPanel();
  }
}

map.on('load', () => {
  map.addSource('land', {type: 'geojson', data: land});
  map.addLayer({
    id: 'land-fill',
    type: 'fill',
    source: 'land',
    paint: {'fill-color': '#f3f0e7', 'fill-opacity': 1}
  });
  map.addLayer({
    id: 'land-outline',
    type: 'line',
    source: 'land',
    paint: {'line-color': '#aaa69b', 'line-width': 0.7}
  });

  map.addSource('practice', {type: 'geojson', data: brazil});
  map.addLayer({
    id: 'practice-fill',
    type: 'fill',
    source: 'practice',
    paint: {
      'fill-color': '#8f4c3d',
      'fill-opacity': 0.7
    }
  });
  map.addLayer({
    id: 'practice-outline',
    type: 'line',
    source: 'practice',
    paint: {
      'line-color': '#5e2f27',
      'line-width': 1.5
    }
  });

  map.on('mouseenter', 'practice-fill', () => { map.getCanvas().style.cursor = 'pointer'; });
  map.on('mouseleave', 'practice-fill', () => { map.getCanvas().style.cursor = ''; });
  map.on('click', 'practice-fill', () => {
    panel.dataset.open = 'true';
    renderPanel();
  });

  yearInput.addEventListener('input', updateYear);
  updateYear();
});
