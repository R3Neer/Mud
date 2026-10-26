---
id: D-172
title: Shared functional selector locals and demand-preserving reuse
status: current
date: 2026-10-14
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/10-names-and-anchors.md
  - specification/17-dictionaries.md
  - specification/20-blocks-and-recovery.md
  - specification/21-expressions.md
  - specification/names
  - specification/syntax
  - specification/types
---

# ADR-172 — Shared functional selector locals and demand-preserving reuse

- Extended by: [[ADR-188-structural-selector-patterns-and-boolean-literals|D-188]].

- Amended by: [[ADR-186-arrow-owned-dictionary-specifications|D-186]].

- Amended by: [[ADR-183-functional-families-currification-and-input-syntax|D-183]].

## Accepted policy

The author accepts sharing direct selector-preamble locals with the same branch's
result, retaining ordinary := derivation rather than silently freezing it as a
stored capture. Nested/other-branch/fallback locals remain unavailable; each
application/branch has independent instances and no shadowing. Direct pure pattern
leaves and completed immutable foreign exports retain their ordinary local scope
meaning. Exact key/value and comprehension filter/result scopes remain separate.

Successful refutable branch-pattern captures follow D-188 and join the same
definitely established branch-result environment. Repeated capture names test
equality against their first binding, without shadowing or extra symbols.

A first demanded successful computation must be reused while its inputs and
transitive dependencies are unchanged. No eager computation is introduced.
Explicit permitted dependency changes invalidate, unknown overlaps conservatively
invalidate, and hits retain complete dependency footprints. Faults do not supply
cached normal values; protected rollback does not resurrect selector locals.
Existing scope/definite-availability and native purity contracts remain mandatory.
No physical cache representation or host world-version protocol is chosen.

AllMatches remains the unmodified default, useful for overlapping tags,
modifiers, diagnostics and interactions; exhaustive coverage does not imply
one applicable branch. FirstMatch is selected by -->[ordered], independently
of output ordering.
This partially amends D-085/D-169 scope wording without selecting runtime causal
algorithms, stochastic caching or compiler/IR implementation.

## Evidence

MUD-DICT-005, nominal scope-parent review, retained branch AST blocks, bounded
source cases and supplied finite visibility/reuse/invalidation/footprint traces
cover the contract. The witnesses execute no Mud RHS and implement no runtime.
