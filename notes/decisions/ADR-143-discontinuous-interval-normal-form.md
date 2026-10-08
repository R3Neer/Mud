---
id: D-143
title: Discontinuous interval normal form
status: current
date: 2026-10-08
supersedes: []
superseded-by: []
questions:
  - Q-018
affects:
  - specification/08-concrete-grammar.md
  - specification/21-expressions.md
  - specification/types/
---

# ADR-143 — Discontinuous interval normal form

## Context

The author selects existing interval algebra, rather than a new multi-segment literal. This completes the source and canonical-key portions of Q-018; D-088 already establishes segment traversal and step restart.

## Decision

Construct discontinuous intervals by union, intersection, difference and symmetric difference of compatible intervals. `[1..3] | [7..9]` requires no new literal production. Normalize the represented set to sorted maximal nonempty convex segments relative to its ordered member universe. Merge segments exactly when their union is one interval; retain excluded boundary holes. Empty has zero segments and a simple nonempty interval one. Preserve endpoint inclusion, intrinsic numeric/magnitude normalization and effective member identity. Equality and keys use this canonical content, not construction order or segment spelling. Existing signed stepping restarts per normalized segment, reversing segment traversal for a negative step. A cyclic point domain retains its separate one-period contract.

## Alternatives and consequences

Reject new discontinuous-literal syntax and source-order keys. Maximality is relative to the admitted member universe: integral adjacency and rational excluded gaps are different. No new enumeration of continuous intervals is inferred.

## Verification

MUD-TYPE-025, reviewed interval cases and finite integral-content witnesses cover union normalization, empty, reordered/overlapping fragments and domain-sensitive gaps. Q-018 closes; chapter states remain unchanged.
