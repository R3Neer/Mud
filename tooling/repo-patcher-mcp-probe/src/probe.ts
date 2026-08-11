import { strToU8, zipSync, type Zippable } from "fflate";

import type {
  ProbeFileInput,
  ProbeFileWithIntegrity,
  StagedProbeBatch,
  StoredProbe,
  StoredProbeBatch,
} from "./types.js";

export const MAX_BASE64_BYTES = 256 * 1024;
export const MAX_FILES = 500;
export const MAX_FILE_BYTES = 512 * 1024;
export const MAX_TOTAL_FILE_BYTES = 1024 * 1024;
export const MAX_BATCH_FILES = 32;
export const MAX_BATCH_CONTENT_CHARS = 24 * 1024;
export const MAX_STAGED_BATCHES = 64;
// fflate serializes local calendar fields, so construct local midnight instead of
// parsing a UTC timestamp. The resulting DOS timestamp is identical in every zone.
export const FIXED_ZIP_MTIME = new Date(1980, 0, 1, 0, 0, 0, 0);

const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$/;
const SHA256 = /^[0-9a-f]{64}$/;
const BASE64 = /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/;
const WINDOWS_FORBIDDEN = /[\u0000-\u001f<>:"|?*]/;
const WINDOWS_RESERVED = /^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?$/i;

export class ProbeError extends Error {
  constructor(
    public readonly code: string,
    message: string,
  ) {
    super(message);
    this.name = "ProbeError";
  }
}

export function validateRequestId(requestId: string): string {
  if (!REQUEST_ID.test(requestId)) {
    throw new ProbeError(
      "invalid_request_id",
      "request_id debe tener entre 1 y 80 caracteres ASCII alfanuméricos, punto, guion o guion bajo.",
    );
  }
  return requestId;
}

export function decodeCanonicalBase64(value: string, maxBytes = MAX_BASE64_BYTES): Uint8Array {
  if (value.length === 0 || value.length % 4 !== 0 || !BASE64.test(value)) {
    throw new ProbeError("invalid_base64", "El contenido no es base64 canónico.");
  }

  const decoded = Uint8Array.from(atob(value), (character) => character.charCodeAt(0));
  if (decoded.byteLength > maxBytes) {
    throw new ProbeError(
      "payload_too_large",
      `El contenido decodificado supera el límite de ${maxBytes} bytes.`,
    );
  }

  const canonical = bytesToBase64(decoded);
  if (canonical !== value) {
    throw new ProbeError("invalid_base64", "El contenido no usa una representación base64 canónica.");
  }
  return decoded;
}

export function bytesToBase64(bytes: Uint8Array): string {
  let binary = "";
  const chunkSize = 0x8000;
  for (let offset = 0; offset < bytes.length; offset += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(offset, offset + chunkSize));
  }
  return btoa(binary);
}

export async function sha256Hex(bytes: Uint8Array): Promise<string> {
  const stableBuffer = Uint8Array.from(bytes).buffer;
  const digest = await crypto.subtle.digest("SHA-256", stableBuffer);
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

export function normalizeProbePath(rawPath: string): string {
  if (!rawPath || rawPath.includes("\\") || rawPath.startsWith("/") || /^[A-Za-z]:/.test(rawPath)) {
    throw new ProbeError("invalid_path", `Ruta no válida: ${rawPath || "(vacía)"}`);
  }
  const segments = rawPath.split("/");
  if (segments.some((segment) => segment === "" || segment === "." || segment === "..")) {
    throw new ProbeError("invalid_path", `Ruta no válida: ${rawPath}`);
  }
  if (
    segments.some(
      (segment) =>
        WINDOWS_FORBIDDEN.test(segment) ||
        segment.endsWith(".") ||
        segment.endsWith(" ") ||
        WINDOWS_RESERVED.test(segment),
    )
  ) {
    throw new ProbeError("invalid_path", `Ruta incompatible con Windows: ${rawPath}`);
  }
  if (rawPath.length > 240) {
    throw new ProbeError("invalid_path", `La ruta supera 240 caracteres: ${rawPath}`);
  }
  return segments.join("/");
}

export function buildDeterministicZip(files: ProbeFileInput[]): Uint8Array {
  const normalized = decodeProbeFiles(files, MAX_FILES, MAX_TOTAL_FILE_BYTES);
  const entries: Zippable = {};
  for (const file of normalized) {
    entries[file.path] = [
      file.bytes,
      {
        level: 6,
        mtime: FIXED_ZIP_MTIME,
      },
    ];
  }
  return zipSync(entries, { level: 6, mtime: FIXED_ZIP_MTIME });
}

export async function createStagedBatch(
  requestId: string,
  batchId: string,
  files: ProbeFileWithIntegrity[],
): Promise<{ batch: StagedProbeBatch; bytes: Uint8Array; sha256: string; totalSize: number }> {
  validateRequestId(requestId);
  validateRequestId(batchId);
  if (files.length === 0 || files.length > MAX_BATCH_FILES) {
    throw new ProbeError(
      "invalid_batch_file_count",
      `Cada lote debe contener entre 1 y ${MAX_BATCH_FILES} archivos completos.`,
    );
  }
  const contentChars = files.reduce((total, file) => total + file.content.length, 0);
  if (contentChars > MAX_BATCH_CONTENT_CHARS) {
    throw new ProbeError(
      "batch_too_large",
      `El contenido textual del lote supera ${MAX_BATCH_CONTENT_CHARS} caracteres.`,
    );
  }

  const decoded = decodeProbeFiles(files, MAX_BATCH_FILES, MAX_TOTAL_FILE_BYTES);
  const byPath = new Map(files.map((file) => [normalizeProbePath(file.path), file]));
  let totalSize = 0;
  const canonicalFiles: ProbeFileWithIntegrity[] = [];
  for (const file of decoded) {
    const source = byPath.get(file.path);
    if (source === undefined) {
      throw new ProbeError("internal_error", `No se pudo canonicalizar ${file.path}.`);
    }
    const actualSha256 = await sha256Hex(file.bytes);
    const expectedSha256 = source.expected_sha256.toLowerCase();
    if (!SHA256.test(expectedSha256)) {
      throw new ProbeError("invalid_file_sha256", `SHA-256 no válido para ${file.path}.`);
    }
    if (source.expected_size !== file.bytes.byteLength || expectedSha256 !== actualSha256) {
      throw new ProbeError(
        "file_integrity_mismatch",
        `Tamaño o SHA-256 no coincide para ${file.path}.`,
      );
    }
    totalSize += file.bytes.byteLength;
    canonicalFiles.push({
      path: file.path,
      encoding: source.encoding,
      content: source.content,
      expected_size: file.bytes.byteLength,
      expected_sha256: actualSha256,
    });
  }

  const batch: StagedProbeBatch = {
    schema: 1,
    protocol: "mud-repo-patcher-staged-files/v1",
    request_id: requestId,
    batch_id: batchId,
    files: canonicalFiles,
  };
  const bytes = strToU8(JSON.stringify(batch));
  return { batch, bytes, sha256: await sha256Hex(bytes), totalSize };
}

export async function parseStagedBatch(
  bytes: Uint8Array,
  requestId: string,
  batchId: string,
): Promise<StagedProbeBatch> {
  let parsed: unknown;
  try {
    parsed = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
  } catch {
    throw new ProbeError("staged_batch_corrupt", `El lote ${batchId} no contiene JSON UTF-8 válido.`);
  }
  if (!isStagedProbeBatch(parsed)) {
    throw new ProbeError("staged_batch_corrupt", `El lote ${batchId} no cumple el esquema.`);
  }
  if (parsed.request_id !== requestId || parsed.batch_id !== batchId) {
    throw new ProbeError("staged_batch_mismatch", `El lote ${batchId} pertenece a otra solicitud.`);
  }
  const canonical = await createStagedBatch(requestId, batchId, parsed.files);
  if (!equalBytes(canonical.bytes, bytes)) {
    throw new ProbeError("staged_batch_noncanonical", `El lote ${batchId} no es canónico.`);
  }
  return canonical.batch;
}

export async function storeImmutableStagedBatch(
  bucket: R2Bucket,
  requestId: string,
  batchId: string,
  files: ProbeFileWithIntegrity[],
): Promise<StoredProbeBatch> {
  const canonical = await createStagedBatch(requestId, batchId, files);
  const objectKey = stagedBatchObjectKey(requestId, batchId);
  const created = await bucket.put(objectKey, canonical.bytes, {
    onlyIf: new Headers({ "If-None-Match": "*" }),
    httpMetadata: { contentType: "application/json" },
    customMetadata: {
      requestId,
      batchId,
      sha256: canonical.sha256,
      size: String(canonical.bytes.byteLength),
    },
  });
  const reused = created === null;
  if (reused) {
    const existing = await bucket.get(objectKey);
    if (existing === null) {
      throw new ProbeError(
        "storage_race_inconsistent",
        "R2 rechazó la creación del lote, pero el objeto ganador no puede leerse.",
      );
    }
    const existingBytes = new Uint8Array(await existing.arrayBuffer());
    if (!equalBytes(existingBytes, canonical.bytes)) {
      throw new ProbeError(
        "staged_batch_conflict",
        "request_id y batch_id ya están asociados a un lote diferente.",
      );
    }
  }
  return {
    requestId,
    batchId,
    objectKey,
    fileCount: canonical.batch.files.length,
    totalSize: canonical.totalSize,
    sha256: canonical.sha256,
    reused,
  };
}

export async function finalizeStagedProbe(
  bucket: R2Bucket,
  requestId: string,
  batchIds: string[],
  expectedFileCount: number,
  publicBaseUrl: string,
  routeSecret: string,
): Promise<{ stored: StoredProbe; batchCount: number; fileCount: number }> {
  validateRequestId(requestId);
  if (batchIds.length === 0 || batchIds.length > MAX_STAGED_BATCHES) {
    throw new ProbeError(
      "invalid_batch_count",
      `Se requieren entre 1 y ${MAX_STAGED_BATCHES} lotes.`,
    );
  }
  const uniqueBatchIds = new Set(batchIds);
  if (uniqueBatchIds.size !== batchIds.length) {
    throw new ProbeError("duplicate_batch_id", "batch_ids contiene identificadores duplicados.");
  }

  const files: ProbeFileWithIntegrity[] = [];
  for (const batchId of batchIds) {
    validateRequestId(batchId);
    const objectKey = stagedBatchObjectKey(requestId, batchId);
    const object = await bucket.get(objectKey);
    if (object === null) {
      throw new ProbeError("staged_batch_not_found", `No existe el lote ${batchId}.`);
    }
    const bytes = new Uint8Array(await object.arrayBuffer());
    const actualSha256 = await sha256Hex(bytes);
    if (
      object.customMetadata?.requestId !== requestId ||
      object.customMetadata?.batchId !== batchId ||
      object.customMetadata?.sha256 !== actualSha256 ||
      object.customMetadata?.size !== String(bytes.byteLength)
    ) {
      throw new ProbeError("staged_batch_corrupt", `Metadatos incoherentes para ${batchId}.`);
    }
    const batch = await parseStagedBatch(bytes, requestId, batchId);
    files.push(...batch.files);
  }
  if (files.length !== expectedFileCount) {
    throw new ProbeError(
      "file_count_mismatch",
      `Se esperaban ${expectedFileCount} archivos y se recibieron ${files.length}.`,
    );
  }
  const zip = buildDeterministicZip(files);
  const stored = await storeImmutableProbe(
    bucket,
    requestId,
    zip,
    undefined,
    publicBaseUrl,
    routeSecret,
  );
  return { stored, batchCount: batchIds.length, fileCount: files.length };
}

function stagedBatchObjectKey(requestId: string, batchId: string): string {
  validateRequestId(requestId);
  validateRequestId(batchId);
  return `staging/${requestId}/batches/${batchId}.json`;
}

function decodeProbeFiles(
  files: ProbeFileInput[],
  maxFiles: number,
  maxTotalBytes: number,
): Array<{ path: string; bytes: Uint8Array }> {
  if (files.length === 0 || files.length > maxFiles) {
    throw new ProbeError("invalid_file_count", `Se requieren entre 1 y ${maxFiles} archivos.`);
  }
  const decoded = files.map((file) => {
    const path = normalizeProbePath(file.path);
    const bytes =
      file.encoding === "utf8"
        ? strToU8(file.content)
        : decodeCanonicalBase64(file.content, MAX_FILE_BYTES);
    if (bytes.byteLength > MAX_FILE_BYTES) {
      throw new ProbeError(
        "file_too_large",
        `${path} supera el límite de ${MAX_FILE_BYTES} bytes.`,
      );
    }
    return { path, bytes };
  });

  const caseFolded = new Set<string>();
  let totalBytes = 0;
  for (const file of decoded) {
    const key = file.path.normalize("NFC").toLocaleLowerCase("en-US");
    if (caseFolded.has(key)) {
      throw new ProbeError("duplicate_path", `Ruta duplicada o incompatible con Windows: ${file.path}`);
    }
    caseFolded.add(key);
    totalBytes += file.bytes.byteLength;
  }
  if (totalBytes > maxTotalBytes) {
    throw new ProbeError(
      "payload_too_large",
      `Los archivos superan el límite total de ${maxTotalBytes} bytes.`,
    );
  }
  decoded.sort((left, right) => compareUtf8(left.path, right.path));
  return decoded;
}

function isStagedProbeBatch(value: unknown): value is StagedProbeBatch {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Record<string, unknown>;
  if (
    candidate.schema !== 1 ||
    candidate.protocol !== "mud-repo-patcher-staged-files/v1" ||
    typeof candidate.request_id !== "string" ||
    typeof candidate.batch_id !== "string" ||
    !Array.isArray(candidate.files)
  ) {
    return false;
  }
  return candidate.files.every((file: unknown) => {
    if (typeof file !== "object" || file === null) return false;
    const item = file as Record<string, unknown>;
    return (
      typeof item.path === "string" &&
      (item.encoding === "utf8" || item.encoding === "base64") &&
      typeof item.content === "string" &&
      Number.isSafeInteger(item.expected_size) &&
      typeof item.expected_sha256 === "string"
    );
  });
}

function equalBytes(left: Uint8Array, right: Uint8Array): boolean {
  if (left.byteLength !== right.byteLength) return false;
  return left.every((byte, index) => byte === right[index]);
}

function compareUtf8(left: string, right: string): number {
  const leftBytes = strToU8(left);
  const rightBytes = strToU8(right);
  const length = Math.min(leftBytes.length, rightBytes.length);
  for (let index = 0; index < length; index += 1) {
    if (leftBytes[index] !== rightBytes[index]) {
      return leftBytes[index] - rightBytes[index];
    }
  }
  return leftBytes.length - rightBytes.length;
}

export async function storeImmutableProbe(
  bucket: R2Bucket,
  requestId: string,
  bytes: Uint8Array,
  expectedSha256: string | undefined,
  publicBaseUrl: string,
  routeSecret: string,
): Promise<StoredProbe> {
  validateRequestId(requestId);
  const sha256 = await sha256Hex(bytes);
  if (expectedSha256 !== undefined && expectedSha256.toLowerCase() !== sha256) {
    throw new ProbeError(
      "sha256_mismatch",
      `SHA-256 declarado ${expectedSha256.toLowerCase()} no coincide con ${sha256}.`,
    );
  }

  const objectKey = `probe/${requestId}.zip`;
  const created = await bucket.put(objectKey, bytes, {
    onlyIf: new Headers({ "If-None-Match": "*" }),
    httpMetadata: { contentType: "application/zip" },
    customMetadata: { requestId, sha256, size: String(bytes.byteLength) },
  });
  const reused = created === null;
  if (reused) {
    const existing = await bucket.get(objectKey);
    if (existing === null) {
      throw new ProbeError(
        "storage_race_inconsistent",
        "R2 rechazó la creación condicional, pero el objeto ganador no puede leerse.",
      );
    }
    const existingBytes = new Uint8Array(await existing.arrayBuffer());
    const existingSha256 = await sha256Hex(existingBytes);
    if (existingSha256 !== sha256 || existingBytes.byteLength !== bytes.byteLength) {
      throw new ProbeError(
        "request_id_conflict",
        "request_id ya está asociado a unos bytes diferentes y no se sobrescribirá.",
      );
    }
  }

  const base = publicBaseUrl.replace(/\/$/, "");
  const secret = encodeURIComponent(routeSecret);
  const id = encodeURIComponent(requestId);
  return {
    requestId,
    objectKey,
    sha256,
    size: bytes.byteLength,
    reused,
    downloadUrl: `${base}/${secret}/probe-files/${id}`,
  };
}

export async function readImmutableProbe(
  bucket: R2Bucket,
  requestId: string,
  publicBaseUrl: string,
  routeSecret: string,
): Promise<StoredProbe> {
  validateRequestId(requestId);
  const objectKey = `probe/${requestId}.zip`;
  const object = await bucket.get(objectKey);
  if (object === null) {
    throw new ProbeError("not_found", `No existe un objeto para ${requestId}.`);
  }

  const bytes = new Uint8Array(await object.arrayBuffer());
  const sha256 = await sha256Hex(bytes);
  if (
    object.customMetadata?.requestId !== requestId ||
    object.customMetadata?.sha256 !== sha256 ||
    object.customMetadata?.size !== String(bytes.byteLength)
  ) {
    throw new ProbeError(
      "stored_object_corrupt",
      "Los metadatos del objeto almacenado no coinciden con sus bytes.",
    );
  }

  const base = publicBaseUrl.replace(/\/$/, "");
  const secret = encodeURIComponent(routeSecret);
  const id = encodeURIComponent(requestId);
  return {
    requestId,
    objectKey,
    sha256,
    size: bytes.byteLength,
    reused: true,
    downloadUrl: `${base}/${secret}/probe-files/${id}`,
  };
}
