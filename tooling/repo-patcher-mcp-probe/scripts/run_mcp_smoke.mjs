import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";


const endpoint =
  process.argv.slice(2).find((argument) => !argument.startsWith("--")) ??
  "http://127.0.0.1:8787/local-probe/mcp";
const runMatrix = process.argv.includes("--matrix");
const inputs = join(tmpdir(), "mud-repo-patcher-mcp-probe", "inputs");

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
  return {
    tool,
    request_id: response.request_id,
    size: response.size,
    sha256: response.sha256,
    latency_ms: Math.round(performance.now() - started),
  };
}

const client = new Client({ name: "mud-phase-0-local-smoke", version: "0.1.0" });
const transport = new StreamableHTTPClientTransport(new URL(endpoint));
await client.connect(transport);
try {
  const listed = await client.listTools();
  const names = listed.tools.map((tool) => tool.name).sort();
  const expected = ["probe_get_file", "probe_store_base64", "probe_store_files"];
  if (JSON.stringify(names) !== JSON.stringify(expected)) {
    throw new Error(`unexpected tool list: ${JSON.stringify(names)}`);
  }
  const nonce = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
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
  console.log(JSON.stringify({ endpoint, tools: names, results }, null, 2));
} finally {
  await client.close();
}
