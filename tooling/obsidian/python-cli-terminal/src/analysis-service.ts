import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";

import { parseHelpSpec } from "./help-parser";
import { runLimitedProcess } from "./process-runner";
import {
  findDefinition,
  findProjectRoot,
  formatInvocation,
  loadProjectConfiguration,
  normalizeRelative,
  resolveKindAndArguments,
} from "./resolver";
import type {
  AnalysisContext,
  CliAdapter,
  CliAnalysis,
  CliCommand,
  CliSpec,
  ProjectCliDefinition,
  StaticAnalysis,
  ValueProvider,
} from "./types";

const MAX_OUTPUT = 256 * 1024;

function safeEnvironment(): NodeJS.ProcessEnv {
  const allowed = [
    "SystemRoot",
    "WINDIR",
    "PATH",
    "PATHEXT",
    "TEMP",
    "TMP",
    "LOCALAPPDATA",
    "APPDATA",
    "USERPROFILE",
  ];
  return Object.fromEntries(allowed.flatMap((name) => process.env[name] === undefined ? [] : [[name, process.env[name]]]));
}

function commandByName(spec: CliSpec, name: string): CliCommand | undefined {
  return spec.commands.find((command) => command.name === name);
}

function mergeHelp(spec: CliSpec | null, arguments_: string[], output: string): CliSpec {
  const parsed = parseHelpSpec(output);
  if (spec === null) return parsed;
  const commandName = arguments_.at(-1) === "--help" ? arguments_.at(-2) : undefined;
  const target = commandName === undefined ? spec : commandByName(spec, commandName);
  if (target !== undefined) {
    for (const option of parsed.options) {
      if (!target.options.some((current) => current.names.some((name) => option.names.includes(name)))) {
        target.options.push(option);
      }
    }
  }
  return spec;
}

export class AnalysisService {
  private readonly cache = new Map<string, CliAnalysis>();
  private readonly adapters: CliAdapter[] = [];
  private readonly valueProviders: ValueProvider[] = [];

  constructor(
    private readonly vaultRoot: string,
    private readonly helperPath: string,
    private readonly pythonExecutable: string,
  ) {}

  registerAdapter(adapter: CliAdapter): () => void {
    this.adapters.push(adapter);
    return () => this.adapters.splice(this.adapters.indexOf(adapter), 1);
  }

  registerValueProvider(provider: ValueProvider): () => void {
    this.valueProviders.push(provider);
    return () => this.valueProviders.splice(this.valueProviders.indexOf(provider), 1);
  }

  get customValueProviders(): readonly ValueProvider[] {
    return this.valueProviders;
  }

  clear(): void {
    this.cache.clear();
  }

  async analyze(filePath: string): Promise<CliAnalysis> {
    const projectRoot = await findProjectRoot(filePath, this.vaultRoot);
    const relativePath = normalizeRelative(path.relative(projectRoot, filePath));
    const configuration = await loadProjectConfiguration(projectRoot);
    const definition = findDefinition(configuration, relativePath);
    const cacheKey = await this.cacheKey(filePath, projectRoot, definition);
    const cached = this.cache.get(cacheKey);
    if (cached !== undefined) return cached;

    const context: AnalysisContext = {
      filePath,
      relativePath,
      projectRoot,
      pythonExecutable: this.pythonExecutable,
    };
    const diagnostics: string[] = [];
    const staticAnalysis = await this.runStaticAnalysis(filePath);
    if (staticAnalysis.error !== undefined) diagnostics.push(staticAnalysis.error);
    const resolved = await resolveKindAndArguments(
      staticAnalysis,
      filePath,
      projectRoot,
      this.pythonExecutable,
      definition,
    );
    let spec = staticAnalysis.spec;
    let framework = staticAnalysis.frameworks[0] ?? null;

    for (const adapter of this.adapters) {
      if (await adapter.detect(context) <= 0) continue;
      spec = (await adapter.analyzeStatic(context)) ?? spec;
      framework = adapter.id;
      break;
    }

    if (resolved.kind !== "none" && definition?.disableHelp !== true && framework !== null) {
      const probes = definition?.helpProbes ?? [["--help"]];
      for (const probe of probes) {
        try {
          const output = await this.runTarget(resolved.arguments, probe, projectRoot);
          spec = mergeHelp(spec, probe, output);
        } catch (error) {
          diagnostics.push(`No se pudo inspeccionar ${probe.join(" ")}: ${String(error)}`);
        }
      }
    }

    const dynamicValues = await this.loadDynamicValues(definition, resolved.arguments, projectRoot, diagnostics);
    const result: CliAnalysis = {
      context,
      kind: resolved.kind,
      invocationArgs: resolved.arguments,
      invocation: formatInvocation(resolved.arguments),
      framework,
      spec,
      dynamicValues,
      diagnostics,
      minimumPython: definition?.minimumPython,
    };
    this.cache.set(cacheKey, result);
    return result;
  }

  private async runStaticAnalysis(filePath: string): Promise<StaticAnalysis> {
    const { stdout } = await runLimitedProcess(
      this.pythonExecutable,
      ["-I", "-S", this.helperPath, filePath],
      {
        cwd: this.vaultRoot,
        env: safeEnvironment(),
        timeoutMs: 5_000,
        maxOutputBytes: MAX_OUTPUT,
      },
    );
    return JSON.parse(stdout) as StaticAnalysis;
  }

  private async runTarget(base: string[], suffix: string[], cwd: string): Promise<string> {
    const [executable, ...prefix] = base;
    if (executable === undefined) throw new Error("No hay ejecutable.");
    const { stdout } = await runLimitedProcess(executable, [...prefix, ...suffix], {
      cwd,
      env: safeEnvironment(),
      timeoutMs: 4_000,
      maxOutputBytes: MAX_OUTPUT,
    });
    return stdout;
  }

  private async loadDynamicValues(
    definition: ProjectCliDefinition | undefined,
    base: string[],
    cwd: string,
    diagnostics: string[],
  ): Promise<Record<string, string[]>> {
    const result: Record<string, string[]> = {};
    for (const provider of definition?.valueProviders ?? []) {
      try {
        const output = await this.runTarget(base, provider.arguments, cwd);
        result[`${provider.command ?? "*"}:${provider.option}`] = output
          .split(/\r?\n/u)
          .filter(Boolean)
          .map((line) =>
            provider.format === "colon-prefix"
              ? line.split(":", 1)[0].replace(/\s+\([^)]*\)$/u, "").trim()
              : line.trim(),
          );
      } catch (error) {
        diagnostics.push(`No se pudieron cargar valores para ${provider.option}: ${String(error)}`);
      }
    }
    return result;
  }

  private async cacheKey(
    filePath: string,
    projectRoot: string,
    definition: ProjectCliDefinition | undefined,
  ): Promise<string> {
    const hash = createHash("sha256");
    hash.update(await readFile(filePath));
    hash.update(this.pythonExecutable);
    for (const provider of definition?.valueProviders ?? []) {
      for (const watched of provider.watch ?? []) {
        try {
          hash.update(await readFile(path.join(projectRoot, watched)));
        } catch {
          hash.update(`missing:${watched}`);
        }
      }
    }
    return hash.digest("hex");
  }
}
