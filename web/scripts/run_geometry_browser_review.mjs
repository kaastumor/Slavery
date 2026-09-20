import { chromium } from "playwright";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 2) {
    const key = argv[i];
    const value = argv[i + 1];
    if (!key?.startsWith("--") || value === undefined) {
      throw new Error("Arguments must be --key value pairs");
    }
    out[key.slice(2)] = value;
  }
  return out;
}

function slug(value) {
  return String(value)
    .normalize("NFKD")
    .replace(/[^a-zA-Z0-9_-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase() || "geometry";
}

function geometryId(feature) {
  const value = feature?.properties?.geometry_id;
  return value === null || value === undefined || value === "" ? null : String(value);
}

function collectCoordinates(value, out = []) {
  if (!Array.isArray(value)) return out;
  if (
    value.length >= 2 &&
    typeof value[0] === "number" &&
    typeof value[1] === "number"
  ) {
    out.push([Number(value[0]), Number(value[1])]);
    return out;
  }
  for (const item of value) collectCoordinates(item, out);
  return out;
}

function featureCoordinateMap(collection) {
  const result = new Map();
  for (const feature of collection.features ?? []) {
    const id = geometryId(feature);
    if (!id || !feature.geometry || !("coordinates" in feature.geometry)) continue;
    result.set(id, collectCoordinates(feature.geometry.coordinates));
  }
  return result;
}

function sampleEvenly(points, maxCount) {
  if (points.length <= maxCount) return points;
  const sampled = [];
  const step = points.length / maxCount;
  for (let i = 0; i < maxCount; i += 1) {
    sampled.push(points[Math.floor(i * step)]);
  }
  return sampled;
}

function projectedDistanceSquared(a, b) {
  const meanLat = ((a[1] + b[1]) / 2) * Math.PI / 180;
  const dx = (a[0] - b[0]) * Math.cos(meanLat);
  const dy = a[1] - b[1];
  return dx * dx + dy * dy;
}

function maxBoundaryDisplacementFocus(sourcePoints, candidatePoints) {
  if (!sourcePoints?.length || !candidatePoints?.length) return null;

  const sourceSample = sampleEvenly(sourcePoints, 1200);
  const candidateSample = sampleEvenly(candidatePoints, 4000);

  let bestPoint = candidateSample[0];
  let bestDistance = -1;

  for (const candidate of candidateSample) {
    let nearest = Number.POSITIVE_INFINITY;
    for (const source of sourceSample) {
      const distance = projectedDistanceSquared(candidate, source);
      if (distance < nearest) nearest = distance;
      if (nearest <= bestDistance) break;
    }
    if (nearest > bestDistance) {
      bestDistance = nearest;
      bestPoint = candidate;
    }
  }

  return {
    center: bestPoint,
    approximate_displacement_degrees: Math.sqrt(Math.max(bestDistance, 0)),
  };
}

async function loadCollection(filePath) {
  return JSON.parse(await readFile(filePath, "utf8"));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const required = ["base-url", "manifest", "source", "candidate", "decision", "land", "output"];
  for (const key of required) {
    if (!args[key]) throw new Error("Missing --" + key);
  }

  const outputDir = path.resolve(args.output);
  await mkdir(outputDir, { recursive: true });

  const sourceCollection = await loadCollection(path.resolve(args.source));
  const candidateCollection = await loadCollection(path.resolve(args.candidate));
  const sourceCoordinates = featureCoordinateMap(sourceCollection);
  const candidateCoordinates = featureCoordinateMap(candidateCollection);

  const browser = await chromium.launch({
    headless: true,
    args: [
      "--use-gl=swiftshader",
      "--enable-webgl",
      "--ignore-gpu-blocklist",
      "--disable-dev-shm-usage",
    ],
  });

  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(String(error)));

  try {
    await page.goto(args["base-url"].replace(/\/$/, "") + "/review.html", {
      waitUntil: "networkidle",
    });

    await page.locator("#manifest-file").setInputFiles(path.resolve(args.manifest));
    await page.locator("#source-file").setInputFiles(path.resolve(args.source));
    await page.locator("#candidate-file").setInputFiles(path.resolve(args.candidate));
    await page.locator("#decision-file").setInputFiles(path.resolve(args.decision));
    await page.locator("#land-file").setInputFiles(path.resolve(args.land));

    await page.waitForFunction(() => {
      const node = document.querySelector("#review-status");
      return node?.classList.contains("ready");
    }, null, { timeout: 20_000 });

    await page.locator("#review-map canvas").waitFor({ state: "visible", timeout: 10_000 });

    const verification = await page.locator("#review-status").innerText();
    const options = await page.locator("#geometry-select option").evaluateAll((nodes) =>
      nodes
        .map((node) => ({
          value: node.value,
          label: node.textContent?.trim() || node.value,
        }))
        .filter((item) => item.value),
    );

    if (options.length === 0) {
      throw new Error("No shared geometry_id values were available for browser review");
    }

    const captures = [];
    const mapWrap = page.locator(".map-wrap");

    for (const option of options) {
      await page.locator("#geometry-select").selectOption(option.value);
      await page.locator("#fit-selected").click();
      await page.waitForTimeout(450);

      const geometryDir = path.join(outputDir, slug(option.label));
      await mkdir(geometryDir, { recursive: true });

      const fitZoom = await page.evaluate(() => {
        const reviewWindow = window;
        const map = reviewWindow.__atlasGeometryReviewMap;
        if (!map) throw new Error("Review map test hook is unavailable");
        return map.getZoom();
      });

      const focus = maxBoundaryDisplacementFocus(
        sourceCoordinates.get(option.value),
        candidateCoordinates.get(option.value),
      );

      const states = [
        {
          name: "fit",
          camera: null,
        },
        {
          name: "boundary-plus-2",
          camera: focus
            ? { center: focus.center, zoom: Math.min(9.25, fitZoom + 2) }
            : null,
        },
        {
          name: "boundary-plus-4",
          camera: focus
            ? { center: focus.center, zoom: Math.min(9.75, fitZoom + 4) }
            : null,
        },
      ];

      for (const state of states) {
        if (state.camera) {
          await page.evaluate((camera) => {
            const reviewWindow = window;
            const map = reviewWindow.__atlasGeometryReviewMap;
            if (!map) throw new Error("Review map test hook is unavailable");
            map.jumpTo({ center: camera.center, zoom: camera.zoom });
          }, state.camera);
        } else {
          await page.locator("#fit-selected").click();
        }

        await page.waitForTimeout(500);
        const zoomLabel = await page.locator("#zoom-label").innerText();
        const metrics = await page.locator("#metrics").innerText();
        const filename = state.name + ".png";
        await mapWrap.screenshot({ path: path.join(geometryDir, filename) });

        captures.push({
          geometry_id: option.value,
          label: option.label,
          state: state.name,
          zoom_label: zoomLabel,
          focus_coordinate: state.camera?.center ?? null,
          max_boundary_displacement_probe: focus,
          metrics,
          screenshot: path.posix.join(slug(option.label), filename),
        });
      }
    }

    const summary = {
      review_status: verification,
      input_set: {
        manifest: path.basename(args.manifest),
        source: path.basename(args.source),
        candidate: path.basename(args.candidate),
        decision: path.basename(args.decision),
        land: path.basename(args.land),
      },
      review_strategy:
        "fit + candidate boundary point with maximum approximate nearest-source displacement at two closer zooms",
      geometries: options,
      captures,
      page_errors: pageErrors,
    };

    await writeFile(
      path.join(outputDir, "review-summary.json"),
      JSON.stringify(summary, null, 2) + "\n",
      "utf8",
    );

    if (pageErrors.length > 0) {
      throw new Error("Browser page errors occurred: " + pageErrors.join(" | "));
    }

    console.log(JSON.stringify(summary, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
