import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

function currentUtcYear() {
  return new Date().getUTCFullYear();
}

async function setYear(page, year) {
  await page.locator("#year").evaluate((node, value) => {
    const input = node;
    input.value = String(value);
    input.dispatchEvent(new Event("input", { bubbles: true }));
  }, year);
  await page.waitForTimeout(300);
}

async function main() {
  const baseUrl = process.argv[2] || "http://127.0.0.1:4173/";
  const outputDir = path.resolve(process.argv[3] || "/tmp/v070-stage-review");
  const forceApiFailure = process.argv.includes("--force-api-failure");
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

  const failures = [];
  const captures = [];

  if (forceApiFailure) {
    await page.route(
      "https://dilnayfllygkplsdymel.supabase.co/functions/v1/atlas-data-v070-stage",
      (route) => route.abort("failed"),
    );
  }

  try {
    await page.goto(baseUrl, { waitUntil: "networkidle", timeout: 30_000 });
    await page.locator("#year").waitFor({ state: "visible", timeout: 15_000 });
    await page.locator("#map canvas").waitFor({ state: "visible", timeout: 15_000 });

    const badge = (await page.locator("#release-badge").innerText()).trim();
    const badgeTitle = await page.locator("#release-badge").getAttribute("title");
    if (!badge.startsWith("v0.7.0")) failures.push(`unexpected release badge: ${badge}`);
    if (forceApiFailure && !badge.includes("static fallback")) {
      failures.push(`forced API failure did not activate v0.7.0 fallback: ${badge}`);
    }
    if (!forceApiFailure && badge.includes("static fallback")) {
      failures.push(`normal staged review unexpectedly used static fallback: ${badge}`);
    }
    if (!badgeTitle?.includes("serving adapter v0.7.0-public-mvp-v1")) {
      failures.push(`release badge does not expose serving adapter: ${badgeTitle}`);
    }
    if (await page.locator("#map-warning").isVisible()) {
      failures.push("map warning visible at stage startup");
    }

    const slider = page.locator("#year");
    const currentYear = currentUtcYear();
    const sliderMax = Number(await slider.getAttribute("max"));
    if (sliderMax < currentYear) {
      failures.push(`open-ended claims stop at slider max ${sliderMax}, before ${currentYear}`);
    }

    await setYear(page, currentYear);
    const brazil = page.locator("[data-place-id]").filter({ hasText: "Brazil" }).first();
    await brazil.waitFor({ state: "visible", timeout: 10_000 });
    await brazil.click();
    await page.waitForTimeout(250);
    const brazilPanel = (await page.locator("#panel").innerText()).trim();
    if (!brazilPanel.includes("Debt bondage")) failures.push("Brazil claim not visible");
    if (!brazilPanel.includes("P-level unassigned")) failures.push("Brazil invents or hides null P-level");
    if (!brazilPanel.includes("Source version 9dfc9c89-f9b9-4d12-b6fd-28ddc3f399db")) {
      failures.push("Brazil exact source-version ID not visible");
    }
    if (!brazilPanel.includes("No defensible geometry has been attached")) {
      failures.push("Brazil unresolved geometry caveat missing");
    }
    const brazilShot = path.join(outputDir, "brazil-present.png");
    await page.screenshot({ path: brazilShot, fullPage: true });
    captures.push(path.basename(brazilShot));

    await page.locator("#back-overview").click();
    await setYear(page, -1500);
    const shang = page.locator("[data-place-id]").filter({ hasText: "Shang China" }).first();
    await shang.waitFor({ state: "visible", timeout: 10_000 });
    const shangMeta = ((await shang.locator(".place-card-meta").textContent()) || "").trim();
    if (!shangMeta.toLowerCase().includes("geometry unresolved")) {
      failures.push("Shang list card does not expose unresolved geometry");
    }
    await shang.click();
    await page.waitForTimeout(250);
    const shangPanel = (await page.locator("#panel").innerText()).trim();
    if (!shangPanel.toLowerCase().includes("disputed")) {
      failures.push("Shang disputed state not visible");
    }
    if (!shangPanel.includes("Source version 0e0358e5-6b88-526e-a65d-16f0a2958482")) {
      failures.push("Shang exact source-version ID not visible");
    }
    const shangShot = path.join(outputDir, "shang-disputed.png");
    await page.screenshot({ path: shangShot, fullPage: true });
    captures.push(path.basename(shangShot));

    await page.locator("#back-overview").click();
    const overviewText = (await page.locator("#panel").innerText()).trim();
    if (!overviewText.includes("Canonical-release territorial-practice evidence")) {
      failures.push("overview does not distinguish canonical release from legacy preview");
    }

    if (pageErrors.length) {
      failures.push("page errors: " + pageErrors.join(" | "));
    }
    if (await page.locator("#map-warning").isVisible()) {
      failures.push("map warning visible after representative stage review");
    }

    const summary = {
      base_url: baseUrl,
      mode: forceApiFailure ? "forced_static_fallback" : "stage_api",
      release_badge: badge,
      release_badge_title: badgeTitle,
      current_year: currentYear,
      slider_max: sliderMax,
      page_errors: pageErrors,
      failures,
      captures,
      checked_at: new Date().toISOString(),
    };
    await writeFile(
      path.join(outputDir, "review-summary.json"),
      JSON.stringify(summary, null, 2) + "\n",
      "utf8",
    );
    console.log(JSON.stringify(summary, null, 2));
    if (failures.length) {
      throw new Error("v0.7.0 stage browser review failures: " + failures.join(" || "));
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
