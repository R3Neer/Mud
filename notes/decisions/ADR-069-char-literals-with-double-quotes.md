---
id: D-069
title: "`Char` literals with double quotes"
status: current
date: 2026-08-02
supersedes: []
superseded-by: []
questions:
  - "Q-047"
affects:
  - "lexicon, literal elaboration, Char, String, defaults and syntax highlighting"
---
# ADR-069 — `Char` literals with double quotes

- Amended by: [[ADR-112-explicit-storage-initialisation|D-112]].

- Amends: [[notes/decisions/ADR-017-everything-type-well-built-has-default-value|D-017]], [[notes/decisions/ADR-032-contextual-construction-and-nominal-casting-of-aliases|D-032]], [[notes/decisions/ADR-050-comments-terminators-text-and-numeric-separators|D-050]] and [[notes/decisions/ADR-056-char-text-and-unicode-ordering|D-056]]
- Related question: [[notes/questions/Q-047-s-selection-of-defaults-by-type|Q-047]]
- Affected documents: lexicon, literal elaboration, `Char`, `String`, defaults and syntax highlighting

## Context

Separating `Char` with single quotes and `String` with double quotes imports a technical-language convention that offers MUD's audience no evident visual distinction. The expected type already resolves other contextual forms and can distinguish text from a single scalar without introducing a second punctuation style.

## Decision

Ordinary `Char` and `String` literals begin with double quotes. The same form is elaborated as follows:

- Its preferred and default type is `String`.
- When the context requires `Char`, it may be elaborated as `Char` if, after interpreting escapes, it contains exactly one Unicode scalar value.
- The `Char` form requires an explicit closing quote and permits no value or anchor interpolation.
- The multiline form is always `String`.
- Without an expected type, `let payload := "a"` infers `String`.
- An empty literal or one containing several scalars is invalid when `Char` is required.

```mud
let letter: Char = "a"
let newline: Char = "\n"
let face: Char = "\u{1F642}"
let word: String = "a"
```

In a comparison or other bidirectional expression, the other operand may provide the expected type:

```mud
pressedKey == "x"
```

Single quotes no longer delimit literals and are not part of the MUD lexicon. An apostrophe remains an ordinary character inside a double-quoted literal.

`"\u{0}"` is a valid explicit initialiser in a Char context, preserving its Unicode domain and order.

Syntax highlighting classifies double-quoted forms as text because choosing `Char` or `String` requires type information. A historical internal character category may remain for theme compatibility, but the MUD tokeniser does not emit it for single quotes.

## Consequences

- MUD has one quote class for textual content.
- A single-scalar literal remains `String` when no `Char` context exists.
- The parser produces one common textual form and static elaboration decides whether it can become a `Char` literal.
- Older code using single quotes is invalid and must be migrated to double quotes.

## Verification

1. `"a"`, `"ñ"`, `"\n"` and `"\u{1F642}"` in a `Char` context.
2. Inference of `String` for `let payload := "a"`.
3. Rejection of `""`, `"ab"`, multiline text and interpolations in a `Char` context.
4. Resolution of `charValue == "x"` as a `Char` comparison.
5. Lexical rejection of single-quoted forms.
6. Explicit Char initialiser `"\u{0}"`.
7. Highlighting with double quotes and no `character` highlighting for single quotes in MUD.
