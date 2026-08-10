import { getRequest } from "./db.js";
import { ServiceError, errorResponse } from "./errors.js";
import { bearerToken, verifyBaseOidc, verifyRequestClaims } from "./oidc.js";
import {
  authorizeAndReadCandidate,
  readResult,
  readValidatedCandidate,
  refreshRequest,
  submitFiles,
  submitZip,
  type SubmitFiles,
  type SubmitZip,
} from "./service.js";
import { tokensEqual } from "./crypto.js";
import type { Env } from "./types.js";

function noStore(response: Response): Response {
  response.headers.set("Cache-Control", "private, no-store");
  response.headers.set("X-Content-Type-Options", "nosniff");
  return response;
}

function responseBytes(bytes: Uint8Array): ArrayBuffer {
  return Uint8Array.from(bytes).buffer;
}

function requestIdFrom(pathname: string, prefix: string, suffix = ""): string | null {
  if (!pathname.startsWith(prefix) || (suffix && !pathname.endsWith(suffix))) return null;
  const end = suffix ? pathname.length - suffix.length : pathname.length;
  const encoded = pathname.slice(prefix.length, end);
  if (!encoded || encoded.includes("/")) return null;
  try {
    return decodeURIComponent(encoded);
  } catch {
    return null;
  }
}

async function authorizeAdapter(request: Request, env: Env): Promise<void> {
  if (!env.ADAPTER_TOKEN) throw new ServiceError("server_not_configured", "Adapter token is missing.", 503);
  if (!(await tokensEqual(bearerToken(request), env.ADAPTER_TOKEN))) {
    throw new ServiceError("authorization_rejected", "Adapter authorization was rejected.", 403);
  }
}

async function jsonBody<T>(request: Request): Promise<T> {
  const contentType = request.headers.get("Content-Type") ?? "";
  if (!contentType.toLowerCase().startsWith("application/json")) {
    throw new ServiceError("content_type_required", "Content-Type must be application/json.", 415);
  }
  try {
    return (await request.json()) as T;
  } catch {
    throw new ServiceError("invalid_json", "Request body is not valid JSON.");
  }
}

async function handle(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  if (url.pathname === "/health" && request.method === "GET") {
    return Response.json({ status: "ok", protocol: "mud-repo-patcher-validator/v1" });
  }

  if (url.pathname === "/adapter/v1/candidates/zip" && request.method === "POST") {
    await authorizeAdapter(request, env);
    return Response.json(await submitZip(env, await jsonBody<SubmitZip>(request)), { status: 202 });
  }
  if (url.pathname === "/adapter/v1/candidates/files" && request.method === "POST") {
    await authorizeAdapter(request, env);
    return Response.json(await submitFiles(env, await jsonBody<SubmitFiles>(request)), { status: 202 });
  }

  const internalId = requestIdFrom(url.pathname, "/internal/v1/candidates/");
  if (internalId !== null && request.method === "GET") {
    const payload = await verifyBaseOidc(bearerToken(request), env);
    const row = await getRequest(env.VALIDATION_DB, internalId);
    if (row === null) throw new ServiceError("not_found", "Unknown request_id.", 404);
    verifyRequestClaims(payload, env, row);
    const candidate = await authorizeAndReadCandidate(env, row);
    return new Response(responseBytes(candidate.bytes), {
      headers: {
        "Content-Disposition": `attachment; filename="${candidate.row.request_id}.zip"`,
        "Content-Length": String(candidate.row.package_size),
        "Content-Type": "application/zip",
        ETag: `"${candidate.row.package_sha256}"`,
        "X-Package-SHA256": candidate.row.package_sha256,
      },
    });
  }

  const resultId = requestIdFrom(url.pathname, "/adapter/v1/requests/", "/result");
  if (resultId !== null && request.method === "GET") {
    await authorizeAdapter(request, env);
    return new Response(responseBytes(await readResult(env, resultId)), {
      headers: { "Content-Type": "application/json" },
    });
  }
  const candidateId = requestIdFrom(url.pathname, "/adapter/v1/requests/", "/candidate");
  if (candidateId !== null && request.method === "GET") {
    await authorizeAdapter(request, env);
    const candidate = await readValidatedCandidate(env, candidateId);
    return new Response(responseBytes(candidate.bytes), {
      headers: {
        "Content-Disposition": `attachment; filename="${candidate.row.request_id}.zip"`,
        "Content-Length": String(candidate.row.package_size),
        "Content-Type": "application/zip",
        ETag: `"${candidate.row.package_sha256}"`,
        "X-Package-SHA256": candidate.row.package_sha256,
      },
    });
  }
  const statusId = requestIdFrom(url.pathname, "/adapter/v1/requests/");
  if (statusId !== null && request.method === "GET") {
    await authorizeAdapter(request, env);
    return Response.json(await refreshRequest(env, statusId));
  }

  return new Response("Not found", { status: 404 });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    try {
      return noStore(await handle(request, env));
    } catch (error) {
      return noStore(errorResponse(error));
    }
  },
} satisfies ExportedHandler<Env>;
