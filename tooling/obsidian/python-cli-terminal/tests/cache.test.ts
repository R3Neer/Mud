import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { afterEach, describe, expect, it } from "vitest";

import { AnalysisService } from "../src/analysis-service";

const pluginRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const helperPath = path.join(pluginRoot, "resources", "analyze_cli.py");
const python = process.env.PYTHON ?? "python";
const temporaryDirectories: string[] = [];

afterEach(async () => {
  await Promise.all(temporaryDirectories.splice(0).map((directory) => rm(directory, { recursive: true, force: true })));
});

describe("caché de análisis", () => {
  it("se invalida al cambiar un archivo observado por un proveedor", async () => {
    const root = await mkdtemp(path.join(tmpdir(), "mud-cli-cache-"));
    temporaryDirectories.push(root);
    await mkdir(path.join(root, ".git"));
    await mkdir(path.join(root, "app"));
    await mkdir(path.join(root, "tooling"));
    await writeFile(path.join(root, "app", "__init__.py"), "", "utf8");
    await writeFile(
      path.join(root, "app", "__main__.py"),
      [
        "import argparse",
        "from pathlib import Path",
        "def make_parser():",
        "    parser = argparse.ArgumentParser()",
        "    commands = parser.add_subparsers(dest='command', required=True)",
        "    commands.add_parser('list-profiles')",
        "    return parser",
        "def main():",
        "    args = make_parser().parse_args()",
        "    if args.command == 'list-profiles':",
        "        print(Path('profiles.txt').read_text(encoding='utf-8').strip() + ': perfil')",
        "if __name__ == '__main__':",
        "    main()",
      ].join("\n"),
      "utf8",
    );
    await writeFile(path.join(root, "profiles.txt"), "one\n", "utf8");
    await writeFile(
      path.join(root, "tooling", "python-cli-terminal.json"),
      JSON.stringify({
        version: 1,
        clis: [{
          path: "app/__main__.py",
          module: "app",
          helpProbes: [["--help"]],
          valueProviders: [{
            option: "--profile",
            command: "*",
            arguments: ["list-profiles"],
            format: "colon-prefix",
            watch: ["profiles.txt"],
          }],
        }],
      }),
      "utf8",
    );

    const service = new AnalysisService(root, helperPath, python);
    const file = path.join(root, "app", "__main__.py");
    const first = await service.analyze(file);
    expect(first.dynamicValues["*:--profile"]).toEqual(["one"]);

    await writeFile(path.join(root, "profiles.txt"), "two\n", "utf8");
    const second = await service.analyze(file);
    expect(second.dynamicValues["*:--profile"]).toEqual(["two"]);
  });
});
