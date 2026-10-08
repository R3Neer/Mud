---
id: D-142
title: Canonical pruning and empty-filter closures
status: current
date: 2026-10-08
supersedes: []
superseded-by: []
questions:
  - Q-050
affects:
  - specification/21-expressions.md
  - specification/types/
---

# ADR-142 — Canonical pruning and empty-filter closures

## Context

The author accepts canonical inequality/XOR expansion, no-filter closure for erased predicates and demand evaluation of original operands. This extends D-022 and leaves the independent speculative/error-boundary questions active.

## Decision

Boolean equality expands as `(p and q) or (not p and not q)`. Boolean `!=` and word `xor` expand as its negation. Apply structural deletion before residual evaluation. One erased operand and one ordinary Bool make inequality/XOR false; two erased operands close to true. Bind each original source operand to one demand-evaluated occurrence: repeated references in this expansion do not repeat its evaluation. Distinct written occurrences remain distinct. Deleted receivers/arguments and short-circuited operands are not evaluated; this is not general memoisation.

Close a completely erased per-element predicate to true: it means no filter. Nonempty exists/forall therefore return true; empty exists is false and empty forall true. Selection retains all members, count counts them, and min/max select the first/last accepted witness under their semantic order. Empty selection/min/max return empty and empty count zero. Finiteness, enumeration, purity and ordering obligations remain mandatory.

## Alternatives and consequences

Reject XOR truth-table completion of an erased operand: erased is not a third Bool. Reject treating erased predicates as false, because it removes rather than removes the filter. No new pruning through stored values, speculative operations or error boundaries is selected.

## Verification

MUD-TYPE-024 and finite pruning witnesses cover all pairs of Bool/erased inputs, quantifier empty/nonempty boundaries and demand sharing. Q-050 remains partial for its independent boundary interactions. Chapter publication states are unchanged.
