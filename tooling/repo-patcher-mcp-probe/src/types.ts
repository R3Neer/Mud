export type Env = Cloudflare.Env;

export type ProbeFileEncoding = "utf8" | "base64";

export interface ProbeFileInput {
  path: string;
  encoding: ProbeFileEncoding;
  content: string;
}

export interface ProbeFileWithIntegrity extends ProbeFileInput {
  expected_size: number;
  expected_sha256: string;
}

export interface StagedProbeBatch {
  schema: 1;
  protocol: "mud-repo-patcher-staged-files/v1";
  request_id: string;
  batch_id: string;
  files: ProbeFileWithIntegrity[];
}

export interface StoredProbeBatch {
  requestId: string;
  batchId: string;
  objectKey: string;
  fileCount: number;
  totalSize: number;
  sha256: string;
  reused: boolean;
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
