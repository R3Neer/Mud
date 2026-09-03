---
id: D-065
title: "File-level `using` header"
status: current
date: 2026-07-30
supersedes: []
superseded-by: []
questions: []
affects:
  - "file model, concrete grammar, parser and diagnostics"
---
# ADR-065 — File-level `using` header

- Amends: [[notes/decisions/ADR-035-organisation-names-using-and-anchors|D-035]] and [[notes/decisions/ADR-057-concrete-grammar-precedence-and-continuation|D-057]]
- Affected documents: file model, concrete grammar, parser and diagnostics

## Context

`using` declarations have file scope and their textual position does not affect resolution. Allowing them between top-level declarations falsely suggested a local or sequential scope.

## Decision

A MUD file consists, in this order, of:

1. Zero or more `using` declarations.
2. Zero or more top-level declarations.

After the first top-level declaration, no `using` may appear.

```mud
using world.people
using physics.*

thing Player {
    ...
}

action Move {
    ...
}
```

The restriction is syntactic. It does not change:

- The file scope of each `using`.
- Resolution precedence.
- Independence from textual order among several `using` declarations.
- The identity or anchor of declarations.

## Consequences

- Tools may treat `using` declarations as one physical header.
- An interleaved `using` is an error, not a scope change.
- Moving an existing `using` to the header preserves meaning when the file has no other independent ambiguity.

## Verification

1. Empty file.
2. File containing only `using` declarations.
3. File containing only declarations.
4. Several `using` declarations followed by several declarations.
5. Rejection of a `using` after the first top-level declaration.

## Current amendment by D-096

`using` remains the name-resolution header of a `.mud` file. The new modular dependency `uses` lives in `mud.module` and authorises crossing the semantic boundary; `using` does not grant that authorisation and `uses` does not automatically import every name into each file.
