import { McpServer } from "@modelcontextprotocol/server";
import { z } from "zod";

import {
  buildDeterministicZip,
  decodeCanonicalBase64,
  MAX_BASE64_BYTES,
  ProbeError,
  readImmutableProbe,
  storeImmutableProbe,
} from "./probe.js";
import type { Env, ProbeFileInput, StoredProbe } from "./types.js";

const requestId = z.string().min(1).max(80);
const sha256 = z.string().regex(/^[0-9a-fA-F]{64}$/);
const storedProbeSchema = {
  request_id: z.string(),
  sha256: z.string(),
  size: z.number().int().nonnegative(),
  reused: z.boolean(),
  download_url: z.string().url(),
};

export function createProbeServer(env: Env, publicBaseUrl: string): McpServer {
  const server = new McpServer(
    { name: "mud-repo-patcher-transport-probe", version: "0.1.0" },
    {
      instructions:
        "Servidor experimental de Fase 0. Conserva request_id, compara siempre SHA-256 y usa probe_get_file para recuperar exactamente el objeto almacenado.",
    },
  );

  server.registerTool(
    "probe_store_base64",
    {
      title: "Store exact probe bytes",
      description:
        "Store candidate ZIP bytes supplied as canonical base64. Use only to measure whether ChatGPT can transmit exact binary data.",
      inputSchema: {
        request_id: requestId,
        content_base64: z.string().min(4).max(Math.ceil(MAX_BASE64_BYTES / 3) * 4),
        expected_sha256: sha256,
      },
      outputSchema: storedProbeSchema,
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ request_id, content_base64, expected_sha256 }) => {
      try {
        const bytes = decodeCanonicalBase64(content_base64);
        const stored = await storeImmutableProbe(
          env.PROBE_BUCKET,
          request_id,
          bytes,
          expected_sha256,
          publicBaseUrl,
          env.PROBE_ROUTE_SECRET,
        );
        return toolResult(stored);
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "probe_store_files",
    {
      title: "Build and store a probe ZIP",
      description:
        "Build the definitive ZIP from logical UTF-8 or base64 files using fixed ordering, metadata, and compression, then store those exact bytes.",
      inputSchema: {
        request_id: requestId,
        files: z
          .array(
            z.object({
              path: z.string().min(1),
              encoding: z.enum(["utf8", "base64"]),
              content: z.string(),
            }),
          )
          .min(1)
          .max(500),
      },
      outputSchema: storedProbeSchema,
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ request_id, files }) => {
      try {
        const bytes = buildDeterministicZip(files as ProbeFileInput[]);
        const stored = await storeImmutableProbe(
          env.PROBE_BUCKET,
          request_id,
          bytes,
          undefined,
          publicBaseUrl,
          env.PROBE_ROUTE_SECRET,
        );
        return toolResult(stored);
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "probe_get_file",
    {
      title: "Get a stored probe file",
      description:
        "Return a downloadable resource link for the exact object previously stored under request_id.",
      inputSchema: { request_id: requestId },
      outputSchema: storedProbeSchema,
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ request_id }) => {
      try {
        const stored = await readImmutableProbe(
          env.PROBE_BUCKET,
          request_id,
          publicBaseUrl,
          env.PROBE_ROUTE_SECRET,
        );
        return toolResult(stored);
      } catch (error) {
        return toolError(error);
      }
    },
  );

  return server;
}

function toolResult(stored: StoredProbe) {
  const structuredContent = {
    request_id: stored.requestId,
    sha256: stored.sha256,
    size: stored.size,
    reused: stored.reused,
    download_url: stored.downloadUrl,
  };
  return {
    content: [
      {
        type: "text" as const,
        text: `Objeto ${stored.requestId}: ${stored.size} bytes, SHA-256 ${stored.sha256}.`,
      },
      {
        type: "resource_link" as const,
        uri: stored.downloadUrl,
        name: `${stored.requestId}.zip`,
        description: "Exact bytes stored by the Phase 0 transport probe.",
        mimeType: "application/zip",
      },
    ],
    structuredContent,
  };
}

function toolError(error: unknown) {
  const probeError =
    error instanceof ProbeError
      ? error
      : new ProbeError("internal_error", error instanceof Error ? error.message : String(error));
  return {
    isError: true,
    content: [{ type: "text" as const, text: `${probeError.code}: ${probeError.message}` }],
  };
}
