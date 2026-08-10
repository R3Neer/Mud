import { env } from "cloudflare:workers";
import { applyD1Migrations } from "cloudflare:test";
import { beforeAll, describe, expect, it } from "vitest";

import { sha256Hex } from "../src/crypto.js";
import { acceptRequest, getRequest, transition } from "../src/db.js";
import { ServiceError } from "../src/errors.js";
import { buildWorkflowDispatchInputs } from "../src/github.js";
import { verifyRequestClaims } from "../src/oidc.js";
import { candidateKey, putImmutableCandidate, readVerifiedObject } from "../src/storage.js";
import type { CandidateIdentity, Env, ValidationRow } from "../src/types.js";
import { buildDeterministicZip } from "../src/zip.js";
import worker from "../src/index.js";

const bindings = env as unknown as {
  VALIDATION_DB: D1Database;
  VALIDATION_BUCKET: R2Bucket;
  TEST_MIGRATIONS: Parameters<typeof applyD1Migrations>[1];
};

beforeAll(async () => {
  await applyD1Migrations(bindings.VALIDATION_DB, bindings.TEST_MIGRATIONS);
});

function identity(requestId = "candidate-001"): CandidateIdentity {
  return {
    requestId,
    targetSha: "1".repeat(40),
    packageSha256: "2".repeat(64),
    packageSize: 123,
    trustPlugin: false,
    transportKind: "logical_files",
  };
}

describe("deterministic ZIP", () => {
  it("matches the Phase 0 golden bytes independently of input order", async () => {
    const files = [
      { path: "zeta.md", encoding: "utf8" as const, content: "último\n" },
      {
        path: "patch.yaml",
        encoding: "utf8" as const,
        content: "schema: 1\nid: prueba\ntitle: Prueba\noperations: []\n",
      },
      { path: "files/data.bin", encoding: "base64" as const, content: "AAEC/v8=" },
    ];
    const first = buildDeterministicZip(files);
    const second = buildDeterministicZip([...files].reverse());
    expect(second).toEqual(first);
    expect(await sha256Hex(first)).toBe(
      "40134ed750ba056b22124ea6dc50059f352688fd35abae3b8f59579f0e19df58",
    );
  });
});

describe("D1 state machine", () => {
  it("accepts idempotently and rejects a changed identity", async () => {
    const first = await acceptRequest(bindings.VALIDATION_DB, identity("db-idempotent"));
    const second = await acceptRequest(bindings.VALIDATION_DB, identity("db-idempotent"));
    expect(first.created).toBe(true);
    expect(second.created).toBe(false);
    await expect(
      acceptRequest(bindings.VALIDATION_DB, {
        ...identity("db-idempotent"),
        targetSha: "3".repeat(40),
      }),
    ).rejects.toMatchObject({ code: "request_id_conflict" });
  });

  it("allows only the expected monotonic transition", async () => {
    await acceptRequest(bindings.VALIDATION_DB, identity("db-transition"));
    expect(await transition(bindings.VALIDATION_DB, "db-transition", "accepted", "dispatching")).toBe(true);
    expect(await transition(bindings.VALIDATION_DB, "db-transition", "accepted", "dispatching")).toBe(false);
    const row = await getRequest(bindings.VALIDATION_DB, "db-transition");
    expect(row?.state).toBe("dispatching");
    await expect(
      transition(bindings.VALIDATION_DB, "db-transition", "accepted", "running"),
    ).rejects.toMatchObject({ code: "state_transition_conflict" });
  });
});

describe("GitHub workflow dispatch", () => {
  it("serializes number inputs in the form accepted by the REST API", () => {
    const row = {
      request_id: "dispatch-inputs",
      target_sha: "1".repeat(40),
      package_sha256: "2".repeat(64),
      package_size: 321,
      trust_plugin: 0,
      transport_kind: "logical_files",
    } as ValidationRow;

    expect(buildWorkflowDispatchInputs(row)).toMatchObject({
      package_size: "321",
      trust_plugin: false,
    });
  });
});

describe("R2 immutability", () => {
  it("creates once, reuses exact bytes and detects corruption", async () => {
    const bytes = new TextEncoder().encode("candidate bytes");
    const sha = await sha256Hex(bytes);
    const value: CandidateIdentity = {
      ...identity("r2-idempotent"),
      packageSha256: sha,
      packageSize: bytes.byteLength,
    };
    expect((await putImmutableCandidate(bindings.VALIDATION_BUCKET, value, bytes)).reused).toBe(false);
    expect((await putImmutableCandidate(bindings.VALIDATION_BUCKET, value, bytes)).reused).toBe(true);
    const stored = await readVerifiedObject(
      bindings.VALIDATION_BUCKET,
      candidateKey(sha),
      sha,
      bytes.byteLength,
    );
    expect(stored.bytes).toEqual(bytes);
    await bindings.VALIDATION_BUCKET.put(candidateKey(sha), "corrupt", {
      customMetadata: { sha256: sha, size: String(bytes.byteLength) },
    });
    await expect(
      readVerifiedObject(bindings.VALIDATION_BUCKET, candidateKey(sha), sha, bytes.byteLength),
    ).rejects.toMatchObject({ code: "stored_object_corrupt" });
  });
});

describe("OIDC request binding", () => {
  it("accepts the exact run and rejects another run", () => {
    const row = {
      github_run_id: 123,
      github_run_attempt: 1,
      control_sha: "a".repeat(40),
    } as ValidationRow;
    const workerEnv = {
      GITHUB_OWNER: "R3Neer",
      GITHUB_REPO: "Mud",
      GITHUB_WORKFLOW: "validate-repo-patcher-remote.yml",
      GITHUB_REF: "main",
      GITHUB_REPOSITORY_ID: "456",
      GITHUB_ALLOWED_ACTORS: "R3Neer,efferra",
    } as Env;
    const payload = {
      repository: "R3Neer/Mud",
      repository_id: "456",
      event_name: "workflow_dispatch",
      runner_environment: "github-hosted",
      run_id: "123",
      run_attempt: "1",
      workflow_ref:
        "R3Neer/Mud/.github/workflows/validate-repo-patcher-remote.yml@refs/heads/main",
      workflow_sha: "a".repeat(40),
      ref: "refs/heads/main",
      actor: "R3Neer",
    };
    expect(() => verifyRequestClaims(payload, workerEnv, row)).not.toThrow();
    expect(() => verifyRequestClaims({ ...payload, run_id: "999" }, workerEnv, row)).toThrow(
      ServiceError,
    );
  });
});

describe("Worker surface", () => {
  it("exposes only a no-store health response without credentials", async () => {
    const response = await worker.fetch(
      new Request("https://example.com/health"),
      env as unknown as Env,
    );
    expect(response.status).toBe(200);
    expect(response.headers.get("Cache-Control")).toBe("private, no-store");
    expect(await response.json()).toMatchObject({ status: "ok" });
  });
});
