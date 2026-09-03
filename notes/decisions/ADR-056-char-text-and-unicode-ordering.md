---
id: D-056
title: "`Char`, `Text` and Unicode ordering"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-001"
affects:
  - "[[specification/06-lexicon]], [[specification/07-concrete-grammar]], future chapters 10 and 15"
---
# ADR-056 — `Char`, `Text` and Unicode ordering

- Extended by: [[ADR-081-collection-filtering-take-and-indexing|D-081]]

- Amended by: [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]]
- Amended by: [[notes/decisions/ADR-069-char-literals-with-double-quotes|D-069]]
- Partially closes: [[notes/questions/Q-001-g-grammar-and-line-breaks|Q-001]]
- Affected documents: [[specification/06-lexicon]], [[specification/07-concrete-grammar]], future chapters 10 and 15

## Context

Modelling `Text` literally as `Char [* ordered]` would conflate two distinct concepts:

1. The position of characters in a text.
2. The canonical ordering of a collection.

If they were equivalent, ordinary text such as `"cba"` would have to be normalised or rejected because it was not ordered.

## Decision

### `Char`

`Char` is a non-numeric basic type. Each value denotes exactly one Unicode scalar value; isolated surrogate code points are not permitted.

Its literals use the ordinary double-quoted form and require a `Char` context:

```mud
"a"
"ñ"
"界"
"\n"
"\u{1F642}"
```

After escape sequences have been interpreted, a literal must contain exactly one Unicode scalar value. The `Char` form requires an explicit closing quote and does not permit interpolation; without a context requiring `Char`, even `"a"` has type `Text`.

ASCII is the subset of Unicode from `U+0000` to `U+007F`. It is not a separate type.

The default value of `Char` is the `U+0000` scalar, written `"\u{0}"` in a `Char` context. It is an ordinary `Char` value, neither absence nor a text terminator. MUD does not introduce the special escape `\0`; the general Unicode notation already expresses the value without relying on a C-specific convention.

### Ordering

The natural order of `Char` is the ascending order of its Unicode scalar value. Therefore, in a collection:

```mud
letters: Char [* ordered] = "abc"
```

`ordered` requires that canonical order. The following initialisation is invalid:

```mud
letters: Char [* ordered] = "cba"
```

`ordered by` is not permitted for `Char`: it cannot replace the natural Unicode order.

### `Text`

`Text` remains a distinct basic type. It denotes a finite sequence of `Char` values and preserves their written positional order:

```mud
word: Text = "cba"
```

This value remains `"cba"`. In particular:

$$
\mathsf{Text}
\not\equiv
\mathsf{Char}[\ast\ \mathsf{ordered}]
$$

`Text` may expose sequence operations such as indexing, membership, length and iteration without thereby becoming a canonically ordered collection. It does not permit collection modifiers or `ordered by`.

`take n from text` produces another `Text` containing its first `n` `Char` values, or the entire text if it contains fewer. It is deterministic because position is part of `Text`; it does not convert the result into `Char [* ordered]`.

The `|` operator concatenates `Text` values. The set operators `&`, `^` and `-` do not apply to `Text`. A nominal alias based on `Text` requires an explicit conversion to `Text` for concatenation and another conversion to the destination alias.

Under D-061, `Text` literals are also templates. Their literal fragments and interpolated values produce a single sequence of `Char`; this elaboration neither converts `Text` into a collection nor introduces general implicit conversions.

## Consequences

- The lexer provides a common textual form; static elaboration distinguishes `Char` from `Text`.
- The type system includes `Char` among the non-numeric basic types.
- Iteration over `Text` preserves position; enumeration of `Char [* ordered]` uses Unicode ordering.
- Materialisation cannot order text as an effect of its representation.
- Unicode ordering is defined by scalar values, not by language, collation, visible grapheme or cultural normalisation.

## Verification

1. Valid ASCII and non-ASCII literals.
2. Rejection of zero or multiple scalar values after interpreting escape sequences.
3. Rejection of isolated Unicode surrogates.
4. Confirmation that ASCII occupies `U+0000`–`U+007F`.
5. Preservation of `"cba"` as `Text`.
6. Rejection of `"cba"` as a value of `Char [* ordered]`.
7. Rejection of `ordered by` for `Char` and of collection modifiers on `Text`.
8. The default `"\u{0}"` for `Char`, and rejection of `"\0"` as an undeclared escape.
9. Positional preservation of literal and interpolated fragments within a template.
