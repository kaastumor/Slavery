import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

export default defineConfig({
  base: "./",
  build: {
    rollupOptions: {
      input: {
        atlas: fileURLToPath(new URL("./index.html", import.meta.url)),
        researchPreview: fileURLToPath(new URL("./research-preview.html", import.meta.url)),
      },
    },
  },
});
