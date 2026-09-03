---
id: D-087
title: "Reflective metadata, stable descriptors and external visibility"
status: current
date: 2026-08-15
supersedes: []
superseded-by: []
questions: []
affects:
  - "postfix metadata, reflection, subordinate anchors, participants, fields and components, documentation, external visibility, file defaults, grammar, CST, AST, IR, diagnostics and tooling"
---

# ADR-087 — Reflective metadata, stable descriptors and external visibility

- Modified by: [[ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|D-101]].

- Modifies: [[ADR-036-participants-recipients-and-calls|D-036]], [[ADR-037-fields-and-declarative-domains|D-037]], [[ADR-076-named-units-prefixes-and-adjacent-notation|D-076]] and [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]].
- Extends: [[ADR-035-organisation-names-using-and-anchors|D-035]], [[ADR-051-graph-future-semantics-and-reconstructable-information|D-051]], [[ADR-070-lossless-cst-and-normalised-surface-ast|D-070]] and [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]].
- Further clarified by: [[ADR-090-functional-branches-without-public-anchor|D-090]], [[ADR-091-family-data-as-anchored-descriptors|D-091]], [[ADR-092-disponibilidad-estatica-de-propiedades-reflectivas|D-092]] and [[ADR-094-anclas-terminales-de-metadatos-configurados|D-094]].

## Context

D-085 introduced postfix metadata `~name`, `~path`, `~anchor` and `~file`, but did not fix a general reflection system or a uniform rule for author-defined metadata. It also retained runtime writes to `~name` and anonymous individual participants. The current extension needs stable descriptors for declarations and subordinate elements, structured documentation, file defaults and an explicit boundary between world state and model metadata.

## Decision

### Postfix `~` operator

The only access form is:

```mud
expression~property
```

`expression.~property` and `~~` are not part of MUD. The `~` space is distinct from the ordinary-field space.

Every `~` access is read-only during execution. No `~` property may appear as the target of a runtime assignment or update. This replaces D-085's former authorisation to write `~name` during an action. Configurable metadata changes through model editing and new elaboration, not through world effects.

`mut` is invalid in a metadata declaration. Metadata may be stored through `=` or computed through `:=`. Computed metadata may depend on changing values and be reevaluated with them, but remains non-assignable.

Metadata is not part of an alias payload, value equality, value construction, ordinary fields, outer cardinality or ordinary `thing` storage. It exists even when its owner is inactive. `create` and `destroy` do not create or remove metadata.

### Owner preamble

Configurable and user metadata is written at the start of the owner's body, before fields, components, members, participants, clauses or ordinary content:

```mud
thing Nora as Person {
    ~name = "Nora"
    ~summary = "Main person in the example"
    ~author: Text = "Samuel"

    mut health: Nat = 100
}
```

A `~...` declaration appearing after the first ordinary content of the same body is invalid. Intrinsic metadata is not declared.

### Admission principle

An element may have metadata of its own only when it jointly satisfies:

1. it exists as a stable semantic entity after resolution;
2. it has its own typed descriptor;
3. it has a stable public anchor;
4. the metadata describes the complete element, not an accidental syntactic occurrence;
5. its existence does not depend on a particular execution.

Accordingly, anchored nominal declarations, `family` members, units, stored/computed/public fields, stored/computed associated `family` data, alias components and `for`/`on`/`given` participants may be metadata-bearing.

Expressions, statements, operands, conditions, clause bodies, tokens, arbitrary AST nodes and functional branches without a stable descriptor are not. A functional-dictionary branch likewise has no public anchor: its local structural identity belongs to the owning dictionary and serves later reconstruction and analysis without becoming an anchor or symbol. `when`, `if`, `then`, `after` and `otherwise` may be reflected as present classes through `~clauses`, but their bodies do not become metadata-bearing objects.

A configured `Metadata` value does have its own descriptor and anchor for reflection and tooling, but is **terminal**: it cannot have metadata of its own and does not expose `~metadata`. D-094 fixes this deliberate exception to the admission principle.

The global `start with` declaration remains unnamed and without a public anchor, so it does not admit metadata. A test's local `start with` is part of the test descriptor, not an independent declaration, and likewise does not admit metadata.

### Common intrinsic properties

Depending on the receiver's static category, the following are exposed where meaningful:

```text
~identifier : Name
~anchor     : Anchor
~path       : MudPath
~file       : MudFile
~kind       : specific reflective family
```

`~identifier` is the source identifier. `~name` is configurable human presentation and does not participate in resolution, equality or anchor formation.

`~file` may be read in expressions. If reading `~file` influences a condition, calculation or effect that alters world behaviour, the physical-fragility warning fixed by D-085 is retained.

### Declaration reflection

Anchored declarations expose, by category:

```text
~metadata           : Metadata [* unique]
~creatable          : Bool
~destroyable        : Bool
~active             : Bool
~abstract           : Bool
~parents            : Declaration [* unique]
~ancestors          : Declaration [* unique]
~children           : Declaration [* unique]
~descendants        : Declaration [* unique]
~fields              : Field [* unique]
~declaredFields      : Field [* unique]
~components          : Component [* unique]
~declaredComponents  : Component [* unique]
```

`~parents` returns only direct parents; `~ancestors` returns the strict transitive closure and never the receiver. `~children` and `~descendants` are the inverse relations. Standard or user metadata does not appear in `~fields`.

`~metadata` materialises only configured standard metadata and the receiver's user metadata. Intrinsic properties do not appear as `Metadata` values.

### Reflective families

The following conceptual families are introduced:

```mud
family DeclarationKind {
    Thing, Alias, Family, FamilyMember, Magnitude, Unit,
    Rule, Action, Subaction, Look, Message, Test, Start
}

family RuleKind { Boolean, Reactive, Always }
family ActionKind { Action, Subaction }
family FieldKind { Stored, Calculated, Public }
family ClauseKind { When, If, Then, After, Otherwise }
family ParticipantClause { For, On, Given }
family MetadataKind { Standard, User }
```

`Start` may describe the category of a global declaration in project tooling/reflection, but does not imply that the construct has an anchor or `~metadata`.

Category hard keywords already present in the grammar may appear bare in expression position as `DeclarationKind` values: `thing`, `alias`, `family`, `magnitude`, `rule`, `action`, `subaction`, `look`, `message` and `test`. The surface form is retained as a categorical value, not as a nominal reference. `DeclarationKind` members without their own hard keyword do not receive a new literal spelling under this decision.

Categorical narrowing admits forms such as `declaration is rule`, `declaration is action`, `declaration is subaction` and `declaration is thing`. `~type` does not replace this classification.

The complete catalogue of `TypeKind` members belongs to the type-system specification; this decision does not invent that catalogue.

### Signatures and participants

The availability of a reflective property depends on the receiver's compatible static category. The fact that the grammar can recognise `expression~name` does not make that name exist for every receiver. D-092 sets this lookup boundary.

Participant properties have these capabilities by declaration subcategory:

| Subcategory | `~for` | `~on` | `~given` |
| --- | --- | --- | --- |
| Boolean rule | yes | no | yes |
| Reactive rule | no | yes | no |
| `always` rule | no | yes | no |
| `action` | yes | no | yes |
| `subaction` | yes | no | yes |
| `look` | yes | no | yes |
| `message` | no | yes | no |
| other declarations | no | no | no |

When a property is supported by the subcategory but the concrete declaration omits its optional clause, the value is `empty` with the corresponding collection type. When the property is not supported by the static subcategory, access is a static error; it does not produce `empty` or a default value. For example, `thing A` makes `A~for` invalid, whereas an `action` without a `for` clause admits `ActionName~for` and returns `empty`.

```text
~for     : Participant [* unique ordered]
~on      : Participant [* unique ordered]
~given   : Participant [* unique ordered]
~clauses : ClauseKind [* unique]
```

`~clauses` reports only the presence of clause classes; it never exposes the body AST. Its availability likewise follows the property's owner contract; the preceding rule about `empty` does not make `~clauses` or any other property universal.

Every `for`, `on` and `given` participant must have an explicit source identifier. The anonymous form admitted by D-036 is withdrawn. Order remains part of the signature, but not of persistent identity.

Each participant has a public anchor derived from:

```text
owner-anchor + clause-class + identifier
```

Position is never used as identity. Reordering participants does not change their anchors. Two same-named participants in different clauses remain distinct because the `For`, `On` or `Given` class forms part of the derivation.

`Participant` exposes:

```text
~identifier       : Name
~anchor           : Anchor
~path             : MudPath
~file             : MudFile
~owner            : Declaration
~clause           : ParticipantClause
~position         : Nat
~type             : Type
~domain           : Domain
~cardinality      : Cardinality
~mutable          : Bool
~elementsMutable  : Bool
~hasDefault       : Bool
~default          : Any [0..1]
~metadata         : Metadata [* unique]
```

A `metadata-body` attached to a participant describes the signature slot, not the received value.

A header may group several identifiers with a type and a single `metadata-body`:

```mud
for attacker, target: Fighter {
    ~category: ParticipantCategory = Combatant
}
```

The body is copied semantically to each descriptor. The group introduces neither an additional descriptor nor an additional anchor. Participants with different metadata are written as separate elements of the same clause, separated by commas.

### Fields and components

`Field` descriptors expose:

```text
~identifier ~anchor ~kind ~type ~domain ~cardinality
~mutable ~elementsMutable ~hasDefault ~default
~inherited ~declaredBy ~metadata
```

`~kind` uses `FieldKind`. Associated data declared by a `family` reuses `Field`: stored data uses `FieldKind.Stored` and calculated data uses `FieldKind.Calculated`. No `FamilyDataKind` is created. Its anchor is subordinate to the `family`; the value projected by each member obtains neither a descriptor nor its own metadata. Alias components expose the same structural contract except that `~mutable` is always `false`; this decision does not create a new `ComponentKind`.

An inherited member retains the anchor, descriptor and metadata of the element that declared it. No metadata-bearing copies are manufactured for each descendant.

Fields, components and associated data declared by a `family` may carry their own metadata. With a short value, they retain the immediate body exclusively from `~...`; when they use `ValueBlock`, those declarations may be integrated as a preamble contiguous with the beginning of the same body. In both cases they belong to the descriptor, not to the value or to the `ValueBlock` statements. A declaration does not combine both metadata locations simultaneously. A data assignment within a `family` member does not admit this body because it declares no new descriptor. A field added dynamically by an effect cannot acquire persistent metadata because it does not satisfy the admission principle.

### `Metadata` descriptor

A `Metadata` value exposes at least:

```text
~identifier  : Name
~anchor      : Anchor
~path        : MudPath
~file        : MudFile
~type        : Type
~domain      : Domain
~cardinality : Cardinality
~kind        : MetadataKind
~owner       : Declaration | Field | Component | Participant | FamilyMember | Unit
~calculated  : Bool
```

Intrinsic properties do not become `Metadata` and receive no metadata anchor. Reserved intrinsic and standard names cannot be hidden by user metadata. The anchor of configured metadata is derived as `<owner-anchor>~<metadata-identifier>`; changing its value does not change identity.

For a `Metadata` descriptor, `~path` retains its owner's logical `MudPath` and `~file` is derived from the physical provenance of the metadata declaration. Neither property materialises additional metadata. `Metadata` remains terminal and does not expose `~metadata`.

### Collections and dictionaries

Collections expose:

```text
~count       : Nat
~domain      : Domain
~cardinality : Cardinality
~unique      : Bool
~ordered     : Bool
~order       : Order [0..1]
```

Exact dictionaries add `~keyDomain` and `~valueDomain`. Functionals expose `~inputDomain`, `~outputDomain`, `~resultCardinality`, `~recursive` and `~count`, where `~count` counts branches.

Every MUD value exposes `~type: Type`. `Type` descriptors expose `~kind`, `~domain` and `~cardinality`; the concrete `TypeKind` catalogue is fixed by the type system.

### Configurable standard metadata

Standard presentation and configuration metadata are retained with these principal contracts:

```text
~name         : Name
~plural       : Text
~abbreviation : Text
~prefixes     : Prefix [* unique] = empty
~format       : Text
~summary      : Text = ""
~description  : Text = ""
~deprecated   : Text [0..1] = empty
```

`Prefix` is a built-in nominal type. The SI catalogue fixed by D-076 provides built-in `Prefix` values from `quecto` to `quetta`. Their names are ordinary identifiers resolved at the built-in level. Therefore `~prefixes = [kilo, milli]` is an ordinary MUD collection, `all` enumerates the built-in `Prefix` domain and `empty` represents the empty collection. Units retain neither `unit-property`, `prefix-selection` nor another parallel subgrammar: their body contains only general metadata declarations.

`~name`, `~summary`, `~description` and `~deprecated` are available on every compatible metadata-bearing element. `~name` defaults to a presentation derived from `~identifier`. `~summary` is a brief description; `~description` accepts presentation Markdown; a non-empty `~deprecated` activates a deprecation diagnostic but does not invalidate use.

### User metadata

A non-reserved name may declare stored or calculated metadata:

```mud
~author: Text = "Samuel"
~important := Nora~path in world.main
```

They may declare type, domain, cardinality and modifiers compatible with read-only values. They do not admit `mut`, are not inherited and do not alter the shape of the described value.

### File defaults

A file may begin, before any `using`, with defaults for stored metadata and constants:

```mud
~stability: Stability = Experimental
~summary = "Subsistema interno"

using world.shared
```

These lines are not `MudFile` metadata; they are syntactic sugar applied to top-level declarations written directly in that file and compatible with the metadata.

They do not propagate to fields, components, participants, family members, imported declarations or descendants from other files. Precedence is:

```text
explicit element value > file default > language default
```

A file default does not admit `:=`, `ValueBlock`, runtime reads or intrinsic properties. Its form remains separate from ordinary metadata assignment on an owner. `~summary`, `~description` and `~deprecated` may be used as defaults. `~name`, `~plural`, `~abbreviation`, `~prefixes` and `~format` cannot be used as file defaults because they are inherently individual. User metadata is admitted as defaults unless its definition is explicitly restricted in future.

### Text and tooling

`Text` templates interpolate an ordinary expression and use the canonical textual conversion of its value. No special `anchor{...}` interpolation exists.

The LSP and official tooling preferentially present, when available:

1. `~name` or `~identifier`;
2. structural signature;
3. `~summary`;
4. `~description`;
5. warning for `~deprecated`.

## Consequences

- Anonymous participants are no longer valid syntax.
- Anchored participants, fields and components become part of the nominal graph as persistent descriptors.
- The surface AST retains metadata declarations and bodies; typing and elaboration distinguish intrinsic properties from configured `Metadata` values. The subsequent mechanical encoding of that distinction is not yet fixed.
- Runtime writes to any `~` access are static errors.
- External visibility is derived from the owning module, its `uses` contract, the operational category and type closure; tooling presents that boundary, it does not invent it.
- `start with` contributions from modules and tests remain outside the metadata-bearing surface.

## Future verification

1. Dotless postfix reads and rejection of runtime writes.
2. Preamble before ordinary content and rejection of late metadata.
3. Stored and calculated user metadata.
4. `~metadata` reflection without intrinsic properties.
5. Mandatory names and stable `for`, `on` and `given` anchors under reordering.
6. Field, component and participant metadata-bodies, including copied groups.
7. Field inheritance without descriptor or metadata copies.
8. Absence of metadata in `start with`, clauses and bodies.
9. File defaults and explicit > file > language precedence.
10. Rejection of calculated or individual defaults.
11. `~summary`, `~description` and `~deprecated` on subordinate elements.
12. Collections and dictionaries with typed intrinsic properties.
13. Categorical narrowing of declarations.
14. Complete removal of `anchor{...}`.

## Current amendment by D-096

External visibility is derived from module, operational category and type closure. Cross-module reflection is valid only if its contract guarantees that it cannot return invisible entities; silently filtering a reflective collection to hide them is not permitted. Full tooling and reflection available to MUD code remain distinct surfaces.
