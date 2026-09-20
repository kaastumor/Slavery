#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from qgis.core import (
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsVectorLayer,
)


def vertex_count(geom):
    return sum(1 for _ in geom.vertices())


def transformed(geom, source_crs, target_epsg):
    out = geom.constGet().clone()
    wrapped = geom.__class__(out)
    transform = QgsCoordinateTransform(
        source_crs,
        QgsCoordinateReferenceSystem(f"EPSG:{target_epsg}"),
        QgsProject.instance(),
    )
    wrapped.transform(transform)
    return wrapped


def load_by_id(path):
    layer = QgsVectorLayer(str(path), Path(path).stem, "ogr")
    if not layer.isValid():
        raise RuntimeError(f"Could not open {path}")
    if "geometry_id" not in [f.name() for f in layer.fields()]:
        raise RuntimeError(f"{path} lacks geometry_id")
    return layer, {str(f["geometry_id"]): f for f in layer.getFeatures()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("candidate")
    parser.add_argument("output")
    args = parser.parse_args()

    app = QgsApplication([], False)
    app.initQgis()
    try:
        src_layer, src = load_by_id(args.source)
        cand_layer, cand = load_by_id(args.candidate)

        rows = []
        for gid, sf in sorted(src.items()):
            if gid not in cand:
                rows.append({"geometry_id": gid, "ok": False, "reason": "missing_candidate"})
                continue

            cf = cand[gid]
            sg = sf.geometry()
            cg = cf.geometry()

            sg_area = transformed(sg, src_layer.crs(), 6933)
            cg_area = transformed(cg, cand_layer.crs(), 6933)
            source_area = sg_area.area()
            render_area = cg_area.area()
            area_delta_pct = 0.0 if source_area == 0 else 100.0 * (render_area - source_area) / source_area
            symmetric_difference_pct = (
                0.0
                if source_area == 0
                else 100.0 * sg_area.symDifference(cg_area).area() / source_area
            )

            sg_3857 = transformed(sg, src_layer.crs(), 3857)
            cg_3857 = transformed(cg, cand_layer.crs(), 3857)
            hausdorff_m = sg_3857.hausdorffDistance(cg_3857)

            rows.append({
                "geometry_id": gid,
                "name": sf["name"] if "name" in sf.fields().names() else None,
                "from_year": sf["from_year"] if "from_year" in sf.fields().names() else None,
                "to_year": sf["to_year"] if "to_year" in sf.fields().names() else None,
                "ok": bool(cg.isGeosValid() and not cg.isEmpty()),
                "source_npoints": vertex_count(sg),
                "render_npoints": vertex_count(cg),
                "area_delta_pct": area_delta_pct,
                "symmetric_difference_pct": symmetric_difference_pct,
                "hausdorff_m": hausdorff_m,
            })

        report = {
            "source": args.source,
            "candidate": args.candidate,
            "feature_count": len(rows),
            "valid_count": sum(1 for r in rows if r.get("ok")),
            "max_abs_area_delta_pct": max((abs(r.get("area_delta_pct", 0.0)) for r in rows), default=0.0),
            "max_symmetric_difference_pct": max((r.get("symmetric_difference_pct", 0.0) for r in rows), default=0.0),
            "max_hausdorff_m": max((r.get("hausdorff_m", 0.0) for r in rows), default=0.0),
            "features": rows,
        }
        Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))

        if report["valid_count"] != report["feature_count"]:
            raise SystemExit(2)
    finally:
        app.exitQgis()


if __name__ == "__main__":
    main()
