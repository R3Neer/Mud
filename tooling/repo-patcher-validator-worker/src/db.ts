import { ServiceError } from "./errors.js";
import type { CandidateIdentity, RequestState, ValidationRow } from "./types.js";

const TERMINAL: ReadonlySet<RequestState> = new Set([
  "succeeded",
  "failed",
  "infrastructure_error",
  "expired",
]);

function now(): string {
  return new Date().toISOString();
}

function expiresAt(): string {
  return new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString();
}

export function identityMatches(row: ValidationRow, identity: CandidateIdentity): boolean {
  return (
    row.target_sha === identity.targetSha &&
    row.package_sha256 === identity.packageSha256 &&
    row.package_size === identity.packageSize &&
    Boolean(row.trust_plugin) === identity.trustPlugin &&
    row.transport_kind === identity.transportKind
  );
}

export async function getRequest(db: D1Database, requestId: string): Promise<ValidationRow | null> {
  return db
    .prepare("SELECT * FROM validation_requests WHERE request_id = ?")
    .bind(requestId)
    .first<ValidationRow>();
}

export async function acceptRequest(
  db: D1Database,
  identity: CandidateIdentity,
): Promise<{ row: ValidationRow; created: boolean }> {
  const createdAt = now();
  const insert = await db
    .prepare(
      `INSERT INTO validation_requests (
        request_id, schema_version, transport_kind, target_sha, package_sha256,
        package_size, trust_plugin, state, github_run_attempt, created_at, expires_at
      ) VALUES (?, 1, ?, ?, ?, ?, ?, 'accepted', 1, ?, ?)
      ON CONFLICT(request_id) DO NOTHING`,
    )
    .bind(
      identity.requestId,
      identity.transportKind,
      identity.targetSha,
      identity.packageSha256,
      identity.packageSize,
      identity.trustPlugin ? 1 : 0,
      createdAt,
      expiresAt(),
    )
    .run();
  const row = await getRequest(db, identity.requestId);
  if (row === null) throw new ServiceError("database_inconsistency", "Accepted request is missing.", 500);
  if (!identityMatches(row, identity)) {
    throw new ServiceError("request_id_conflict", "request_id already has a different identity.", 409);
  }
  if (insert.meta.changes > 0) {
    await addEvent(db, identity.requestId, "accepted", { package_sha256: identity.packageSha256 });
  }
  return { row, created: insert.meta.changes > 0 };
}

export async function transition(
  db: D1Database,
  requestId: string,
  from: RequestState,
  to: RequestState,
  columns: Record<string, string | number | null> = {},
): Promise<boolean> {
  const allowedColumns = new Set([
    "github_run_id", "github_run_url", "github_run_attempt", "control_sha", "conclusion",
    "runtime_version", "result_object_key", "evidence_object_key", "dispatched_at",
    "started_at", "completed_at",
  ]);
  for (const key of Object.keys(columns)) {
    if (!allowedColumns.has(key)) throw new ServiceError("invalid_transition", `Invalid column: ${key}`, 500);
  }
  const assignments = ["state = ?", ...Object.keys(columns).map((key) => `${key} = ?`)];
  const values = [to, ...Object.values(columns), requestId, from];
  const result = await db
    .prepare(`UPDATE validation_requests SET ${assignments.join(", ")} WHERE request_id = ? AND state = ?`)
    .bind(...values)
    .run();
  if (result.meta.changes > 0) {
    await addEvent(db, requestId, to, columns);
    return true;
  }
  const current = await getRequest(db, requestId);
  if (current?.state === to) return false;
  if (current && TERMINAL.has(current.state)) return false;
  throw new ServiceError(
    "state_transition_conflict",
    `Cannot transition ${requestId} from ${from} to ${to}; current=${current?.state ?? "missing"}.`,
    409,
  );
}

export async function patchDispatch(
  db: D1Database,
  requestId: string,
  runId: number,
  runUrl: string,
): Promise<void> {
  const result = await db
    .prepare(
      `UPDATE validation_requests
       SET github_run_id = COALESCE(github_run_id, ?),
           github_run_url = COALESCE(github_run_url, ?),
           dispatched_at = COALESCE(dispatched_at, ?)
       WHERE request_id = ? AND state = 'dispatching'
         AND (github_run_id IS NULL OR github_run_id = ?)`,
    )
    .bind(runId, runUrl, now(), requestId, runId)
    .run();
  if (result.meta.changes === 0) {
    const row = await getRequest(db, requestId);
    if (row?.github_run_id !== runId) {
      throw new ServiceError("run_association_conflict", "Request is associated with another run.", 409);
    }
  }
  await addEvent(db, requestId, "run_associated", { run_id: runId });
}

export async function markQueued(
  db: D1Database,
  requestId: string,
  controlSha: string,
  runAttempt: number,
): Promise<void> {
  const changed = await transition(db, requestId, "dispatching", "queued", {
    control_sha: controlSha,
    github_run_attempt: runAttempt,
    dispatched_at: now(),
  });
  if (!changed) {
    const row = await getRequest(db, requestId);
    if (row?.control_sha !== controlSha || row.github_run_attempt !== runAttempt) {
      throw new ServiceError("run_association_conflict", "Queued run identity differs.", 409);
    }
  }
}

export async function markRunning(db: D1Database, row: ValidationRow): Promise<void> {
  if (row.state === "queued") {
    await transition(db, row.request_id, "queued", "running", { started_at: now() });
  }
}

export async function expireIfDue(db: D1Database, row: ValidationRow): Promise<ValidationRow> {
  if (TERMINAL.has(row.state) || new Date(row.expires_at).getTime() > Date.now()) return row;
  const result = await db
    .prepare(
      `UPDATE validation_requests SET state = 'expired', completed_at = ?
       WHERE request_id = ? AND state IN ('accepted', 'dispatching', 'queued', 'running')
         AND expires_at <= ?`,
    )
    .bind(now(), row.request_id, now())
    .run();
  if (result.meta.changes > 0) await addEvent(db, row.request_id, "expired", {});
  return (await getRequest(db, row.request_id))!;
}

export async function markTerminal(
  db: D1Database,
  row: ValidationRow,
  state: "succeeded" | "failed" | "infrastructure_error",
  values: {
    conclusion: string;
    runtimeVersion: string | null;
    resultObjectKey: string | null;
    evidenceObjectKey: string | null;
  },
): Promise<void> {
  if (TERMINAL.has(row.state)) return;
  const from = row.state === "queued" ? "queued" : "running";
  await transition(db, row.request_id, from, state, {
    conclusion: values.conclusion,
    runtime_version: values.runtimeVersion,
    result_object_key: values.resultObjectKey,
    evidence_object_key: values.evidenceObjectKey,
    completed_at: now(),
  });
}

export async function addEvent(
  db: D1Database,
  requestId: string,
  event: string,
  detail: unknown,
): Promise<void> {
  await db
    .prepare(
      "INSERT INTO validation_events (request_id, event, detail_json, created_at) VALUES (?, ?, ?, ?)",
    )
    .bind(requestId, event, JSON.stringify(detail), now())
    .run();
}
