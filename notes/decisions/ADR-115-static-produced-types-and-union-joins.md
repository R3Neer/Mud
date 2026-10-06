---
id: D-115
title: Static produced types and union joins
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-065
  - Q-068
affects:
  - Language contracts and their developed normative surfaces
---

# ADR-115 — Static produced types and union joins

- Formalised by: [[ADR-122-finite-type-graphs-and-proof-obligations|D-122]].

## Context

The author retains producer identity for look values, structural identity for anonymous literals, and the union where a common result join is ambiguous. This amends D-096 and closes Q-065/Q-068.

## Decision

Each look declaration has one statically determined produced nominal result type, identified internally by its declaration identity and result schema. Different look declarations have different result types even if fields coincide. Calls to the same declaration share the produced type, irrespective of receiver or runtime state. Each message declaration similarly has a static produced payload type; occurrence identity and multiplicity are separate from payload type and equality.

Anonymous literal products have structural type identity determined statically by normalized components, names/order, domains and collection/capability contracts. Contextual literal construction may obtain a nominal expected type; this does not merge different producer types. A local := preserves the inferred type, including producer identity. Explicit annotation validates compatibility rather than granting an implicit nominal cast. Runtime evaluation creates values, never a new result type. ~type returns the static type at the program point, including flow narrowing.

A produced type receives no new public anchor solely by existing. Its originating declaration supplies predictable tooling provenance; a programmer can query ~type or explicitly name an ordinary alias. Equality/hashing/caches include effective nominal type for produced values and normalized structural type for structural literals; equal field contents from different producers do not erase nominality.

For dynamic look results, use the unique most specific common type when that type covers and preserves the alternatives under the existing contract. With several incomparable minimal common supertypes, retain the normalized union of the original result alternatives. Do not choose by source order, create an intersection or drop an alternative because its domain happens to be included in another. This also applies when no common type is more informative than that union.

## Verification

Two calls to Stats on different receivers have one produced type. Stats and Summary with identical fields remain distinct. Storing either with := retains its type. Two context-free literals with identical normalized shape share structural type. A join with incomparable ancestors A and B remains LeftResult | RightResult. Message payload equality does not deduplicate distinct occurrences.

## Integration review

Existing look/AST descriptions and the roadmap distinguish static produced identity from syntax. The names chapter retains no public anchor for interim results; existing nominal references identify their producer. The nominal HIR needs no runtime type or join node. Chapter 10 develops the static inference and proof contract; an executable typechecker remains unimplemented.
