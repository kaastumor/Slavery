#!/usr/bin/env python3
"""Build scalable SVG review sheets for geometry render candidates.

Uses only the Python standard library so it can run inside the pinned QGIS CI
container without adding another plotting dependency. The output is review-only;
it never mutates source/candidate geometry.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import re
from pathlib import Path
from typing import Iterable

SVG_W = 1400
SVG_H = 860
MARGIN = 34
HEADER_H = 104
GAP = 26
PANEL_W = (SVG_W - 2 * MARGIN - GAP) / 2
PANEL_H = SVG_H - HEADER_H - MARGIN


def load_fc(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("type") != "FeatureCollection":
        raise SystemExit(f"expected FeatureCollection: {path}")
    return payload


def feature_id(feature: dict) -> str:
    props = feature.get("properties") or {}
    value = props.get("geometry_id")
    if value in (None, ""):
        raise SystemExit("every review feature requires properties.geometry_id")
    return str(value)


def geometry_rings(geometry: dict | None) -> list[list[list[float]]]:
    if not geometry:
        return []
    gtype = geometry.get("type")
    coords = geometry.get("coordinates") or []
    if gtype == "Polygon":
        return coords
    if gtype == "MultiPolygon":
        return [ring for poly in coords for ring in poly]
    return []


def bounds_from_rings(rings: Iterable[list[list[float]]]) -> tuple[float, float, float, float] | None:
    xs: list[float] = []
    ys: list[float] = []
    for ring in rings:
        for point in ring:
            if len(point) >= 2:
                xs.append(float(point[0]))
                ys.append(float(point[1]))
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def merge_bounds(*bounds: tuple[float, float, float, float] | None) -> tuple[float, float, float, float]:
    real = [b for b in bounds if b is not None]
    if not real:
        raise SystemExit("cannot render empty geometry")
    minx = min(b[0] for b in real)
    miny = min(b[1] for b in real)
    maxx = max(b[2] for b in real)
    maxy = max(b[3] for b in real)
    dx = max(maxx - minx, 0.2)
    dy = max(maxy - miny, 0.2)
    pad = max(dx, dy) * 0.08
    return minx - pad, miny - pad, maxx + pad, maxy + pad


def intersects(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])


def project(point: list[float], bbox: tuple[float, float, float, float], x0: float, y0: float, w: float, h: float) -> tuple[float, float]:
    minx, miny, maxx, maxy = bbox
    spanx = max(maxx - minx, 1e-9)
    spany = max(maxy - miny, 1e-9)
    scale = min(w / spanx, h / spany)
    draw_w = spanx * scale
    draw_h = spany * scale
    ox = x0 + (w - draw_w) / 2
    oy = y0 + (h - draw_h) / 2
    x = ox + (float(point[0]) - minx) * scale
    y = oy + draw_h - (float(point[1]) - miny) * scale
    return x, y


def path_data(rings: Iterable[list[list[float]]], bbox, x0, y0, w, h) -> str:
    parts: list[str] = []
    for ring in rings:
        if len(ring) < 2:
            continue
        points = [project(p, bbox, x0, y0, w, h) for p in ring]
        parts.append("M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in points) + " Z")
    return " ".join(parts)


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-")
    return value or "geometry"


def fmt_metric(value, suffix="") -> str:
    if value is None:
        return "n/a"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return str(value)
    if math.isfinite(v):
        return f"{v:.3f}{suffix}"
    return str(v)


def svg_for_feature(source: dict, candidate: dict, land_features: list[dict], decision: dict | None) -> str:
    props = source.get("properties") or {}
    name = str(props.get("name") or feature_id(source))
    gid = feature_id(source)
    src_rings = geometry_rings(source.get("geometry"))
    cand_rings = geometry_rings(candidate.get("geometry"))
    bbox = merge_bounds(bounds_from_rings(src_rings), bounds_from_rings(cand_rings))

    local_land: list[list[list[float]]] = []
    for feature in land_features:
        for ring in geometry_rings(feature.get("geometry")):
            rb = bounds_from_rings([ring])
            if rb and intersects(rb, bbox):
                local_land.append(ring)

    left_x = MARGIN
    right_x = MARGIN + PANEL_W + GAP
    panel_y = HEADER_H
    src_path_left = path_data(src_rings, bbox, left_x, panel_y, PANEL_W, PANEL_H)
    src_path_right = path_data(src_rings, bbox, right_x, panel_y, PANEL_W, PANEL_H)
    cand_path_right = path_data(cand_rings, bbox, right_x, panel_y, PANEL_W, PANEL_H)
    land_left = path_data(local_land, bbox, left_x, panel_y, PANEL_W, PANEL_H)
    land_right = path_data(local_land, bbox, right_x, panel_y, PANEL_W, PANEL_H)

    status = (decision or {}).get("status", "unclassified")
    metrics = (decision or {}).get("metrics") or {}
    metric_text = (
        f"status={status} · area Δ {fmt_metric(metrics.get('area_delta_pct'), '%')} · "
        f"sym diff {fmt_metric(metrics.get('symmetric_difference_pct'), '%')} · "
        f"Hausdorff {fmt_metric((metrics.get('hausdorff_m') or 0) / 1000.0, ' km')}"
    )
    reasons = (decision or {}).get("reasons") or []
    reason_text = " · quarantine: " + ", ".join(map(str, reasons)) if reasons else ""

    def esc(s: str) -> str:
        return html.escape(s, quote=True)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}">
  <rect width="100%" height="100%" fill="white"/>
  <style>
    text {{ font-family: system-ui, sans-serif; fill: #111; }}
    .title {{ font-size: 26px; font-weight: 700; }}
    .meta {{ font-size: 15px; fill: #333; }}
    .panel {{ font-size: 18px; font-weight: 600; }}
    .land {{ fill: #eeeeee; stroke: #555; stroke-width: 1.0; fill-rule: evenodd; vector-effect: non-scaling-stroke; }}
    .source {{ fill: #d9d9d9; fill-opacity: 0.34; stroke: #8a4b08; stroke-width: 2.0; fill-rule: evenodd; vector-effect: non-scaling-stroke; }}
    .candidate {{ fill: #b9d8f2; fill-opacity: 0.50; stroke: #145a86; stroke-width: 2.2; fill-rule: evenodd; vector-effect: non-scaling-stroke; }}
    .source-overlay {{ fill: none; stroke: #8a4b08; stroke-width: 1.4; stroke-dasharray: 7 5; fill-rule: evenodd; vector-effect: non-scaling-stroke; }}
    .frame {{ fill: none; stroke: #999; stroke-width: 1; }}
  </style>
  <text class="title" x="{MARGIN}" y="36">{esc(name)}</text>
  <text class="meta" x="{MARGIN}" y="62">geometry_id={esc(gid)}</text>
  <text class="meta" x="{MARGIN}" y="84">{esc(metric_text + reason_text)}</text>
  <defs>
    <clipPath id="leftclip"><rect x="{left_x}" y="{panel_y}" width="{PANEL_W}" height="{PANEL_H}"/></clipPath>
    <clipPath id="rightclip"><rect x="{right_x}" y="{panel_y}" width="{PANEL_W}" height="{PANEL_H}"/></clipPath>
  </defs>
  <text class="panel" x="{left_x}" y="{panel_y - 10}">Source + canonical land</text>
  <g clip-path="url(#leftclip)">
    <path class="land" d="{land_left}"/>
    <path class="source" d="{src_path_left}"/>
  </g>
  <rect class="frame" x="{left_x}" y="{panel_y}" width="{PANEL_W}" height="{PANEL_H}"/>
  <text class="panel" x="{right_x}" y="{panel_y - 10}">Candidate + source outline + canonical land</text>
  <g clip-path="url(#rightclip)">
    <path class="land" d="{land_right}"/>
    <path class="candidate" d="{cand_path_right}"/>
    <path class="source-overlay" d="{src_path_right}"/>
  </g>
  <rect class="frame" x="{right_x}" y="{panel_y}" width="{PANEL_W}" height="{PANEL_H}"/>
</svg>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("land", type=Path)
    parser.add_argument("decision", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--title", default="Geometry visual review")
    args = parser.parse_args()

    source = load_fc(args.source)
    candidate = load_fc(args.candidate)
    land = load_fc(args.land)
    decisions_payload = json.loads(args.decision.read_text(encoding="utf-8"))
    decisions = {str(d.get("geometry_id")): d for d in decisions_payload.get("features", [])}
    candidates = {feature_id(f): f for f in candidate.get("features", [])}

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for sf in source.get("features", []):
        gid = feature_id(sf)
        cf = candidates.get(gid)
        if cf is None:
            raise SystemExit(f"candidate missing geometry_id={gid}")
        name = str((sf.get("properties") or {}).get("name") or gid)
        filename = f"{safe_name(name)}__{safe_name(gid)}.svg"
        (args.output_dir / filename).write_text(
            svg_for_feature(sf, cf, land.get("features", []), decisions.get(gid)),
            encoding="utf-8",
        )
        rows.append((name, gid, decisions.get(gid, {}).get("status", "unclassified"), filename))

    items = "\n".join(
        f'<li><strong>{html.escape(name)}</strong> — {html.escape(status)} — '
        f'<a href="{html.escape(filename, quote=True)}">open SVG</a></li>'
        for name, _gid, status, filename in rows
    )
    index = f'''<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(args.title)}</title></head>
<body><h1>{html.escape(args.title)}</h1>
<p>Review-only output generated from immutable source geometry, the exact candidate artifact, and the pinned canonical land fabric. SVG sheets are scalable for high-zoom inspection. Automated QC is not visual acceptance.</p>
<ul>{items}</ul></body></html>'''
    (args.output_dir / "index.html").write_text(index, encoding="utf-8")
    print(f"Wrote {len(rows)} visual-review sheets to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
