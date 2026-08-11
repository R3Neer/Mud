import { env } from "cloudflare:workers";
import { applyD1Migrations, createExecutionContext, SELF } from "cloudflare:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";
import { beforeAll, describe, expect, it } from "vitest";

import { sha256Hex } from "../src/crypto.js";
import { acceptRequest, getRequest, transition } from "../src/db.js";
import { ServiceError } from "../src/errors.js";
import { artifactDownloadRequestInit, buildWorkflowDispatchInputs } from "../src/github.js";
import { verifyRequestClaims } from "../src/oidc.js";
import { candidateKey, putImmutableCandidate, readVerifiedObject } from "../src/storage.js";
import { finalizeStagedFiles, stageCandidateFiles } from "../src/staging.js";
import type { CandidateIdentity, Env, ValidationRow } from "../src/types.js";
import { buildDeterministicZip } from "../src/zip.js";
import worker from "../src/index.js";

const bindings = env as Cloudflare.Env & {
  TEST_MIGRATIONS: Parameters<typeof applyD1Migrations>[1];
};
const testWorkerEnv: Env = {
  ...env,
  ADAPTER_TOKEN: "test-adapter-token",
  MCP_ROUTE_SECRET: "test-mcp-route-secret",
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

describe("staged UTF-8 transport", () => {
  it("computes integrity metadata when the caller has no prior byte identity", async () => {
    const content = "schema: 1\nid: generated-by-chatgpt\noperations: []\n";
    const bytes = new TextEncoder().encode(content);
    const stored = await stageCandidateFiles(bindings.VALIDATION_BUCKET, {
      request_id: "staged-computed-integrity",
      batch_id: "text",
      files: [{ path: "patch.yaml", content }],
    });
    expect(stored.files).toEqual([{
      path: "patch.yaml",
      size: bytes.byteLength,
      sha256: await sha256Hex(bytes),
    }]);
  });

  it("still rejects an optional integrity assertion that does not match", async () => {
    await expect(
      stageCandidateFiles(bindings.VALIDATION_BUCKET, {
        request_id: "staged-bad-assertion",
        batch_id: "text",
        files: [{
          path: "patch.yaml",
          content: "schema: 1\n",
          expected_size: 999,
        }],
      }),
    ).rejects.toMatchObject({ code: "file_integrity_mismatch" });
  });

  it("stores immutable complete files and finalizes exact deterministic bytes", async () => {
    const firstContent = "schema: 1\nid: staged\noperations: []\n";
    const secondContent = "# Árbol\n";
    const firstBytes = new TextEncoder().encode(firstContent);
    const secondBytes = new TextEncoder().encode(secondContent);
    const input = {
      request_id: "staged-transport",
      batch_id: "text",
      files: [
        {
          path: "patch.yaml",
          content: firstContent,
          expected_size: firstBytes.byteLength,
          expected_sha256: await sha256Hex(firstBytes),
        },
        {
          path: "docs/arbol.md",
          content: secondContent,
          expected_size: secondBytes.byteLength,
          expected_sha256: await sha256Hex(secondBytes),
        },
      ],
    };

    expect((await stageCandidateFiles(bindings.VALIDATION_BUCKET, input)).reused).toBe(false);
    expect((await stageCandidateFiles(bindings.VALIDATION_BUCKET, input)).reused).toBe(true);
    const finalized = await finalizeStagedFiles(
      bindings.VALIDATION_BUCKET,
      input.request_id,
      [input.batch_id],
      2,
    );
    expect(finalized.fileCount).toBe(2);
    expect(finalized.batchCount).toBe(1);
    expect(finalized.bytes).toEqual(
      buildDeterministicZip([
        { path: "patch.yaml", encoding: "utf8", content: firstContent },
        { path: "docs/arbol.md", encoding: "utf8", content: secondContent },
      ]),
    );

    const changedContent = `${secondContent}cambio\n`;
    const changedBytes = new TextEncoder().encode(changedContent);
    await expect(
      stageCandidateFiles(bindings.VALIDATION_BUCKET, {
        ...input,
        files: [
          input.files[0],
          {
            ...input.files[1],
            content: changedContent,
            expected_size: changedBytes.byteLength,
            expected_sha256: await sha256Hex(changedBytes),
          },
        ],
      }),
    ).rejects.toMatchObject({ code: "staged_batch_conflict" });
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

  it("persists the final staged transport identity", async () => {
    const accepted = await acceptRequest(bindings.VALIDATION_DB, {
      ...identity("db-staged-transport"),
      transportKind: "files_staged_v1",
    });
    expect(accepted.row.transport_kind).toBe("files_staged_v1");
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

  it("uses the redirect mode supported at the Workers edge", () => {
    expect(artifactDownloadRequestInit()).toEqual({ redirect: "manual" });
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
    };
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
      testWorkerEnv,
      createExecutionContext(),
    );
    expect(response.status).toBe(200);
    expect(response.headers.get("Cache-Control")).toBe("private, no-store");
    expect(await response.json()).toMatchObject({ status: "ok" });
  });

  it("serves exactly the five stable MCP tools behind the secret route", async () => {
    const client = new Client({ name: "validator-test", version: "0.1.0" });
    const transport = new StreamableHTTPClientTransport(
      new URL("https://example.com/test-mcp-route-secret/mcp"),
      { fetch: (input, init) => SELF.fetch(new Request(input, init)) },
    );
    await client.connect(transport);
    try {
      const listed = await client.listTools();
      expect(listed.tools.map((tool) => tool.name).sort()).toEqual([
        "await_validation",
        "get_validated_candidate",
        "read_validation_evidence",
        "stage_candidate_files",
        "submit_candidate",
      ]);
      const stage = listed.tools.find((tool) => tool.name === "stage_candidate_files");
      const stageInput = stage?.inputSchema as {
        properties?: { files?: { items?: { required?: string[] } } };
      };
      expect(stageInput.properties?.files?.items?.required).toEqual(["path", "content"]);
      expect(stage?.annotations).toMatchObject({
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      });
      expect(listed.tools.find((tool) => tool.name === "submit_candidate")?.annotations).toMatchObject({
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true,
      });
      expect(listed.tools.find((tool) => tool.name === "await_validation")?.annotations).toMatchObject({
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true,
      });
      for (const name of ["read_validation_evidence", "get_validated_candidate"]) {
        expect(listed.tools.find((tool) => tool.name === name)?.annotations).toMatchObject({
          readOnlyHint: true,
          destructiveHint: false,
          idempotentHint: true,
          openWorldHint: false,
        });
      }
      const content = "schema: 1\nid: mcp\noperations: []\n";
      const bytes = new TextEncoder().encode(content);
      const result = await client.callTool({
        name: "stage_candidate_files",
        arguments: {
          request_id: "mcp-stage-test",
          batch_id: "text",
          files: [{
            path: "patch.yaml",
            content,
          }],
        },
      });
      expect(result.isError).not.toBe(true);
      expect(result.structuredContent).toMatchObject({
        request_id: "mcp-stage-test",
        batch_id: "text",
        file_count: 1,
        total_size: bytes.byteLength,
        files: [{
          path: "patch.yaml",
          size: bytes.byteLength,
          sha256: await sha256Hex(bytes),
        }],
        reused: false,
      });
    } finally {
      await client.close();
    }
  });

  it("hides the MCP route when the secret segment is wrong", async () => {
    const response = await SELF.fetch("https://example.com/wrong-secret/mcp");
    expect(response.status).toBe(404);
  });
});
