export interface Env extends Cloudflare.Env {
  // Secrets are intentionally absent from wrangler.jsonc and therefore cannot
  // be inferred by `wrangler types`.
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
