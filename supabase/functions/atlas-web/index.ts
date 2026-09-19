import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const base = new URL(".", import.meta.url);

const files = {
  html: await Deno.readTextFile(new URL("./index.html", base)),
  js: await Deno.readTextFile(new URL("./app.js", base)),
  css: await Deno.readTextFile(new URL("./styles.css", base)),
  land: await Deno.readTextFile(new URL("./world-land.geojson", base)),
};

const headers = {
  "cache-control": "public, max-age=300",
  "x-content-type-options": "nosniff",
};

Deno.serve((req) => {
  const path = new URL(req.url).pathname;

  if (path.endsWith("/app.js")) {
    return new Response(files.js, { headers: { ...headers, "content-type": "text/javascript; charset=utf-8" } });
  }
  if (path.endsWith("/styles.css")) {
    return new Response(files.css, { headers: { ...headers, "content-type": "text/css; charset=utf-8" } });
  }
  if (path.endsWith("/world-land.geojson")) {
    return new Response(files.land, { headers: { ...headers, "content-type": "application/geo+json; charset=utf-8" } });
  }

  return new Response(files.html, {
    headers: {
      ...headers,
      "cache-control": "no-cache",
      "content-type": "text/html; charset=utf-8",
    },
  });
});
