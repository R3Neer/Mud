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
import { LONG_CALL_DURATIONS, runLongCallProbe } from "./timing.js";
import type {
  Env,
  LongCallResult,
  ProbeFileInput,
  ProbeRequestContext,
  StoredProbe,
} from "./types.js";

const requestId = z.string().min(1).max(80);
const sha256 = z.string().regex(/^[0-9a-fA-F]{64}$/);
const storedProbeSchema = {
  request_id: z.string(),
  sha256: z.string(),
  size: z.number().int().nonnegative(),
  reused: z.boolean(),
  download_url: z.string().url(),
};

export function createProbeServer(
  env: Env,
  publicBaseUrl: string,
  requestContext: ProbeRequestContext = {},
): McpServer {
  const server = new McpServer(
    { name: "mud-repo-patcher-transport-probe", version: "0.1.0" },
    {
      instructions:
        "Servidor experimental de Fase 0. Conserva request_id, compara siempre SHA-256 y usa probe_get_file para recuperar exactamente el objeto almacenado.",
    },
  );

  server.registerTool(
    "probe_wait_and_record",
    {
      title: "Run one timed long MCP call",
      description:
        "Keep this single tool call open for the requested duration while recording server-side start, heartbeat, and completion events. Use it to test whether ChatGPT can complete a long autonomous MCP operation after one approval.",
      inputSchema: {
        probe_id: requestId,
        duration_seconds: z.union([
          z.literal(LONG_CALL_DURATIONS[0]),
          z.literal(LONG_CALL_DURATIONS[1]),
          z.literal(LONG_CALL_DURATIONS[2]),
          z.literal(LONG_CALL_DURATIONS[3]),
        ]),
      },
      outputSchema: {
        probe_id: z.string(),
        requested_duration_seconds: z.number().int(),
        started_at: z.string(),
        completed_at: z.string(),
        server_elapsed_ms: z.number().int().nonnegative(),
        event_count: z.number().int().positive(),
        timing_url: z.string().url(),
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ probe_id, duration_seconds }) => {
      try {
        const result = await runLongCallProbe(
          env.PROBE_BUCKET,
          probe_id,
          duration_seconds,
          publicBaseUrl,
          env.PROBE_ROUTE_SECRET,
          requestContext,
        );
        return longCallToolResult(result);
      } catch (error) {
        return toolError(error);
      }
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

function longCallToolResult(result: LongCallResult) {
  const structuredContent = {
    probe_id: result.probeId,
    requested_duration_seconds: result.requestedDurationSeconds,
    started_at: result.startedAt,
    completed_at: result.completedAt,
    server_elapsed_ms: result.serverElapsedMs,
    event_count: result.eventCount,
    timing_url: result.timingUrl,
  };
  return {
    content: [
      {
        type: "text" as const,
        text: `Llamada ${result.probeId} completada en ${result.serverElapsedMs} ms con ${result.eventCount} eventos persistidos.`,
      },
    ],
    structuredContent,
  };
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
