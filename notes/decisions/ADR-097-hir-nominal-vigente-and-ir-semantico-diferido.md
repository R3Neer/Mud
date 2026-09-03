---
id: D-097
title: "Current nominal HIR and deferred semantic IR"
status: current
date: 2026-08-28
supersedes: []
superseded-by: []
questions: []
affects:
  - "pipeline, nominal resolution, nominal HIR, typing, elaboration, future semantic representation, chapter 09, validators and mechanical artefacts"
---

# ADR-097 — Current nominal HIR and deferred semantic IR

- Modifies: [[ADR-051-graph-future-semantics-and-reconstructable-information|D-051]], [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]] and [[ADR-093-ast-superficial-hir-nominal-and-fase-semantica-posterior|D-093]].
- Clarifies the phase boundary used by [[ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|D-092]].

## Context

MUD's architecture correctly distinguishes the superficial AST, nominal resolution and the later typing and elaboration phases. However, the repository had fixed a detailed ASDL schema for the later semantic output before a developed specification of the type system and elaboration that should produce it was available. This turned still-future decisions about internal representation into a premature normative contract.

Nominal resolution is sufficiently delimited: names, scopes, symbols, bindings, anchors and the nominal relations of ownership, specialisation and reference can be defined without resolving effective types or dynamic semantics.

## Decision

MUD currently maintains two normative representations in the frontend chain:

1. the Surface AST in `specification/syntax/mud-surface-ast.asdl`;
2. the Nominal HIR produced by name resolution in `specification/names/mud-nominal-hir.asdl`.

The nominal HIR contains only information justifiable by nominal resolution. Its graph admits ownership, specialisation and nominal reference. It contains no effective types, effective domains, inferred cardinalities, elaborated conversions, effects, semantic dependencies or termination evidence.

Typing and elaboration remain later architectural phases and may produce their own semantic representation. That representation is conceptually called **future semantic IR**, but MUD does not yet fix:

- an ASDL file for it;
- a serialisation schema;
- concrete node or edge names;
- a current `schemaVersion`;
- which derived information must be stored materially rather than reconstructed.

The conceptual catalogue from D-051 becomes a set of requirements to be reviewed when a sufficiently developed typing and elaboration surface exists to design that representation. It does not require maintaining an anticipated mechanical schema today.

The generic `specification/ir/` directory is no longer a normative surface. The nominal HIR is located alongside name resolution in `specification/names/`.

Every future change that introduces or modifies names, scopes, owners, bindings, nominal categories, anchors, nominal visibility or specialisation must review chapter 09 and the nominal HIR in the same change, in accordance with MUD-EDIT-004.

## Consequences

- No validator may require `mud-semantic-ir.asdl` to exist.
- No current specification document presents a post-typing and elaboration contract as existing.
- The nominal HIR remains a normative mechanical contract reconstructible from the superficial AST and resolution rules.
- Decisions requiring a later semantic distinction may retain it as a future elaboration requirement without fixing its encoding in advance.
- Designing the future IR will require integrating the typing and elaboration surfaces that exist then and may adopt a structure different from any previous experimental schema.

## Verification

1. `specification/ir/` does not exist.
2. `specification/names/mud-nominal-hir.asdl` exists and models only nominal information.
3. Validators require no current semantic IR.
4. The documentation pipeline distinguishes the current nominal HIR from the future semantic representation, which is not yet formalised.
5. Changes affecting nominal resolution have an explicit editorial obligation to review chapter 09 and the nominal HIR.
