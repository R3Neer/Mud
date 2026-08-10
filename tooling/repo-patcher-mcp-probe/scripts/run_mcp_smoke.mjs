import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";


const cliArguments = process.argv.slice(2);
const endpoint =
  cliArguments.find((argument) => /^https?:\/\//.test(argument)) ??
  "http://127.0.0.1:8787/local-probe/mcp";
const runMatrix = cliArguments.includes("--matrix");
const longCallIndex = cliArguments.indexOf("--long-call");
const longCallDuration =
  longCallIndex === -1 ? undefined : Number.parseInt(cliArguments[longCallIndex + 1] ?? "", 10);
const probeIdIndex = cliArguments.indexOf("--probe-id");
const requestedProbeId = probeIdIndex === -1 ? undefined : cliArguments[probeIdIndex + 1];
const inputs = join(tmpdir(), "mud-repo-patcher-mcp-probe", "inputs");

function displayEndpoint(value) {
  const parsed = new URL(value);
  return `${parsed.origin}/<redacted>/mcp`;
}

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

async function payload(name, requestId) {
  const parsed = JSON.parse(await readFile(join(inputs, name), "utf8"));
  parsed.request_id = requestId;
  return parsed;
}

async function callAndVerify(client, tool, args) {
  const started = performance.now();
  const result = await client.callTool({ name: tool, arguments: args });
  if (result.isError || !result.structuredContent) {
    throw new Error(`${tool} failed: ${JSON.stringify(result)}`);
  }
  const response = result.structuredContent;
  const downloaded = new Uint8Array(await (await fetch(response.download_url)).arrayBuffer());
  const downloadedSha = sha256(downloaded);
  if (downloaded.length !== response.size || downloadedSha !== response.sha256) {
    throw new Error(`${tool} download mismatch`);
  }
  if (args.expected_sha256 && args.expected_sha256 !== response.sha256) {
    throw new Error(`${tool} source hash mismatch`);
  }
  const retrieved = await client.callTool({
    name: "probe_get_file",
    arguments: { request_id: response.request_id },
  });
  if (
    retrieved.isError ||
    !retrieved.structuredContent ||
    retrieved.structuredContent.sha256 !== response.sha256 ||
    retrieved.structuredContent.size !== response.size
  ) {
    throw new Error(`probe_get_file mismatch after ${tool}`);
  }
  return {
    tool,
    request_id: response.request_id,
    size: response.size,
    sha256: response.sha256,
    latency_ms: Math.round(performance.now() - started),
  };
}

async function main() {
  const client = new Client({ name: "mud-phase-0-local-smoke", version: "0.1.0" });
  const transport = new StreamableHTTPClientTransport(new URL(endpoint));
  await client.connect(transport);
  try {
  const listed = await client.listTools();
  const names = listed.tools.map((tool) => tool.name).sort();
  const expected = [
    "probe_get_file",
    "probe_store_base64",
    "probe_store_files",
    "probe_wait_and_record",
  ];
  if (JSON.stringify(names) !== JSON.stringify(expected)) {
    throw new Error(`unexpected tool list: ${JSON.stringify(names)}`);
  }
  const toolsByName = new Map(listed.tools.map((tool) => [tool.name, tool]));
  for (const name of ["probe_store_base64", "probe_store_files"]) {
    const annotations = toolsByName.get(name)?.annotations;
    if (
      annotations?.readOnlyHint !== false ||
      annotations?.destructiveHint !== false ||
      annotations?.idempotentHint !== true ||
      annotations?.openWorldHint !== false
    ) {
      throw new Error(`unsafe or inaccurate annotations for ${name}`);
    }
  }
  const getAnnotations = toolsByName.get("probe_get_file")?.annotations;
  if (
    getAnnotations?.readOnlyHint !== true ||
    getAnnotations?.destructiveHint !== false ||
    getAnnotations?.idempotentHint !== true ||
    getAnnotations?.openWorldHint !== false
  ) {
    throw new Error("unsafe or inaccurate annotations for probe_get_file");
  }
  const longCallAnnotations = toolsByName.get("probe_wait_and_record")?.annotations;
  if (
    longCallAnnotations?.readOnlyHint !== false ||
    longCallAnnotations?.destructiveHint !== false ||
    longCallAnnotations?.idempotentHint !== false ||
    longCallAnnotations?.openWorldHint !== false
  ) {
    throw new Error("unsafe or inaccurate annotations for probe_wait_and_record");
  }
  const nonce = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  if (longCallDuration !== undefined) {
    if (![15, 30, 60, 120].includes(longCallDuration)) {
      throw new Error("--long-call must be 15, 30, 60, or 120");
    }
    const probeId = requestedProbeId ?? `reference-long-${longCallDuration}-${nonce}`;
    const started = performance.now();
    const result = await client.callTool({
      name: "probe_wait_and_record",
      arguments: { probe_id: probeId, duration_seconds: longCallDuration },
    });
    if (result.isError || !result.structuredContent) {
      throw new Error(`probe_wait_and_record failed: ${JSON.stringify(result)}`);
    }
    const response = result.structuredContent;
    const timingResponse = await fetch(response.timing_url);
    if (!timingResponse.ok) {
      throw new Error(`timing download failed: ${timingResponse.status}`);
    }
    const timing = await timingResponse.json();
    if (
      timing.probe_id !== probeId ||
      timing.complete !== true ||
      timing.events.at(-1)?.event !== "completed"
    ) {
      throw new Error(`incomplete timing evidence: ${JSON.stringify(timing)}`);
    }
    console.log(
      JSON.stringify(
        {
          endpoint: displayEndpoint(endpoint),
          tools: names,
          client_elapsed_ms: Math.round(performance.now() - started),
          result: response,
          timing,
        },
        null,
        2,
      ),
    );
    return;
  }
  const cases = runMatrix
    ? [
        ...["001", "016", "064", "128", "256"].map((size) => ({
          tool: "probe_store_base64",
          file: `zip-${size}k-request.json`,
          label: `base64-${size}k`,
        })),
        { tool: "probe_store_files", file: "files-minimal-request.json", label: "files-minimal" },
        {
          tool: "probe_store_files",
          file: "files-representative-request.json",
          label: "files-representative",
        },
        {
          tool: "probe_store_files",
          file: "files-unicode-binary-request.json",
          label: "files-unicode-binary",
        },
      ]
    : [
        { tool: "probe_store_base64", file: "zip-001k-request.json", label: "base64-001k" },
        { tool: "probe_store_files", file: "files-minimal-request.json", label: "files-minimal" },
      ];
  const results = [];
  for (const item of cases) {
    for (let attempt = 1; attempt <= (runMatrix ? 3 : 1); attempt += 1) {
      results.push(
        await callAndVerify(
          client,
          item.tool,
          await payload(item.file, `local-${item.label}-${attempt}-${nonce}`),
        ),
      );
    }
  }
  console.log(JSON.stringify({ endpoint: displayEndpoint(endpoint), tools: names, results }, null, 2));
  } finally {
    await client.close();
  }
}

await main();
