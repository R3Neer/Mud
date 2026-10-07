---
id: D-131
title: "Parts, file privacy and sub operations"
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions: []
affects:
  - "[[specification/05-source-text]]"
  - "[[specification/07-concrete-grammar]]"
  - "[[specification/08-abstract-syntax]]"
  - "[[specification/09-names-and-anchors]]"
  - "[[specification/10-type-system]]"
  - Grammar, syntax catalogues, nominal resolution and host contracts
---

# ADR-131 — Parts, file privacy and sub operations

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

The optional header `part only` applies to its entire `.mud` file. It must be the first content after an optional BOM and whitespace; comments, metadata, `using` and declarations cannot precede it. It is followed by ordinary statement separation. Declarations remain available throughout their owning part but cannot cross to another part or the host. The header does not affect other files or nested parts, and is not accepted in `mud.part`. No declaration-level visibility modifiers or export-selection list exist.

```mud
part only
using world.people

sublook Detail { score := 0 }
```

Normal `action`, `look` and `message` form host operations. Their sub forms `subaction`, `sublook` and `submessage` are visible to authorised Mud parts by default but are not direct host endpoints. A subaction has no outer-root capability; sublook is a pure query with no action-only calling restriction; submessage supplies internal causal occurrences without host delivery. A `part only` file restricts normal and sub forms alike. Tests retain test-context visibility.

A visible signature, produced value, nested alias/type component or reflective result cannot expose a `part only` declaration. Contract closure cannot lift this restriction. A visible ordinary value projection may be computed using private implementation state without exposing its private type. Ordinary thing fields remain private; imports, specialisation and descriptor widening grant no additional authority.

Contract-visible thing and alias types may be specialised under direct uses authorisation and public type closure. Inherited initialisation keeps the declaring owner's rights. Part dependency cycles are valid with a cyclic-coupling warning; they imply no startup order and do not permit cycles of domain evaluation. Part start contributions are materialised jointly.


## Integration

The existing source, grammar, AST, nominal-resolution and type contracts describe the accepted boundary. ASDL's technical module syntax and foreign-language modules retain their terminology. This specifies the language and conformance artefacts; it does not implement a compiler, host transport or package manager.
