---
id: D-051
title: "Graph future semantics and reconstructable information"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-009"
  - "Q-016"
  - "Q-027"
  - "Q-034"
  - "Q-054"
  - "Q-059"
affects:
  - "architecture, nominal HIR, future semantic graph, future post-typing and elaboration representation, conformance"
---
# ADR-051 — Graph future semantics and reconstructable information

- Amended by: [[ADR-097-current-nominal-hir-and-deferred-semantic-ir|D-097]].
- Expanded by: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]] and [[ADR-086-exact-nominal-identity-external-arrows-and-dictionary-algebra|D-086]].
- Amended by: [[notes/decisions/ADR-063-signatures-given-and-joint-on-bindings|D-063]], [[notes/decisions/ADR-066-static-values-and-local-bindings-in-then|D-066]], [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]] and [[ADR-093-surface-ast-nominal-hir-and-later-semantic-phase|D-093]].
- Related to: [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]].

## Context

Impact assessments, explanation and implementation will require information semantics derived, but that information must not become an alternative source of truth, nor should it be mechanically established before the stages by which it is produced have been formalised.

## Decision

The files `.mud` and versioning decisions are the source semantics. The Surface AST and the Nominal HIR are current reconstructible derivatives. The nominal resolution produces `specification/names/mud-nominal-hir.asdl`, with symbols, scopes, bindings, anchors and nominal relations, without type inferences or elaboration.

After typing and elaboration there may be a semantic representation rear and a graph a searchable semantic model derived from it. Its specific encoding is deliberately left undefined until such time as these phases have sufficiently developed normative frameworks.

When designing this future representation, it must be capable of preserving or reconstructing, as appropriate, at least the following conceptual distinctions:

- provenance up to the source file and range;
- symbols and anchors resolved;
- the three types of ruler;
- participants `for` and `on`, values `given`, cardinality, mutability and relationship types;
- pre-defined types, aliases, domains, cardinalities, units and intervals;
- local links and the order in which they are assessed;
- effects, readings, writings, calls and dependencies;
- logical activity and suspended dependencies;
- `look`, `message`, its outflows and deferred liabilities;
- tests, activation local, effects, assertions and diagnoses;
- dependencies of `allowed`, `eventually`, `when`, `if`, `after`, `old` and `always`;
- structural effects `create`, `destroy`, the addition and removal of collections;
- derivation of dimensions, quantities, units and equivalences;
- general departments, including domain, stochastic and hard when they form part of the defined analysis.

Which information is explicitly stored, what is derived and how it is serialised are matters for the future design of the typing system and elaboration. If a persistent exchange format is introduced, it must have a compatible schema version and allow deterministic reconstruction from the previous normative sources.

Q-009 It leaves the external format and specific names open for when such a representation comes into existence; that question does not require it to be created in advance.

## Consequences

- A discrepancy in a derivative is resolved by discarding it and reconstructing it from the regulatory sources.
- There is currently no contract neither a semantic IR mechanism nor a graph normative final semantics.
- The Nominal HIR cannot absorb effective types, effective domains, inferred cardinalities, effects or evidence of termination to make up for that absence.
- Future analysis tools must wait until they reach the surface semantics relevant information or to provide only information authorised by the stages that have already been completed.

## Verification

1. The Nominal HIR can be reconstructed from Surface AST + nominal resolution.
2. The nominal HIR remains free of typing conclusions and elaboration.
3. There is no regulatory framework for semantic IR until its production phases have been developed.
4. The conceptual requirements set out above remain available for use in reviewing future designs without specifying their technical implementation at this stage.

