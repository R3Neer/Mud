import { createMcpHandler } from "agents/mcp/server";

import { sha256Hex, validateRequestId } from "./probe.js";
import { createProbeServer } from "./server.js";
import type { Env } from "./types.js";

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const basePath = `/${encodeURIComponent(env.PROBE_ROUTE_SECRET)}`;

    if (url.pathname === `${basePath}/health` && request.method === "GET") {
      return Response.json({ status: "ok", phase: 0, protocol: "mud-repo-patcher-mcp-probe/v1" });
    }

    if (url.pathname.startsWith(`${basePath}/probe-files/`) && request.method === "GET") {
      const rawId = url.pathname.slice(`${basePath}/probe-files/`.length);
      let requestId: string;
      try {
        requestId = decodeURIComponent(rawId);
        validateRequestId(requestId);
      } catch {
        return Response.json({ code: "invalid_request_id" }, { status: 400 });
      }
      const object = await env.PROBE_BUCKET.get(`probe/${requestId}.zip`);
      if (object === null) {
        return Response.json({ code: "not_found" }, { status: 404 });
      }
      const bytes = new Uint8Array(await object.arrayBuffer());
      const actualSha256 = await sha256Hex(bytes);
      if (object.customMetadata?.sha256 !== actualSha256) {
        return Response.json({ code: "stored_object_corrupt" }, { status: 500 });
      }
      return new Response(bytes, {
        headers: {
          "Cache-Control": "private, no-store",
          "Content-Disposition": `attachment; filename="${requestId}.zip"`,
          "Content-Length": String(bytes.byteLength),
          "Content-Type": "application/zip",
          ETag: `"${actualSha256}"`,
          "X-Content-Type-Options": "nosniff",
          "X-Probe-SHA256": actualSha256,
        },
      });
    }

    if (url.pathname === `${basePath}/mcp`) {
      return createMcpHandler(() => createProbeServer(env, url.origin), {
        route: `${basePath}/mcp`,
      })(request, env, ctx);
    }

    return new Response("Not found", { status: 404 });
  },
} satisfies ExportedHandler<Env>;
