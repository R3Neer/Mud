"use strict";

const IDENTIFIER_START = /[A-Za-z]/;
const IDENTIFIER_PART = /[A-Za-z0-9-]/;
const DIGIT = /[0-9]/;
const UPPER_TERMINAL = /^[A-Z][A-Z0-9_]*$/;

const OPERATORS = [
  "<=>",
  "::=",
  ":=",
  "->",
  "..",
  "=>",
  "==",
  "!=",
  "<=",
  ">=",
  "+=",
  "-=",
  "*=",
  "/=",
  "|",
  ",",
  ";",
  "=",
];

function tokenizeEbnf(text) {
  const tokens = [];
  let position = 0;

  while (position < text.length) {
    const start = position;

    if (text.startsWith("(*", position)) {
      const closing = text.indexOf("*)", position + 2);
      position = closing === -1 ? text.length : closing + 2;
      tokens.push(token("comment", start, position));
      continue;
    }

    if (text[position] === '"') {
      position += 1;
      let escaped = false;
      while (position < text.length) {
        const character = text[position];
        position += 1;
        if (character === '"' && !escaped) break;
        escaped = character === "\\" && !escaped;
        if (character !== "\\") escaped = false;
      }
      tokens.push(token("string", start, position));
      continue;
    }

    if (text[position] === "?") {
      const closing = text.indexOf("?", position + 1);
      position = closing === -1 ? text.length : closing + 1;
      tokens.push(token("meta", start, position));
      continue;
    }

    if (IDENTIFIER_START.test(text[position])) {
      position += 1;
      while (
        position < text.length &&
        IDENTIFIER_PART.test(text[position])
      ) {
        position += 1;
      }

      const value = text.slice(start, position);
      tokens.push(
        token(
          isDefinition(text, start, position)
            ? "definition"
            : UPPER_TERMINAL.test(value)
              ? "terminal"
              : "reference",
          start,
          position,
        ),
      );
      continue;
    }

    if (DIGIT.test(text[position])) {
      position += 1;
      while (position < text.length && DIGIT.test(text[position])) {
        position += 1;
      }
      tokens.push(token("number", start, position));
      continue;
    }

    const operator = OPERATORS.find((candidate) =>
      text.startsWith(candidate, position),
    );
    if (operator !== undefined) {
      position += operator.length;
      tokens.push(token("operator", start, position));
      continue;
    }

    if ("()[]{}".includes(text[position])) {
      position += 1;
      tokens.push(token("bracket", start, position));
      continue;
    }

    position += 1;
  }

  return tokens;
}

function isDefinition(text, start, end) {
  let after = end;
  while (text[after] === " " || text[after] === "\t") after += 1;
  if (text.startsWith("::=", after)) return true;

  const lineStart = text.lastIndexOf("\n", start - 1) + 1;
  const startsLine = text.slice(lineStart, start).trim() === "";
  const endsLine =
    after === text.length || text[after] === "\r" || text[after] === "\n";
  return startsLine && endsLine;
}

function token(kind, from, to) {
  return { kind, from, to };
}

module.exports = { tokenizeEbnf };
