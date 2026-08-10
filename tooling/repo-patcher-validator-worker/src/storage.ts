import { sha256Hex } from "./crypto.js";
import { ServiceError } from "./errors.js";
import type { CandidateIdentity } from "./types.js";

export function candidateKey(sha256: string): string {
  return `candidates/${sha256}.zip`;
}

export async function putImmutableCandidate(
  bucket: R2Bucket,
  identity: CandidateIdentity,
  bytes: Uint8Array,
): Promise<{ key: string; reused: boolean }> {
  const key = candidateKey(identity.packageSha256);
  const created = await bucket.put(key, bytes, {
    onlyIf: new Headers({ "If-None-Match": "*" }),
    httpMetadata: { contentType: "application/zip" },
    customMetadata: {
      sha256: identity.packageSha256,
      size: String(identity.packageSize),
    },
    sha256: identity.packageSha256,
  });
  if (created !== null) return { key, reused: false };
  const existing = await readVerifiedObject(
    bucket,
    key,
    identity.packageSha256,
    identity.packageSize,
  );
  if (existing.bytes.byteLength !== bytes.byteLength) {
    throw new ServiceError("storage_inconsistency", "Existing content-addressed object differs.", 500);
  }
  return { key, reused: true };
}

export async function readVerifiedObject(
  bucket: R2Bucket,
  key: string,
  expectedSha256: string,
  expectedSize: number,
): Promise<{ object: R2ObjectBody; bytes: Uint8Array }> {
  const object = await bucket.get(key);
  if (object === null) {
    throw new ServiceError("stored_object_missing", `R2 object is missing: ${key}`, 500);
  }
  const bytes = new Uint8Array(await object.arrayBuffer());
  const actualSha256 = await sha256Hex(bytes);
  if (
    bytes.byteLength !== expectedSize ||
    actualSha256 !== expectedSha256 ||
    object.customMetadata?.sha256 !== expectedSha256 ||
    object.customMetadata?.size !== String(expectedSize)
  ) {
    throw new ServiceError("stored_object_corrupt", `R2 object failed identity checks: ${key}`, 500);
  }
  return { object, bytes };
}

export async function putImmutableEvidence(
  bucket: R2Bucket,
  key: string,
  bytes: Uint8Array,
  metadata: Record<string, string>,
  contentType: string,
): Promise<void> {
  const sha256 = await sha256Hex(bytes);
  const created = await bucket.put(key, bytes, {
    onlyIf: new Headers({ "If-None-Match": "*" }),
    httpMetadata: { contentType },
    customMetadata: { ...metadata, sha256, size: String(bytes.byteLength) },
    sha256,
  });
  if (created !== null) return;
  await readVerifiedObject(bucket, key, sha256, bytes.byteLength);
}
