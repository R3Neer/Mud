export const PROTOCOL = "mud-repo-patcher-validation/v1" as const;
export const RESULT_PROTOCOL = "mud-repo-patcher-validation-result/v1" as const;

export type TransportKind = "zip_base64" | "logical_files";
export type RequestState =
  | "accepted"
  | "dispatching"
  | "queued"
  | "running"
  | "succeeded"
  | "failed"
  | "infrastructure_error"
  | "expired";

export interface Env {
  VALIDATION_DB: D1Database;
  VALIDATION_BUCKET: R2Bucket;
  ADAPTER_TOKEN: string;
  GITHUB_DISPATCH_TOKEN?: string;
  GITHUB_APP_ID?: string;
  GITHUB_APP_PRIVATE_KEY?: string;
  GITHUB_INSTALLATION_ID?: string;
  GITHUB_OWNER: string;
  GITHUB_REPO: string;
  GITHUB_WORKFLOW: string;
  GITHUB_REF: string;
  GITHUB_REPOSITORY_ID: string;
  GITHUB_ALLOWED_ACTORS: string;
  OIDC_AUDIENCE: string;
}

export interface CandidateIdentity {
  requestId: string;
  targetSha: string;
  packageSha256: string;
  packageSize: number;
  trustPlugin: boolean;
  transportKind: TransportKind;
}

export interface ValidationRow {
  request_id: string;
  schema_version: number;
  transport_kind: TransportKind;
  target_sha: string;
  package_sha256: string;
  package_size: number;
  trust_plugin: number;
  state: RequestState;
  github_run_id: number | null;
  github_run_url: string | null;
  github_run_attempt: number;
  control_sha: string | null;
  conclusion: string | null;
  runtime_version: string | null;
  result_object_key: string | null;
  evidence_object_key: string | null;
  created_at: string;
  dispatched_at: string | null;
  started_at: string | null;
  completed_at: string | null;
  expires_at: string;
}

export interface LogicalFile {
  path: string;
  encoding: "utf8" | "base64";
  content: string;
}

export interface WorkflowDispatchResponse {
  workflow_run_id: number;
  run_url: string;
  html_url: string;
}

export interface WorkflowRun {
  id: number;
  run_attempt: number;
  status: "queued" | "in_progress" | "completed" | string;
  conclusion: string | null;
  head_sha: string;
  html_url: string;
  display_title: string;
  event: string;
  created_at: string;
}

export interface ValidationResult {
  protocol: typeof RESULT_PROTOCOL;
  request_id: string;
  workflow_run_id: number;
  run_attempt: number;
  control_sha: string;
  target_sha: string;
  package_sha256: string;
  package_size: number;
  runtime_version: "0.2.0" | null;
  conclusion: "success" | "failure" | "infrastructure_error";
  failure_kind: string | null;
  diagnostic: string;
}
