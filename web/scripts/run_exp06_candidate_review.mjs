import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const baseUrl = process.argv[2] || "http://127.0.0.1:4173/exp06-candidate.html";
const outputDir = path.resolve(process.argv[3] || "/tmp/exp06-candidate-review");

const cases = [
  { name: "Chámpa", must: ["Under review", "too historically ambiguous", "Do not equate Linyi"] },
  { name: "Magadha – Haryanka dynasty", must: ["Under review", "chronologically contested", "Do not treat one Bimbisāra"] },
  { name: "Later Mayan City-States", must: ["Internally researched · bounded", "cannot be generalized to all Later Maya city-states", "Mayapán is a reference locus only"] },
  { name: "Mongol Yam/postal network", must: ["Internally researched · bounded", "compulsory station-household labor", "not automatically slaves"] },
  { name: "Yaghan communities, Tierra del Fuego", must: ["Researched inconclusive", "does not establish or disprove", "not an internal-practice classification"] },
  { name: "Khmer Empire", must: ["Internally researched · bounded", "Angkor/Yasodharapura", "polity-wide"] },
];

function slug(value) {
  return value.normalize("NFKD").replace(/[^a-zA-Z0-9_-]+/g, "-").replace(/^-+|-+$/g, "").toLowerCase();
}

async function main() {
  await mkdir(outputDir, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    args: ["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist", "--disable-dev-shm-usage"],
  });
  const failures = [];
  const pageErrors = [];
  const page = await browser.newPage({ viewport: { width: 1600, height: 1100 } });
  page.on("pageerror", (error) => pageErrors.push(String(error)));

  try {
    await page.goto(baseUrl, { waitUntil: "networkidle", timeout: 30000 });
    await page.locator("#candidate-panel").waitFor({ state: "visible", timeout: 15000 });
    await page.locator("#map canvas").waitFor({ state: "visible", timeout: 15000 });

    const badge = (await page.locator("#release-badge").innerText()).trim();
    const status = (await page.locator("#status").innerText()).trim();
    const boundary = (await page.locator(".preview-boundary").innerText()).trim();
    const overview = (await page.locator("#candidate-panel").innerText()).trim();

    for (const expected of ["exp06-candidate-v1", "pending gate"]) {
      if (!badge.includes(expected)) failures.push("Release badge missing: " + expected);
    }
    for (const expected of ["3 bounded", "1 inconclusive", "2 under review"]) {
      if (!status.includes(expected)) failures.push("Status missing: " + expected);
    }
    for (const expected of ["NON-CANONICAL CANDIDATE", "v0.6.1 remains canonical", "no P-levels or practice polygons"]) {
      if (!boundary.toUpperCase().includes(expected.toUpperCase())) failures.push("Boundary missing: " + expected);
    }
    for (const expected of ["Non-absence rule", "Independent historical review: 0"]) {
      if (!overview.includes(expected)) failures.push("Overview missing: " + expected);
    }

    await page.screenshot({ path: path.join(outputDir, "overview-desktop.png"), fullPage: true });

    const captures = [];
    for (const item of cases) {
      const button = page.locator("button.table-target", { hasText: item.name }).first();
      await button.waitFor({ state: "visible", timeout: 10000 });
      await button.click();
      await page.waitForTimeout(250);

      const panelText = (await page.locator("#candidate-panel").innerText()).trim();
      for (const expected of [
        "Strongest bounded proposition",
        "Required abstention",
        "Evidence locus",
        "Inference extent",
        "Map / geometry boundary",
        "Source/version evidence",
        ...item.must,
      ]) {
        if (!panelText.includes(expected)) failures.push(item.name + " missing: " + expected);
      }

      const sourceLinks = await page.locator("#candidate-panel .source-link").count();
      if (sourceLinks < 1) failures.push(item.name + " has no visible source rows");

      const screenshot = slug(item.name) + ".png";
      await page.screenshot({ path: path.join(outputDir, screenshot), fullPage: true });
      captures.push({ name: item.name, source_links: sourceLinks, screenshot });

      const back = page.locator("#candidate-back");
      await back.click();
      await page.waitForTimeout(120);
    }

    await page.setViewportSize({ width: 768, height: 1024 });
    await page.screenshot({ path: path.join(outputDir, "overview-mobile.png"), fullPage: true });

    if (pageErrors.length) failures.push("Page errors: " + pageErrors.join(" | "));

    const summary = {
      base_url: baseUrl,
      checked_at: new Date().toISOString(),
      release_badge: badge,
      status,
      boundary,
      page_errors: pageErrors,
      failures,
      captures,
      screenshots: ["overview-desktop.png", "overview-mobile.png", ...captures.map((item) => item.screenshot)],
    };
    await writeFile(path.join(outputDir, "review-summary.json"), JSON.stringify(summary, null, 2) + "\n", "utf8");
    console.log(JSON.stringify(summary, null, 2));

    if (failures.length) throw new Error("EXP-06 candidate review failed: " + failures.join(" || "));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
