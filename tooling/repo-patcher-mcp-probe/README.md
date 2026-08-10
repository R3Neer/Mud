# RepoPatcher MCP transport probe

This directory implements only Phase 0 of the MUD RepoPatcher validation architecture. It answers two empirical questions before the production validator is built:

1. Can ChatGPT transmit exact ZIP bytes to a custom MCP tool?
2. Can ChatGPT instead send a representative logical file set and receive the exact ZIP built by the server?

The probe deliberately has no GitHub integration, D1 state, validation workflow, or RepoPatcher execution.

## Endpoints

After copying `.dev.vars.example` to `.dev.vars`, the local defaults are:

```text
MCP:      http://localhost:8787/local-probe/mcp
Health:   http://localhost:8787/local-probe/health
Download: http://localhost:8787/local-probe/probe-files/<request_id>
```

The production deployment must store `PROBE_ROUTE_SECRET` with Wrangler secrets. Download links derive their origin from the incoming MCP request, so there is no separately configured public URL to drift.

## Tools

- `probe_store_base64`: stores exact canonical-base64 bytes after checking a caller-provided SHA-256.
- `probe_store_files`: constructs a ZIP with sorted paths, fixed metadata, fixed compression, and strict Windows-safe paths.
- `probe_get_file`: returns a resource link for the exact R2 object already stored.

A `request_id` is immutable: repeating it with the same bytes reuses the object; different bytes fail instead of overwriting it.

## Local verification

```powershell
npm install
npm run types
npm run check
npm run fixtures
npm run dev
```

`npm run fixtures` creates the five exact-size ZIPs and the three logical payloads under `%TEMP%\mud-repo-patcher-mcp-probe\inputs\`. Replace `REPLACE` in each request ID with attempt `1`, `2`, or `3`. The local Worker uses Wrangler's local R2 implementation. Run MCP Inspector against the MCP URL before connecting ChatGPT.

With the local Worker running, `npm run smoke` negotiates Streamable HTTP through the real MCP client, lists the three tools, stores one direct ZIP and one logical package, downloads both, and verifies their size and SHA-256.
`npm run smoke:matrix` repeats all eight Phase 0 variants three times. This proves the Worker stack locally, but it does not replace the required experiment initiated by ChatGPT.

## Deployment prerequisites

Authenticate Wrangler and create the two R2 buckets declared in `wrangler.jsonc`. For a new Worker, deploy once, immediately store a freshly generated route secret, and never pass its value as a command argument:

```powershell
npx wrangler login
npx wrangler r2 bucket create mud-repo-patcher-mcp-probe
npx wrangler r2 bucket create mud-repo-patcher-mcp-probe-preview
npx wrangler deploy
npx wrangler secret put PROBE_ROUTE_SECRET
```

The Worker fails closed with HTTP 503 while the secret is absent. A new Cloudflare account must also register its account-wide `workers.dev` subdomain in **Workers & Pages → Overview** before the public URL resolves. This is a one-time account setting, not a setting of the R2 bucket.

Do not commit the deployed route secret. Phase 0 is not an authenticated production service.

In ChatGPT developer mode, add a custom MCP server whose URL is:

```text
https://<worker>.workers.dev/<random-secret>/mcp
```

Generate fresh `request_id` values for every attempt. Record only tests initiated by ChatGPT in the decision table; `npm run smoke:matrix` is supporting local evidence, not a substitute.

## Exit gate

Record three attempts for each transport and fixture in `notas/FASE-0-TRANSPORTE-MCP.md`. Do not implement the production workflow or harness until one transport satisfies the gate described there.
