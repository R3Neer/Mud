import { strToU8, zipSync, type Zippable } from "fflate";

import { decodeCanonicalBase64 } from "./crypto.js";
import { ServiceError } from "./errors.js";
import type { LogicalFile } from "./types.js";

export const MAX_PACKAGE_BYTES = 10 * 1024 * 1024;
export const MAX_FILES = 500;
export const MAX_FILE_BYTES = 512 * 1024;
export const MAX_TOTAL_FILE_BYTES = 1024 * 1024;
export const FIXED_ZIP_MTIME = new Date(1980, 0, 1, 0, 0, 0, 0);

const WINDOWS_FORBIDDEN = /[\u0000-\u001f<>:"|?*]/;
const WINDOWS_RESERVED = /^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?$/i;

export function normalizePath(raw: string): string {
  if (!raw || raw.includes("\\") || raw.startsWith("/") || /^[A-Za-z]:/.test(raw)) {
    throw new ServiceError("invalid_path", `Invalid path: ${raw || "(empty)"}`);
  }
  const segments = raw.split("/");
  if (segments.some((part) => !part || part === "." || part === "..")) {
    throw new ServiceError("invalid_path", `Invalid path: ${raw}`);
  }
  if (
    segments.some(
      (part) =>
        WINDOWS_FORBIDDEN.test(part) ||
        part.endsWith(".") ||
        part.endsWith(" ") ||
        WINDOWS_RESERVED.test(part),
    )
  ) {
    throw new ServiceError("invalid_path", `Path is incompatible with Windows: ${raw}`);
  }
  if (raw.length > 240) {
    throw new ServiceError("invalid_path", `Path exceeds 240 characters: ${raw}`);
  }
  return segments.join("/");
}

export function buildDeterministicZip(files: LogicalFile[]): Uint8Array {
  if (files.length < 1 || files.length > MAX_FILES) {
    throw new ServiceError("invalid_file_count", `Expected between 1 and ${MAX_FILES} files.`);
  }
  const normalized = files.map((file) => {
    const path = normalizePath(file.path);
    const bytes =
      file.encoding === "utf8"
        ? strToU8(file.content)
        : decodeCanonicalBase64(file.content, MAX_FILE_BYTES);
    if (bytes.byteLength > MAX_FILE_BYTES) {
      throw new ServiceError("file_too_large", `${path} exceeds ${MAX_FILE_BYTES} bytes.`, 413);
    }
    return { path, bytes };
  });
  const caseFolded = new Set<string>();
  let total = 0;
  for (const file of normalized) {
    const key = file.path.normalize("NFC").toLocaleLowerCase("en-US");
    if (caseFolded.has(key)) {
      throw new ServiceError("duplicate_path", `Duplicate or Windows-colliding path: ${file.path}`);
    }
    caseFolded.add(key);
    total += file.bytes.byteLength;
  }
  if (total > MAX_TOTAL_FILE_BYTES) {
    throw new ServiceError("payload_too_large", "Logical files exceed the total size limit.", 413);
  }
  normalized.sort((left, right) => compareUtf8(left.path, right.path));
  const entries: Zippable = {};
  for (const file of normalized) {
    entries[file.path] = [file.bytes, { level: 6, mtime: FIXED_ZIP_MTIME }];
  }
  return zipSync(entries, { level: 6, mtime: FIXED_ZIP_MTIME });
}

function compareUtf8(left: string, right: string): number {
  const a = strToU8(left);
  const b = strToU8(right);
  for (let index = 0; index < Math.min(a.length, b.length); index += 1) {
    if (a[index] !== b[index]) return a[index] - b[index];
  }
  return a.length - b.length;
}
