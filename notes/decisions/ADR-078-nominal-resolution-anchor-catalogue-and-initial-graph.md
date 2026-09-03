---
id: D-078
title: "Nominal resolution, anchor catalogue and initial graph"
status: current
date: 2026-08-03
supersedes: []
superseded-by: []
questions:
  - "Q-014"
affects:
  - "chapter 09, surface AST, nominal HIR, nominal resolution, symbol table, anchors, diagnostics, LSP, nominal graph, later typing and elaboration"
---
# ADR-078 — Nominal resolution, anchor catalogue and initial graph

- Amended by: [[notes/decisions/ADR-084-especializacion-de-aliases-miembros-heredados-and-vistas-derivadas|D-084]], [[ADR-093-ast-superficial-hir-nominal-and-fase-semantica-posterior|D-093]], [[ADR-096-modulos-callables-look-message-and-activacion|D-096]] and [[ADR-097-hir-nominal-vigente-and-ir-semantico-diferido|D-097]].
- Extends: [[ADR-035-organisation-names-using-and-anchors|D-035]] and [[ADR-072-resolution-environments-and-explicit-anchor-migrations|D-072]].

## Decision

The specification calls the logical identity derived from folders a **MUD path**. There is no `namespace` header and `path` is not reserved. LSP may show a virtual header, copy the qualified name and reveal physical provenance without modifying the file.

All top-level declarations in a path share one nominal namespace. An unqualified name is searched in this order: lexical environment, owner or implicit receiver, current path, exact `using`, recursive `using` and built-ins. The first non-empty level is selected; an incompatible category does not permit continuing. Candidates with the same anchor are deduplicated and distinct anchors are ambiguous. A `using` does not re-export. When a candidate belongs to another module, `using` contributes it only to nominal resolution: reaching it also requires `uses` to authorise the dependency and the symbol to belong to the visible closure of the modular contract. A qualified name cannot bypass this boundary.

There is no shadowing of a visible name. `PascalCase`, `lowerCamel` and the unit `lowerCamel` convention are static requirements with an automatic fix.

Anchors belong to top-level nominal declarations, fields in their original owner, components, associated data declared by a `family`, `family` members, declared units, `for`/`on`/`given` participants, configured metadata materialised as `Metadata`, and built-in types. An inherited field retains its ancestor's declarative anchor although its state is independent in each `thing`. Iterators, ordinary local bindings and non-nominal global values receive only ephemeral internal identity.

Canonical categories are `thing`, `alias`, `family`, `magnitude`, `unit`, `rule`, `action`, `look`, `message`, `test` and `type`. Nested declarations extend the owner's anchor with `::<member>`; a first-level modular `start with` contribution has neither name nor anchor. Module membership is a visibility and dependency dimension, not an additional nominal-anchor component.

Nominal resolution creates symbols, anchors, scopes and reference bindings whose category can already be determined, materialising them in `specification/names/mud-nominal-hir.asdl`. Type names are nominally bound to symbols, but compatibility, unions, domains, cardinalities and type-dependent members belong to typing and elaboration. The specification uses environments and candidate sets; a scope graph is an implementation option, not authority.

The nominal HIR contains only relationship families this phase can justify: ownership/containment (`Owns`), specialisation (`Specializes`) and nominal reference (`RefersTo`). Relationships depending on effective type, domain, elaborated initialisation, computation, effects or termination remain outside the HIR and belong to later phases whose mechanical representation is not yet fixed.

Nominal specialisation includes `thing` and aliases. Components and fields derived from an alias have anchors under the `alias` category; an inherited member retains its origin anchor. Overriding a default introduces neither a new public member nor a new anchor.

## Migrations

An anchor changes with category, path or qualified name. Tooling retains an explicit directed correspondence for migrating persistent references, but the former anchor does not become a source alias. Q-014 remains open on external format, composition, collisions, retention and application to persisted worlds.

## Verification

1. First non-empty level and incompatible category without falling through.
2. Global collision between categories.
3. Anchor deduplication and genuine ambiguity.
4. No shadowing and repairable casing errors.
5. Anchors for inherited fields, members, units and built-ins.
6. Declared participants with public anchors and ordinary local symbols without them.
7. Nominal HIR constructible before complete typing and free of elaborated types, domains, cardinalities and termination.
8. HIR graph limited to `Owns`, `Specializes` and `RefersTo`.
9. `using` or a qualified name cannot cross a module boundary without `uses` and a visible contract.
10. Module membership does not alter the nominal anchor.
