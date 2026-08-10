import { createRemoteJWKSet, jwtVerify, type JWTPayload } from "jose";

import { ServiceError } from "./errors.js";
import type { Env, ValidationRow } from "./types.js";

const ISSUER = "https://token.actions.githubusercontent.com";
const JWKS = createRemoteJWKSet(new URL(`${ISSUER}/.well-known/jwks`));

function claim(payload: JWTPayload, name: string): string {
  const value = payload[name];
  if (typeof value !== "string" && typeof value !== "number") {
    throw new ServiceError("oidc_claim_missing", `OIDC claim is missing: ${name}`, 403);
  }
  return String(value);
}

export async function verifyBaseOidc(token: string, env: Env): Promise<JWTPayload> {
  try {
    const verified = await jwtVerify(token, JWKS, {
      issuer: ISSUER,
      audience: env.OIDC_AUDIENCE,
      algorithms: ["RS256"],
      clockTolerance: 15,
    });
    const iat = verified.payload.iat;
    const now = Math.floor(Date.now() / 1000);
    if (typeof iat !== "number" || iat > now + 15 || iat < now - 10 * 60) {
      throw new ServiceError("oidc_iat_invalid", "OIDC iat is outside the accepted window.", 403);
    }
    return verified.payload;
  } catch (error) {
    if (error instanceof ServiceError) throw error;
    throw new ServiceError("oidc_invalid", "OIDC token could not be verified.", 403);
  }
}

export function verifyRequestClaims(payload: JWTPayload, env: Env, row: ValidationRow): void {
  if (row.github_run_id === null || row.control_sha === null) {
    throw new ServiceError(
      "dispatch_not_committed_yet",
      "The workflow run is not fully associated with the durable request yet.",
      409,
      true,
    );
  }
  const expectedWorkflow =
    `${env.GITHUB_OWNER}/${env.GITHUB_REPO}/.github/workflows/${env.GITHUB_WORKFLOW}` +
    `@refs/heads/${env.GITHUB_REF}`;
  const allowedActors = new Set(env.GITHUB_ALLOWED_ACTORS.split(",").map((value) => value.trim()));
  const checks: Array<[string, string, string]> = [
    ["repository", claim(payload, "repository"), `${env.GITHUB_OWNER}/${env.GITHUB_REPO}`],
    ["repository_id", claim(payload, "repository_id"), env.GITHUB_REPOSITORY_ID],
    ["event_name", claim(payload, "event_name"), "workflow_dispatch"],
    ["runner_environment", claim(payload, "runner_environment"), "github-hosted"],
    ["run_id", claim(payload, "run_id"), String(row.github_run_id)],
    ["run_attempt", claim(payload, "run_attempt"), String(row.github_run_attempt)],
    ["workflow_ref", claim(payload, "workflow_ref"), expectedWorkflow],
    ["workflow_sha", claim(payload, "workflow_sha"), row.control_sha],
    ["ref", claim(payload, "ref"), `refs/heads/${env.GITHUB_REF}`],
  ];
  for (const [name, actual, expected] of checks) {
    if (actual !== expected) {
      throw new ServiceError("oidc_claim_mismatch", `OIDC ${name} does not match the request.`, 403);
    }
  }
  if (!allowedActors.has(claim(payload, "actor"))) {
    throw new ServiceError("oidc_actor_rejected", "OIDC actor is not authorized.", 403);
  }
}

export function bearerToken(request: Request): string {
  const authorization = request.headers.get("Authorization") ?? "";
  const match = /^Bearer ([^\s]+)$/.exec(authorization);
  if (!match) throw new ServiceError("authorization_required", "Bearer authorization is required.", 401);
  return match[1];
}
