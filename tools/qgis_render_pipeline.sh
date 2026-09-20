#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  tools/qgis_render_pipeline.sh INPUT_GEOJSON LAND_GEOJSON OUTPUT_GEOJSON [SNAP_TOLERANCE_M]

Runs a standard, offline QGIS render-preprocessing pipeline:
  1. reproject both layers to EPSG:8857 (metric Equal Earth)
  2. smooth the historical polygon with QGIS native:smoothgeometry
  3. snap it to the canonical land layer with native:snapgeometries
     using "prefer closest point, insert extra vertices where required"
  4. fix geometry
  5. clip to the canonical land layer
  6. reproject output to EPSG:4326

This creates display geometry only. Never overwrite canonical/source geometry.
EOF
}

if [[ $# -lt 3 || $# -gt 4 ]]; then
  usage >&2
  exit 2
fi

INPUT=$1
LAND=$2
OUTPUT=$3
SNAP_TOLERANCE_M=${4:-15000}

command -v qgis_process >/dev/null 2>&1 || {
  echo "qgis_process is required (use the official qgis/qgis container in CI)." >&2
  exit 127
}

for path in "$INPUT" "$LAND"; do
  [[ -f "$path" ]] || { echo "Missing input: $path" >&2; exit 2; }
done

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

hist_metric="$workdir/historical_metric.gpkg"
land_subset="$workdir/land_subset.geojson"
land_metric="$workdir/land_metric.gpkg"
smoothed="$workdir/historical_smoothed.gpkg"
snapped="$workdir/historical_snapped.gpkg"
fixed="$workdir/historical_fixed.gpkg"
clipped="$workdir/historical_clipped.gpkg"
final_fixed="$workdir/historical_final_fixed.gpkg"
wgs84="$workdir/historical_wgs84.gpkg"

export QT_QPA_PLATFORM=offscreen

# Limit the global physical reference to the historical layer's neighborhood
# before QGIS snapping. This is a standard spatial-index optimization only:
# it does not alter reference coordinates or the resulting topology.
read -r minx miny maxx maxy < <(python3 - "$INPUT" <<'PY'
import json
import sys

payload = json.load(open(sys.argv[1], encoding="utf-8"))
xs, ys = [], []

def visit(coords):
    if coords and isinstance(coords[0], (int, float)):
        xs.append(float(coords[0]))
        ys.append(float(coords[1]))
        return
    for item in coords:
        visit(item)

for feature in payload.get("features", []):
    geom = feature.get("geometry")
    if geom:
        visit(geom.get("coordinates", []))

if not xs:
    raise SystemExit("input contains no coordinates")

pad = 2.0
print(min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)
PY
)

ogr2ogr -f GeoJSON "$land_subset" "$LAND" -spat "$minx" "$miny" "$maxx" "$maxy"

qgis_process run native:reprojectlayer -- \
  INPUT="$INPUT" \
  TARGET_CRS="EPSG:8857" \
  OUTPUT="$hist_metric"

qgis_process run native:reprojectlayer -- \
  INPUT="$land_subset" \
  TARGET_CRS="EPSG:8857" \
  OUTPUT="$land_metric"

# Conservative first-pass defaults for evaluation, not yet canonical policy.
# QGIS exposes all parameters so tuning stays explicit and reproducible.
qgis_process run native:smoothgeometry -- \
  INPUT="$hist_metric" \
  ITERATIONS=1 \
  OFFSET=0.20 \
  MAX_ANGLE=120 \
  OUTPUT="$smoothed"

qgis_process run native:snapgeometries -- \
  INPUT="$smoothed" \
  REFERENCE_LAYER="$land_metric" \
  TOLERANCE="$SNAP_TOLERANCE_M" \
  BEHAVIOR=1 \
  OUTPUT="$snapped"

qgis_process run native:fixgeometries -- \
  INPUT="$snapped" \
  OUTPUT="$fixed"

qgis_process run native:clip -- \
  INPUT="$fixed" \
  OVERLAY="$land_metric" \
  OUTPUT="$clipped"

# Overlay operations can reintroduce ring self-intersections even when both
# inputs were valid. Repair once more after clipping before export.
qgis_process run native:fixgeometries -- \
  INPUT="$clipped" \
  OUTPUT="$final_fixed"

qgis_process run native:reprojectlayer -- \
  INPUT="$final_fixed" \
  TARGET_CRS="EPSG:4326" \
  OUTPUT="$wgs84"

# Reprojection/export precision can expose tiny ring defects. Run the standard
# repair once more in the delivery CRS before emitting GeoJSON.
qgis_process run native:fixgeometries -- \
  INPUT="$wgs84" \
  OUTPUT="$OUTPUT"

echo "Wrote standard-QGIS render geometry: $OUTPUT"
