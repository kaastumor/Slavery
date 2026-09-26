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
    if (!badge.includes("candidate") || !badge.includes("non-canonical")) {
      failures.push("current root no longer exposes its candidate/non-canonical boundary: " + badge);
    }
    if (!status.includes("frozen targets")) {
      failures.push("current root no longer exposes frozen-target candidate status: " + status);
    }
    if (await page.locator("#map-warning").isVisible()) {
      failures.push("current candidate map warning is visible");
    }

    const firstTarget = page.locator("[data-target-id]").first();
    await firstTarget.waitFor({ state: "visible", timeout: 10_000 });
    const targetLabel = ((await firstTarget.locator(".place-card-name").textContent()) || "").trim();
    await firstTarget.click();
    await page.waitForTimeout(250);
    const panel = (await page.locator("#panel").innerText()).trim();
    if (!targetLabel || !panel.includes(targetLabel)) {
      failures.push("candidate evidence-register navigation did not open the selected target");
    }
    const panelLower = panel.toLowerCase();
    if (!panelLower.includes("independent review") && !panelLower.includes("independent historical review")) {
      failures.push("candidate detail no longer exposes the independent-review boundary");
    }

    const screenshot = path.join(outputDir, "current-candidate.png");
    await page.screenshot({ path: screenshot, fullPage: true });
    const summary = {
      base_url: baseUrl,
      release_badge: badge,
      status,
      selected_target: targetLabel,
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
