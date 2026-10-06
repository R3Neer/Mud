---
id: D-114
title: Callable variance and static named binding
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-063
  - Q-066
affects:
  - Language contracts and their developed normative surfaces
---

# ADR-114 — Callable variance and static named binding

- Formalised by: [[ADR-122-finite-type-graphs-and-proof-obligations|D-122]].

## Context

The author accepts ordinary variance subject to capabilities, and named binding only through an unequivocal static contract. This amends D-036, D-063 and D-096 and closes Q-063 and Q-066.

## Decision

A callable can substitute for a requested callable contract exactly when every call admitted by the requested contract is admitted by the supplied callable. Read-only receiver/given inputs are contravariant: the supplied operation accepts at least the requested values, including domains and cardinalities. Query outputs are covariant: its possible returned values satisfy the requested output contract. An outer read/write receiver place is invariant in its writable value contract, because it must safely accept writes and reads in both directions. Additional mandatory arguments or receiver roles are not introduced by substitution; optional arguments/defaults must preserve every call admitted by the target contract.

Inner authority over immediately contained thing members is distinct from replacing the receiver place. It is not a blanket rule making every type mentioning [mut] invariant. Substitution must require no stronger caller authority and promise no weaker guarantee; it preserves the declared authorized write footprint and applicable domain constraints. Purity, external effects and determinism are additional contract obligations, not consequences of variance. Outer-root capability remains separate: widening subaction to action never grants the ability to start an outer resolution.

Named for/given binding requires role names and their corresponding positions to be unequivocal in the static contract. A concrete named operation admits its names. A union or collection element type admits names only if every possible callable alternative preserves the same names at compatible signature positions. The check uses static types, not scanning runtime members. Otherwise positional calls may use the compatible erased contract, or an is refinement can narrow to a concrete operation before named binding. Name recovery from the current runtime descriptor is not implicit.

## Examples and verification

An operation accepting Animal read-only may implement a Dog-input contract; an operation accepting only Dog cannot implement an Animal-input contract. A Dog result may implement an Animal-result contract. A place that can be overwritten with Animal is not substitutable for writable Dog storage.

Two callable alternatives naming their sole receiver `actor` permit that named binding under a compatible common contract. Alternatives naming it `hero` and `actor` do not; positional binding or static narrowing is required. An action-typed value that may contain a subaction remains invalid as an outer request.

## Integration review

The callable grammar/AST already preserve receiver contracts and written role names. Names and anchors retain pending candidates until typing; variance and named admissibility are not stored in nominal HIR. The developed names chapter states the boundary; chapter 10 develops the type contract, while the complete public-boundary chapter remains planned.
