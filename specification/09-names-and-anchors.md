---
title: Names, paths and anchors
aliases:
  - Name resolution by MUD
tags:
  - mud/specification
  - mud/nombres
status: proposed
normative: true
depends-on:
  - "[[05-source-text]]"
  - "[[08-abstract-syntax]]"
questions:
  - Q-014
decisions:
  - D-101
  - D-035
  - D-065
  - D-072
  - D-078
  - D-085
  - D-086
  - D-087
  - D-088
  - D-090
  - D-091
  - D-093
  - D-094
  - D-096
  - D-097
  - D-100
---
# 09. Names, paths and anchors

## State and purpose

This chapter defines which names a programme introduces, how they are resolved, and which ones have persistent identity. A file and an declaration are distinct entities: the path provides logical context, but is not part of the file’s written syntax.

## MUD Paths

> [!definition] MUD-NAME-001 — Path de MUD
> The path of a file is the sequence of segments `lowerCamel` derived from its relative path under the programme’s root, excluding the file name and its extension.

There is no declaration `namespace` or reserved word `path`. An editor may display the path as a virtual header and offer options to copy qualified names or anchors, but that presentation does not belong to the source text.

A qualified name concatenates path and the nominal name using dots:

```text
game.combat.Heal
```

Moving an declaration between files within the same path does not change its qualified name. Moving it between paths does.

## Symbols and namespaces

> [!rule] MUD-NAME-002 — Single upper nominal space
> All top-level declarations within the same path must have distinct names, regardless of their category.

The expected category does not resolve ambiguity between two homonymous parent statements. Nested fields and members belong to the scope of their owner and may have the same name under different owners.

Participants `for`, `on` and `given` are lexical symbols with a stable subordinate anchor according to the model of descriptors. Iterators and ordinary local bindings continue without public anchor. Names may be repeated in independent scopes, but may not shadow a name that is already in scope.

> [!rule] MUD-NAME-003 — Mandatory conventions
> Nominal declarations and members of family use `PascalCase`; fields, components, roles, `given`, variables and segments of path use `lowerCamel`; identifiers in unit use `lowerCamel`. A violation is a static error with a mechanical fix when there is a single safe correction.

## Environments of resolution

Let $Gamma$ be an environment and let $n$ be an unqualified name. The resolution query has the following levels:

1.  Symbols from the scope lexicon.
2. Members of the implicit owner or receiver.
3. Statements by the current path.
4. Statements provided by `using` are accurate.
5. Statements provided by recursive `using`s.
6.  Names included.

> [!rule] MUD-NAME-004 — First non-empty level
> The resolution uses only the first level that produces candidates. If none of its candidates belong to the required category, the reference is invalid; it does not proceed to subsequent levels.

Candidates that refer to the same anchor are deduplicated. Two different anchors at the same level result in ambiguity. The textual order of files and `using` does not resolve ties.

An exact `using` imports a specific path, whilst a recursive one imports its descendants. Neither re-exports the `using`s contained in the files reached. A fully qualified reference avoids level-by-level searching.

`Prefix` appears at the top-level as an embedded type. The SI names `quecto`…`quetta` are also resolved there as built-in constants of `Prefix`; they do not introduce declarations or anchors of their own.

Access paths with nodes are constructed in stages: first, the nominal root is resolved, and then each member is resolved using the resulting type or owner. A qualified path and a chain of members may share surface writing without sharing internal resolution.


## Local scopes, iteration and blocks

Iteration bindings and all local declarations are `LocalSymbol`: they do not receive public anchor and are subject to the first lexical level of resolution. The HIR’s `kind` distinguishes, at a minimum, between iterators, computed locals and stored locals; mutability is a capability checked at a later stage and not a category of anchor.

In `ExpressionBlock` and in the shared preambles of action/rule/message, only pure computed locals are introduced. Each local variable is visible from the next declaration until the end of the block owner and cannot shadow a visible name.

`ValueBlock` creates its own lexical scope. Its computed and stored declarations are introduced sequentially. An `LocalForEach` resolves `source` and `by` before introducing its binding; the binding is visible in the filter and in `LocalStatementBlock`. Locals created within an iteration do not survive into the next one. A mutation may refer to a mutable local variable of an enclosing scope of the same `ValueBlock`; the check that the final destination does not escape the block is part of type checking/elaboration.

In the `for each` executable, the same rules for introducing bindings apply, but the body belongs to `EffectBlock` and can write to external locations in accordance with its authority. In a selection or quantifier, the binding exists only within its `ExpressionBlock`.

In associations `->` and branches `-->`, the left and right blocks create sibling scopes: the /selector-scoped locals are not visible in value/resultado. Both can see the common outer environment, and the function branches also retain their contextual bindings `value` where applicable.

The calculated and stored locals still do not satisfy a public anchor. A mutable stored local may satisfy participant `for mut`; nominal resolution binds the name to `LocalSymbol`, whilst typing/elaboration checks ensure that the occurrence used as receiver refers to a writable slot. The Nominal HIR does not require a reference class or any additional symbol.

No local scope permits forward references, loops, redeclarations or shading of a name that is already visible.

## Stages

1.  The Surface AST provides names and provenance.
2.  The nominal resolution creates symbols, scopes, bindings and anchors, and instantiates them in the Nominal HIR of `nombres/mud-nominal-hir.asdl`.
3. The type system consumes Surface AST + Nominal HIR and resolves unions, domains and references dependent on type.
4. The elaboration covers accesses, calls, contextual abbreviations and other type-dependent meanings; its subsequent mechanical representation has not yet been finalised.

The Nominal HIR does not contain effective types, effective domains, cardinalities or proofs from termination. It is the contract between name resolution and typed, not a resolved copy of Surface AST.

The specification is expressed in terms of environments and sets of candidates. An implementation may use scope graphs provided that it accurately reproduces priorities, candidates, ambiguities and rejections.

## Anchors

> [!definition] MUD-NAME-005 — Public anchor
> An anchor is the human-readable, global, case-sensitive identity of a semantics to which the specification assigns a public identity.

Typical forms:

```text
thing::game.people.Person
thing::game.people.Person::friends
alias::game.ids.UserId
family::game.rules.Severity
family::game.rules.Severity::Critical
family::game.world.Terrain::movementCost
magnitude::physics.Length
unit::physics.Length::meter
action::game.combat.Heal
type::Nat
type::Prefix
thing::game.people.Person::friends~summary
```

The canonical form is `<category>::<qualified-name>` and, for a nested declaration, `::<member>` is added for each owner. Configured metadata adds `~<metadata-identifier>` to its owner's anchor. MUD identifiers do not contain `::` and `~` belongs to the reserved postfix space, so both separators are unambiguous. The MUD 1.0 category catalogue is:

| Declaration | Category: anchor |
|---|---|
| `thing` and their fields | `thing` |
| alias, their components and their derived fields | `alias` |
| family, data and members | `family` |
| magnitude | `magnitude` |
| unit declared | `unit` |
| any of the three types of rule | `rule` |
| action | `action` |
| look | `look` |
| message | `message` |
| test | `test` |
| type incorporated | `type` |

The participants `for`, `on` and `given` do not introduce a new superordinate category: their anchor is subordinate to that of owner and is also derived from the clause class and the identifier, in accordance with the model of descriptors. The position is never part of that identity.

`start with` of module does not introduce a name and therefore does not have anchor. The category describes the parent declaration: an field of `look` retains an anchor as `look::game.Status::score`, not an additional category `field`.

They have anchor:

- first-order nominal statements;
-  fields, components and associated data declared by an `family`;
-  members of family;
-  units reported;
-  participants `for`, `on` and `given`;
-  configured and user metadata represented as `Metadata`;
-  built-in types.

They do not have public anchor:

-  local or iteration variables;
-  temporary appointments other than registered participants;
- interim results;
- units created structurally by prefixes;
-  the built-in values `Prefix`, which are defined as constants rather than declarations;
-  the branches of functional dictionaries, which are identified only locally within their dictionary owner;
- intrinsic reflective properties, which do not materialise objects `Metadata`.

An associated data item declared by an `family` has a stable subordinate anchor formed from the category `family`, the qualified family name and the data identifier. That anchor identifies the descriptor of the uniform schema, not every value obtained by querying an member. An assignment within the body of an member does not introduce an anchor and does not alter that of the declared data.

An inherited member retains the anchor of the owner that declared it. In `thing`, this does not share state; in aliases, it identifies the source used to deduplicate diamonds. A default override does not introduce a new member or anchor.

An diagnostic can describe a local symbol using the anchor of its owner:

```text
action::game.combat.Heal - given amount
```

The full description does not constitute a new anchor.

## Contextual value names

An member of family may be abbreviated when the expected type determines the family:

```mud
severity: Severity = Critical
```

`Severity.Critical` remains available. Units follow the same rule for magnitude, identifier, `name`, plural and abbreviation. If two values remain possible, further specification is required.

## Migration

Renaming, changing the category or moving between paths alters the anchor. The tooling records a directed mapping from the previous one to current. This mapping can migrate persistent references and history, but never converts the old name to alias, which is supported by the compiler.

The external format and the complete cycle record remain open in [[notes/questions/Q-014-m-anchor-migration|Q-014]].

## Nominal graph initial

After the nominal resolution, a partial graph is constructed using resolved symbols. The Nominal HIR retains exactly these edge families:

- `Owns`: nominal property or containment;
- `Specializes`: nominal specialisation between declarations;
- `RefersTo`: a nominal reference whose source and destination are already resolved symbols.

Types and effective domains, elaborate initialisation, calculations, reads, writes, effects, derived magnitudes and other type-dependent relationships do not belong to this phase. They are determined, where applicable, during subsequent typing and elaboration phases.

The partial graph does not replace the AST nor does it constitute an source of truth. Its sole purpose is to implement the conclusions of nominal resolution that are to be retained as contract between Surface AST and the type system.

## Conformidad

An conforming implementation must produce the same candidates and anchors, reject the shading and collisions indicated, preserve the provenance and allow the nominal graph to be reconstructed from the source programme.

## Alias specialisation

`alias` declarations can provide specialisation aspects. nominal graph retains the written direct predecessors, and the closure `is` is computed during elaboration. Inherited members retain the anchor of their origin. The nominal resolution preserves independent contributions; their possible fusion by equivalence or their explicit resolution depend on typing and elaboration, not on the nominal order of `as`.


## Metadata, descriptors and subordinate anchors

Reflective access `~` distinguishes between intrinsic properties and configured metadata: `~identifier` is the source identifier, `~name` is configurable presentation, and all `~` accesses are runtime-readonly. Only stable semantic entities with descriptor typing and public anchor possess their own metadata: nominal declarations, members of `family`, units, fields, components and participants. Expressions, clause bodies and both `start with` are excluded as owners; that of module remains without anchor.

All participant `for`, `on` and `given` have a name and a subordinate anchor based on owner, a clause type and an identifier. The position is not part of identity. Participants are anchored symbols; ordinary locals remain as `LocalSymbol`. Inherited members retain descriptor, anchor and metadata from their original declaration. `~metadata` lists only configured metadata, never intrinsic properties.

Each configured value `Metadata` in turn has an terminal anchor formed by adding `~<identificador-metadata>` to the anchor of the owner, for example `thing::game.Person::health~description`. That anchor is used for reflection and tooling; it does not convert `Metadata` into owner from other metadata.

`Metadata` specifies `~anchor`, `~path` and `~file`. Its `~path` is the logical path of the owning entity, and its `~file` comes from the physical file where that metadata configuration was declared. Entering `~<identificador-metadata>` changes the terminal identity, not the logical namespace. These properties are intrinsic to the descriptor and do not appear in the collection `~metadata`. `Metadata~metadata` is not part of the contract.

## Local keys for functional branches

> [!rule] MUD-NAME-006 — Without public anchor from branch
>  A functional dictionary branch does not introduce an anchored symbol, a public name or a metadata owner. Its persistent identity is that of the dictionary in which it is contained.

Each functional branch has a structural `decision_branch_key` local to the dictionary for phases requiring reconstruction or subsequent dependencies. For an ordinary branch, the key is the canonical form of the resolved selector. Two ordinary branches with the same canonical form within the same dictionary are invalid: they would share the same local structural key. `_` uses a distinct and unique `FallbackBranchKey` key. That key is not an symbol, does not belong to the Nominal HIR and its subsequent mechanical representation is not yet fixed. The source ordinal is retained separately because it features in `FirstMatch`, but it is not converted to anchor either.

Tooling operations requiring a persistent reference must refer to the owner dictionary and then specify the structural edition of its set or sequence of branches. `CREATE`, `UPDATE`, `REMOVE` and `MOVE` cannot treat an branch as an independent global entity.

Functional join operations do not create or merge global keys of branch: the composite node retains references to both operands, and its graph dependency is the transitive union of the two.

## Path ownership

Regarding `MudPath`, the membership operator uses `q has p`: it is reflexive and compares entire segments. The negation form uses `q has not p`:

```mud
world.combat has world.combat                  # true
world.combat has world.combat.melee            # true
world.combat has world.combatant                # false
world.combat has not world.trade                # true
```

## Identity exact nominal

`is` query specialisation closure; `iis` compares exact effective nominal type. The narrowing of `iis not` eliminates a single nominal possibility and does not eliminate its specialisations. This distinction does not create new anchors nor does it replace the singleton identity equality via `==`.

## Modules, `uses` and anchors

Membership of module is a dimension of visibility and a dependency, not an additional component of the nominal anchor. `uses` authorises knowledge of the contract of another module; an `using` does not grant that authorisation. Cross-resolution can only reach operations and types belonging to the visible closure of the modular contract.

