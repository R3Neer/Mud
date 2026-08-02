import { access, copyFile, cp, mkdir, readFile, rename, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

export const PLUGIN_ID = "mud-python-cli-terminal";

export async function activatePlugin(communityFile) {
  let active = [];
  try {
    active = JSON.parse(await readFile(communityFile, "utf8"));
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
  if (!Array.isArray(active) || !active.every((value) => typeof value === "string")) {
    throw new Error(`${communityFile} no contiene una lista válida de plugins.`);
  }
  if (!active.includes(PLUGIN_ID)) active.push(PLUGIN_ID);
  const temporary = `${communityFile}.${process.pid}.tmp`;
  await writeFile(temporary, `${JSON.stringify(active, null, 2)}\n`, "utf8");
  await rename(temporary, communityFile);
  return active;
}

export async function installLocal(pluginRoot) {
  const repositoryRoot = path.resolve(pluginRoot, "../../..");
  const configDirectory = path.join(repositoryRoot, ".obsidian");
  const target = path.join(configDirectory, "plugins", PLUGIN_ID);
  await mkdir(path.join(target, "resources"), { recursive: true });
  await mkdir(path.join(target, "node_modules"), { recursive: true });
  await Promise.all([
    copyFile(path.join(pluginRoot, "dist", "main.js"), path.join(target, "main.js")),
    copyFile(path.join(pluginRoot, "dist", "main.css"), path.join(target, "styles.css")),
    copyFile(path.join(pluginRoot, "manifest.json"), path.join(target, "manifest.json")),
    copyFile(
      path.join(pluginRoot, "resources", "analyze_cli.py"),
      path.join(target, "resources", "analyze_cli.py"),
    ),
    copyFile(
      path.join(pluginRoot, "resources", "pty_bridge.cjs"),
      path.join(target, "resources", "pty_bridge.cjs"),
    ),
    copyNodePtyIfMissing(pluginRoot, target),
  ]);
  const active = await activatePlugin(path.join(configDirectory, "community-plugins.json"));
  return { target, active };
}

async function copyNodePtyIfMissing(pluginRoot, target) {
  const installed = path.join(target, "node_modules", "node-pty");
  try {
    await access(path.join(installed, "package.json"));
    return;
  } catch {
    await cp(path.join(pluginRoot, "node_modules", "node-pty"), installed, {
      recursive: true,
      force: false,
    });
  }
}

const currentFile = fileURLToPath(import.meta.url);
if (process.argv[1] !== undefined && path.resolve(process.argv[1]) === currentFile) {
  const pluginRoot = path.resolve(path.dirname(currentFile), "..");
  const result = await installLocal(pluginRoot);
  console.log(`Plugin instalado en ${result.target}`);
  console.log("Recarga Obsidian para cargar o actualizar el plugin.");
}
