"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");

const { tokenizeEbnf } = require("../tokenizer.cjs");

function valuesByKind(source) {
  const result = {};
  for (const current of tokenizeEbnf(source)) {
    (result[current.kind] ??= []).push(source.slice(current.from, current.to));
  }
  return result;
}

test("clasifica las categorías visibles de la gramática MUD", () => {
  const source = `(* comentario *)
mud-file
    ::= layout , [ file-item ] , EOF ;

identifier ::= IDENTIFIER ;
literal ::= "true" | ? secuencia especial ? ;
`;

  const values = valuesByKind(source);

  assert.deepEqual(values.comment, ["(* comentario *)"]);
  assert.deepEqual(values.definition, [
    "mud-file",
    "identifier",
    "literal",
  ]);
  assert.ok(values.reference.includes("layout"));
  assert.ok(values.reference.includes("file-item"));
  assert.ok(values.terminal.includes("EOF"));
  assert.ok(values.terminal.includes("IDENTIFIER"));
  assert.deepEqual(values.string, ['"true"']);
  assert.deepEqual(values.meta, ["? secuencia especial ?"]);
  assert.ok(values.operator.includes("::="));
  assert.ok(values.bracket.includes("["));
});

test("un comentario o una cadena no generan tokens interiores", () => {
  const source = `(* fake ::= IDENTIFIER *) "fake ::= IDENTIFIER"`;
  const tokens = tokenizeEbnf(source);

  assert.deepEqual(
    tokens.map((current) => current.kind),
    ["comment", "string"],
  );
});

test("un comentario sin cierre consume hasta el final", () => {
  const source = "rule ::= value ;\n(* comentario";
  const tokens = tokenizeEbnf(source);
  const last = tokens.at(-1);

  assert.equal(last.kind, "comment");
  assert.equal(last.to, source.length);
});
