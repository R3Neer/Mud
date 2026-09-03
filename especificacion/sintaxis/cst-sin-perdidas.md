---
title: Lossless CST
aliases:
  - Concrete syntax tree
  - Lossless CST
tags:
  - mud/especificacion
  - mud/sintaxis
status: proposed
normative: true
depends-on:
  - 03-notacion
  - 05-texto-fuente
  - 06-lexico
  - 07-gramatica-concreta
  - gramatica/mud-lexico.ebnf
  - gramatica/mud.ebnf
questions: []
decisions:
  - D-015
  - D-054
  - D-070
  - D-071
  - D-085
  - D-086
  - D-088
  - D-087
  - D-100
  - D-096
---

# Lossless CST

## State and purpose

This document defines the specific structure retained by a MUD file following lexical and syntactic analysis. The CST enables the original byte stream to be reconstructed, preserves comments and formatting, provides local diagnostics and supports editing tools without attributing any semantic meaning to the physical layout of the text.

The CST is **per file**. A project may contain several CSTs, but there is no single CST that physically spans multiple files.

## Layers and authority

Authority is distributed as follows:

- [[mud-lexico]] defines which sequences constitute lexical items.
- [[mud]] defines syntactic productions.
- [[06-lexico]] defines lexical algorithms and rules that do not fit within EBNF.
- [[07-gramatica-concreta]] defines precedence, associativity and contextual parsing constraints.
- `mud-syntax-kinds.yaml` maintains the mechanical inventory for the CST categories.
- This document defines the common model, text preservation and recovery.

A discrepancy between these files is a fault in the specification and must be detected by means of `validate_syntax_model.py`.

Among the specific categories is `ExpressionBlockSyntax`, which preserves the initial local declarations and final expression in order. The category does not itself determine that expression's contract: its owner decides whether it must be Boolean, temporal, aggregatable or sortable. In `for each`, selections and quantifiers, the `TERMINATOR` written between `:` and the beginning of the body remains in the CST as concrete separation and disappears when the AST is projected. The CST does not itself extend its scope to `otherwise`; that relation is determined when elaborating the owning construct.

## Terminology

> [!definition] Significant token
> A lexical element consumed by the concrete grammar: words, identifiers, literals, operators, delimiters, `TERMINATOR` and `EOF`.

> [!definition] Trivia
> Preserved source-text elements that do not function as grammatical terminals: horizontal whitespace and comments. Trivia retains exact formatting, including delimiters and line breaks within the text.

> [!definition] Full width
> The range from the beginning of an element's leading trivia to the end of its last token.

> [!definition] Syntactic span
> The range of significant tokens belonging to the element, excluding the first token's leading trivia.

> [!definition] Synthetic token
> A zero-width token introduced by a normative rule — such as an implicit `TEXT_END` — or by error recovery.

## Two perspectives on lexical analysis

Conceptually, the scanner produces a complete flow:

```text
trivia* token trivia* token ... trivia* EOF
```

The significant view filters out trivia and is the view consumed by the grammar:

```text
token token ... EOF
```

Comments are only deleted from the **significant view**. The recogniser does not treat them as terminals; the representation retains them as trivia.

## Abstract model

A conforming implementation may use green trees, red trees, arrays, indices or ordinary classes. It must be observationally equivalent to the following model:

```text
SyntaxTree
    source: SourceId
    root: SyntaxNode
    diagnostics: Diagnostic*

SyntaxElement
    = SyntaxNode
    | SyntaxToken

SyntaxNode
    kind: SyntaxKind
    children: SyntaxElement*
    span: SourceSpan
    fullSpan: SourceSpan

SyntaxToken
    kind: TokenKind
    text: bytes UTF-8
    leadingTrivia: SyntaxTrivia*
    span: SourceSpan
    fullSpan: SourceSpan
    origin: Written | ImplicitTextEnd | MissingForRecovery

SyntaxTrivia
    kind: TriviaKind
    text: bytes UTF-8
    span: SourceSpan
```

`SyntaxNode.children` preserves the physical order. The punctuation and keywords are actual children; they are not reconstructed on the basis of knowledge of the `kind`.

## Lossless property

Let `bytes(t)` be the left-to-right concatenation of:

1. The leading trivia of each token.
2. The text of the token when its origin is `Written`.
3. No bytes for synthetic tokens.

For every lexically accepted UTF-8 input:

```text
bytes(CST(source)) = sourceBytesWithoutConsumedBOM
```

The BOM is retained as file-level metadata because it can appear only before the first element. The physical form of line breaks (`LF`, `CRLF` or `CR`) remains in the bytes of the `TERMINATOR` token or the trivia that contains them.

## Trivia ownership

MUD uses a single, deterministic rule:

> [!rule] MUD-CST-001 — Owned by trivia
> All trivia situated between two significant tokens is classified as `leadingTrivia` of the token on the right. Trivia before the first token belongs to that token. Trivia following the last token belongs to `EOF`.

Example:

```mud
health # explanation # : Nat
```

It is represented conceptually as follows:

```text
IDENTIFIER("health")
COLON(leadingTrivia = [" ", "# explanation #", " "])
IDENTIFIER("Nat", leadingTrivia = [" "])
EOF
```

This rule prevents decisions from depending on the comment class. An implementation may provide a derived trailing-trivia view, but standard serialisation uses the preceding ownership rule.

## Types of trivia

The minimum catalogue is:

- `HorizontalWhitespaceTrivia`.
- `OpenLineCommentTrivia`.
- `ClosedLineCommentTrivia`.
- `MultilineCommentTrivia`.
- `SkippedTokensTrivia`, for recovery purposes only.

A multiline comment preserves its delimiters, indentation and internal line breaks in a single trivia element. Its line breaks do not produce `TERMINATOR`, in accordance with [[06-lexico]].

## `TERMINATOR`

`TERMINATOR` is a significant token because it participates in `required-separation`. Its text preserves the form originally written:

- `LF`.
- `CRLF`.
- `CR`.
- `;` when the grammar checker and the scanner classify it as a terminator.

Terminators ignored by `layout` remain present as tokens in the CST.

## Other significant tokens

The CST retains the fixed tokens `-->` and `~`, the operator word `iis`, and contextual words written in their usual positions. Longest match must prevent `-->` from being split into `--` and `>`, or into `-` and `->`. `has not` and `iis not` retain two tokens with their own trivia. There is no `ANCHOR_INTERPOLATION_START`; an expression `~anchor` inside `{...}` uses the same nodes and tokens as outside a template.

## `Text` literals

The tokens generated by the modal scanner are retained:

- `TEXT_START`.
- `TEXT_FRAGMENT`.
- `INTERPOLATION_START`.
- `INTERPOLATION_END`.
- `TEXT_END`.

An implicit closure following a newline or end of file produces a zero-width synthetic `TEXT_END` with origin `ImplicitTextEnd`. The CST therefore preserves the concrete distinction between:

```mud
"Ada"
```

and the implicit closed form:

```mud
"Ada
```

The Surface AST normalises both to the same permanent value.

## CST categories

Every production from `mud.ebnf` belongs to a category `PascalCaseSyntax` listed in `mud-syntax-kinds.yaml`. For example:

```text
thing-declaration        → ThingDeclarationSyntax
thing-body               → ThingBodySyntax
thing-body-declaration   → ThingBodyDeclarationSyntax
thing-initializer         → ThingInitializerSyntax
metadata-assignment       → MetadataAssignmentSyntax
stored-field-declaration → StoredFieldDeclarationSyntax
postfix-expression       → PostfixExpressionSyntax
```

Auxiliary productions also have a category, although an optimised implementation may represent them using typed views on a generic node.

The catalogue does not require a physical class for every production. It does, however, require that:

- The grouping must be observable.
- The children can go through them in order.
- The specific tokens must be recoverable.
- The category declared must be identifiable.

## Special recovery nodes

In addition to grammatical constructions, there are also:

### `ErrorSyntax`

It groups a region for which the parser could not select a valid production, without discarding its tokens.

### `SkippedTokensSyntax`

It retains unexpected tokens skipped up to a synchronisation point.

An implementation may encode `SkippedTokensSyntax` such as `SkippedTokensTrivia` when it doesn’t change:

- The exact reconstruction.
- The order.
- Spans.
- The ability to issue the diagnostic in the correct position.

## Missing tokens

> [!rule] MUD-CST-002 — Token absent
> When recovery requires an unwritten token, the CST shall contain a token of the expected type, with empty text, a zero-width span and origin `MissingForRecovery`.

Example:

```mud
thing Person {
    label Text
}
```

can be represented by a missing `COLON` between `label` and `Text`, with an associated diagnostic.

A token 'absent' is never serialised as if the user had written it.

## Synchronisation points

The parser can synchronise to:

- `TERMINATOR` at the level of statements and judgements.
- `,` within lists.
- `)`, `]` or `}` for the relevant delimited construction.
- The unambiguous beginning of another top-level declaration.
- `EOF`.

The specific choice may vary provided it preserves the same error region and does not produce a valid AST for an invalid construct.

## CST for invalid files

The construction of a CST does not imply validity. It must be possible to obtain a CST for inputs with recoverable syntactic errors.

The phase sequence is:

```text
bytes UTF-8
→ full token stream
→ lossless CST
→ contextual syntactic validation
→ normalised Surface AST
```

A file may have a CST without producing a complete Surface AST.

## Contextual syntactic validation

The validation step between the CST and AST checks conditions that should not be encoded by expanding the EBNF, including:

- Duplicate collection modifiers.
- Two incompatible `ordered` criteria.
- Duplicate metadata declarations within the same owner, including units.
- Missing required properties.
- Mixing positional arguments after a named argument.
- Combinations prohibited by the concrete-syntax prose.
- Capitalisation required by category when it is still classified as a contextual syntactic rule.

Validation of existing names, types, domains and effects belongs to later stages.

## Spans

The offsets of `SourceSpan` are:

- Zero-based.
- Measured in UTF-8 bytes.
- Exclusive end.

Lines and columns also start at zero. A column counts Unicode scalar values from the logical start of the line. An LSP interface converts UTF-16 units at its boundary; that conversion does not alter the normative model.

For a token written:

```text
span.start.byteOffset < span.end.byteOffset
```

except for permitted empty tokens. For a token summary:

```text
span.start = span.end
```

`fullSpan` begins at the start of the first leading trivia and ends at the end of the final token. A node's `span` runs from its first significant token to its last. If all its tokens are synthetic, it is anchored at the recovery point.

## Order and files

CST always retains the source order:

- `using`.
- Statements.
- Predecessors.
- Fields.
- Members.
- Arguments.
- Effects.
- Statements.

The fact that the order of certain lists has no semantic significance does not justify ordering them in the CST.

## Future documentation

MUD 1.0 does not define structured documentation comments. All current comments are ordinary trivia. A future extension may:

- Classify a form of comment as supporting documentation.
- Create a separate document tree.
- Attach it to a syntactic owner.
- Resolve short references to anchors.

That extension will not convert ordinary comments into executable AST statements.

## Correspondence with the AST

The CST does not:

- Desugar.
- Name resolution.
- Inference of types.
- Classify callable invocations, external capabilities or consequence composition semantically.
- Interpreting a tuple as multiple receivers.
- Calculation of default values.
- Canonically order files.

The normative transformation is defined in [[cst-a-ast-superficial]].

## Conformance

A compliant frontend must meet the following requirements:

1. Exact reconstruction of the file, except for the separate BOM as metadata.
2. An inventory of every reachable grammar production.
3. Preservation of trivia and unexpected tokens.
4. Consistent spans and unique endpoints.
5. The distinction between written tokens and synthetic tokens.
6. No resolution or typing decisions in the CST.
7. Output compatible with the Surface AST normalisations.
