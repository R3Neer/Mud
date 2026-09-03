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
  - "lexicon, literal elaboration, Char, Text, defaults and syntax highlighting"
---
# ADR-069 — `Char` literals with double quotes

- Amends: [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|D-017]], [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|D-032]], [[notas/decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos|D-050]] and [[notas/decisiones/ADR-056-char-texto-y-orden-unicode|D-056]]
- Related question: [[notas/preguntas/Q-047-seleccion-de-predeterminados-por-tipo|Q-047]]
- Affected documents: lexicon, literal elaboration, `Char`, `Text`, defaults and syntax highlighting

## Context

Separating `Char` with single quotes and `Text` with double quotes imports a technical-language convention that offers MUD's audience no evident visual distinction. The expected type already resolves other contextual forms and can distinguish text from a single scalar without introducing a second punctuation style.

## Decision

Ordinary `Char` and `Text` literals begin with double quotes. The same form is elaborated as follows:

- Its preferred and default type is `Text`.
- When the context requires `Char`, it may be elaborated as `Char` if, after interpreting escapes, it contains exactly one Unicode scalar value.
- The `Char` form requires an explicit closing quote and permits no value or anchor interpolation.
- The multiline form is always `Text`.
- Without an expected type, `value := "a"` infers `Text`.
- An empty literal or one containing several scalars is invalid when `Char` is required.

```mud
letter: Char = "a"
newline: Char = "\n"
face: Char = "\u{1F642}"
word: Text = "a"
```

In a comparison or other bidirectional expression, the other operand may provide the expected type:

```mud
pressedKey == "x"
```

Single quotes no longer delimit literals and are not part of the MUD lexicon. An apostrophe remains an ordinary character inside a double-quoted literal.

The default for `Char` is written `"\u{0}"` in a `Char` context. This does not change the Unicode domain, natural order or semantic distinction between `Char` and `Text`.

Syntax highlighting classifies double-quoted forms as text because choosing `Char` or `Text` requires type information. A historical internal character category may remain for theme compatibility, but the MUD tokeniser does not emit it for single quotes.

## Consequences

- MUD has one quote class for textual content.
- A single-scalar literal remains `Text` when no `Char` context exists.
- The parser produces one common textual form and static elaboration decides whether it can become a `Char` literal.
- Older code using single quotes is invalid and must be migrated to double quotes.

## Verification

1. `"a"`, `"ñ"`, `"\n"` and `"\u{1F642}"` in a `Char` context.
2. Inference of `Text` for `value := "a"`.
3. Rejection of `""`, `"ab"`, multiline text and interpolations in a `Char` context.
4. Resolution of `charValue == "x"` as a `Char` comparison.
5. Lexical rejection of single-quoted forms.
6. `Char` default `"\u{0}"`.
7. Highlighting with double quotes and no `character` highlighting for single quotes in MUD.
