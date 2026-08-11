import { createHash, randomUUID } from "node:crypto";

import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";

const endpoint =
  process.env.MUD_VALIDATOR_MCP_URL ??
  "http://127.0.0.1:8787/local-validator/mcp";
const shouldStage = process.argv.includes("--stage");

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function redactedEndpoint(value) {
  const url = new URL(value);
  return `${url.origin}/<redacted>/mcp`;
}

async function main() {
  const client = new Client({ name: "mud-validator-mcp-smoke", version: "0.1.0" });
  const transport = new StreamableHTTPClientTransport(new URL(endpoint));
  await client.connect(transport);
  try {
    const listed = await client.listTools();
    const names = listed.tools.map((tool) => tool.name).sort();
    const expected = [
      "await_validation",
      "get_validated_candidate",
      "read_validation_evidence",
      "stage_candidate_files",
      "submit_candidate",
    ];
    if (JSON.stringify(names) !== JSON.stringify(expected)) {
      throw new Error(`Unexpected MCP tool list: ${JSON.stringify(names)}`);
    }

    let staged;
    if (shouldStage) {
      const content = "schema: 1\nid: mcp-smoke\noperations: []\n";
      const bytes = Buffer.from(content, "utf8");
      const requestId = `mcp-smoke-${randomUUID()}`;
      const result = await client.callTool({
        name: "stage_candidate_files",
        arguments: {
          request_id: requestId,
          batch_id: "text",
          files: [{
            path: "patch.yaml",
            content,
            expected_size: bytes.length,
            expected_sha256: sha256(bytes),
          }],
        },
      });
      if (result.isError || !result.structuredContent) {
        throw new Error(`stage_candidate_files failed: ${JSON.stringify(result)}`);
      }
      staged = result.structuredContent;
    }

    console.log(JSON.stringify({ endpoint: redactedEndpoint(endpoint), tools: names, staged }, null, 2));
  } finally {
    await client.close();
  }
}

await main();
