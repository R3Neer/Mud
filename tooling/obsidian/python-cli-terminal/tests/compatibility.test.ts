import path from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import { AnalysisService } from "../src/analysis-service";
import { complete } from "../src/completions";

const pluginRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = path.resolve(pluginRoot, "../../..");
const helperPath = path.join(pluginRoot, "resources", "analyze_cli.py");
const python = process.env.PYTHON ?? "python";

describe("compatibilidad con los CLI reales de MUD", () => {
  it("resuelve y analiza tooling.markdown_export como módulo", async () => {
    const service = new AnalysisService(repositoryRoot, helperPath, python);
    const analysis = await service.analyze(
      path.join(repositoryRoot, "tooling", "markdown_export", "__main__.py"),
    );

    expect(analysis.kind).toBe("module");
    expect(analysis.invocation).toBe("python -m tooling.markdown_export");
    expect(analysis.framework).toBe("argparse");
    expect(analysis.spec?.commands.map((command) => command.name)).toEqual([
      "list-profiles",
      "export",
      "serve",
    ]);
    const exportCommand = analysis.spec?.commands.find((command) => command.name === "export");
    const exportNames = exportCommand?.options.flatMap((option) => option.names) ?? [];
    expect(exportNames).toEqual(expect.arrayContaining([
      "--root",
      "--config",
      "--profile",
      "--files",
      "--name",
      "--output",
      "--follow-links",
      "--no-follow-links",
      "--strip-frontmatter",
      "--keep-frontmatter",
      "--source-markers",
      "--no-source-markers",
      "--strict-links",
      "--max-chars",
      "--timestamp",
    ]));
    const profile = exportCommand?.options.find((option) => option.names.includes("--profile"));
    const files = exportCommand?.options.find((option) => option.names.includes("--files"));
    expect(profile?.group).toBe(files?.group);
    expect(files?.nargs).toBe("+");
    expect(exportCommand?.options.find((option) => option.names.includes("--max-chars"))?.valueType)
      .toBe("integer");
    expect(
      analysis.spec?.commands
        .find((command) => command.name === "serve")
        ?.options.find((option) => option.names.includes("--port"))
        ?.valueType,
    ).toBe("integer");
    expect(analysis.dynamicValues["export:--profile"]).toEqual([
      "specification",
      "decisions",
      "language",
      "current",
    ]);
  }, 20_000);

  it("completa opciones, perfiles y exclusiones del exportador", async () => {
    const service = new AnalysisService(repositoryRoot, helperPath, python);
    const analysis = await service.analyze(
      path.join(repositoryRoot, "tooling", "markdown_export", "__main__.py"),
    );

    const profiles = await complete(`${analysis.invocation} export --profile `, analysis);
    expect(profiles.suggestions.map((item) => item.value)).toContain("specification");
    expect(profiles.suggestions.map((item) => item.value)).toContain("current");

    const commands = await complete(analysis.invocation, analysis);
    expect(commands.suggestions.map((item) => item.value)).toEqual(
      expect.arrayContaining(["list-profiles", "export", "serve"]),
    );

    const excluded = await complete(`${analysis.invocation} export --files README.md --`, analysis);
    const profile = excluded.suggestions.find((item) => item.value === "--profile");
    expect(profile?.disabled).toBe(true);
    expect(excluded.suggestions.map((item) => item.value)).toContain("--follow-links");
    expect(excluded.suggestions.map((item) => item.value)).toContain("--no-follow-links");
  }, 20_000);

  it("clasifica el validador sin ejecutar una sonda --help", async () => {
    const service = new AnalysisService(repositoryRoot, helperPath, python);
    const analysis = await service.analyze(
      path.join(repositoryRoot, "especificacion", "gramatica", "validate_grammar.py"),
    );

    expect(analysis.kind).toBe("script");
    expect(analysis.invocation).toBe("python especificacion/gramatica/validate_grammar.py");
    expect(analysis.framework).toBeNull();
    expect(analysis.spec).toBeNull();
    expect(analysis.diagnostics).toEqual([]);
  });

  it.each([
    ["tooling", "markdown_export", "core.py"],
    ["tooling", "markdown_export", "web.py"],
    ["tooling", "markdown_export", "__init__.py"],
  ])("no propone ejecutar %s/%s/%s", async (...segments: string[]) => {
    const service = new AnalysisService(repositoryRoot, helperPath, python);
    const analysis = await service.analyze(path.join(repositoryRoot, ...segments));
    expect(analysis.kind).toBe("none");
    expect(analysis.invocation).toBe("");
  });
});
