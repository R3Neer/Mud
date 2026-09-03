---
id: D-050
title: "Comments, terminators, text and numeric separators"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-001"
affects:
  - "[[specification/06-lexicon]], [[specification/07-concrete-grammar]], formateador"
---
# ADR-050 — Comments, terminators, text and numeric separators

- Amended by: [[notes/decisions/ADR-069-char-literals-with-double-quotes|D-069]]

- Related to: [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]], [[notes/decisions/ADR-056-char-text-and-unicode-ordering|D-056]], [[notes/decisions/ADR-057-concrete-grammar-precedence-and-continuation|D-057]]
- Amended by: [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]]
- Partially closes: [[notes/questions/Q-001-g-grammar-and-line-breaks|Q-001]]
- Documents concerned: [[specification/06-lexicon]], [[specification/07-concrete-grammar]], formatter

## Context

These lexical rules are independent of the ontology and must be set in stone without the need to manually maintain a parallel catalogue of keywords. The delimiters for comment and the text follows a deliberate symmetry between standard and multiline fonts.

## Decision

### Comments

The MUD states:

1. Comment line from `#` up to the line break.
2. Comment line disconnected for a second `#` before the jump.
3. Comment multi-line, of which delimiter the opening and closing times are `###`.

```mud
soldiers = 1_000 # hasta fin de línea
soldiers = 1_000 # comentario # morale = 100
###
Comentario multilínea.
###
```

The `###` The opening tag must be the last non-blank element on the line. The content begins on the following line. The `###` The closing tag must appear on its own line, with no horizontal spacing. The opening and closing tags do not form part of the comment. The form `### comentario ###` is invalid.

Multi-line comments are not nested. The lexer recognises `###` rather than `#`. Within a textual element enclosed in double quotation marks, it should be written as `Text` or as `Char`, the delimiters for comment have no lexical meaning.

The content of a comment It does not generate tokens, instructions or terminators. After removing it, the remaining text must remain syntactically valid.

A comment A line that is explicitly closed does not cross a jump. A delimiter a multi-line entry without a matching line, a start containing text on the same line, or a closing line that is not isolated results in diagnostic.

### Textual forms

A literal 'ordinary' begins with `"` and prefers the type `Text`. It can be closed with another one `"` along the same line, or close implicitly upon reaching the break:

```mud
name = "Ada"
name = "Ada
```

Both forms produce the same result value. An explicit closing token is required when other tokens are to appear on that line.

A literal multi-line uses `"""`. The delimiter The opening tag must be the last non-blank character on its line; the content begins on the next line. The closing tag must appear on its own line, separated only by horizontal space.

```mud
description = """
    First line.
      Indented line.
    """
```

The haemorrhage from the delimiter The closing tag defines the margin that is removed from each non-empty line. A non-empty line with less indentation than the margin is a error. The first line following the start and the line immediately preceding the close are structural and do not form part of the value. The additional indentation is retained. The omissions and insertions of D-061 remain active.

A literal 'ordinary' in double quotation marks prefers `Text` and can be prepared as `Char` when the context requires it and contains exactly one value Unicode scaling in accordance with D-069. Single quotation marks do not delimit literals.

### Terminators

A statement ends with `;` or a line break.

The jump does not act as a terminator when it appears within a syntactically open construct. A prefix it is open when it is not yet able to form a unit syntactically complete, but can be supplemented with subsequent tokens. The grammar of D-057 provides an exhaustive list. It includes:

- A delimiter `(` o `[` still open.
- A headline that still needs participants, arguments or other content.
- A line ending with a comma or an operator that requires a subsequent operand.
- A heading or clause ending in a word that requires content, such as `for`, `given`, `if`, `then` o `:=`.
- The contents of a literal o comment multi-line.

The keys `{}` they do not remove the terminators within them: a block contains instructions or statements separated by jumps or `;`.

If the prefix prior to the jump, it can already form a unit A complete expression is terminated by a jump, even if the following line might begin another expression. Continuation never depends on indentation.

```mud
rule CanAttack for
    attacker: Army,
    defender: Army
{
    attacker.strength >
        defender.strength
}
```

D-057 and the consolidated grammar bring it to a close Q-001.

### Number separators

Scientific notation uses `e` o `E`: a mantis $m$ followed by an integer exponent $n$ denotes $m\times 10^n$. The optional character following `e` o `E` belongs to the exponent; the sign of the value It remains a foreign operator in its entirety.

`_` It can group figures for ease of reading and does not alter the value. The whole part of the mantissa, its fractional part and the exponent are grouped independently: use `_` Just because it’s included in one component doesn’t mean you have to use it in the others.

When a component contains `_`, the figures must be grouped in full. The whole part and the exponent are grouped from the right, with the first group consisting of one to three digits and the remaining groups of three. The fractional part is grouped from the point decimal places to the right, in groups of three, except for the last one, which may contain between one and three digits.

Therefore, `1_000.123456e1000`, `1000.123_456` y `3e1_000` are valid. `1_000000`, `1.123_456789` y `3e1_000000` are invalid because they fail to group figures from the same component. The prefix `r` is governed by D-034 and does not alter these rules.

## Consequences

- The lexer removes comments and outputs skip tokens; the parser determines which are terminators based on whether the prefix The syntactic structure is complete.
- The highlighter can implement the lexicon without knowing the model semantic.
- The list of reserved words is generated from the consolidated grammar.
- The catalogue distinguishes between reserved words and contextual words in accordance with D-035, D-054 y D-055. `using`, `with`, `test`, `otherwise` y `ordered` are reserved; `start`, `abstract`, `always`, `name` y `prefixes` are contextual in their grammatical functions.

## Verification

1. The three ways of comment.
2. Multi-line opening and closing on own lines.
3. Delimiters within strings.
4. Priority of `###` and rejection of nesting.
5. Run-on text with explicit and implicit endings.
6. Margins, structural lines and line breaks in multi-line text.
7. `Char` with exactly one scalar.
8. Harmless syntactic symbols within comments.
9. Termination by `;` and by jump.
10. Continued from delimiter, comma, operator and introductory word.
11. Termination when the prefix The previous one is now complete.
12. Independence from indentation outside multi-line blocks.
13. Literals without separators, with the integer, fractional and exponential parts grouped entirely independently.
14. Rejection of partial clusters, internal groups of a size other than three and `_` at the ends or duplicated.
15. Decimal equivalence of positive, negative and explicitly signed exponents in exact literals and `Rum`.
16. Nested text and code modes, curly brace escapes and the suppression of an implicit closure with open interpolation.
