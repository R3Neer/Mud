import { importPKCS8, SignJWT } from "jose";

import { ServiceError } from "./errors.js";
import type {
  Env,
  ValidationRow,
  WorkflowDispatchResponse,
  WorkflowRun,
} from "./types.js";

const API_VERSION = "2026-03-10";

async function appJwt(env: Env): Promise<string> {
  if (!env.GITHUB_APP_ID || !env.GITHUB_APP_PRIVATE_KEY) {
    throw new ServiceError("github_auth_not_configured", "GitHub App credentials are incomplete.", 503);
  }
  const now = Math.floor(Date.now() / 1000);
  const pem = env.GITHUB_APP_PRIVATE_KEY.replace(/\\n/g, "\n");
  const key = await importPKCS8(pem, "RS256");
  return new SignJWT({})
    .setProtectedHeader({ alg: "RS256" })
    .setIssuer(env.GITHUB_APP_ID)
    .setIssuedAt(now - 30)
    .setExpirationTime(now + 9 * 60)
    .sign(key);
}

async function installationToken(env: Env): Promise<string> {
  if (env.GITHUB_DISPATCH_TOKEN) return env.GITHUB_DISPATCH_TOKEN;
  if (!env.GITHUB_INSTALLATION_ID) {
    throw new ServiceError(
      "github_auth_not_configured",
      "Set GITHUB_DISPATCH_TOKEN or all GitHub App credentials.",
      503,
    );
  }
  const response = await fetch(
    `https://api.github.com/app/installations/${encodeURIComponent(env.GITHUB_INSTALLATION_ID)}/access_tokens`,
    {
      method: "POST",
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${await appJwt(env)}`,
        "User-Agent": "mud-repo-patcher-validator",
        "X-GitHub-Api-Version": API_VERSION,
      },
    },
  );
  if (!response.ok) {
    throw new ServiceError(
      "github_auth_failed",
      `GitHub App installation token failed: ${response.status} ${await response.text()}`,
      502,
      true,
    );
  }
  const body = (await response.json()) as { token?: string };
  if (!body.token) throw new ServiceError("github_auth_failed", "GitHub returned no installation token.", 502);
  return body.token;
}

async function githubFetch(env: Env, path: string, init: RequestInit = {}): Promise<Response> {
  const token = await installationToken(env);
  return fetch(`https://api.github.com${path}`, {
    ...init,
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      "User-Agent": "mud-repo-patcher-validator",
      "X-GitHub-Api-Version": API_VERSION,
      ...init.headers,
    },
  });
}

function repositoryPath(env: Env): string {
  return `/repos/${encodeURIComponent(env.GITHUB_OWNER)}/${encodeURIComponent(env.GITHUB_REPO)}`;
}

export async function dispatchWorkflow(
  env: Env,
  row: ValidationRow,
): Promise<WorkflowDispatchResponse> {
  const response = await githubFetch(
    env,
    `${repositoryPath(env)}/actions/workflows/${encodeURIComponent(env.GITHUB_WORKFLOW)}/dispatches`,
    {
      method: "POST",
      body: JSON.stringify({
        ref: env.GITHUB_REF,
        inputs: {
          protocol: "mud-repo-patcher-validation/v1",
          request_id: row.request_id,
          target_sha: row.target_sha,
          package_sha256: row.package_sha256,
          package_size: row.package_size,
          trust_plugin: Boolean(row.trust_plugin),
          transport_kind: row.transport_kind,
        },
      }),
    },
  );
  if (response.status !== 200) {
    throw new ServiceError(
      "github_dispatch_failed",
      `workflow_dispatch failed: ${response.status} ${await response.text()}`,
      502,
      true,
    );
  }
  const body = (await response.json()) as Partial<WorkflowDispatchResponse>;
  if (
    !Number.isInteger(body.workflow_run_id) ||
    typeof body.run_url !== "string" ||
    typeof body.html_url !== "string"
  ) {
    throw new ServiceError("github_dispatch_invalid_response", "Dispatch response omitted run identity.", 502);
  }
  return body as WorkflowDispatchResponse;
}

export async function getWorkflowRun(env: Env, runId: number): Promise<WorkflowRun> {
  const response = await githubFetch(env, `${repositoryPath(env)}/actions/runs/${runId}`);
  if (!response.ok) {
    throw new ServiceError(
      "github_run_unavailable",
      `Workflow run lookup failed: ${response.status} ${await response.text()}`,
      502,
      true,
    );
  }
  return (await response.json()) as WorkflowRun;
}

export async function findAmbiguousDispatch(
  env: Env,
  row: ValidationRow,
): Promise<WorkflowRun | null> {
  const workflow = encodeURIComponent(env.GITHUB_WORKFLOW);
  const query = new URLSearchParams({
    actor: "",
    branch: env.GITHUB_REF,
    event: "workflow_dispatch",
    per_page: "100",
  });
  query.delete("actor");
  const response = await githubFetch(
    env,
    `${repositoryPath(env)}/actions/workflows/${workflow}/runs?${query.toString()}`,
  );
  if (!response.ok) {
    throw new ServiceError("github_reconciliation_failed", "Could not list workflow runs.", 502, true);
  }
  const body = (await response.json()) as { workflow_runs?: WorkflowRun[] };
  const earliest = new Date(row.created_at).getTime() - 60_000;
  const title = `RepoPatcher remote validation ${row.request_id}`;
  const matches = (body.workflow_runs ?? []).filter(
    (run) =>
      run.event === "workflow_dispatch" &&
      run.display_title === title &&
      new Date(run.created_at).getTime() >= earliest,
  );
  if (matches.length > 1) {
    throw new ServiceError("ambiguous_dispatch", "More than one workflow run matches request_id.", 409);
  }
  return matches[0] ?? null;
}

interface ArtifactListItem {
  id: number;
  name: string;
  expired: boolean;
}

export async function downloadEvidenceArtifact(env: Env, row: ValidationRow): Promise<Uint8Array> {
  if (row.github_run_id === null) throw new ServiceError("run_not_associated", "Run is not associated.", 409);
  const list = await githubFetch(
    env,
    `${repositoryPath(env)}/actions/runs/${row.github_run_id}/artifacts?per_page=100`,
  );
  if (!list.ok) {
    throw new ServiceError("artifact_list_failed", `Could not list artifacts: ${list.status}`, 502, true);
  }
  const body = (await list.json()) as { artifacts?: ArtifactListItem[] };
  const expected = `repo-patcher-validation-${row.request_id}-${row.github_run_attempt}`;
  const matches = (body.artifacts ?? []).filter((item) => item.name === expected && !item.expired);
  if (matches.length !== 1) {
    throw new ServiceError(
      "artifact_not_unique",
      `Expected one non-expired artifact named ${expected}, found ${matches.length}.`,
      502,
      true,
    );
  }
  const redirect = await githubFetch(
    env,
    `${repositoryPath(env)}/actions/artifacts/${matches[0].id}/zip`,
    { redirect: "manual" },
  );
  const location = redirect.headers.get("Location");
  const response =
    redirect.status >= 300 && redirect.status < 400 && location
      ? await fetch(location, { redirect: "error" })
      : redirect;
  if (!response.ok) {
    throw new ServiceError("artifact_download_failed", `Could not download artifact: ${response.status}`, 502, true);
  }
  const maximum = 64 * 1024 * 1024;
  const declared = Number(response.headers.get("Content-Length") ?? "0");
  if (declared > maximum) {
    throw new ServiceError("artifact_too_large", `Artifact exceeds ${maximum} bytes.`, 502);
  }
  const bytes = new Uint8Array(await response.arrayBuffer());
  if (bytes.byteLength > maximum) {
    throw new ServiceError("artifact_too_large", `Artifact exceeds ${maximum} bytes.`, 502);
  }
  return bytes;
}
