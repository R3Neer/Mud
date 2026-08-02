import type { CliCommand, CliOption, CliSpec, ValueType } from "./types";

function valueTypeFor(metavar: string | null): ValueType {
  if (metavar === null) return "text";
  const upper = metavar.toUpperCase();
  if (upper.includes("PORT") || upper.includes("CHARS") || upper === "INT") return "integer";
  if (upper.includes("CONFIG") || upper.includes("TOML")) return "toml";
  if (upper.includes("ROOT") || upper.includes("DIR")) return "directory";
  if (upper.includes("FILE") || upper.includes("PATH") || upper.includes("RUTA") || upper.includes("OUTPUT")) {
    return "path";
  }
  return "text";
}

export function parseHelpOptions(output: string): CliOption[] {
  const options: CliOption[] = [];
  for (const line of output.split(/\r?\n/u)) {
    const match = /^\s{2,}(-\w(?:,\s*)?|--[\w-]+)(.*?)(?:\s{2,}.*)?$/u.exec(line);
    if (match === null) continue;
    const declaration = `${match[1]}${match[2]}`.trim();
    if (!declaration.includes("-")) continue;
    const names = [...declaration.matchAll(/(?<!\w)(--?[\w-]+)/gu)].map((item) => item[1]);
    if (names.length === 0) continue;
    const tail = declaration.replace(/(?:--?[\w-]+)(?:,\s*)?/gu, "").trim();
    const metavar = tail === "" ? null : tail.split(/\s+/u)[0]?.replace(/[[\].]/gu, "") ?? null;
    options.push({
      names,
      help: "",
      metavar,
      nargs: tail.includes("...") ? "+" : null,
      valueType: valueTypeFor(metavar),
      choices: [],
      takesValue: metavar !== null,
      group: null,
    });
  }
  return options;
}

export function parseHelpCommands(output: string): CliCommand[] {
  const usage = output.split(/\r?\n/u).find((line) => line.trimStart().startsWith("usage:"));
  const braces = usage === undefined ? null : /\{([^}]+)\}/u.exec(usage);
  if (braces === null) return [];
  return braces[1].split(",").map((name) => ({
    name: name.trim(),
    help: "",
    options: [],
    commands: [],
  }));
}

export function parseHelpSpec(output: string, name = "python"): CliSpec {
  return {
    name,
    help: "",
    options: parseHelpOptions(output),
    commands: parseHelpCommands(output),
  };
}
