import { resolve } from "node:path";
import { defineConfig } from "vite";

export default defineConfig({
  base: "./",
  build: {
    rollupOptions: {
      input: {
        atlas: resolve(__dirname, "index.html"),
        researchPreview: resolve(__dirname, "research-preview.html"),
      },
    },
  },
});
