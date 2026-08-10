import { ProbeError, validateRequestId } from "./probe.js";
import type {
  LongCallDurationSeconds,
  LongCallResult,
  ProbeRequestContext,
  TimingEvent,
  TimingEventKind,
} from "./types.js";

export const LONG_CALL_DURATIONS = [15, 30, 60, 120] as const;
const HEARTBEAT_INTERVAL_MS = 5_000;

export async function runLongCallProbe(
  bucket: R2Bucket,
  probeId: string,
  durationSeconds: LongCallDurationSeconds,
  publicBaseUrl: string,
  routeSecret: string,
  requestContext: ProbeRequestContext,
): Promise<LongCallResult> {
  validateRequestId(probeId);
  const startedAt = new Date().toISOString();
  const startedMonotonic = performance.now();
  let sequence = 0;

  await writeTimingEvent(
    bucket,
    makeEvent(
      probeId,
      durationSeconds,
      "started",
      sequence,
      startedAt,
      0,
      requestContext,
    ),
    true,
  );

  const requestedMs = durationSeconds * 1_000;
  while (performance.now() - startedMonotonic < requestedMs) {
    const remainingMs = requestedMs - (performance.now() - startedMonotonic);
    await delay(Math.min(HEARTBEAT_INTERVAL_MS, Math.max(0, remainingMs)));
    if (performance.now() - startedMonotonic < requestedMs) {
      sequence += 1;
      await writeTimingEvent(
        bucket,
        makeEvent(
          probeId,
          durationSeconds,
          "heartbeat",
          sequence,
          new Date().toISOString(),
          Math.round(performance.now() - startedMonotonic),
        ),
      );
    }
  }

  sequence += 1;
  const completedAt = new Date().toISOString();
  const serverElapsedMs = Math.round(performance.now() - startedMonotonic);
  await writeTimingEvent(
    bucket,
    makeEvent(
      probeId,
      durationSeconds,
      "completed",
      sequence,
      completedAt,
      serverElapsedMs,
    ),
  );

  const base = publicBaseUrl.replace(/\/$/, "");
  return {
    probeId,
    requestedDurationSeconds: durationSeconds,
    startedAt,
    completedAt,
    serverElapsedMs,
    eventCount: sequence + 1,
    timingUrl: `${base}/${encodeURIComponent(routeSecret)}/probe-timings/${encodeURIComponent(probeId)}`,
  };
}

export async function readTimingEvents(bucket: R2Bucket, probeId: string): Promise<TimingEvent[]> {
  validateRequestId(probeId);
  const listed = await bucket.list({ prefix: timingPrefix(probeId), limit: 100 });
  if (listed.objects.length === 0) {
    throw new ProbeError("not_found", `No existe telemetría para ${probeId}.`);
  }
  const events: TimingEvent[] = [];
  for (const entry of listed.objects.sort((left, right) => left.key.localeCompare(right.key))) {
    const object = await bucket.get(entry.key);
    if (object === null) {
      throw new ProbeError("timing_event_missing", `Ha desaparecido ${entry.key}.`);
    }
    events.push(JSON.parse(await object.text()) as TimingEvent);
  }
  return events;
}

export function timingEventKey(probeId: string, sequence: number, kind: TimingEventKind): string {
  validateRequestId(probeId);
  if (!Number.isSafeInteger(sequence) || sequence < 0 || sequence > 999) {
    throw new ProbeError("invalid_timing_sequence", "La secuencia de telemetría no es válida.");
  }
  return `${timingPrefix(probeId)}${String(sequence).padStart(3, "0")}-${kind}.json`;
}

function timingPrefix(probeId: string): string {
  return `timing/${probeId}/`;
}

function makeEvent(
  probeId: string,
  durationSeconds: LongCallDurationSeconds,
  event: TimingEventKind,
  sequence: number,
  recordedAt: string,
  elapsedMs: number,
  requestContext: ProbeRequestContext = {},
): TimingEvent {
  return {
    schema: 1,
    protocol: "mud-repo-patcher-long-call-probe/v1",
    probe_id: probeId,
    event,
    sequence,
    recorded_at: recordedAt,
    elapsed_ms: elapsedMs,
    requested_duration_seconds: durationSeconds,
    ...(requestContext.cfRay ? { cf_ray: requestContext.cfRay } : {}),
    ...(requestContext.colo ? { colo: requestContext.colo } : {}),
  };
}

async function writeTimingEvent(
  bucket: R2Bucket,
  event: TimingEvent,
  createOnly = false,
): Promise<void> {
  const stored = await bucket.put(
    timingEventKey(event.probe_id, event.sequence, event.event),
    JSON.stringify(event),
    {
      ...(createOnly ? { onlyIf: new Headers({ "If-None-Match": "*" }) } : {}),
      httpMetadata: { contentType: "application/json; charset=utf-8" },
      customMetadata: {
        probeId: event.probe_id,
        event: event.event,
        sequence: String(event.sequence),
      },
    },
  );
  if (createOnly && stored === null) {
    throw new ProbeError(
      "probe_id_conflict",
      "probe_id ya tiene telemetría y no se reutilizará para otra llamada.",
    );
  }
}

function delay(milliseconds: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}
