---
id: D-188
title: Structural selector patterns and Boolean literals
status: current
date: 2026-10-26
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/17-dictionaries.md
  - specification/21-expressions.md
  - specification/22-quantifiers-and-iteration.md
  - specification/grammar
  - specification/syntax
  - specification/names/mud-nominal-hir.asdl
  - specification/types
---

# ADR-188 — Structural selector patterns and Boolean literals

## Context

The author accepts structural patterns in functional branches, repeated capture
names as equality constraints, field patterns inspired by C#, and collection
head/tail patterns inspired by Haskell. The proposed Python-style slice DSL is
explicitly discarded. Boolean literals should mean the expected Boolean value,
rather than an unconditional or impossible branch predicate.

## Decision

Functional selectors admit positional `(0, y)`, `(x, x)`, typed field
`Impact { damage: > 0, target: victim }`, exact collection `[]`, `[x]`,
`[x, y]` and head/tail `x : resto` patterns. Colon associates to the right:
`x:y:resto` means `x:(y:resto)`. A field label selects a visible field; its
subpattern tests or captures the field value. Named fields and original nominal
identity are not reconstructed as positional tuples. Omitted fields are not tested.

Capture leaves bind on first occurrence in a branch pattern. Repeated names
compare complete values through ordinary supported equality, with no new
unification or functional-value equality. `_` discards inside a pattern;
the complete `_ -->` remains residual fallback. Plain root identifiers retain
ordinary selector interpretation; use explicit == to compare a complete tuple,
collection or outer value rather than introduce pattern captures.

Empty and singleton collection patterns need no ordering guarantee. Patterns
that distinguish multiple positions or head/tail require static observable order.
Tails preserve surviving sequence, member contracts and supplied authority;
nested collection members never flatten. Refutable matching belongs to branch
selection, not local declarations or traversal bindings. No lazy collections,
implicit construction, arbitrary property projection or new write permission arises.

Literal true/false, including grouping, compare with the selected input in both
complete selectors and nested patterns. Other Boolean expressions remain
predicates. Explicit == true/false remains valid. Fallback is not an always-added
AllMatches contribution. Boolean predicates elsewhere retain their meaning.

The result sees successful pattern captures and direct selector-preamble locals
that every successful selecting path establishes. Nested locals, failed scopes,
other branches and fallback do not export bindings. Existing no-shadowing,
same-application derivation reuse, purity, demand and recovery rules remain.
Exact dictionary keys create no selector/result scope.

## Integration and compatibility

Partially amends D-169 and extends the direct shared-selector scope of D-172.
Update current effective ADR text and grammar/CST/AST/nominal/type surfaces
atomically. Check literal Boolean branch uses for intent preservation. The
ordinary scalar selector conveniences, branch modes, coverage obligations,
collection indexing and cardinality contracts remain in force.

## Verification

Preclassified-token witnesses cover structural branches and reject their use as
local/traversal binding syntax. Finite supplied match certificates distinguish
equality from capture, sequence constraints, nested empty members, scope rollback,
faults, visible fields, and Boolean literal versus computed-predicate selection.
They do not implement a Mud parser, typechecker, compiler or runtime.
