export interface Env {
  PROBE_BUCKET: R2Bucket;
  PROBE_ROUTE_SECRET: string;
}

export type ProbeFileEncoding = "utf8" | "base64";

export interface ProbeFileInput {
  path: string;
  encoding: ProbeFileEncoding;
  content: string;
}

export interface StoredProbe {
  requestId: string;
  objectKey: string;
  sha256: string;
  size: number;
  reused: boolean;
  downloadUrl: string;
}
