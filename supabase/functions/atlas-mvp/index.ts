Deno.serve(() => new Response(
  JSON.stringify({
    error: "deprecated_endpoint",
    message: "This prototype endpoint has been retired. Use /functions/v1/atlas-data."
  }),
  {
    status: 410,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store"
    }
  }
));
