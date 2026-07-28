import assert from "node:assert/strict";
import { test } from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { bundleMain } from "../scripts/bundle.mjs";

const pluginRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

test("empaqueta el tokenizador dentro de main.js", async () => {
  const bundled = await bundleMain(pluginRoot);

  assert.doesNotMatch(bundled, /require\("\.\/tokenizer\.cjs"\)/);
  assert.match(bundled, /function tokenizeEbnf\(text\)/);
  assert.doesNotThrow(() => new Function(bundled));
});
