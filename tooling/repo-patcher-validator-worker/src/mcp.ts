import { McpServer } from "@modelcontextprotocol/server";
import { z } from "zod";

import { getRequest } from "./db.js";
import { ServiceError } from "./errors.js";
import {
  readResult,
  readValidatedCandidate,
  refreshRequest,
  submitStagedFiles,
} from "./service.js";
import {
  MAX_BATCH_CONTENT_CHARS,
  MAX_BATCH_FILES,
  MAX_STAGED_BATCHES,
  stageCandidateFiles,
} from "./staging.js";
import { MAX_FILES, MAX_FILE_BYTES } from "./zip.js";
import { PROTOCOL, type Env, type StagedUtf8FileInput, type ValidationResult } from "./types.js";

const requestId = z.string().min(1).max(96).regex(/^[A-Za-z0-9][A-Za-z0-9._-]*$/);
const sha256 = z.string().regex(/^[0-9a-fA-F]{64}$/);
const targetSha = z.string().regex(/^[0-9a-f]{40}$/);
const state = z.enum([
  "accepted",
  "dispatching",
  "queued",
  "running",
  "succeeded",
  "failed",
  "infrastructure_error",
  "expired",
]);
const statusSchema = {
  protocol: z.literal(PROTOCOL),
  request_id: z.string(),
  target_sha: z.string(),
  package_sha256: z.string(),
  package_size: z.number().int().positive(),
  trust_plugin: z.boolean(),
  transport_kind: z.enum(["zip_base64", "logical_files", "files_staged_v1"]),
  state,
  github_run_id: z.number().int().nullable(),
  github_run_url: z.string().nullable(),
  github_run_attempt: z.number().int().positive(),
  control_sha: z.string().nullable(),
  conclusion: z.string().nullable(),
  runtime_version: z.string().nullable(),
  created_at: z.string(),
  completed_at: z.string().nullable(),
};
const stagedFile = z.object({
  path: z.string().min(1).max(240),
  content: z.string().max(MAX_BATCH_CONTENT_CHARS),
  expected_size: z.number().int().nonnegative().max(MAX_FILE_BYTES).optional(),
  expected_sha256: sha256.optional(),
});

export function createValidatorMcpServer(env: Env, publicBaseUrl: string): McpServer {
  const server = new McpServer(
    { name: "mud-repo-patcher-validator", version: "0.2.1" },
    {
      instructions:
        "Validate RepoPatcher candidates against an exact MUD commit. Stage complete UTF-8 files, submit explicit batches, poll durable state, inspect evidence, and only download a candidate after success.",
    },
  );

  server.registerTool(
    "stage_candidate_files",
    {
      title: "Stage complete candidate files",
      description:
        "Store one small immutable batch of complete UTF-8 files. The Worker computes byte size and SHA-256; optional expected values add a strict assertion. Never split a file across calls.",
      inputSchema: {
        request_id: requestId,
        batch_id: requestId,
        files: z.array(stagedFile).min(1).max(MAX_BATCH_FILES),
      },
      outputSchema: {
        request_id: z.string(),
        batch_id: z.string(),
        file_count: z.number().int().positive(),
        total_size: z.number().int().nonnegative(),
        batch_sha256: z.string(),
        files: z.array(z.object({
          path: z.string(),
          size: z.number().int().nonnegative(),
          sha256: z.string(),
        })),
        reused: z.boolean(),
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ request_id, batch_id, files }) => {
      try {
        const stored = await stageCandidateFiles(env.VALIDATION_BUCKET, {
          request_id,
          batch_id,
          files: files as StagedUtf8FileInput[],
        });
        const structuredContent = {
          request_id: stored.requestId,
          batch_id: stored.batchId,
          file_count: stored.fileCount,
          total_size: stored.totalSize,
          batch_sha256: stored.batchSha256,
          files: stored.files,
          reused: stored.reused,
        };
        return {
          content: [{
            type: "text" as const,
            text: `Staged ${stored.fileCount} complete files in batch ${stored.batchId}; ${stored.totalSize} UTF-8 bytes verified.`,
          }],
          structuredContent,
        };
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "submit_candidate",
    {
      title: "Build and submit a candidate",
      description:
        "Revalidate explicitly named immutable batches, build the deterministic ZIP, persist its exact bytes, and start Windows validation against target_sha.",
      inputSchema: {
        protocol: z.literal(PROTOCOL),
        request_id: requestId,
        batch_ids: z.array(requestId).min(1).max(MAX_STAGED_BATCHES),
        expected_file_count: z.number().int().positive().max(MAX_FILES),
        target_sha: targetSha,
        trust_plugin: z.boolean(),
      },
      outputSchema: {
        ...statusSchema,
        reused: z.boolean(),
        batch_count: z.number().int().positive(),
        file_count: z.number().int().positive(),
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true,
      },
    },
    async (input) => {
      try {
        const result = await submitStagedFiles(env, input);
        return {
          content: [{
            type: "text" as const,
            text: `Candidate ${input.request_id} accepted for exact commit ${input.target_sha}. State: ${String(result.state)}.`,
          }],
          structuredContent: result,
        };
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "await_validation",
    {
      title: "Refresh durable validation state",
      description:
        "Perform one short refresh of the durable request. If the state is not terminal, call this tool again later; the operation never relies on one long HTTP connection.",
      inputSchema: { request_id: requestId },
      outputSchema: statusSchema,
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true,
      },
    },
    async ({ request_id }) => {
      try {
        const result = await refreshRequest(env, request_id);
        return {
          content: [{
            type: "text" as const,
            text: `Validation ${request_id} is ${String(result.state)}.`,
          }],
          structuredContent: result,
        };
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "read_validation_evidence",
    {
      title: "Read validation evidence",
      description:
        "Return the terminal structured result and a downloadable link to the immutable evidence artifact. Use after await_validation reports a terminal state.",
      inputSchema: { request_id: requestId },
      outputSchema: {
        request_id: z.string(),
        state,
        conclusion: z.string().nullable(),
        failure_kind: z.string().nullable(),
        diagnostic: z.string(),
        evidence_url: z.string().url(),
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ request_id }) => {
      try {
        const row = await getRequest(env.VALIDATION_DB, request_id);
        if (row === null) throw new ServiceError("not_found", "Unknown request_id.", 404);
        if (!row.evidence_object_key) {
          throw new ServiceError("evidence_not_available", `Request state is ${row.state}.`, 409);
        }
        let result: ValidationResult | null = null;
        if (row.result_object_key) {
          result = JSON.parse(new TextDecoder().decode(await readResult(env, request_id))) as ValidationResult;
        }
        const evidenceUrl = downloadUrl(publicBaseUrl, request_id, "evidence.zip");
        const structuredContent = {
          request_id,
          state: row.state,
          conclusion: result?.conclusion ?? row.conclusion,
          failure_kind: result?.failure_kind ?? null,
          diagnostic: result?.diagnostic ?? "No result.json was produced; inspect the infrastructure evidence.",
          evidence_url: evidenceUrl,
        };
        return {
          content: [
            { type: "text" as const, text: structuredContent.diagnostic },
            {
              type: "resource_link" as const,
              uri: evidenceUrl,
              name: `${request_id}-evidence.zip`,
              description: "Immutable validation evidence downloaded from R2.",
              mimeType: "application/zip",
            },
          ],
          structuredContent,
        };
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "get_validated_candidate",
    {
      title: "Get the exact validated candidate",
      description:
        "Return a downloadable link to the exact R2 ZIP that obtained a successful validation. Fails for every non-success state.",
      inputSchema: { request_id: requestId },
      outputSchema: {
        request_id: z.string(),
        sha256: z.string(),
        size: z.number().int().positive(),
        candidate_url: z.string().url(),
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ request_id }) => {
      try {
        const candidate = await readValidatedCandidate(env, request_id);
        const candidateUrl = downloadUrl(publicBaseUrl, request_id, "candidate.zip");
        const structuredContent = {
          request_id,
          sha256: candidate.row.package_sha256,
          size: candidate.row.package_size,
          candidate_url: candidateUrl,
        };
        return {
          content: [
            {
              type: "text" as const,
              text: `Validated candidate ${request_id}: ${candidate.row.package_size} bytes, SHA-256 ${candidate.row.package_sha256}.`,
            },
            {
              type: "resource_link" as const,
              uri: candidateUrl,
              name: `${request_id}.zip`,
              description: "Exact candidate bytes that obtained a successful validation.",
              mimeType: "application/zip",
            },
          ],
          structuredContent,
        };
      } catch (error) {
        return toolError(error);
      }
    },
  );

  return server;
}

function downloadUrl(baseUrl: string, requestId: string, filename: string): string {
  return `${baseUrl.replace(/\/$/, "")}/downloads/${encodeURIComponent(requestId)}/${filename}`;
}

function toolError(error: unknown) {
  const serviceError =
    error instanceof ServiceError
      ? error
      : new ServiceError("internal_error", error instanceof Error ? error.message : String(error), 500);
  return {
    isError: true,
    content: [{ type: "text" as const, text: `${serviceError.code}: ${serviceError.message}` }],
  };
}
