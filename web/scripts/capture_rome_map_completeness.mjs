import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const cases = [
  { year: 9, slug: "rome-9ce" },
  { year: 14, slug: "rome-14ce" },
];

async function main() {
  const baseUrl = process.argv[2] || "https://kaastumor.github.io/Slavery/";
  const outputDir = path.resolve(process.argv[3] || "/tmp/rome-gap-review");
  await mkdir(outputDir, { recursive: true });

  const browser = await chromium.launch({
    headless: true,
    args: ["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist", "--disable-dev-shm-usage"],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const captures = [];

  try {
    await page.goto(baseUrl, { waitUntil: "networkidle", timeout: 30_000 });
    await page.locator("#map canvas").waitFor({ state: "visible", timeout: 15_000 });

    for (const item of cases) {
      await page.locator("#year").evaluate((node, year) => {
        node.value = String(year);
        node.dispatchEvent(new Event("input", { bubbles: true }));
      }, item.year);
      await page.waitForTimeout(500);

      const card = page.locator("[data-place-id]").filter({ hasText: "Roman Empire — early Principate" }).first();
      await card.waitFor({ state: "visible", timeout: 10_000 });
      await card.click();
      await page.waitForTimeout(800);

      const fit = path.join(outputDir, item.slug + "-fit.png");
      await page.screenshot({ path: fit, fullPage: true });

      await page.locator(".maplibregl-ctrl-zoom-in").click();
      await page.waitForTimeout(300);
      const close = path.join(outputDir, item.slug + "-zoom-plus-1.png");
      await page.screenshot({ path: close, fullPage: true });

      captures.push({
        year: item.year,
        panel: (await page.locator("#panel").innerText()).trim(),
        geometry_details: ((await page.locator(".geometry-details").textContent()) || "").trim(),
        fit: path.basename(fit),
        zoom: path.basename(close),
      });

      const back = page.locator("#back-overview");
      if (await back.isVisible()) {
        await back.click();
        await page.waitForTimeout(250);
      }
    }

    await writeFile(
      path.join(outputDir, "summary.json"),
      JSON.stringify({ base_url: baseUrl, captures }, null, 2) + "\n",
      "utf8",
    );
    console.log(JSON.stringify({ captures }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
