import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

async function main() {
  const baseUrl = process.argv[2] || "https://kaastumor.github.io/Slavery/";
  const outputDir = path.resolve(process.argv[3] || "/tmp/current-candidate-review");
  await mkdir(outputDir, { recursive: true });

  const browser = await chromium.launch({
    headless: true,
    args: ["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist", "--disable-dev-shm-usage"],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(String(error)));

  const failures = [];
  try {
    await page.goto(baseUrl, { waitUntil: "networkidle", timeout: 30_000 });
    await page.locator("#map canvas").waitFor({ state: "visible", timeout: 15_000 });
    await page.locator("#release-badge").waitFor({ state: "visible", timeout: 15_000 });

    const badge = (await page.locator("#release-badge").innerText()).trim();
    const status = (await page.locator("#status").innerText()).trim();
    if (!badge.startsWith("v0.8.1")) {
      failures.push("current canonical root does not expose v0.8.1 release identity: " + badge);
    }
    if (badge.includes("candidate") || badge.includes("non-canonical") || badge.includes("preview")) {
      failures.push("current canonical root still presents a candidate/preview boundary: " + badge);
    }
    if (!/claim/.test(status) || !/place/.test(status)) {
      failures.push("current canonical root status no longer exposes claim/place counts: " + status);
    }
    if (await page.locator("#map-warning").isVisible()) {
      failures.push("current candidate map warning is visible");
    }

    const firstPlace = page.locator("[data-place-id]").first();
    await firstPlace.waitFor({ state: "visible", timeout: 10_000 });
    const placeLabel = ((await firstPlace.locator(".place-card-name").textContent()) || "").trim();
    await firstPlace.click();
    await page.waitForTimeout(250);
    const panel = (await page.locator("#panel").innerText()).trim();
    if (!placeLabel || !panel.includes(placeLabel)) {
      failures.push("canonical year-overview navigation did not open the selected place");
    }
    if (!panel.includes("Historical geometry")) {
      failures.push("canonical place detail no longer exposes historical geometry state");
    }
    if (!panel.includes("Evidence")) {
      failures.push("canonical place detail no longer exposes claim-specific evidence");
    }

    const screenshot = path.join(outputDir, "current-canonical.png");
    await page.screenshot({ path: screenshot, fullPage: true });
    const summary = {
      base_url: baseUrl,
      release_badge: badge,
      status,
      selected_place: placeLabel,
      page_errors: pageErrors,
      failures,
      checked_at: new Date().toISOString(),
    };
    await writeFile(path.join(outputDir, "review-summary.json"), JSON.stringify(summary, null, 2) + "\n", "utf8");
    console.log(JSON.stringify(summary, null, 2));
    if (pageErrors.length) failures.push("page errors: " + pageErrors.join(" | "));
    if (failures.length) throw new Error("current candidate regression failures: " + failures.join(" || "));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
