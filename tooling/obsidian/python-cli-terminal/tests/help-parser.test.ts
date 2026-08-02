import { describe, expect, it } from "vitest";

import { parseHelpCommands, parseHelpOptions } from "../src/help-parser";

describe("parser de ayuda argparse", () => {
  it("reconoce subcomandos desde usage", () => {
    const output = "usage: tool [-h] {list-profiles,export,serve} ...\n";
    expect(parseHelpCommands(output).map((command) => command.name)).toEqual([
      "list-profiles",
      "export",
      "serve",
    ]);
  });

  it("reconoce opciones largas y parejas booleanas", () => {
    const output = [
      "options:",
      "  -h, --help            show this help message and exit",
      "  --port PORT",
      "  --follow-links, --no-follow-links",
    ].join("\n");
    const options = parseHelpOptions(output);
    expect(options.some((option) => option.names.includes("--port") && option.takesValue)).toBe(true);
    expect(options.some((option) => option.names.includes("--no-follow-links"))).toBe(true);
  });
});
