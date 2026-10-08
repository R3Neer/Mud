---
id: D-150
title: Transparent derived Boolean pruning boundaries
status: current
date: 2026-10-08
supersedes: []
superseded-by: []
questions:
  - Q-050
affects:
  - specification/21-expressions.md
  - specification/types
---

# ADR-150 — Transparent derived Boolean pruning boundaries

## Decision

A Boolean binding defined by := transmits structural erasure from its registered derivation when read in a Boolean formula. This applies to locals, computed fields/components and computed metadata, using each derivation's ordinary view, access and dependency contracts. A Bool annotation does not turn a derivation into stored capture. Bindings defined by = materialize/capture ordinary values; erasure is never a storable third Boolean value.

For an inactive rule R, not R and not p with p := R close to true. With p: Bool = R, the initializer closes to true and not p is false. Ordinary value consumers close residual erasure rather than storing it or deleting collection members. Derived reads are not indiscriminate substitution through arbitrary calls.

On an actual read, independent prefix computations in the derivation remain executable. A stored prefix initializer can fail even when the final Boolean expression is wholly erased. Such Fault is handled by the existing producing-block recovery contract; a recovered ordinary Bool is an ordinary result. An unread derivation remains unevaluated. No prefix or failed recovery is silently deleted by erasing the final expression.

If an admitted eventually query's initial goal is wholly erased, the query transmits erasure to its surrounding Boolean formula instead of materializing ordinary true. Its goal's demanded prefix work and faults remain protected, and the query's static finiteness/enumerability/termination obligations are not waived. A non-erased initial goal retains ordinary reachability semantics; the causal/search algorithm is not specified here.

Imagine retains its ordinary ActionReply contract. If it occurs in a deleted inactive call's arguments, the arguments are not evaluated. Otherwise pruning of internal Boolean conditions does not turn ActionReply into erasure.

No conformance warning is required merely for pruning-sensitive syntax. Tooling may provide requested explanations or optional diagnostics; ordinary static errors remain mandatory.

## Boundaries still requiring formalization

Q-050 retains the complete compositional demand/short-circuit account for erased derived/query fragments carrying independent prefix work. The accepted actual-read and standalone examples must hold; this decision does not silently select an ordering policy for every enclosing short-circuit combination.

## Verification and provenance

Extends [[ADR-142-canonical-pruning-and-empty-filter-closures|D-142]] and [[ADR-022-structural-deletion-of-inactive-boolean-rules|D-022]]. The chapter and static corpus contrast derived/stored reads, prefix faults, recovery, eventually and ordinary imagine capture. Finite certificates test these selected boundary cases, not a general evaluator or causal implementation. Q-050 remains partial until its remaining compositional contract is evidenced.
