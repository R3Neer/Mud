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

export type LongCallDurationSeconds = 15 | 30 | 60 | 120;

export interface ProbeRequestContext {
  cfRay?: string;
  colo?: string;
}

export type TimingEventKind = "started" | "heartbeat" | "completed";

export interface TimingEvent {
  schema: 1;
  protocol: "mud-repo-patcher-long-call-probe/v1";
  probe_id: string;
  event: TimingEventKind;
  sequence: number;
  recorded_at: string;
  elapsed_ms: number;
  requested_duration_seconds: LongCallDurationSeconds;
  cf_ray?: string;
  colo?: string;
}

export interface LongCallResult {
  probeId: string;
  requestedDurationSeconds: LongCallDurationSeconds;
  startedAt: string;
  completedAt: string;
  serverElapsedMs: number;
  eventCount: number;
  timingUrl: string;
}
