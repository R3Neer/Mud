import { access, readFile } from "node:fs/promises";
import path from "node:path";

import type {
  CliKind,
  ProjectCliConfiguration,
  ProjectCliDefinition,
  StaticAnalysis,
} from "./types";

const CONFIG_PATH = path.join("tooling", "python-cli-terminal.json");

async function exists(candidate: string): Promise<boolean> {
  try {
    await access(candidate);
    return true;
  } catch {
    return false;
  }
}

export function normalizeRelative(value: string): string {
  return value.replaceAll("\\", "/");
}

export function quotePowerShell(value: string): string {
  if (/^[A-Za-z0-9_./:\\-]+$/u.test(value)) return value;
  return `'${value.replaceAll("'", "''")}'`;
}

export function formatInvocation(arguments_: string[]): string {
  return arguments_.map(quotePowerShell).join(" ");
}

export async function findProjectRoot(filePath: string, vaultRoot: string): Promise<string> {
  const resolvedVault = path.resolve(vaultRoot);
  let directory = path.dirname(path.resolve(filePath));
  let fallback = resolvedVault;
  while (directory.startsWith(resolvedVault)) {
    const markers = await Promise.all([
      exists(path.join(directory, "pyproject.toml")),
      exists(path.join(directory, ".git")),
    ]);
    if (markers.some(Boolean)) {
      return directory;
    }
    fallback = directory;
    const parent = path.dirname(directory);
    if (parent === directory) break;
    directory = parent;
  }
  return fallback === resolvedVault ? resolvedVault : resolvedVault;
}

export async function loadProjectConfiguration(
  projectRoot: string,
): Promise<ProjectCliConfiguration | null> {
  try {
    const raw = JSON.parse(
      await readFile(path.join(projectRoot, CONFIG_PATH), "utf8"),
    ) as unknown;
    if (
      typeof raw !== "object" ||
      raw === null ||
      !("version" in raw) ||
      !("clis" in raw) ||
      raw.version !== 1 ||
      !Array.isArray(raw.clis)
    ) {
      return null;
    }
    return raw as ProjectCliConfiguration;
  } catch {
    return null;
  }
}

export function findDefinition(
  configuration: ProjectCliConfiguration | null,
  relativePath: string,
): ProjectCliDefinition | undefined {
  const normalized = normalizeRelative(relativePath);
  return configuration?.clis.find((definition) => normalizeRelative(definition.path) === normalized);
}

export async function moduleNameForMain(filePath: string, projectRoot: string): Promise<string | null> {
  if (path.basename(filePath).toLowerCase() !== "__main__.py") return null;
  const segments: string[] = [];
  let directory = path.dirname(filePath);
  while (directory.startsWith(projectRoot) && directory !== projectRoot) {
    if (!(await exists(path.join(directory, "__init__.py")))) break;
    segments.unshift(path.basename(directory));
    directory = path.dirname(directory);
  }
  return segments.length > 0 ? segments.join(".") : null;
}

export async function resolveKindAndArguments(
  staticAnalysis: StaticAnalysis,
  filePath: string,
  projectRoot: string,
  pythonExecutable: string,
  definition?: ProjectCliDefinition,
): Promise<{ kind: CliKind; arguments: string[] }> {
  const configuredModule = definition?.module;
  const detectedModule = await moduleNameForMain(filePath, projectRoot);
  if (configuredModule !== undefined || detectedModule !== null) {
    return {
      kind: "module",
      arguments: [pythonExecutable, "-m", configuredModule ?? detectedModule ?? ""],
    };
  }
  const relative = normalizeRelative(path.relative(projectRoot, filePath));
  if (staticAnalysis.unittest) {
    const module = relative.replace(/\.py$/u, "").replaceAll("/", ".");
    return { kind: "test", arguments: [pythonExecutable, "-m", "unittest", module] };
  }
  if (staticAnalysis.hasMainGuard) {
    return { kind: "script", arguments: [pythonExecutable, relative] };
  }
  return { kind: "none", arguments: [] };
}
