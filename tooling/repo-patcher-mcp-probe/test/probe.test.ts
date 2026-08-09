import { unzipSync } from "fflate";
import { describe, expect, it } from "vitest";

import {
  buildDeterministicZip,
  bytesToBase64,
  decodeCanonicalBase64,
  normalizeProbePath,
  ProbeError,
  sha256Hex,
  validateRequestId,
} from "../src/probe.js";

describe("base64 transport", () => {
  it("round-trips arbitrary bytes", () => {
    const bytes = Uint8Array.from([0, 1, 2, 127, 128, 254, 255]);
    expect(decodeCanonicalBase64(bytesToBase64(bytes))).toEqual(bytes);
  });

  it.each(["", "abc", "!!!!", "YQ=A", "YR=="])("rejects non-canonical input %j", (value) => {
    expect(() => decodeCanonicalBase64(value)).toThrow(ProbeError);
  });
});

describe("logical file transport", () => {
  it("builds byte-identical ZIPs independently of input order", async () => {
    const first = buildDeterministicZip([
      { path: "zeta.md", encoding: "utf8", content: "último\n" },
      { path: "patch.yaml", encoding: "utf8", content: "schema: 1\nid: prueba\ntitle: Prueba\noperations: []\n" },
      { path: "files/data.bin", encoding: "base64", content: "AAEC/v8=" },
    ]);
    const second = buildDeterministicZip([
      { path: "files/data.bin", encoding: "base64", content: "AAEC/v8=" },
      { path: "patch.yaml", encoding: "utf8", content: "schema: 1\nid: prueba\ntitle: Prueba\noperations: []\n" },
      { path: "zeta.md", encoding: "utf8", content: "último\n" },
    ]);

    expect(second).toEqual(first);
    expect(await sha256Hex(first)).toBe(await sha256Hex(second));
    expect(await sha256Hex(first)).toBe(
      "40134ed750ba056b22124ea6dc50059f352688fd35abae3b8f59579f0e19df58",
    );
    expect(Object.keys(unzipSync(first)).sort()).toEqual(["files/data.bin", "patch.yaml", "zeta.md"]);
  });

  it("rejects paths unsafe or ambiguous on Windows", () => {
    for (const path of [
      "",
      "/absolute",
      "C:/drive",
      "../escape",
      "a/../b",
      "a\\b",
      "CON",
      "docs/NUL.txt",
      "trailing.",
      "trailing ",
      "colon:name",
    ]) {
      expect(() => normalizeProbePath(path)).toThrow(ProbeError);
    }
    expect(() =>
      buildDeterministicZip([
        { path: "Readme.md", encoding: "utf8", content: "a" },
        { path: "README.md", encoding: "utf8", content: "b" },
      ]),
    ).toThrow(/Windows/);
    expect(() =>
      buildDeterministicZip([
        { path: "café.md", encoding: "utf8", content: "a" },
        { path: "cafe\u0301.md", encoding: "utf8", content: "b" },
      ]),
    ).toThrow(/Windows/);
  });

  it("builds a representative MUD-shaped package reproducibly", async () => {
    const operations = Array.from({ length: 120 }, (_, index) =>
      [
        "  - op: create_file",
        `    path: notas/prueba/ruta-${String(index).padStart(3, "0")}.md`,
        "    content: |",
        `      Evidencia número ${index}: áéíóú, ñ, λ y 日本語.`,
      ].join("\n"),
    );
    const files = [
      {
        path: "patch.yaml",
        encoding: "utf8" as const,
        content: ["schema: 1", "id: representativa", "operations:", ...operations, ""].join("\n"),
      },
      ...Array.from({ length: 24 }, (_, index) => ({
        path: `docs/capitulo-${String(index).padStart(2, "0")}.md`,
        encoding: "utf8" as const,
        content: `# Capítulo ${index}\n\nCanción, árbol y pingüino.\n`,
      })),
      { path: "plugin.py", encoding: "utf8" as const, content: "def build(context):\n    pass\n" },
      {
        path: "assets/recurso.bin",
        encoding: "base64" as const,
        content: bytesToBase64(Uint8Array.from({ length: 8192 }, (_, index) => (index * 73 + 29) % 256)),
      },
    ];

    const hashes = await Promise.all(
      Array.from({ length: 3 }, () => sha256Hex(buildDeterministicZip(files))),
    );
    expect(new Set(hashes).size).toBe(1);
  });
});

describe("identifiers", () => {
  it.each(["probe-001", "candidate_2", "a.b"])("accepts %s", (value) => {
    expect(validateRequestId(value)).toBe(value);
  });

  it.each(["", "with space", "../escape", "a".repeat(81)])("rejects %j", (value) => {
    expect(() => validateRequestId(value)).toThrow(ProbeError);
  });
});
