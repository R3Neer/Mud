---
title: CST sin pérdidas
aliases:
  - Tree of concrete syntax
  - Lossless CST
tags:
  - mud/especificacion
  - mud/sintaxis
status: propuesta
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

# CST sin pérdidas

## State and purpose

This document defines the specific structure retained by a MUD file following lexical and syntactic analysis. The CST enables the original byte stream to be reconstructed, preserves comments and formatting, provides local diagnostics and supports editing tools without attributing any semantic meaning to the physical layout of the text.

The CST is **by file**. A project may contain several CSTs, but there is no single CST that physically spans multiple files.

## Branches and authority

The authority It is distributed as follows:

- [[mud-lexico]] defines which sequences constitute lexical items.
- [[mud]] defines syntactic productions.
- [[06-lexico]] defines the modal algorithms and rules that do not fit within EBNF.
- [[07-gramatica-concreta]] define precedence, associativity and contextual constraints on parsing.
- `mud-syntax-kinds.yaml` maintains the mechanical inventory for the CST categories.
- This document defines the model common, text preservation and retrieval.

A discrepancy between these files is a fault in the specification and must be detected by means of `validate_syntax_model.py`.

Among the specific categories listed are `ExpressionBlockSyntax`, which keeps the initial local declarations and the final expression in order. The category does not, on its own, determine the contract of that expression: the owner decide whether it should be Boolean, temporal, aggregatable or sortable. In `for each`, selection and quantifiers, the `TERMINATOR` written between `:` and the beginning of the body remain in the CST as a concrete separation and disappear when the AST is projected. The CST does not, of its own accord, extend its scope up to `otherwise`; that relation It is determined when planning and finalising the owner-occupied property.

## Terminology

> [!definition] Token significant
> A lexical element that consumes the concrete grammar: words, identifiers, literals, operators, delimiters, `TERMINATOR` y `EOF`.

> [!definition] Trivia
> Source text preserved elements that do not function as grammatical terminals: horizontal space and comments. The trivia retains the exact formatting, including delimiters and line breaks within the text.

> [!definition] Full width
> Time elapsed since the start of the trivia from the start of an element to the end of its last token or son.

> [!definition] Span syntactic
> The range of significant tokens specific to the element, excluding the trivia initial, belonging to the first token.

> [!definition] Token synthetic
> Token zero width introduced by a regulatory provision — such as a `TEXT_END` implicit— or through error recovery.

## Two perspectives on lexical analysis

Conceptually, the scanner produces a complete flow:

```text
trivia* token trivia* token ... trivia* EOF
```

The meaningful view filters the trivia and it is this that consumes grammar:

```text
token token ... EOF
```

Comments are only deleted from the **significant view**. The recogniser does not treat them as terminals; the representation retains them as trivia.

## Model abstract

One conforming implementation You can use green trees, red trees, arrays, indices or ordinary classes. It must be observationally equivalent to the model next:

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

## Zero-loss property

Be `bytes(t)` the concatenation, read from left to right, of:

1. The trivia first letter of each token.
2. The text of the token when its origin is `Written`.
3. No bytes for synthetic tokens.

For every lexically accepted UTF-8 input:

```text
bytes(CST(source)) = sourceBytesWithoutConsumedBOM
```

The BOM is retained as metadata file-level because it can only appear before the first element. The physical form of the jumps (`LF`, `CRLF` o `CR`) remains in the token bytes `TERMINATOR` or the trivia which contains them.

## Allocation of trivia

MUD uses a single, deterministic rule:

> [!rule] MUD-CST-001 — Owned by trivia
> All trivia a value situated between two significant tokens is classified as `leadingTrivia` to the token on the right. The trivia prior to the first token belongs to that token. The trivia following the last one token belongs to `EOF`.

Example:

```mud
health # explicación # : Nat
```

It is represented conceptually as follows:

```text
IDENTIFIER("health")
COLON(leadingTrivia = [" ", "# explicación #", " "])
IDENTIFIER("Nat", leadingTrivia = [" "])
EOF
```

This rule prevents decisions that depend on the class of comment. An implementation may provide a derived view of trivia finally, but standard serialisation uses the previous property.

## Types of trivia

The minimum catalogue is:

- `HorizontalWhitespaceTrivia`.
- `OpenLineCommentTrivia`.
- `ClosedLineCommentTrivia`.
- `MultilineCommentTrivia`.
- `SkippedTokensTrivia`, for recovery purposes only.

A comment multiline preserves its delimiters, indentation and internal line breaks within a single element of trivia. His jumps do not produce `TERMINATOR`, in accordance with [[06-lexico]].

## `TERMINATOR`

`TERMINATOR` is a token significant because it plays a part in `required-separation`. The text retains the handwritten form in which it was originally written:

- `LF`.
- `CRLF`.
- `CR`.
- `;` when the grammar checker and the scanner classify it as a terminator.

Terminators ignored by `layout` they remain present as tokens within the CST.

## Other significant tokens

The CST retains the fixed tokens `-->` y `~`, the operator word `iis` and the contextual words written in their usual positions. The longest match must prevent `-->` is divided into `--` y `>` or in `-` y `->`. `has not` e `iis not` they keep two tokens with trivia its own. There is no such thing as `ANCHOR_INTERPOLATION_START`; an expression `~anchor` inside `{...}` It uses the same nodes and tokens as when not using a template.

## Literal expressions `Text`

The tokens generated by the modal scanner are retained:

- `TEXT_START`.
- `TEXT_FRAGMENT`.
- `INTERPOLATION_START`.
- `INTERPOLATION_END`.
- `TEXT_END`.

An implicit closure following a jump or the end of a file results in a `TEXT_END` zero-width synthetic with origin `ImplicitTextEnd`. The CST thus maintains the specific distinction between:

```mud
"Ada"
```

and the implicit closed form:

```mud
"Ada
```

The Surface AST normalises both at the same time value permanent staff.

## CST Categories

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

The catalogue does not require a physical class to be created for production. It does, however, require that:

- The grouping must be observable.
- The children can go through them in order.
- The specific tokens must be recoverable.
- The category declared must be identifiable.

## Special recovery nodes

In addition to grammatical constructions, there are also:

### `ErrorSyntax`

It groups together a region for which the parser was unable to select one production valid, without discarding its tokens.

### `SkippedTokensSyntax`

Retains unexpected tokens that were skipped up to a point synchronisation.

An implementation may encode `SkippedTokensSyntax` such as `SkippedTokensTrivia` when it doesn’t change:

- The exact reconstruction.
- The order.
- Spans.
- The ability to issue the diagnostic in the correct position.

## Missing tokens

> [!rule] MUD-CST-002 — Token absent
> When recovery involves a token as an unwritten requirement, the CST shall contain a token from the type as expected, empty text, span zero width and origin `MissingForRecovery`.

Example:

```mud
thing Person {
    label Text
}
```

can be represented by a `COLON` absent from `label` y `Text` and a diagnostic associate.

A token 'absent' is never serialised as if the user had written it.

## Synchronisation points

The parser can synchronise to:

- `TERMINATOR` at the level of statements and judgements.
- `,` within lists.
- `)`, `]` o `}` for the relevant defined construction.
- The unmistakable beginning of another declaration top-class.
- `EOF`.

The specific choice may vary depending on whether you keep the same region of error and does not produce a valid AST for an invalid construction.

## CST for invalid files

The construction of a CST does not imply validity. It must be possible to obtain a CST for inputs with recoverable syntactic errors.

The phase sequence is:

```text
bytes UTF-8
→ scanner completo
→ CST sin pérdidas
→ validación sintáctica contextual
→ AST superficial normalizado
```

A file may contain CST and not produce a Surface AST complete.

## Validation contextual syntax

The validation Located after the CST and before the AST, it checks conditions that are not worth encoding as an expansion EBNF, including:

- Modifiers of collection duplicates.
- Two criteria `ordered` incompatible.
- Duplicate metadata declarations within the same owner, including the units.
- Missing required properties.
- Mixing positional arguments after a argument appointed.
- Combinations that the prose of concrete syntax prohibit.
- Capitalisation required by category when it is still classified as a contextual syntactic rule.

The validation The definition of existing names, types, domains and effects is dealt with in later stages.

## Spans

The offsets of `SourceSpan` are:

- Zero-based.
- Measured in UTF-8 bytes.
- Exclusive end piece.

Lines and columns also start at zero. The column counts Unicode scalar values from the logical start of the line. An LSP interface converts UTF-16 units at its boundary; that conversion does not alter the model regulatory.

For a token written:

```text
span.start.byteOffset < span.end.byteOffset
```

except for permitted empty tokens. For a token summary:

```text
span.start = span.end
```

`fullSpan` starts on the first trivia starts at the beginning and ends at the end of the token. The `span` from a node runs from the first token significant right up to the very last one. If all its tokens are synthetic, it anchor in the point recovery.

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

## Future documentary commentary

MUD 1.0 does not define structured documentation comments. All current comments are trivia standard. A future extension may:

- Classify a form of comment as supporting documentation.
- Create a separate document tree.
- Attach it to a syntactic owner.
- Resolve short references to anchors.

That extension will not convert ordinary comments into executable AST statements.

## Correspondence with the AST

The CST does not:

- Sugar-free.
- Resolución de nombres.
- Inference of types.
- Ranking semantics Callable invocations, external capabilities or the composition of consequences.
- Interpreting a tuple as multiple receivers.
- Calculation of default values.
- Canonical organisation of archives.

Regulatory reform is underway [[cst-a-ast-superficial]].

## Conformidad

A compliant frontend must meet the following requirements:

1. Exact reconstruction of the file, except for the separate BOM as metadata.
2. A list of all available productions.
3. Conservation of trivia and unexpected tokens.
4. Consistent spans and unique endpoints.
5. The distinction between written tokens and synthetic tokens.
6. Lack of decisions on resolution or typed into the CST.
7. Result compliant with the standards set out in the Surface AST.
