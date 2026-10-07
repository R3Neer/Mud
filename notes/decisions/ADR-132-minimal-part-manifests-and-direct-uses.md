---
id: D-132
title: "Minimal part manifests and direct uses"
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-062
affects:
  - "[[specification/05-source-text]]"
  - "[[specification/08-concrete-grammar]]"
  - "[[specification/09-abstract-syntax]]"
  - "[[specification/10-names-and-anchors]]"
  - "[[specification/11-type-system]]"
  - Grammar, syntax catalogues, nominal resolution and host contracts
---

# ADR-132 — Minimal part manifests and direct uses

## Context

The author accepts parts, whole-file privacy and a minimal direct dependency grammar. This amends D-096's part boundary and preserves source paths and stable historical document identifiers.

## Decision

A part is an encapsulation unit within a Mud world project. Each `.mud` belongs to the part of its nearest ancestor `mud.part`; no such ancestor is a static error. A nested manifest opens a new part. The part path is derived from its directory relative to the world root, without a repeated name declaration.

A `mud.part` is a minimal manifest: only whitespace, comments and zero or more `uses exact.part.path` statements. Empty manifests are valid. Statements use ordinary newline or `;` separation. Paths are exact MudPaths from the world root and must identify directories containing a `mud.part`. Relative paths, wildcard paths, grouped lists, metadata, source declarations and backend settings are invalid. A repeated `uses` is redundant and produces a warning.

```mud
uses world.people
uses world.weather; uses world.time
```

`uses` authorises direct access to another part's visible contract; it does not import short names. `using` imports names inside an `.mud` and does not grant permission. Operational access is not transitive: if A uses B and B uses C, A cannot call C without its own uses C. The transitive type closure needed to represent B's visible contract remains available, without exporting all of C's operations. Fully qualified references obey the same checks.


Foreign library/version/adapter declarations remain Q-069; they are not silently added to the local manifest grammar.

## Integration

The existing source, grammar, AST, nominal-resolution and type contracts describe the accepted boundary. ASDL's technical module syntax and foreign-language modules retain their terminology. This specifies the language and conformance artefacts; it does not implement a compiler, host transport or package manager.
