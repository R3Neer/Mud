import { strToU8, unzipSync } from "fflate";

import { decodeCanonicalBase64, sha256Hex } from "./crypto.js";
import {
  acceptRequest,
  expireIfDue,
  getRequest,
  markQueued,
  markRunning,
  markTerminal,
  patchDispatch,
  transition,
} from "./db.js";
import { ServiceError } from "./errors.js";
import {
  dispatchWorkflow,
  downloadEvidenceArtifact,
  findAmbiguousDispatch,
  getWorkflowRun,
} from "./github.js";
import { finalizeStagedFiles } from "./staging.js";
import {
  readVerifiedObject,
  putImmutableCandidate,
  putImmutableEvidence,
  candidateKey,
  readVerifiedEvidence,
} from "./storage.js";
import {
  PROTOCOL,
  RESULT_PROTOCOL,
  type CandidateIdentity,
  type Env,
  type LogicalFile,
  type ValidationResult,
  type ValidationRow,
} from "./types.js";
import { buildDeterministicZip, MAX_PACKAGE_BYTES } from "./zip.js";

const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$/;
const SHA40 = /^[0-9a-f]{40}$/;

export interface SubmitCommon {
  protocol: typeof PROTOCOL;
  request_id: string;
  target_sha: string;
  trust_plugin: boolean;
}

export interface SubmitZip extends SubmitCommon {
  package_base64: string;
  expected_sha256?: string;
}

export interface SubmitFiles extends SubmitCommon {
  files: LogicalFile[];
}

export interface SubmitStagedFiles extends SubmitCommon {
  batch_ids: string[];
  expected_file_count: number;
}

function validateCommon(input: SubmitCommon): void {
  if (input.protocol !== PROTOCOL) throw new ServiceError("unsupported_protocol", "Unsupported protocol.");
  if (!REQUEST_ID.test(input.request_id)) throw new ServiceError("invalid_request_id", "Invalid request_id.");
  if (!SHA40.test(input.target_sha)) throw new ServiceError("invalid_target_sha", "Invalid target_sha.");
  if (typeof input.trust_plugin !== "boolean") {
    throw new ServiceError("invalid_trust_plugin", "trust_plugin must be boolean.");
  }
}

function publicRow(row: ValidationRow): Record<string, unknown> {
  return {
    protocol: PROTOCOL,
    request_id: row.request_id,
    target_sha: row.target_sha,
    package_sha256: row.package_sha256,
    package_size: row.package_size,
    trust_plugin: Boolean(row.trust_plugin),
    transport_kind: row.transport_kind,
    state: row.state,
    github_run_id: row.github_run_id,
    github_run_url: row.github_run_url,
    github_run_attempt: row.github_run_attempt,
    control_sha: row.control_sha,
    conclusion: row.conclusion,
    runtime_version: row.runtime_version,
    created_at: row.created_at,
    completed_at: row.completed_at,
  };
}

async function acceptBytes(
  env: Env,
  common: SubmitCommon,
  bytes: Uint8Array,
  transportKind: "zip_base64" | "logical_files" | "files_staged_v1",
  expectedSha256?: string,
): Promise<Record<string, unknown>> {
  validateCommon(common);
  if (bytes.byteLength < 1 || bytes.byteLength > MAX_PACKAGE_BYTES) {
    throw new ServiceError("payload_too_large", `Candidate must be 1-${MAX_PACKAGE_BYTES} bytes.`, 413);
  }
  const packageSha256 = await sha256Hex(bytes);
  if (expectedSha256 !== undefined && expectedSha256.toLowerCase() !== packageSha256) {
    throw new ServiceError("sha256_mismatch", "Declared SHA-256 differs from candidate bytes.");
  }
  const identity: CandidateIdentity = {
    requestId: common.request_id,
    targetSha: common.target_sha,
    packageSha256,
    packageSize: bytes.byteLength,
    trustPlugin: common.trust_plugin,
    transportKind,
  };
  const stored = await putImmutableCandidate(env.VALIDATION_BUCKET, identity, bytes);
  const accepted = await acceptRequest(env.VALIDATION_DB, identity);
  let row = accepted.row;

  if (row.state === "accepted") {
    const won = await transition(env.VALIDATION_DB, row.request_id, "accepted", "dispatching");
    row = (await getRequest(env.VALIDATION_DB, row.request_id))!;
    if (won) {
      const dispatched = await dispatchWorkflow(env, row);
      await patchDispatch(
        env.VALIDATION_DB,
        row.request_id,
        dispatched.workflow_run_id,
        dispatched.html_url,
      );
      const run = await getWorkflowRun(env, dispatched.workflow_run_id);
      await markQueued(env.VALIDATION_DB, row.request_id, run.head_sha, run.run_attempt);
      row = (await getRequest(env.VALIDATION_DB, row.request_id))!;
    }
  } else if (row.state === "dispatching") {
    row = await reconcileDispatch(env, row);
  }

  return { ...publicRow(row), reused: !accepted.created || stored.reused };
}

export async function submitStagedFiles(
  env: Env,
  input: SubmitStagedFiles,
): Promise<Record<string, unknown>> {
  validateCommon(input);
  const finalized = await finalizeStagedFiles(
    env.VALIDATION_BUCKET,
    input.request_id,
    input.batch_ids,
    input.expected_file_count,
  );
  const accepted = await acceptBytes(env, input, finalized.bytes, "files_staged_v1");
  return {
    ...accepted,
    batch_count: finalized.batchCount,
    file_count: finalized.fileCount,
  };
}

export async function submitZip(env: Env, input: SubmitZip): Promise<Record<string, unknown>> {
  validateCommon(input);
  if (typeof input.package_base64 !== "string") {
    throw new ServiceError("invalid_base64", "package_base64 must be a string.");
  }
  return acceptBytes(
    env,
    input,
    decodeCanonicalBase64(input.package_base64, MAX_PACKAGE_BYTES),
    "zip_base64",
    input.expected_sha256,
  );
}

export async function submitFiles(env: Env, input: SubmitFiles): Promise<Record<string, unknown>> {
  validateCommon(input);
  if (!Array.isArray(input.files)) throw new ServiceError("invalid_files", "files must be an array.");
  for (const file of input.files) {
    if (
      typeof file !== "object" ||
      file === null ||
      typeof file.path !== "string" ||
      !["utf8", "base64"].includes(file.encoding) ||
      typeof file.content !== "string"
    ) {
      throw new ServiceError("invalid_files", "Each file needs path, encoding and content.");
    }
  }
  return acceptBytes(env, input, buildDeterministicZip(input.files), "logical_files");
}

async function reconcileDispatch(env: Env, row: ValidationRow): Promise<ValidationRow> {
  if (row.github_run_id === null) {
    const match = await findAmbiguousDispatch(env, row);
    if (match === null) {
      throw new ServiceError(
        "dispatch_reconciliation_pending",
        "Dispatch response was ambiguous and no matching run is visible yet.",
        409,
        true,
      );
    }
    await patchDispatch(env.VALIDATION_DB, row.request_id, match.id, match.html_url);
    row = (await getRequest(env.VALIDATION_DB, row.request_id))!;
  }
  const run = await getWorkflowRun(env, row.github_run_id!);
  await markQueued(env.VALIDATION_DB, row.request_id, run.head_sha, run.run_attempt);
  return (await getRequest(env.VALIDATION_DB, row.request_id))!;
}

function parseResult(files: Record<string, Uint8Array>): ValidationResult | null {
  const raw = files["result.json"];
  if (!raw) return null;
  try {
    return JSON.parse(new TextDecoder().decode(raw)) as ValidationResult;
  } catch {
    throw new ServiceError("invalid_result_artifact", "result.json is not valid JSON.", 502);
  }
}

async function verifyResult(
  env: Env,
  row: ValidationRow,
  result: ValidationResult,
  files: Record<string, Uint8Array>,
): Promise<void> {
  const checks: Array<[string, unknown, unknown]> = [
    ["protocol", result.protocol, RESULT_PROTOCOL],
    ["request_id", result.request_id, row.request_id],
    ["workflow_run_id", result.workflow_run_id, row.github_run_id],
    ["run_attempt", result.run_attempt, row.github_run_attempt],
    ["control_sha", result.control_sha, row.control_sha],
    ["target_sha", result.target_sha, row.target_sha],
    ["package_sha256", result.package_sha256, row.package_sha256],
    ["package_size", result.package_size, row.package_size],
  ];
  for (const [name, actual, expected] of checks) {
    if (actual !== expected) {
      throw new ServiceError("result_identity_mismatch", `Result ${name} does not match request.`, 502);
    }
  }
  if (result.conclusion === "success" && result.runtime_version !== "0.2.0") {
    throw new ServiceError("runtime_version_mismatch", "Successful result did not use RepoPatcher 0.2.0.", 502);
  }
  const candidate = files["candidate.zip"];
  if (!candidate) throw new ServiceError("candidate_missing_from_artifact", "Artifact omitted candidate.zip.", 502);
  const candidateHash = await sha256Hex(candidate);
  if (candidate.byteLength !== row.package_size || candidateHash !== row.package_sha256) {
    throw new ServiceError("artifact_candidate_mismatch", "Artifact candidate differs from R2 identity.", 502);
  }
  const stored = await readVerifiedObject(
    env.VALIDATION_BUCKET,
    candidateKey(row.package_sha256),
    row.package_sha256,
    row.package_size,
  );
  if (await sha256Hex(stored.bytes) !== candidateHash) {
    throw new ServiceError("artifact_candidate_mismatch", "Artifact candidate differs from stored object.", 502);
  }
}

async function finalizeCompleted(
  env: Env,
  row: ValidationRow,
  githubConclusion: string | null,
): Promise<ValidationRow> {
  const artifact = await downloadEvidenceArtifact(env, row);
  let files: Record<string, Uint8Array>;
  const wanted = new Set(["result.json", "candidate.zip", "infrastructure.json"]);
  try {
    files = unzipSync(artifact, {
      filter: (file) => {
        if (!wanted.has(file.name)) return false;
        const maximum = file.name === "candidate.zip" ? MAX_PACKAGE_BYTES : 1024 * 1024;
        if (file.originalSize > maximum) {
          throw new ServiceError("artifact_entry_too_large", `${file.name} exceeds ${maximum} bytes.`, 502);
        }
        return true;
      },
    });
  } catch {
    throw new ServiceError("invalid_evidence_zip", "GitHub artifact is invalid or exceeds limits.", 502);
  }
  const result = parseResult(files);
  const evidenceKey = `evidence/${row.request_id}/${row.github_run_attempt}.zip`;
  await putImmutableEvidence(
    env.VALIDATION_BUCKET,
    evidenceKey,
    artifact,
    { requestId: row.request_id, runId: String(row.github_run_id) },
    "application/zip",
  );

  if (result === null) {
    await markTerminal(env.VALIDATION_DB, row, "infrastructure_error", {
      conclusion: githubConclusion ?? "unknown",
      runtimeVersion: null,
      resultObjectKey: null,
      evidenceObjectKey: evidenceKey,
    });
    return (await getRequest(env.VALIDATION_DB, row.request_id))!;
  }
  await verifyResult(env, row, result, files);
  const resultBytes = strToU8(JSON.stringify(result));
  const resultKey = `results/${row.request_id}/${row.github_run_attempt}.json`;
  await putImmutableEvidence(
    env.VALIDATION_BUCKET,
    resultKey,
    resultBytes,
    { requestId: row.request_id, runId: String(row.github_run_id) },
    "application/json",
  );

  let terminal: "succeeded" | "failed" | "infrastructure_error";
  if (result.conclusion === "success" && githubConclusion === "success") terminal = "succeeded";
  else if (result.conclusion === "failure" && githubConclusion === "failure") terminal = "failed";
  else terminal = "infrastructure_error";
  await markTerminal(env.VALIDATION_DB, row, terminal, {
    conclusion: result.conclusion,
    runtimeVersion: result.runtime_version,
    resultObjectKey: resultKey,
    evidenceObjectKey: evidenceKey,
  });
  return (await getRequest(env.VALIDATION_DB, row.request_id))!;
}

export async function refreshRequest(env: Env, requestId: string): Promise<Record<string, unknown>> {
  let row = await getRequest(env.VALIDATION_DB, requestId);
  if (row === null) throw new ServiceError("not_found", "Unknown request_id.", 404);
  row = await expireIfDue(env.VALIDATION_DB, row);
  if (row.state === "dispatching") row = await reconcileDispatch(env, row);
  if (["queued", "running"].includes(row.state)) {
    const run = await getWorkflowRun(env, row.github_run_id!);
    if (run.head_sha !== row.control_sha || run.run_attempt !== row.github_run_attempt) {
      throw new ServiceError("github_run_identity_mismatch", "GitHub run identity changed.", 502);
    }
    if (run.status === "completed") row = await finalizeCompleted(env, row, run.conclusion);
  }
  return publicRow(row);
}

export async function authorizeAndReadCandidate(
  env: Env,
  row: ValidationRow,
): Promise<{ bytes: Uint8Array; row: ValidationRow }> {
  if (!["queued", "running"].includes(row.state)) {
    throw new ServiceError("candidate_download_rejected", `Request state is ${row.state}.`, 409);
  }
  await markRunning(env.VALIDATION_DB, row);
  const current = (await getRequest(env.VALIDATION_DB, row.request_id))!;
  const stored = await readVerifiedObject(
    env.VALIDATION_BUCKET,
    candidateKey(current.package_sha256),
    current.package_sha256,
    current.package_size,
  );
  return { bytes: stored.bytes, row: current };
}

export async function readValidatedCandidate(
  env: Env,
  requestId: string,
): Promise<{ bytes: Uint8Array; row: ValidationRow }> {
  const row = await getRequest(env.VALIDATION_DB, requestId);
  if (row === null) throw new ServiceError("not_found", "Unknown request_id.", 404);
  if (row.state !== "succeeded") {
    throw new ServiceError("candidate_not_validated", `Request state is ${row.state}.`, 409);
  }
  const object = await readVerifiedObject(
    env.VALIDATION_BUCKET,
    candidateKey(row.package_sha256),
    row.package_sha256,
    row.package_size,
  );
  return { bytes: object.bytes, row };
}

export async function readResult(env: Env, requestId: string): Promise<Uint8Array> {
  const row = await getRequest(env.VALIDATION_DB, requestId);
  if (row === null) throw new ServiceError("not_found", "Unknown request_id.", 404);
  if (!row.result_object_key) {
    throw new ServiceError("result_not_available", `Request state is ${row.state}.`, 409);
  }
  return readVerifiedEvidence(env.VALIDATION_BUCKET, row.result_object_key);
}

export async function readEvidenceArtifact(env: Env, requestId: string): Promise<Uint8Array> {
  const row = await getRequest(env.VALIDATION_DB, requestId);
  if (row === null) throw new ServiceError("not_found", "Unknown request_id.", 404);
  if (!row.evidence_object_key) {
    throw new ServiceError("evidence_not_available", `Request state is ${row.state}.`, 409);
  }
  return readVerifiedEvidence(env.VALIDATION_BUCKET, row.evidence_object_key);
}
