---
id: D-151
title: Finite collections and mandatory enumeration proof basis
status: current
date: 2026-10-08
supersedes: []
superseded-by: []
questions:
  - Q-028
affects:
  - specification/08-concrete-grammar.md
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/types
---

# ADR-151 — Finite collections and mandatory enumeration proof basis

## Decision

Keep all Mud collections finite. An unbounded static upper cardinality permits arbitrarily large finite values, not an infinite collection. No lazy infinite stream/generator type is introduced; internal deferred realization is allowed only when observably equivalent to the finite snapshot/value contract.

All materializes a complete finite canonical domain enumeration. Int [*] = all is invalid because the full integer domain is infinite. Rum [*] = all is not admitted because Mud does not provide canonical enumeration of the full numeric Rum domain. A finite explicit Rum collection can be traversed; its enumeration comes from the container, not numeric progression.

Correct D-034/D-047's mathematical description: binary64 Rum values form a finite set, hence are countable. The prohibition on Rum interval enumeration/by progression is a language contract, not uncountability. Num denotes exact rationals, which are countably infinite; a general rational interval is not made a finite enumeration by having bounded endpoints. An exact stepped rational domain is a selected finite progression, not every rational in the interval.

Require a normative minimum basis of finiteness/enumeration proofs, not wholly implementation-dependent acceptance. The existing elementary rules and established finite source constructions form that basis: finite concrete collections, finite closed families/explicit sets, admitted bounded discrete progressions and justified finite compositions. Producing a source and evaluating each body still require their own termination/purity obligations. Finite individual values do not imply a finite reachable world/state space.

Failure to prove a mandatory obligation is static rejection, never a negative runtime query answer or bounded trial traversal. Q-028 still owns detailed conservative analysis limits and diagnostic contracts for cases beyond the established basis; Q-029 retains general termination certification. This does not implement a compiler or select a causal search algorithm.

## Verification and provenance

Clarifies [[ADR-047-quantifiers-and-finite-iteration|D-047]], [[ADR-075-enumerable-domains-all-and-derived-value-form|D-075]] and [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]], and corrects [[ADR-034-num-exactly-and-rum-binary64|D-034]]. Chapter 11 identifies mandatory proof premises; chapter 21 and the corpus contrast finite values, infinite domains, finite explicit Rum containers and exact rational grids. No chapter is promoted.
