---
title: Lexical structure
aliases:
  - MUD Glossary
tags:
  - mud/especificacion
  - mud/lexico
status: propuesta
normative: true
depends-on:
  - "[[05-texto-fuente]]"
questions: []
decisions:
  - D-034
  - D-035
  - D-050
  - D-056
  - D-057
  - D-061
  - D-062
  - D-067
  - D-068
  - D-069
  - D-076
  - D-070
  - D-080
  - D-081
  - D-082
  - D-085
  - D-086
  - D-087
  - D-089
  - D-100
  - D-101
  - D-096
---

# 06. Lexical structure

## State and purpose

This chapter defines the base scanner and the contextual classification for font shapes. The base scanner transforms Unicode into tokens without consulting model; `POINT_LITERAL` and `UNIT_FORM` are added only in a subsequent contextual view. The base lexical grammar is in [[gramatica/mud-lexico.ebnf]]. The syntax that processes the significant views belongs to [[07-gramatica-concreta]].

## Unicode scalar values

> [!definition] Value Unicode scalar
>  is a point Unicode code point, except for the range reserved for surrogates `U+D800`–`U+DFFF`.

> [!rule] MUD-LEX-010 — Valid Unicode
> The source text must be decoded as valid UTF-8. An isolated surrogate or a malformed UTF-8 sequence is a lexical error.

ASCII is the Unicode subset `U+0000`–`U+007F`.

## Identifiers

The lexical form of an identifier is:

```ebnf
identifier ::= ascii-letter , { ascii-letter | digit } ;
```

> [!rule] MUD-LEX-011 — ASCII identifiers
> Identifiers may only contain ASCII letters and numbers; they must begin with a letter and may not contain `_`.

They are case-sensitive. `Kingdom`, `kingdom` and `KINGDOM` are three different notations.

The verifiable convention by category is:

| Category | Form |
| --- | --- |
| Segment of path of MUD | `lowerCamel` |
| Declaration nominal | `PascalCase` |
| Member of `family` | `PascalCase` |
| Unit, field, role, `given`, component or variable | `lowerCamel` |

A name that does not follow the capitalisation rules is a static error, not an alternative tokenisation.

## Reserved and contextual words

Reserved words cannot be used as identifiers. The standard catalogue is:

```text
using
thing as alias family magnitude
rule action subaction look message test
for on given when changes if then after with otherwise
mut unique ordered
create destroy add to remove from each by take
eventually through allowed old
is iis in has
not and or xor
exists forall count min max
true false empty all _
Text Char Bool Thing Any Nat Int Num Rum Money
Name MudPath Anchor MudFile Prefix Rand
```

The terminals `&`, `|`, `^`, `--`, `->`, `-->`, `~`, `=>` and `<=>` are not words. `-->` is recognised by the longest match before `--` and `->`. `|=`, `&=`, `^=` and `--=` are also indivisible tokens. `!` on its own does not belong to the lexicon; `!=` remains an indivisible token of inequality and is not interpreted as the composition of negation and assignment.

The scanner applies the longest match: `a--b` contains the operator `--`, whilst `a - -b` contains separate subtraction and negation. The parenthesised form `a - (-b)` is equivalent to the latter.

They are contextual:

- `abstract` in front of `thing`.
- `always` in front of `rule`.
- `start` as part of `start with`.
- `value` within the selectors and results of functional branches `-->`.
- `type` in the reflexive positions and in those of type where this is permitted.
- `name`, `path`, `anchor`, `file`, `plural`, `abbreviation`, `prefixes` and `format` after `~` in the permitted positions.
- `root`, `unit`, `point`, `over` and `cycle` in their own productions.
- `Interval` immediately following a reference to type within `interval-type`.

`for`, `on` and `given` remain hard reserved words, but `metadata-name` explicitly permits them after `~` for the reflexive properties `~for`, `~on` and `~given`. This syntactic exception does not make them `IDENTIFIER` nor does it allow them to be used as ordinary names.

`things` and `rules` are not part of the vocabulary current of `start with`.

Outside of these positions, they can be tokenised as `IDENTIFIER`. The classifier cannot use this flexibility to accept a hard reserved word as a name.

`ordered` is a hard reserved word both before `family` and within a specification of collection. It cannot be used as an identifier in any other context.

`all` is an reserved word that serves both as a contextual literal without an operand, whose enumerable domain is derived from the context, and as prefix `all D` to explicitly instantiate an enumerable domain. Its reserved nature makes it possible to distinguish between these two forms of an ordinary declaration even before typing.

`iis` is a reserved operator word. `has not` and `iis not` retain two word tokens with their own trivia; the parser groups each pair in the corresponding comparison. `in` does not form a Boolean membership: its uses are domain, filtering, binding or conversion, depending on the context.

## Adjacency of units

The base scanner does not need to know about units in order to recognise the boundary following a number. When the quantity grammar allows an unit, the contextual classifier query identifies source text from that offset and can cover an enabled form without requiring an intermediate trivia. Consequently, `3m`, `90km/h` and `r0.1m` receive the same classification semantics as their spaced forms. Outside an unit position, `R2D2`, `ronto` and any similar sequence retain only their base tokenisation.

The canonical form inserts a space between the number and the first unit. This standardisation is carried out by the formatter, not by the base scanner or the highlighter.

## Contextual classification in font forms

> [!rule] MUD-LEX-012 — Independence of the base scanner
> The base scanner relies solely on Unicode text and the fixed MUD lexicon. No query declarations, expected types, `~format` or unit catalogues. All its tokens and trivia retain exact offsets in the source text.

> [!rule] MUD-LEX-013 — Contextual alternative for span
> `POINT_LITERAL` and `UNIT_FORM` are contextual classifications of spans in the original text. The classifier may cover one or more units of the base tokenisation, but must retain the exact source interval and must not invent characters when reconstructing tokens.

> [!rule] MUD-LEX-014 — Context-driven priority
> A contextual alternative exists only when its semantic context satisfies the contract defined in this chapter. When a single type of the expected point exactly matches its `~format`, `POINT_LITERAL` takes precedence over an ordinary interpretation of the same span. Without sufficient context, that alternative does not exist.

> [!rule] MUD-LEX-015 — Determinism of unit
> `UNIT_FORM` uses the already resolved semantic catalogue. The expected type restricts candidates; without it, the form must be globally unambiguous. Among compatible matches of different lengths, the longest complete form takes precedence; two distinct candidates for the same span are ambiguous.

> [!rule] MUD-LEX-016 — Admissibility with customisable font styles
> The declared identifier retains the standard identifier grammar of unit. Non-empty values of `~name`, `~plural` and `~abbreviation` share a single criterion when used as `UNIT_FORM`: they may contain U+0020 spaces and punctuation, but must contain at least one alphabetic character and must not exactly match a MUD keyword. An value that does not comply with this contract may still be presentation, but is not included in the catalogue of source forms.

> [!rule] MUD-LEX-017 — Intra-magnitude uniqueness following prefixes
> For each magnitude, the set of source forms of its units is restricted to all permitted prefix combinations before uniqueness is checked. Two distinct units cannot generate the same complete form, either directly or via prefixing. A collision is a static error of the declaration of the magnitude and is not resolved by declaration order or by usage context.

The specific architecture may use the token lattice, localised re-tokenisation or deferred parsing. These strategies are not observable provided that they reproduce the above rules and the CST round-trip.

## Comments

### Comment up to the jump

```mud
# Todo lo restante de la línea es comentario
```

### Comment – line closed

```mud
value = 1 # explicación # + 2
```

The second `#` resumes tokenisation from the same line. This form never crosses a line break.

### Comment multi-line

```mud
###
El contenido puede ocupar varias líneas.
No se anida.
###
```

> [!rule] MUD-LEX-020 — Opening of comment multi-line
> The opening `###` must be the last non-blank character on the line.

> [!rule] MUD-LEX-021 — Multi-line closure of comment
> The closing `###` must be the only non-blank content on that line.

> [!rule] MUD-LEX-022 — No nesting
> The first valid closing tag ends at comment. An inner `###` does not open another level.

The following form is invalid:

```mud
### comentario ###
```

Comments do not emit tokens that are significant for the grammar, but are preserved with their exact text as trivia in the complete lexical stream and in the Lossless CST. A complete multi-line comment does not produce any significant tokens `NEWLINE`; its internal line breaks remain within the trivia of the comment.

## Full flow, significant flow and trivia

The scanner offers two synchronised views:

```text
flujo completo      = trivia y tokens significativos en orden fuente
flujo significativo = tokens que consume mud.ebnf
```

CST is built using the complete flow. The grammar consumes the meaningful view.

The minimum trivia is:

- Horizontal space.
- Comment open-line.
- Comment out of production.
- Comment multi-line.

Every trivia belongs to the next significant token. `EOF` contains the final trivia. This convention is mandatory for lossless serialisation, although an API may expose views derived from the final trivia.

## Synthetic tokens

An implicitly closed `TEXT_END` is emitted as a synthetic token of zero width and origin `ImplicitTextEnd`. Parser recovery may introduce expected zero-width tokens with origin `MissingForRecovery`; these do not convert an invalid construct into a well-formed AST.

## `Char`

`Char` shares the ordinary literals enclosed in double quotation marks with `Text`:

```mud
letter: Char = "a"
letterEnye: Char = "ñ"
newline: Char = "\n"
face: Char = "\u{1F642}"
```

> [!rule] MUD-LEX-025 — A single scalar
> An ordinary literal may be rendered as `Char` when the context requires it and, after interpreting escape sequences, contains exactly one Unicode scalar value. The explicit closing quote is mandatory and does not allow for interpolations. Without context `Char`, the same notation has type `Text`.

The multi-line format is always `Text`. Single quotation marks do not delimit any MUD literal entries.

Its natural order is the ascending value sequence. It is neither a linguistic collation nor an order based on graphemes.

## `Text`

### Ordinary form

An literal begins with `"`. It can be explicitly closed on the same line:

```mud
"Ada"
```

or be implicitly closed before the jump:

```mud
"Ada
```

Both denote the same `Text`. If the content is followed by an operator, delimiter or comment, the closing quotation mark is mandatory:

```mud
greeting = "Hello" | ", world"
name = "Ada" # comentario
```

Without the first closing quotation mark, `| ", world"` would be included. Without the second, `# comentario` would also be included.

###  Multi-line form

```mud
description = """
    First line.
      Second line with two extra spaces.
    """
```

> [!rule] MUD-LEX-030 — Multi-line opening
> `"""` must be the last non-blank character on that line. The value begins on the next line.

> [!rule] MUD-LEX-031 — Multi-line lock
> The final `"""` must be the only non-blank character on that line.

> [!rule] MUD-LEX-032 — Margin
> The horizontal indentation before the closing tag defines the margin. Exactly that prefix is removed from each non-empty line. A non-empty line with a smaller margin is invalid.

> [!rule] MUD-LEX-033 — Structural jumps
> The jump following the start and the one immediately preceding the end are not part of value. The others are.

> [!rule] MUD-LEX-034 — Contents
> A single quotation mark does not close the multi-line format. Only `"""` on a valid closing line does so.

`Text` retains the position of its characters. It is not the same as `Char [* ordered]`.

### Templates and interpolation

Everything in `Text` is a template. `{...}` contains an ordinary MUD expression, which can use postfix operators `~` such as `~anchor`. `anchor{...}` does not exist. Interpolated code braces are balanced and `\{`/`\}` writes literal braces. The scanner delivery `TEXT_START`, `TEXT_FRAGMENT`, `INTERPOLATION_START`, `INTERPOLATION_END` and `TEXT_END`.

## Exhausts

The minimum forms are:

| Escape | Value |
| --- | --- |
| `\\` | backslash |
| `\"` | double quotation mark |
| `\'` | single quotation mark |
| `\n` | jump `LF` |
| `\r` | return `CR` |
| `\t` | tab |
| `\u{H...}` | a scalar written using one or more hexadecimal digits |
| `\{` | opening key literal in `Text` |
| `\}` | locking key literal in `Text` |

> [!rule] MUD-LEX-035 — Unicode escape sequence
> The value of `\u{...}` must lie between `U+0000` and `U+10FFFF` and cannot belong to the substitute interval.

Key escapes form part of standard textual syntax. An literal which, after processing, contains exactly one key can be rendered as `Char` in the relevant context.

## Numbers

Signs are external operators. For example:

```mud
-10
-r0.5
```

Neither `r-10` nor a character embedded in token is valid.

Exact rational numbers may have a decimal part and an exponent:

```mud
10
0.25
.5
3e6
1e-6
```

Pure `Rum` literals use `r`:

```mud
r10
r0.25
r.5
r1e-6
```

> [!rule] MUD-LEX-040 — Decimal exponent
> If a mantissa $m$ carries an integer exponent $n$ introduced by `e` or `E`, then the literal denotes $m\times 10^n$. The optional sign immediately following the introducer belongs to the exponent; signs applied to the complete value remain external operators.

For example, `3e6` denotes `3_000_000` and `3e-6` denotes `0.000_003`.

The whole part of the mantisa, its fractional part and the exponent are three independent components for the purposes of grouping.

> [!rule] MUD-LEX-041 — Complete numerical grouping
> Each component may be written without `_` or grouped using `_`. If a component contains `_`, all its digits must be grouped within that component. The presence of `_` in one component does not require the others to be grouped.
>
> The integer part and the exponent are grouped from the right: the first group contains between one and three digits, and all subsequent groups contain exactly three. The fractional part is grouped from the point decimal point to the right: all groups except the last one contain exactly three digits, and the last one contains between one and three.

The following are valid:

```mud
1_000
r1_000.25
1_000.123456e1000
1000.123_456
3e1_000
```

The following are invalid: `_1`, `1_`, `1__000`, `1_.0`, `1_000000`, `1.123_456789` and `3e1_000000`.

## Units

unit forms may contain Unicode and are not general identifiers. The base scanner retains its standard textual tokenisation; only the context-sensitive classifier may superimpose `UNIT_FORM` at a position where the quantity syntax permits an unit.

> [!warning]
> The catalogue of prefixes and permitted forms belongs to the model catalogue of units. `UNIT_FORM` retains the found spelling and checks it against the already resolved semantic catalogue, without introducing a circular dependency in the base scanner.

`Prefix` is an embedded type. The SI names `quecto`…`quetta` remain ordinary identifiers: in an expression such as `~prefixes = [kilo, milli]`, they are resolved as built-in values of `Prefix`; they do not become reserved words.

## Forms of quantities in point

An magnitude `point over` can enable contextual writes via its metadata `~format`, for example `12:30:00`. The contextual classifier represents a valid match as `POINT_LITERAL`; the base scanner retains its standard tokenisation.

> [!rule]
> `POINT_LITERAL` is interpreted against the single type of magnitude of point required by the context. If `~format` is declared, the text must match its canonical representation exactly and the format must be statically invertible. Unrepresented sub-precision takes the value zero value.

An magnitude of point without `~format` uses an ordinary quantity with a compatible unit as its full coordinate. In both cases, the reconstructed coordinate must belong to the declared domain. Cyclic domains do not normalise out-of-range literals: an literal equivalent to `26 hours` is invalid for `[0..24 hours) cycle`.

This chapter only defines the lexical recognition of these forms; their interpretation is handled by model for magnitudes of point.

## Lexical spans

Every token and trivia contains `SourceSpan`. The text of a written token occupies exactly its byte range. A synthetic token has the same start and end. The `fullSpan` of an token begins at its first initial trivia.

Escape decoding or the normalisation of the `Text` range does not alter the spans of its specific tokens; the decoded value belongs to the AST.

## Scanner priority

In a single position, the aim is to:

1. Multi-line delimiters.
2. Three-character operators.
3. Two-character operators.
4. Literals `Rum`, numbers and identifiers.
5. Single-character operators.

The longest valid match within the same category is selected. Comments and horizontal spaces are excluded from the meaningful stream, but are retained as trivia in the complete stream; `NEWLINE` is retained as token in the meaningful stream to determine termination.

Within a template, `\u{...}` is applied first, followed by the other escape sequences, then `{` and, finally, the longest possible fragment literal. Within an interpolation, the standard priority applies once again. The sequence `anchor{` does not receive any special lexical treatment.

