---
id: D-094
title: "Terminal anchors for configured metadata"
status: current
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "metadata, reflection, subordinate anchors, post-typing and elaboration semantic representation, graph and tooling"
---

# ADR-094 — Terminal anchors for configured metadata

- Clarifies: [[ADR-087-metadatos-reflectivos-descriptores-estables-and-visibilidad-exterior|D-087]].
- Extends: [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]] and [[ADR-093-ast-superficial-hir-nominal-and-fase-semantica-posterior|D-093]].

## Decision

Each configured or author-defined metadata item materialised as a `Metadata` value has a public anchor subordinate to its owner's. The canonical spelling uses the same `~` separator as reflective access:

```text
<ancla-del-propietario>~<identificador-metadata>
```

Ejemplos:

```text
thing::game.Person~summary
thing::game.Person::health~description
family::game.Status::Critical~deprecated
family::game.Status::score~summary
action::game.Attack::for::attacker~summary
```

`::` continues to navigate subordinate semantic entities; `~` enters the owner's metadata space. The identifier after `~` is the canonical form of the metadata name and does not introduce a higher `metadata` category.

Intrinsic properties such as `~type`, `~path`, `~file`, `~kind` or `~anchor` itself are not `Metadata` objects, do not appear in `~metadata` and do not receive a metadata anchor. Intrinsic access remains reflective, but its existence does not materialise a configurable descriptor.

`Metadata` exposes `~anchor: Anchor`, `~path: MudPath` and `~file: MudFile`. `~path` is the owning entity's logical path within the program: entering the terminal `~<metadata>` space does not create a distinct namespace. `~file` identifies the physical file in which that metadata configuration is declared; in a direct declaration it normally matches the owner's file, but it is derived from the `Metadata` value's own provenance rather than from a stored copy of the owner's value.

These three properties are intrinsic and computed from the descriptor. They do not appear in `~metadata`, do not materialise new `Metadata` objects and do not require redundant IR fields when they can be derived from anchor, owner and provenance.

## Terminality

`Metadata` is a terminal descriptor. Although it is a stable, anchored entity, it **cannot have metadata of its own** and does not expose `~metadata`. This is a deliberate exception to D-087's general admission principle and avoids a recursive `owner~meta~meta...` tower.

## IR and resolution

Resolution derives the `Metadata` object's anchor from the owner's resolved anchor and the metadata's canonical identifier. No new source syntax appears and the superficial AST does not change.

The IR distinguishes:

- `metadata_kind`: category of configured `Metadata` objects;
- `metadata_property`: elaborated postfix property, which may be intrinsic or refer to a configurable `metadata_kind`.

An intrinsic property is never accidentally converted into `SemanticMetadata`.

## Consequences

- `Metadata` objects can be referenced stably by tooling and the graph.
- Renaming user metadata changes its anchor; changing its value does not.
- Renaming or moving the owner also changes the metadata's subordinate anchor according to ordinary anchor migration.
- Metadata on a `family` member has an anchor under the member; overriding a `family` datum remains not a descriptor and cannot have metadata.

## Verification

1. `SemanticMetadata` retains its own anchor.
2. `thing::game.Person::health~description` is a valid anchor for configured metadata.
3. No intrinsic property appears as a `Metadata` object or receives a metadata anchor.
4. The `Metadata` descriptor exposes `~anchor`, `~path` and `~file` and does not expose `~metadata`.
5. `Metadata~path` retains the owner's logical path and `Metadata~file` retains the physical provenance of the metadata declaration.
6. The superficial AST does not change because of this decision.
