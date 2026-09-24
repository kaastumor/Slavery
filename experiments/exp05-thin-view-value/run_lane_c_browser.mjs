import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const baseUrl = process.argv[2] || "https://kaastumor.github.io/Slavery/research-preview.html";
const outputDir = path.resolve(process.argv[3] || "/tmp/exp05-lane-c");

const tasks = [
  { id: "T1", label: "temporal-spatial-truth", targets: ["Sumerian City-States", "Cuzco", "Angkor"] },
  { id: "T2", label: "network-versus-territory", targets: ["Indus Valley Civilization", "Viking trade network", "Andaman Islands communities"] },
  { id: "T3", label: "category-dependency-negative-control", targets: ["Sumerian City-States", "Angkor", "Ethiopian Empire"] },
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
  const page = await browser.newPage({ viewport: { width: 1600, height: 1100 } });
  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(String(error)));

  const result = {
    lane: "C",
    surface: "live EXP-04 Research Preview",
    base_url: baseUrl,
    checked_at: new Date().toISOString(),
    page_errors: pageErrors,
    tasks: [],
  };

  try {
    for (const task of tasks) {
      let interactionSteps = 1;
      await page.goto(baseUrl, { waitUntil: "networkidle", timeout: 30000 });
      await page.locator("#preview-panel").waitFor({ state: "visible", timeout: 15000 });
      await page.locator("#map canvas").waitFor({ state: "visible", timeout: 15000 });

      const releaseBadge = (await page.locator("#release-badge").innerText()).trim();
      const status = (await page.locator("#status").innerText()).trim();
      const boundary = (await page.locator(".preview-boundary").innerText()).trim();
      const tableText = (await page.locator(".preview-table").innerText()).trim();
      const captures = [];

      for (let index = 0; index < task.targets.length; index += 1) {
        const targetName = task.targets[index];
        const button = page.locator("button.table-target", { hasText: targetName }).first();
        await button.waitFor({ state: "visible", timeout: 10000 });
        await button.click();
        interactionSteps += 1;
        await page.waitForTimeout(150);

        const panel = page.locator("#preview-panel");
        const panelText = (await panel.innerText()).trim();
        const heading = (await panel.locator("h2").innerText()).trim();
        const sourceLinks = await panel.locator(".source-link").count();
        const sourceMeta = await panel.locator(".source-meta").allInnerTexts();
        const screenshot = path.join(outputDir, task.id.toLowerCase() + "-" + slug(targetName) + ".png");
        await page.screenshot({ path: screenshot, fullPage: true });

        captures.push({
          target: targetName,
          heading,
          panel_text: panelText,
          source_links_visible: sourceLinks,
          source_meta_lines: sourceMeta,
          screenshot: path.basename(screenshot),
        });

        if (index < task.targets.length - 1) {
          const back = page.locator("#preview-back");
          await back.waitFor({ state: "visible", timeout: 10000 });
          await back.click();
          interactionSteps += 1;
          await page.waitForTimeout(100);
        }
      }

      result.tasks.push({
        task_id: task.id,
        label: task.label,
        distinct_pages_opened: 1,
        interaction_steps: interactionSteps,
        release_badge: releaseBadge,
        status,
        boundary,
        table_text: tableText,
        captures,
      });
    }

    await writeFile(path.join(outputDir, "lane-c-summary.json"), JSON.stringify(result, null, 2) + "\n", "utf8");
    console.log(JSON.stringify(result, null, 2));
    if (pageErrors.length) throw new Error("Page errors occurred: " + pageErrors.join(" | "));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
