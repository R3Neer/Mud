---
id: D-093
title: "Surface AST, nominal HIR and later semantic phase"
status: current
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, Surface AST, nominal HIR, name resolution, symbol table, nominal graph, typing, elaboration, future semantic representation and validators"
---

# ADR-093 — Surface AST, nominal HIR and later semantic phase

- Modifies: [[ADR-051-graph-future-semantics-and-reconstructable-information|D-051]] and [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]].
- Modified by: [[ADR-097-hir-nominal-vigente-and-ir-semantico-diferido|D-097]].
- Clarifies: [[ADR-070-lossless-cst-and-normalised-surface-ast|D-070]], [[ADR-086-exact-nominal-identity-external-arrows-and-algebra-de-diccionarios|D-086]], [[ADR-090-functional-branches-without-public-anchor|D-090]] and [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]].

## Context

A representation mixing nominal resolution with effective types, elaborated domains, inferred cardinalities and termination proofs erases useful phase boundaries. The architecture must distinguish source form, nominal-resolution results and meaning that can only be known after typing and elaboration, without prematurely fixing the representation of the latter phase.

## Decision

MUD has a single source AST: the **Surface AST** produced from the lossless CST. It retains the written abstract form and provenance without anticipating resolution, typing or elaboration.

Name resolution consumes that AST and produces a normative **nominal HIR**. The HIR does not duplicate all source syntax; it records only information whose existence depends on nominal resolution:

- anchored symbols and `LocalSymbol`;
- owners and lexical scopes;
- bindings from each surface reference to a symbol;
- public anchors;
- nominal ownership, specialisation and reference edges.

The nominal HIR cannot contain effective types, narrowing, effective domains, collection forms, effective or inferred cardinalities, elaborated conversions, termination proofs or any other conclusion requiring typing or elaboration. Its normative schema lives in `specification/names/mud-nominal-hir.asdl`.

Typing and elaboration consume the Surface AST together with the nominal HIR. Their semantic result belongs to a later architectural phase, but the repository does not yet fix a normative mechanical schema for representing it. That contract will be designed when the typing and elaboration surfaces are sufficiently developed.

No derived artefact is an independent semantic source: it is reconstructed from `.mud` files, version decisions and applicable earlier phases.

## Pipeline

```text
source text
→ scanner and contextual classification
→ lossless CST
→ Surface AST
→ nominal resolution
→ nominal HIR: symbols + scopes + bindings + anchors + partial nominal graph
→ typing and elaboration
→ later semantic representation to be formalised
→ later analysis / execution
```

The nominal HIR is deliberately smaller than a complete resolved AST and does not anticipate type conclusions.

## Consequences

- `mud-surface-ast.asdl` remains the only source AST schema.
- `specification/names/mud-nominal-hir.asdl` is the output contract of nominal resolution.
- No normative ASDL currently exists after typing/elaboration.
- D-078 describes construction of the nominal HIR and does not promise elaborated types or domains.
- Validators must check nominal-HIR self-consistency and prohibit concepts reserved for elaboration.

## Verification

1. The syntax directory contains a single source AST schema: `mud-surface-ast.asdl`.
2. The pipeline explicitly contains `Surface AST → nominal HIR → typing/elaboration → future semantic representation`.
3. The nominal HIR represents symbols, scopes, bindings, anchors and `Owns | Specializes | RefersTo`.
4. The nominal HIR contains no effective types, effective domains, cardinalities or termination evidence.
5. No later semantic schema is required before the phases producing it are formalised.
6. The validator rejects unknown ASDL types and elaborated concepts inside the nominal HIR.
