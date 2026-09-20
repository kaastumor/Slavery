import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
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

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const required = ["base-url", "manifest", "source", "candidate", "decision", "land", "output"];
  for (const key of required) {
    if (!args[key]) throw new Error("Missing --" + key);
  }

  const outputDir = path.resolve(args.output);
  await mkdir(outputDir, { recursive: true });

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
    const zoomIn = page.locator(".maplibregl-ctrl-zoom-in");

    for (const option of options) {
      await page.locator("#geometry-select").selectOption(option.value);
      await page.locator("#fit-selected").click();
      await page.waitForTimeout(450);

      const geometryDir = path.join(outputDir, slug(option.label));
      await mkdir(geometryDir, { recursive: true });

      const states = [
        { name: "fit", extraZoomClicks: 0 },
        { name: "zoom-plus-2", extraZoomClicks: 2 },
        { name: "zoom-plus-4", extraZoomClicks: 4 },
      ];

      for (const state of states) {
        await page.locator("#fit-selected").click();
        await page.waitForTimeout(350);

        for (let i = 0; i < state.extraZoomClicks; i += 1) {
          await zoomIn.click();
          await page.waitForTimeout(160);
        }

        await page.waitForTimeout(250);
        const zoomLabel = await page.locator("#zoom-label").innerText();
        const metrics = await page.locator("#metrics").innerText();
        const filename = state.name + ".png";
        await mapWrap.screenshot({ path: path.join(geometryDir, filename) });

        captures.push({
          geometry_id: option.value,
          label: option.label,
          state: state.name,
          zoom_label: zoomLabel,
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
