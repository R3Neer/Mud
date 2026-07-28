import { readFile } from "node:fs/promises";
import path from "node:path";

const TOKENIZER_IMPORT =
  'const { tokenizeEbnf } = require("./tokenizer.cjs");';

export async function bundleMain(pluginRoot) {
  const [mainSource, tokenizerSource] = await Promise.all([
    readFile(path.join(pluginRoot, "main.js"), "utf8"),
    readFile(path.join(pluginRoot, "tokenizer.cjs"), "utf8"),
  ]);

  if (!mainSource.includes(TOKENIZER_IMPORT)) {
    throw new Error("main.js no contiene la importación esperada del tokenizador.");
  }

  const tokenizerBody = tokenizerSource
    .replace(/^"use strict";\r?\n\r?\n/, "")
    .replace(
      /\r?\nmodule\.exports = \{ tokenizeEbnf \};\r?\n?$/,
      "",
    );

  if (tokenizerBody === tokenizerSource) {
    throw new Error("No se pudo preparar tokenizer.cjs para el empaquetado.");
  }

  return mainSource.replace(TOKENIZER_IMPORT, tokenizerBody);
}
