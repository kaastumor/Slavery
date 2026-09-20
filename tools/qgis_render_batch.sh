#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "Usage: $0 INPUT_FEATURECOLLECTION LAND_GEOJSON OUTPUT_GEOJSON SNAP_TOLERANCE_M" >&2
  exit 2
fi

INPUT=$1
LAND=$2
OUTPUT=$3
TOLERANCE=$4

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

python3 - "$INPUT" "$workdir" <<'PY'
import json
import pathlib
import re
import sys

src = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
payload = json.loads(src.read_text(encoding="utf-8"))
features = payload.get("features", [])
if not features:
    raise SystemExit("feature collection is empty")

manifest = []
for index, feature in enumerate(features):
    props = feature.get("properties") or {}
    gid = str(props.get("geometry_id") or f"feature-{index}")
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", gid)
    path = out / f"{index:03d}_{safe}.geojson"
    path.write_text(json.dumps({"type": "FeatureCollection", "features": [feature]}), encoding="utf-8")
    manifest.append(str(path))

(out / "manifest.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
PY

outputs=()
while IFS= read -r feature_file; do
  [[ -n "$feature_file" ]] || continue
  name=$(basename "$feature_file" .geojson)
  feature_out="$workdir/render_${name}.geojson"
  bash "$(dirname "$0")/qgis_render_pipeline.sh"     "$feature_file" "$LAND" "$feature_out" "$TOLERANCE"
  outputs+=("$feature_out")
done < "$workdir/manifest.txt"

python3 - "$OUTPUT" "${outputs[@]}" <<'PY'
import json
import pathlib
import sys

dest = pathlib.Path(sys.argv[1])
features = []
for filename in sys.argv[2:]:
    payload = json.loads(pathlib.Path(filename).read_text(encoding="utf-8"))
    for feature in payload.get("features", []):
        # Each single-feature QGIS output starts its own provider FID at 1.
        # FID is transport metadata, not atlas identity; remove it before merge
        # so the combined layer can be validated/imported without collisions.
        props = feature.get("properties") or {}
        props.pop("fid", None)
        feature["properties"] = props
        features.append(feature)

if not features:
    raise SystemExit("batch render produced no features")

dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps({"type": "FeatureCollection", "features": features}), encoding="utf-8")
print(f"Wrote {len(features)} features to {dest}")
PY
