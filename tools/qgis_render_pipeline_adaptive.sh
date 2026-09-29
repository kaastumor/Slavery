#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  tools/qgis_render_pipeline_adaptive.sh INPUT_GEOJSON LAND_GEOJSON OUTPUT_GEOJSON REPORT_JSON

Runs the standard QGIS render pipeline at a conservative 25 km baseline and
larger snapping tolerances (30/35/40/50 km), then selects the largest candidate
whose additional recovered land is <=2% of the baseline display area.

Every candidate is produced only with the standard QGIS smooth/snap/fix/clip
pipeline. Source geometry is never overwritten.
EOF
}

if [[ $# -ne 4 ]]; then
  usage >&2
  exit 2
fi

INPUT=$1
LAND=$2
OUTPUT=$3
REPORT=$4

command -v qgis_process >/dev/null 2>&1 || {
  echo "qgis_process is required." >&2
  exit 127
}

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

baseline="$workdir/render_25000.geojson"
bash tools/qgis_render_pipeline.sh "$INPUT" "$LAND" "$baseline" 25000

candidates=()
for tolerance in 30000 35000 40000 50000; do
  path="$workdir/render_${tolerance}.geojson"
  bash tools/qgis_render_pipeline.sh "$INPUT" "$LAND" "$path" "$tolerance"
  candidates+=(--candidate "${tolerance}=${path}")
done

python3 tools/select_adaptive_qgis_coastal_candidate.py \
  --baseline "$baseline" \
  "${candidates[@]}" \
  --max-extra-pct 2.0 \
  --output "$OUTPUT" \
  --report "$REPORT"
