import { strToU8, zipSync, type Zippable } from "fflate";

import type { ProbeFileInput, StoredProbe } from "./types.js";

export const MAX_BASE64_BYTES = 256 * 1024;
export const MAX_FILES = 500;
export const MAX_FILE_BYTES = 512 * 1024;
export const MAX_TOTAL_FILE_BYTES = 1024 * 1024;
// fflate serializes local calendar fields, so construct local midnight instead of
// parsing a UTC timestamp. The resulting DOS timestamp is identical in every zone.
export const FIXED_ZIP_MTIME = new Date(1980, 0, 1, 0, 0, 0, 0);

const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$/;
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
  if (files.length === 0 || files.length > MAX_FILES) {
    throw new ProbeError("invalid_file_count", `Se requieren entre 1 y ${MAX_FILES} archivos.`);
  }

  const normalized = files.map((file) => {
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
  for (const file of normalized) {
    const key = file.path.normalize("NFC").toLocaleLowerCase("en-US");
    if (caseFolded.has(key)) {
      throw new ProbeError("duplicate_path", `Ruta duplicada o incompatible con Windows: ${file.path}`);
    }
    caseFolded.add(key);
    totalBytes += file.bytes.byteLength;
  }
  if (totalBytes > MAX_TOTAL_FILE_BYTES) {
    throw new ProbeError(
      "payload_too_large",
      `Los archivos superan el límite total de ${MAX_TOTAL_FILE_BYTES} bytes.`,
    );
  }

  normalized.sort((left, right) => compareUtf8(left.path, right.path));
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
