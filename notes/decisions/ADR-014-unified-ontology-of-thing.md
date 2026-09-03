---
id: D-014
title: "Unified ontology of `thing`"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-041"
affects:
  - "[[specification/04-mathematical-model]], futuro `11-things.md`"
---
# ADR-014 — Unified ontology of `thing`

- Updated: 28 July 2026 to use the terminology from D-025
- Amended by: [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|D-068]]
- Questions: [[notes/questions/Q-041-o-thing-ontology|Q-041]]
- Documents concerned: [[specification/04-mathematical-model]], future `11-things.md`

## Context

Talking about ‘runtime instances’ may suggest a distinction between classes and objects. That distinction does not correspond to the model MUD’s conceptual model: a formalisation based on a function that assigns a class to each object would introduce two domains that the language does not possess.

## Decisión

The MUD has a single domain conceptual aspect of `thing`.

1. One `thing` It has no instances.
2. All `thing` has identity semantics.
3. All `thing` 'concrete' also denotes a concrete thing with state its own and can serve as ancestor from others.
4. One `thing` 'abstracta' belongs to the same domain and has identity, but does not in itself denote a specific thing with state its own.
5. Every `thing` 'declarable' has only one canonical definition; `as` sets one or more declared relationships on it and `create Nombre` just enable that one identity, according to [[notes/decisions/ADR-054-canonical-definitions-and-initial-activation|D-054]].
6. The relation semantics `is` It is reflexive and transitive.
7. `Thing` is the identity an abstract concept that transcends all others `thing`; it has no source definition or cycle with a programme-controlled lifespan.

The provenance —declaration static or activation during the execution— and the cycle of life do not give rise to distinct ontological categories.

## Formal distinction

`as` e `is` operate at different levels:

- `as` insert direct ancestors at the top of a `thing` static or created.
- `is` is an expression operator that query the relation semantics derived.

Be $R_{\mathrm{decl}}$ the relation declared specialism with `as`. D-068 adds an implicit edge from each root declared towards `Thing`; his union form $R_{\mathrm{dir}}$. [[notes/decisions/ADR-015-acyclic-specialisation-and-state-independent|ADR-015]] complete it with:

$$
R_{\mathsf{is}}
:=
R_{\mathrm{dir}}^*.
$$

Therefore:

$$
t\mathrel{R_{\mathsf{is}}}t
$$

y:

$$
t_1\mathrel{R_{\mathrm{dir}}}t_2
\land
t_2\mathrel{R_{\mathrm{dir}}}t_3
\Rightarrow
t_1\mathrel{R_{\mathsf{is}}}t_3.
$$

The relation direct is acyclic; its reflexive and transitive closure is a partial order.

## Alternatives

### Classes distinct from instances

It is ruled out. It forces a decision on whether a `thing` It is a class or an object and does not represent just one `thing` a particular thing can be both one thing and another ancestor.

### Just one word for declaration y query

This is ruled out. Even if the parser were able to distinguish between the contexts, it would obscure the difference between adding a direct edge and checking for a closure. The syntax current use `as` e `is`, in accordance with [[notes/decisions/ADR-018-as-declares-specialisation-in-is-the-query|ADR-018]] y D-025.

### `is` strict and thoughtless

This is ruled out. Direct specialisation is strict, but `is` query its contemplative closing ceremony.

## Consequences

- The lexer distinguishes between `as` e `is`.
- The parser uses `as` in headers and `is` in expressions.
- The AST represents the predecessors in the declaration and the query in `IsExpression`.
- The resolution checks that the names following `as` appoint `thing`.
- `create` expands the active set and the relation active direct without introducing any other kind of identity.
- Reflexivity does not require the storage of loops $t\to t$.

## Example

```mud
thing Kingdom as Place {}

thing Egypt as Kingdom {}
```

The following are derived from these headings:

```mud
Egypt is Kingdom
Egypt is Place
Egypt is Egypt
```

The following documents must be submitted `is` as ‘it’s the same’ `thing` or ‘an area in which he specialises’, not ‘derives directly from’.

## Verification

1. Reflexivity: `T is T`.
2. Relation direct: `thing B as A {}` implies `B is A`.
3. Transitivity.
4. `thing N as C {}` declares to be true `N is C` when both identities hold; `thing N {}` it does not add declared ancestors, but it does satisfy `N is Thing`.
5. Destroy and recreate `N` retains the identity.
6. Two different names remain distinct even if they share common ancestors and state.
7. Separation of `as` e `is` at the AST.

