import { cloudflareTest, readD1Migrations } from "@cloudflare/vitest-pool-workers";
import { defineConfig } from "vitest/config";

export default defineConfig(async () => {
  const migrations = await readD1Migrations("./migrations");
  return {
    plugins: [
      cloudflareTest({
        wrangler: { configPath: "./wrangler.jsonc" },
        miniflare: {
          bindings: {
            ADAPTER_TOKEN: "test-adapter-token",
            MCP_ROUTE_SECRET: "test-mcp-route-secret",
            TEST_MIGRATIONS: migrations,
          },
        },
      }),
    ],
    test: {
      coverage: { enabled: false },
      include: ["test/**/*.test.ts"],
    },
  };
});
