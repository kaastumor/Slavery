import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const cases = [
  { name: "Hittite central Anatolia", year: -1299, expectExternal: true },
  { name: "New Kingdom Egypt", year: -1399, expectExternal: true },
  { name: "Mauryan Empire", year: -290, expectExternal: true },
  { name: "Western Han China", year: -125, expectExternal: true },
  { name: "Roman Empire — early Principate", year: 6, expectExternal: true },
  { name: "Baekje", year: 369, expectExternal: false },
];

function slug(value) {
  return value
    .normalize("NFKD")
    .replace(/[^a-zA-Z0-9_-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase();
}

async function main() {
  const baseUrl = process.argv[2] || "https://kaastumor.github.io/Slavery/";
  const outputDir = path.resolve(process.argv[3] || "/tmp/public-atlas-review");
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
  const caseFailures = [];
  page.on("pageerror", (error) => pageErrors.push(String(error)));

  try {
    await page.goto(baseUrl, { waitUntil: "networkidle", timeout: 30_000 });
    await page.locator("#year").waitFor({ state: "visible", timeout: 15_000 });
    await page.locator("#map canvas").waitFor({ state: "visible", timeout: 15_000 });

    const releaseBadge = (await page.locator("#release-badge").innerText()).trim();
    const mapWarningVisible = await page.locator("#map-warning").isVisible();

    if (mapWarningVisible) {
      throw new Error("Public map warning is visible before representative review");
    }

    const captures = [];

    for (const item of cases) {
      await page.locator("#year").evaluate((node, year) => {
        const input = node;
        input.value = String(year);
        input.dispatchEvent(new Event("input", { bubbles: true }));
      }, item.year);
      await page.waitForTimeout(350);

      const card = page.locator("[data-place-id]").filter({ hasText: item.name }).first();
      await card.waitFor({ state: "visible", timeout: 10_000 });
      await card.click();
      await page.waitForTimeout(700);

      const panelText = (await page.locator("#panel").innerText()).trim();
      const geometryText = (await page.locator(".geometry-details").innerText()).trim();
      const statusText = (await page.locator("#status").innerText()).trim();
      const yearLabel = (await page.locator("#year-label").innerText()).trim();

      const usesExternalPolicy =
        geometryText.includes("cliopatria-qgis-natural-earth-v1") &&
        geometryText.includes("cached, bounded cartographic generalization");

      if (item.expectExternal && !usesExternalPolicy) {
        caseFailures.push(
          item.name + ": public UI did not report cliopatria-qgis-natural-earth-v1; details=" + geometryText,
        );
      }

      if (!item.expectExternal && usesExternalPolicy) {
        caseFailures.push(
          item.name + ": quarantined/fallback geometry unexpectedly reports promoted policy; details=" + geometryText,
        );
      }

      const nameSlug = slug(item.name);
      const fitPath = path.join(outputDir, nameSlug + "-fit.png");
      await page.screenshot({ path: fitPath, fullPage: true });

      for (let i = 0; i < 2; i += 1) {
        await page.locator(".maplibregl-ctrl-zoom-in").click();
        await page.waitForTimeout(250);
      }
      const closePath = path.join(outputDir, nameSlug + "-zoom-plus-2.png");
      await page.screenshot({ path: closePath, fullPage: true });

      captures.push({
        name: item.name,
        year: item.year,
        year_label: yearLabel,
        status: statusText,
        expect_external: item.expectExternal,
        uses_external_policy: usesExternalPolicy,
        geometry_details: geometryText,
        panel_contains_name: panelText.includes(item.name),
        fit_screenshot: path.basename(fitPath),
        zoom_screenshot: path.basename(closePath),
      });

      const backButton = page.locator("#back-overview");
      if (await backButton.isVisible()) {
        await backButton.click();
        await page.waitForTimeout(200);
      }
    }

    const finalWarningVisible = await page.locator("#map-warning").isVisible();
    if (finalWarningVisible) {
      throw new Error("Public map warning became visible during representative review");
    }
    if (pageErrors.length > 0) {
      caseFailures.push("Public page errors occurred: " + pageErrors.join(" | "));
    }

    const summary = {
      base_url: baseUrl,
      release_badge: releaseBadge,
      checked_at: new Date().toISOString(),
      page_errors: pageErrors,
      case_failures: caseFailures,
      map_warning_visible: finalWarningVisible,
      captures,
    };

    await writeFile(
      path.join(outputDir, "review-summary.json"),
      JSON.stringify(summary, null, 2) + "\n",
      "utf8",
    );
    console.log(JSON.stringify(summary, null, 2));
    if (caseFailures.length > 0) {
      throw new Error("Public atlas review failures: " + caseFailures.join(" || "));
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
