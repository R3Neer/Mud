---
id: D-072
title: "Resolution environments and explicit anchor migrations"
status: current
date: 2026-08-02
supersedes: []
superseded-by: []
questions:
  - "Q-014"
affects:
  - "qualified names, scopes, anchors, diagnostics, migrations, future chapter 09 and tooling"
---
# ADR-072 — Resolution environments and explicit anchor migrations

- Extends: [[ADR-035-organisation-names-using-and-anchors|D-035]]
- Extended by: [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]]
- Adjusted to the phase boundary of [[ADR-093-surface-ast-nominal-hir-and-later-semantic-phase|D-093]].
- Partially decides: [[../preguntas/Q-014-m-anchor-migration|Q-014]]

## Context

Separating the CST, surface AST, nominal-resolution results and later typing and elaboration phases requires fixing how scopes and candidates are represented. It must also distinguish names with persistent semantic identity from names that merely bind values within a declaration.

Readable anchors change when a declaration's qualified name changes. Traceability must be retained without turning the old name into a silent source alias.

## Decision

### Name spaces

All top-level declarations share one nominal namespace, regardless of category. Within one MUD path, two declarations may not have the same nominal name, even if one is a `thing` and the other an `action`, `rule` or another category.

Fields are identified within their owner and may repeat their name in different owners. Their anchor includes the owner's anchor. Other nested members obey the scope of their owning declaration.

Roles, `given` parameters, iteration variables and local bindings are lexical symbols without anchors. They may reuse names in independent declarations or blocks, but not within one scope or by shadowing a visible name.

### Normative resolution model

The specification defines resolution through environments and ordered candidate sets. For an unqualified name, levels are consulted in order: lexical scope, the relevant owner, the same MUD path, exact `using` declarations and recursive `using` declarations. The first non-empty level is selected, and exactly one candidate compatible with the required category is required.

Scope graphs may be used as an implementation or explanatory representation, but are not the normative authority of MUD 1.0. An implementation must preserve the same candidates, priorities, ambiguities and rejections defined by the resolution judgements.

### Diagnostic references

A symbol without an anchor may be described by combining its owner's anchor with a human label:

```text
action::game.Heal - given amount
```

The complete spelling is diagnostic information, not a new anchor. When source is available, the span remains the primary location.

### Anchor migration

MUD retains readable anchors derived from category and qualified name. A path, name or category change changes the anchor. Tooling explicitly records a directed correspondence between the old and new anchors to migrate persistent references, history and associated data.

```text
thing::world.people.Person
→ thing::world.characters.Person
```

The correspondence does not turn the old anchor into an alias accepted by ordinary source resolution. The updated programme produces and resolves only the current anchor.

Q-014 remains partially decided pending the format and location of the record, composition of multiple migrations, collisions, retention period and concrete application to persisted worlds.

## Consequences

- An expected category never permits reusing an occupied top-level name.
- Ephemeral symbols do not pollute the global anchor space.
- Resolution can be specified and tested without imposing an internal compiler structure.
- Moves retain traceability through an explicit tooling operation.
- Historical compatibility does not silently alter source-code meaning.

## Verification

1. Rejection of two homonymous top-level declarations of the same or different category in one path.
2. Homonymous fields valid in different owners, with different owner anchors.
3. No anchor for roles, `given`, iterators or locals.
4. Reuse of a local name in independent scopes.
5. Determinism and independence from physical order through candidate levels.
6. Descriptive diagnostic for a local symbol without fabricating an anchor.
7. Anchor change when renaming or moving between paths.
8. Explicit migration of persistent references without an implicit source alias.
