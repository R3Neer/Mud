import { strToU8 } from "fflate";

import { sha256Hex } from "./crypto.js";
import { ServiceError } from "./errors.js";
import type { StagedFileBatch, StagedUtf8File, StagedUtf8FileInput } from "./types.js";
import {
  buildDeterministicZip,
  MAX_FILES,
  MAX_FILE_BYTES,
  MAX_TOTAL_FILE_BYTES,
  normalizePath,
} from "./zip.js";

export const STAGED_FILES_PROTOCOL = "mud-repo-patcher-staged-files/v1" as const;
export const MAX_BATCH_FILES = 32;
export const MAX_BATCH_CONTENT_CHARS = 24 * 1024;
export const MAX_STAGED_BATCHES = 64;

const IDENTIFIER = /^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$/;
const SHA256 = /^[0-9a-f]{64}$/;

export interface StageFilesInput {
  request_id: string;
  batch_id: string;
  files: StagedUtf8FileInput[];
}

export interface StoredBatch {
  requestId: string;
  batchId: string;
  fileCount: number;
  totalSize: number;
  batchSha256: string;
  files: Array<{ path: string; size: number; sha256: string }>;
  reused: boolean;
}

export interface FinalizedStagedFiles {
  bytes: Uint8Array;
  batchCount: number;
  fileCount: number;
}

export function validateStagingIdentifier(value: string, name: string): string {
  if (!IDENTIFIER.test(value)) {
    throw new ServiceError(`invalid_${name}`, `${name} is not a valid identifier.`);
  }
  return value;
}

function batchKey(requestId: string, batchId: string): string {
  validateStagingIdentifier(requestId, "request_id");
  validateStagingIdentifier(batchId, "batch_id");
  return `staging/${requestId}/batches/${batchId}.json`;
}

async function canonicalBatch(
  requestId: string,
  batchId: string,
  files: StagedUtf8FileInput[],
): Promise<{ batch: StagedFileBatch; bytes: Uint8Array; totalSize: number; sha256: string }> {
  validateStagingIdentifier(requestId, "request_id");
  validateStagingIdentifier(batchId, "batch_id");
  if (!Array.isArray(files) || files.length < 1 || files.length > MAX_BATCH_FILES) {
    throw new ServiceError(
      "invalid_batch_file_count",
      `A batch must contain 1-${MAX_BATCH_FILES} complete files.`,
    );
  }
  const contentChars = files.reduce(
    (total, file) => total + (typeof file?.content === "string" ? file.content.length : 0),
    0,
  );
  if (contentChars > MAX_BATCH_CONTENT_CHARS) {
    throw new ServiceError(
      "batch_too_large",
      `Batch content exceeds ${MAX_BATCH_CONTENT_CHARS} characters.`,
      413,
    );
  }

  const canonicalFiles: StagedUtf8File[] = [];
  const collisionKeys = new Set<string>();
  let totalSize = 0;
  for (const file of files) {
    if (
      typeof file !== "object" ||
      file === null ||
      typeof file.path !== "string" ||
      typeof file.content !== "string" ||
      (file.expected_size !== undefined && !Number.isSafeInteger(file.expected_size)) ||
      (file.expected_sha256 !== undefined && typeof file.expected_sha256 !== "string")
    ) {
      throw new ServiceError(
        "invalid_staged_file",
        "Each staged file needs path and UTF-8 content; integrity assertions are optional.",
      );
    }
    const path = normalizePath(file.path);
    const collisionKey = path.normalize("NFC").toLocaleLowerCase("en-US");
    if (collisionKeys.has(collisionKey)) {
      throw new ServiceError("duplicate_path", `Duplicate or Windows-colliding path: ${path}`);
    }
    collisionKeys.add(collisionKey);
    const bytes = strToU8(file.content);
    if (bytes.byteLength > MAX_FILE_BYTES) {
      throw new ServiceError("file_too_large", `${path} exceeds ${MAX_FILE_BYTES} bytes.`, 413);
    }
    const actualSha256 = await sha256Hex(bytes);
    const expectedSha256 = file.expected_sha256?.toLowerCase();
    if (expectedSha256 !== undefined && !SHA256.test(expectedSha256)) {
      throw new ServiceError("invalid_file_sha256", `Invalid SHA-256 for ${path}.`);
    }
    if (
      (file.expected_size !== undefined && file.expected_size !== bytes.byteLength) ||
      (expectedSha256 !== undefined && expectedSha256 !== actualSha256)
    ) {
      throw new ServiceError(
        "file_integrity_mismatch",
        `Declared size or SHA-256 differs from UTF-8 bytes for ${path}.`,
      );
    }
    totalSize += bytes.byteLength;
    canonicalFiles.push({
      path,
      content: file.content,
      expected_size: bytes.byteLength,
      expected_sha256: actualSha256,
    });
  }
  if (totalSize > MAX_TOTAL_FILE_BYTES) {
    throw new ServiceError("payload_too_large", "Batch files exceed the total size limit.", 413);
  }
  canonicalFiles.sort((left, right) => compareUtf8(left.path, right.path));
  const batch: StagedFileBatch = {
    schema: 1,
    protocol: STAGED_FILES_PROTOCOL,
    request_id: requestId,
    batch_id: batchId,
    files: canonicalFiles,
  };
  const bytes = strToU8(JSON.stringify(batch));
  return { batch, bytes, totalSize, sha256: await sha256Hex(bytes) };
}

export async function stageCandidateFiles(
  bucket: R2Bucket,
  input: StageFilesInput,
): Promise<StoredBatch> {
  const canonical = await canonicalBatch(input.request_id, input.batch_id, input.files);
  const key = batchKey(input.request_id, input.batch_id);
  const created = await bucket.put(key, canonical.bytes, {
    onlyIf: new Headers({ "If-None-Match": "*" }),
    httpMetadata: { contentType: "application/json" },
    customMetadata: {
      requestId: input.request_id,
      batchId: input.batch_id,
      sha256: canonical.sha256,
      size: String(canonical.bytes.byteLength),
    },
    sha256: canonical.sha256,
  });
  const reused = created === null;
  if (reused) {
    const existing = await bucket.get(key);
    if (existing === null) {
      throw new ServiceError(
        "storage_race_inconsistent",
        "R2 rejected batch creation but the winning object cannot be read.",
        500,
      );
    }
    const existingBytes = new Uint8Array(await existing.arrayBuffer());
    if (
      existing.customMetadata?.requestId !== input.request_id ||
      existing.customMetadata?.batchId !== input.batch_id ||
      existing.customMetadata?.sha256 !== canonical.sha256 ||
      existing.customMetadata?.size !== String(canonical.bytes.byteLength) ||
      !equalBytes(existingBytes, canonical.bytes)
    ) {
      throw new ServiceError(
        "staged_batch_conflict",
        "request_id and batch_id are already associated with different files.",
        409,
      );
    }
  }
  return {
    requestId: input.request_id,
    batchId: input.batch_id,
    fileCount: canonical.batch.files.length,
    totalSize: canonical.totalSize,
    batchSha256: canonical.sha256,
    files: canonical.batch.files.map((file) => ({
      path: file.path,
      size: file.expected_size,
      sha256: file.expected_sha256,
    })),
    reused,
  };
}

async function readBatch(
  bucket: R2Bucket,
  requestId: string,
  batchId: string,
): Promise<StagedFileBatch> {
  const key = batchKey(requestId, batchId);
  const object = await bucket.get(key);
  if (object === null) {
    throw new ServiceError("staged_batch_not_found", `Staged batch does not exist: ${batchId}.`, 404);
  }
  const bytes = new Uint8Array(await object.arrayBuffer());
  const actualSha256 = await sha256Hex(bytes);
  if (
    object.customMetadata?.requestId !== requestId ||
    object.customMetadata?.batchId !== batchId ||
    object.customMetadata?.sha256 !== actualSha256 ||
    object.customMetadata?.size !== String(bytes.byteLength)
  ) {
    throw new ServiceError("staged_batch_corrupt", `Stored batch metadata is invalid: ${batchId}.`, 500);
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
  } catch {
    throw new ServiceError("staged_batch_corrupt", `Stored batch is not UTF-8 JSON: ${batchId}.`, 500);
  }
  if (!isStagedBatch(parsed)) {
    throw new ServiceError("staged_batch_corrupt", `Stored batch does not match its schema: ${batchId}.`, 500);
  }
  if (parsed.request_id !== requestId || parsed.batch_id !== batchId) {
    throw new ServiceError("staged_batch_mismatch", `Stored batch belongs to another request.`, 500);
  }
  const canonical = await canonicalBatch(requestId, batchId, parsed.files);
  if (!equalBytes(bytes, canonical.bytes)) {
    throw new ServiceError("staged_batch_noncanonical", `Stored batch is not canonical: ${batchId}.`, 500);
  }
  return canonical.batch;
}

export async function finalizeStagedFiles(
  bucket: R2Bucket,
  requestId: string,
  batchIds: string[],
  expectedFileCount: number,
): Promise<FinalizedStagedFiles> {
  validateStagingIdentifier(requestId, "request_id");
  if (!Array.isArray(batchIds) || batchIds.length < 1 || batchIds.length > MAX_STAGED_BATCHES) {
    throw new ServiceError(
      "invalid_batch_count",
      `Expected 1-${MAX_STAGED_BATCHES} batch identifiers.`,
    );
  }
  if (new Set(batchIds).size !== batchIds.length) {
    throw new ServiceError("duplicate_batch_id", "batch_ids contains duplicates.");
  }
  if (!Number.isSafeInteger(expectedFileCount) || expectedFileCount < 1 || expectedFileCount > MAX_FILES) {
    throw new ServiceError("invalid_file_count", `Expected 1-${MAX_FILES} files.`);
  }
  const files: StagedUtf8File[] = [];
  for (const batchId of batchIds) {
    files.push(...(await readBatch(bucket, requestId, batchId)).files);
  }
  if (files.length !== expectedFileCount) {
    throw new ServiceError(
      "file_count_mismatch",
      `Expected ${expectedFileCount} files but staged batches contain ${files.length}.`,
    );
  }
  const logicalFiles = files.map((file) => ({
    path: file.path,
    encoding: "utf8" as const,
    content: file.content,
  }));
  return {
    bytes: buildDeterministicZip(logicalFiles),
    batchCount: batchIds.length,
    fileCount: files.length,
  };
}

function isStagedBatch(value: unknown): value is StagedFileBatch {
  if (typeof value !== "object" || value === null) return false;
  const batch = value as Record<string, unknown>;
  if (
    batch.schema !== 1 ||
    batch.protocol !== STAGED_FILES_PROTOCOL ||
    typeof batch.request_id !== "string" ||
    typeof batch.batch_id !== "string" ||
    !Array.isArray(batch.files)
  ) {
    return false;
  }
  return batch.files.every((value: unknown) => {
    if (typeof value !== "object" || value === null) return false;
    const file = value as Record<string, unknown>;
    return (
      typeof file.path === "string" &&
      typeof file.content === "string" &&
      Number.isSafeInteger(file.expected_size) &&
      typeof file.expected_sha256 === "string"
    );
  });
}

function equalBytes(left: Uint8Array, right: Uint8Array): boolean {
  if (left.byteLength !== right.byteLength) return false;
  return left.every((byte, index) => byte === right[index]);
}

function compareUtf8(left: string, right: string): number {
  const a = strToU8(left);
  const b = strToU8(right);
  for (let index = 0; index < Math.min(a.length, b.length); index += 1) {
    if (a[index] !== b[index]) return a[index] - b[index];
  }
  return a.length - b.length;
}
