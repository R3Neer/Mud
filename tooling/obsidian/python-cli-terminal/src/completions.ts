import { readdir } from "node:fs/promises";
import path from "node:path";

import { quotePowerShell } from "./resolver";
import type {
  CliAnalysis,
  CliCommand,
  CliOption,
  CompletionContext,
  Suggestion,
  ValueProvider,
} from "./types";

export interface Token {
  value: string;
  start: number;
  end: number;
}

export function tokenizePowerShell(input: string): Token[] {
  const tokens: Token[] = [];
  let start = -1;
  let quote: "'" | '"' | null = null;
  let value = "";
  for (let index = 0; index < input.length; index += 1) {
    const character = input[index];
    if (start < 0) {
      if (/\s/u.test(character)) continue;
      start = index;
    }
    if ((character === "'" || character === '"') && (quote === null || quote === character)) {
      quote = quote === character ? null : character;
      continue;
    }
    if (/\s/u.test(character) && quote === null) {
      tokens.push({ value, start, end: index });
      start = -1;
      value = "";
      continue;
    }
    value += character;
  }
  if (start >= 0) tokens.push({ value, start, end: input.length });
  return tokens;
}

function commandFor(tokens: Token[], baseCount: number, analysis: CliAnalysis): CliCommand | null {
  const candidate = tokens[baseCount]?.value;
  return analysis.spec?.commands.find((command) => command.name === candidate) ?? null;
}

function allOptions(analysis: CliAnalysis, command: CliCommand | null): CliOption[] {
  return [...(analysis.spec?.options ?? []), ...(command?.options ?? [])];
}

function findOption(options: CliOption[], name: string | undefined): CliOption | null {
  if (name === undefined) return null;
  return options.find((option) => option.names.includes(name)) ?? null;
}

function activeValueOption(tokens: Token[], options: CliOption[], endedWithSpace: boolean): CliOption | null {
  if (tokens.length === 0) return null;
  if (!endedWithSpace && tokens.at(-1)?.value.startsWith("-") === true) return null;
  const previous = endedWithSpace ? tokens.at(-1)?.value : tokens.at(-2)?.value;
  const direct = findOption(options, previous);
  if (direct?.takesValue === true) return direct;
  for (let index = tokens.length - (endedWithSpace ? 1 : 2); index >= 0; index -= 1) {
    const option = findOption(options, tokens[index]?.value);
    if (option === null) continue;
    if (option.takesValue && (option.nargs === "+" || option.nargs === "*")) return option;
    break;
  }
  return null;
}

function currentFragment(input: string, tokens: Token[]): { fragment: string; start: number } {
  if (input.length === 0 || /\s$/u.test(input)) return { fragment: "", start: input.length };
  const token = tokens.at(-1);
  return token === undefined ? { fragment: "", start: input.length } : { fragment: token.value, start: token.start };
}

function fuzzyFilter(suggestions: Suggestion[], fragment: string): Suggestion[] {
  const query = fragment.toLocaleLowerCase();
  return suggestions
    .filter((suggestion) => query === "" || suggestion.value.toLocaleLowerCase().includes(query))
    .sort((left, right) => {
      const leftStarts = left.value.toLocaleLowerCase().startsWith(query) ? 0 : 1;
      const rightStarts = right.value.toLocaleLowerCase().startsWith(query) ? 0 : 1;
      return leftStarts - rightStarts || left.value.localeCompare(right.value);
    });
}

async function pathSuggestions(
  root: string,
  fragment: string,
  directoriesOnly: boolean,
  tomlOnly: boolean,
): Promise<Suggestion[]> {
  const normalized = fragment.replaceAll("\\", "/");
  const directoryPart = normalized.includes("/") ? normalized.slice(0, normalized.lastIndexOf("/") + 1) : "";
  const namePart = normalized.slice(directoryPart.length).toLocaleLowerCase();
  const target = path.resolve(root, directoryPart || ".");
  if (!target.startsWith(path.resolve(root))) return [];
  try {
    const entries = await readdir(target, { withFileTypes: true });
    return entries
      .filter((entry) => entry.name.toLocaleLowerCase().includes(namePart))
      .filter((entry) => !directoriesOnly || entry.isDirectory())
      .filter((entry) => !tomlOnly || entry.isDirectory() || entry.name.endsWith(".toml"))
      .slice(0, 100)
      .map((entry) => {
        const relative = `${directoryPart}${entry.name}${entry.isDirectory() ? "/" : ""}`;
        return {
          value: quotePowerShell(relative),
          label: relative,
          detail: entry.isDirectory() ? "carpeta" : "ruta",
        };
      });
  } catch {
    return [];
  }
}

function normalizedType(option: CliOption): CliOption["valueType"] {
  const names = new Set(option.names);
  if (names.has("--root")) return "directory";
  if (names.has("--config")) return "toml";
  if (names.has("--files") || names.has("--output")) return "path";
  return option.valueType;
}

export interface CompletionResult {
  suggestions: Suggestion[];
  replaceFrom: number;
}

export async function complete(
  input: string,
  analysis: CliAnalysis,
  providers: readonly ValueProvider[] = [],
): Promise<CompletionResult> {
  if (analysis.spec === null) return { suggestions: [], replaceFrom: input.length };
  const tokens = tokenizePowerShell(input);
  const baseCount = tokenizePowerShell(analysis.invocation).length;
  const command = commandFor(tokens, baseCount, analysis);
  const options = allOptions(analysis, command);
  const fragmentInfo =
    tokens.length <= baseCount && input.trimEnd() === analysis.invocation
      ? { fragment: "", start: input.length }
      : currentFragment(input, tokens);
  const option = activeValueOption(tokens, options, /\s$/u.test(input));
  const context: CompletionContext = {
    analysis,
    command,
    option,
    fragment: fragmentInfo.fragment,
  };

  if (option !== null) {
    const dynamicKey = `${command?.name ?? "*"}:${option.names[0] ?? ""}`;
    const dynamic = analysis.dynamicValues[dynamicKey] ?? option.choices;
    const suggestions: Suggestion[] = dynamic.map((value) => ({ value }));
    for (const provider of providers) {
      if (provider.supports(context)) suggestions.push(...await provider.getValues(context));
    }
    const type = normalizedType(option);
    if (type === "path" || type === "directory" || type === "toml") {
      suggestions.push(
        ...await pathSuggestions(
          analysis.context.projectRoot,
          fragmentInfo.fragment,
          type === "directory",
          type === "toml",
        ),
      );
    } else if (type === "integer" && fragmentInfo.fragment === "") {
      suggestions.push({ value: "0", detail: "entero" });
    }
    return { suggestions: fuzzyFilter(suggestions, fragmentInfo.fragment), replaceFrom: fragmentInfo.start };
  }

  const usedNames = new Set(tokens.map((token) => token.value).filter((value) => value.startsWith("-")));
  const usedGroups = new Set(
    options
      .filter((candidate) => candidate.group !== null && candidate.names.some((name) => usedNames.has(name)))
      .map((candidate) => candidate.group),
  );
  const suggestions: Suggestion[] = [];
  if (command === null) {
    suggestions.push(
      ...analysis.spec.commands.map((candidate) => ({
        value: candidate.name,
        detail: candidate.help || "subcomando",
      })),
    );
  }
  suggestions.push(
    ...options.flatMap((candidate) =>
      candidate.names
        .filter((name) => !usedNames.has(name))
        .map((name) => ({
          value: name,
          detail: candidate.help || (candidate.takesValue ? candidate.metavar ?? "valor" : "opción"),
          disabled: candidate.group !== null && usedGroups.has(candidate.group),
        })),
    ),
  );
  return {
    suggestions: fuzzyFilter(suggestions, fragmentInfo.fragment),
    replaceFrom: fragmentInfo.start,
  };
}
