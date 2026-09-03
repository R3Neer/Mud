---
id: D-035
title: "Organisation, names, `using` and anchors"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-001"
  - "Q-014"
  - "Q-054"
affects:
  - "futuro `05-modelo-de-programa.md`, futuro `06-lexicon.md`, futuro `09-names-and-anchors.md`"
---
# ADR-035 — Organisation, names, `using` and anchors

- Amended by: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]]
- Amended by: [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|D-068]]

- Related to: [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]]
- Amended by: [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]]
- As further amended by: [[notes/decisions/ADR-065-file-level-using-header|D-065]]
- Expanded by: [[notes/decisions/ADR-072-resolution-environments-and-explicit-anchor-migrations|D-072]]
- Further expanded by: [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]]
- Related questions: Q-001, Q-014, Q-054
- Documents affected: future `05-modelo-de-programa.md`, future `06-lexicon.md`, future `09-names-and-anchors.md`

## Decision

### MUD files and paths

The path MUD is derived from the path relative within the root MUD and is not declared in the file. `namespace` it is not just superficial vocabulary and `path` is not reserved. A file may contain statements `using` and various statements of all kinds.

The file is a unit physical, not a unit from identity semantics. Each declaration store separately anchor, dependencies, node of graph, provenance and history.

Move a declaration between files within the same path does not change its anchor. Move it to another one path it does change it, unless an explicit migration is still defined by Q-014.

### Statements `using`

Statements are accepted `using` exact and recursive:

```mud
using warfare.armies
using warfare.armies.*
```

All statements `using` These form the header of the file and must appear before any declaration top-class. After the first declaration nominal or `start with` no other one can appear `using`. Its order within the header does not introduce scope sequential.

For an unqualified name, the search continues:

1. Local statements.
2. Same path from the MUD.
3. Statements `using` exact.
4. Statements `using` recursive.

A fully qualified reference avoids name ambiguity, but is only resolved if the declaration is part of the visible modular closure; this classification does not replace the authorisation `uses` from D-096. If two imported candidates provide the same unqualified name, there is ambiguity and the qualified name must be specified.

The textual order of files and statements `using` It does not decide draws.

### Identifier conventions

- Namespace: segments `lowerCamelCase` separated by full stops.
- Nominal statements (`thing`, `alias`, `family`, `magnitude`, `rule`, `action`, `test`, `look` y `message`): `PascalCase`.
- Members of a `family`: `PascalCase`.
- Fields, components, roles, `given` and iteration variables: `lowerCamelCase`.

Identifiers are case-sensitive. The list of reserved words cannot be used as the name of a field, component, role, `given`, local variable or declaration.

D-038, D-054 and D-055 distinguish between reserved words and contextual words. A contextual word is recognised only in a specific grammatical position and may be an ordinary identifier outside that position. `start` is contextual in `start with`; `abstract` is contextual before `thing`; `always` is contextual before `rule`. Metadata such as `~name` or `~prefixes` uses the general postfix grammar `~`, not special contextual tags.

`using`, `with`, `family`, `test`, `otherwise`, `ordered` and the type incorporated `Thing` These are reserved words. In particular, `ordered` It cannot be used as an identifier, even if it appears outside a declaration `family` or a specification from collection. `name` does not have a syntactic exception for the body of `thing`: the presentation The standard is configured as follows: `~name`, in a space distinct from that of ordinary fields.

### Qualified names and anchors

Qualified names use full stops:

```text
warfare.armies.Army
geometry.Square
```

Anchors use `::` and do not contain the file:

```text
thing::warfare.armies.Army
thing::warfare.armies.Army::morale
alias::geometry.Square
alias::geometry.Square::file
family::warfare.armies.Severity
magnitude::physics.Length
rule::warfare.armies.IsDestroyed
action::warfare.armies.Recruit
test::warfare.armies.RecruitIncreasesArmy
look::warfare.armies.Summary
message::warfare.armies.Destroyed
```

The root Incorporated uses the anchor confidential `thing::Thing` in accordance with D-068.

One anchor is globally unique, case-sensitive and stable with respect to changes within the same path. It is used in the graph, IR, consultations, diagnoses, traceability and semantic operations.

D-087 withdraw `anchor{...}`. The anchor Canonical access is obtained through the standard method `expression~anchor` and a template interpolates it just like any other expression: `"{expression~anchor}"`.

D-076 sets the identity stable for each unit using the identifier `lowerCamel` mandatory for its masthead.

## Consequences

- The name resolution It does not depend on the order of the files.
- The provenance physics and the identity semantics They are different dimensions.
- The compiler should detect ambiguities rather than making a choice silently.
- The migration of path It requires an explicit operation, not simply moving a file.

## Future verification

1. Several statements per file.
2. Movement in and out of the path.
3. Declaration `using` precise, recursive and ambiguous.
4. Resolution qualified.
5. Capital letter collision and reserved word.
6. Common use of a contextual word outside his special position.
7. Anchor stability.
8. Separation between `action::*`, `test::*`, `rule::*`, `family::*` and `thing::*`.
9. Reading of a anchor by means of `~anchor` and interpolation using a standard expression slot.
10. Rejection of a `using` following a declaration top-class.

## Amendment current by D-096

D-096 enter the module as a dimension semantics from visibility without incorporating it into the anchors. The MudPath nominal, and the existing anchors retain their shape. `using` continues to resolve/importando names within a `.mud`; it does not grant on its own permission to cross a modular boundary, which corresponds to `uses` in `mud.module`.

