import { copyFile, mkdir, readFile, rename, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import { bundleMain } from "./bundle.mjs";

const PLUGIN_ID = "mud-ebnf-viewer";
const currentFile = fileURLToPath(import.meta.url);
const pluginRoot = path.resolve(path.dirname(currentFile), "..");
const repositoryRoot = path.resolve(pluginRoot, "../../..");
const obsidianDirectory = path.join(repositoryRoot, ".obsidian");
const target = path.join(obsidianDirectory, "plugins", PLUGIN_ID);

await mkdir(target, { recursive: true });
const bundledMain = await bundleMain(pluginRoot);
await Promise.all(
  [
    writeFile(path.join(target, "main.js"), bundledMain, "utf8"),
    ...["manifest.json", "styles.css"].map((file) =>
      copyFile(path.join(pluginRoot, file), path.join(target, file)),
    ),
  ],
);

const communityPluginsFile = path.join(
  obsidianDirectory,
  "community-plugins.json",
);
const activePlugins = JSON.parse(
  await readFile(communityPluginsFile, "utf8").catch(() => "[]"),
);

if (
  !Array.isArray(activePlugins) ||
  !activePlugins.every((plugin) => typeof plugin === "string")
) {
  throw new Error("community-plugins.json no contiene una lista válida.");
}

if (!activePlugins.includes(PLUGIN_ID)) activePlugins.push(PLUGIN_ID);

const temporaryFile = `${communityPluginsFile}.${process.pid}.tmp`;
await writeFile(
  temporaryFile,
  `${JSON.stringify(activePlugins, null, 2)}\n`,
  "utf8",
);
await rename(temporaryFile, communityPluginsFile);

console.log(`Plugin instalado en ${target}`);
console.log("Recarga Obsidian para empezar a abrir archivos .ebnf.");
