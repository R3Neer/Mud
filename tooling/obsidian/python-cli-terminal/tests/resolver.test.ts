import path from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import {
  findProjectRoot,
  formatInvocation,
  moduleNameForMain,
  quotePowerShell,
} from "../src/resolver";

const pluginRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = path.resolve(pluginRoot, "../../..");

describe("resolución de entradas", () => {
  it("encuentra la raíz Git aunque no haya pyproject.toml", async () => {
    const file = path.join(repositoryRoot, "tooling", "markdown_export", "__main__.py");
    await expect(findProjectRoot(file, repositoryRoot)).resolves.toBe(repositoryRoot);
  });

  it("convierte __main__.py en el módulo completo", async () => {
    const file = path.join(repositoryRoot, "tooling", "markdown_export", "__main__.py");
    await expect(moduleNameForMain(file, repositoryRoot)).resolves.toBe("tooling.markdown_export");
  });

  it("protege rutas PowerShell con espacios y apóstrofos", () => {
    expect(quotePowerShell("D:\\Una ruta\\script.py")).toBe("'D:\\Una ruta\\script.py'");
    expect(quotePowerShell("Samuel's script.py")).toBe("'Samuel''s script.py'");
    expect(formatInvocation(["python", "ruta con espacios.py"])).toBe("python 'ruta con espacios.py'");
  });
});
