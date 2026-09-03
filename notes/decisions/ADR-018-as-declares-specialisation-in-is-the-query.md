---
id: D-018
title: "`as` declares specialisation in `is` the query"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "future `07-concrete-grammar.md`, future `08-abstract-syntax.md`, future `11-things.md`"
---
# ADR-018 — `as` declares specialisation in `is` the query

- Amended by: [[notes/decisions/ADR-084-alias-specialisation-inherited-members-and-derived-views|D-084]]
- Updated: 28 July 2026
- Amended by: [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|D-068]]
- As further amended by: [[notes/decisions/ADR-073-explicit-but-redundant-as-thing|D-073]]
- Documents affected: future `07-concrete-grammar.md`, future `08-abstract-syntax.md`, future `11-things.md`

## Context

The declaration area of specialisation and its query Different formats are needed to ensure that a header is not confused with an expression. D-025 fixed `as` for the declaration and preserves `is` as an operator.

Although the parser could distinguish between a header and an expression, the two operations have different meanings: one adds direct edges and the other query one relation derived.

## Decision

All declaration specialisation uses `as`:

```mud
thing A {}

abstract thing B as A {}

thing D as A, B, C {}

thing E as D {}
```

`is` is reserved for expressions:

```mud
D is A
E is B
```

The conceptual forms are:

```text
[abstract] thing name [as ancestor-list] body
```

The list following `as` is finite and its position does not indicate priority. A declaration without `as` It retains zero declared predecessors and semantically receives the root incorporated `Thing`. D-073 supports `as Thing` It is explicitly identified as non-blocking redundancy and it is suggested that it be removed.

## Correspondence semantics

A header `thing D as A, B` contributes:

$$
(\mathsf D,\mathsf A),\quad
(\mathsf D,\mathsf B)
\in R_{\mathrm{dir}}.
$$

`D is A` consulta:

$$
(\mathsf D,\mathsf A)
\in
R_{\mathrm{dir}}^*.
$$

Therefore:

- `as` provides direct links;
- `is` query its reflective and transitive conclusion.

## Consequences

- The lexer reserves `as` and `is`; `abstract` is contextual before `thing`, in accordance with D-054; `construct` is not reserved, and `from` does not introduce specialisation.
- The AST uses a list of predecessors in `ThingDecl`; `CreateReference` It contains neither antecedents nor a body.
- The absence of predecessors in `ThingDecl` is preserved in the AST; the edge towards `Thing` is added during the elaboration semantics.
- `IsExpression` is the node associated with the query `is`.
- The medical records refer to ‘relatives reported to have `as`».
- Static headers and those from `create` are parallel.

The token `from` may still exist in other independent productions, such as `remove x from collection`; that does not make it a specialisation clause.

## Verification

1. `thing` root without `as`, with no declared predecessors and `is Thing` true.
2. Abstract and concrete statements with one or more antecedents.
3. Activation by means of `create Nombre` without altering the previously stated predecessors.
4. Rejection of `is` as a header clause.
5. Acceptance of `is` as an expression.
6. Correspondence between edges `as` and results from `is`.
7. Diagnostic non-blocking and suggested correction for `as Thing` explicit.

## Extension by D-084

`as` e `is` also apply to aliases. In a nominal alias or structural, `as` declares a direct specialisation between types of value; `is` query the nominal closure whilst retaining the type specifically regarding the value. Multiple specialisations do not establish textual priority.

