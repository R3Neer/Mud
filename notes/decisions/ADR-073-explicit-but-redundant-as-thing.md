---
id: D-073
title: "Explicit but redundant `as Thing`"
status: current
date: 2026-08-02
supersedes: []
superseded-by: []
questions: []
affects:
  - "thing specialisation, diagnostics, nominal resolution, post-typing semantic representation, formatters and code actions"
---
# ADR-073 — Explicit but redundant `as Thing`

- Amends: [[ADR-018-as-declares-specialisation-in-is-the-query|D-018]] and [[ADR-068-universal-thing-and-intrinsic-name|D-068]]
- Adjusted to the phase boundary of [[ADR-093-ast-superficial-hir-nominal-and-fase-semantica-posterior|D-093]].

## Context

D-068 introduced `Thing` as a built-in abstract root and rejected writing it in an `as` clause. However, `thing Place as Thing {}` expresses a relationship that is necessarily true and introduces no ambiguity, state or second semantic path.

Rejecting a correct, readily repairable assertion is disproportionate, especially for someone making the hierarchy explicit while learning the language.

## Decision

`Thing` may appear explicitly as an ancestor in an `as` clause:

```mud
thing Place as Thing {}
```

The declaration is valid and has exactly the same effective semantics as:

```mud
thing Place {}
```

The compiler emits a non-blocking redundancy diagnostic and offers an automatic correction that removes `as Thing`. The diagnostic must explain that every `thing` already reaches the built-in root.

The CST and surface AST retain the explicit spelling for round-tripping, provenance and code actions. Resolution normalises `Thing` as the already-guaranteed effective root: it creates no second edge, changes no linearisation and does not publish it as a distinct declared ancestor in the semantic graph.

If `Thing` appears with other ancestors, only that element is removed by the correction:

```mud
thing Port as Place, Thing {}
```

is suggested as:

```mud
thing Port as Place {}
```

All other restrictions remain: `Thing` may not be declared, redefined, activated, created or destroyed.

## Consequences

- A pedagogically understandable redundancy does not prevent compilation.
- The semantic model still has one built-in root.
- Simplification is applied by an explicit code action, not silently.
- Linters and LSP may flag the redundancy without presenting it as a type or name error.

## Verification

1. `thing Place {}` and `thing Place as Thing {}` produce the same effective graph.
2. The second form produces a non-blocking diagnostic and a correction removing `as Thing`.
3. The CST and surface AST of the second form retain `Thing` with its provenance.
4. `thing Port as Place, Thing {}` simplifies to `thing Port as Place {}` without altering `Place`.
5. Normalisation creates no duplicate edges and does not change the result of `is`.
6. Declaration, creation, destruction or activation of `Thing` remains rejected.
