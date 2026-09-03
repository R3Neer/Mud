---
id: D-085
title: "Functional dictionaries, metadata and structured activation"
status: current
date: 2026-08-05
supersedes: []
superseded-by: []
questions:
  - "Q-061"
affects:
  - "actions and subactions, file organisation, operators, types, dictionaries, products, absence, cardinality, selection, initial activation, Thing, Any, metadata, magnitudes, text, grammar, CST, AST, IR and diagnostics"
---

# ADR-085 — Functional dictionaries, metadata and structured activation

- Modified by: [[ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|D-101]].

- Modified by: [[ADR-086-exact-nominal-identity-external-arrows-and-algebra-de-diccionarios|D-086]]
- Modified by: [[ADR-087-metadatos-reflectivos-descriptores-estables-and-visibilidad-exterior|D-087]] and [[ADR-090-ramas-funcionales-sin-ancla-publica|D-090]]
- Modified by: [[ADR-096-modulos-callables-look-message-and-activation|D-096]].

- Modifies: [[ADR-017-everything-type-well-built-has-default-value|D-017]], [[ADR-035-organisation-names-using-and-anchors|D-035]], [[ADR-037-fields-and-declarative-domains|D-037]], [[ADR-039-collections-and-dictionaries|D-039]], [[ADR-042-shares-root-and-results|D-042]], [[ADR-047-quantifiers-and-finite-iteration|D-047]], [[ADR-049-operators-precedence-and-standardised-intervals|D-049]], [[ADR-054-canonical-definitions-and-initial-activation|D-054]], [[ADR-061-non-accepted-results-and-text-templates|D-061]], [[ADR-068-universal-thing-and-intrinsic-name|D-068]], [[ADR-074-nominal-unions-and-type-narrowing|D-074]], [[ADR-081-filtering-take-and-indexing-de-collectiones|D-081]], [[ADR-083-unitless-base-quantities|D-083]] and [[ADR-084-specialisation-de-aliases-inherited-members-and-derived-views|D-084]].
- Extends: [[ADR-051-graph-future-semantics-and-reconstructable-information|D-051]], [[ADR-052-pipelines-renderers-and-conformance|D-052]] and [[ADR-053-semantic-operator-and-authoring-flow|D-053]].
- Affected documents: chapters 05 to 09, future chapters 10 to 20, 24, 26, 32, 34 and 38, grammar, syntax models, diagnostics and semantic operations.
- Modified by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].

## Context

MUD already has collections, exact dictionaries, sequential composition through calls within `then`, nominal names, initial activation and `Text` templates. Several later decisions show four related needs:

1. Express pure policies defined by cases without introducing a general function category.
2. Uniformly separate world content from nominal and provenance metadata.
3. Allow absence and cardinality to model partial queries without turning a missing result into an immediate failure.
4. Make the boundaries between public API, internal helpers and initial catalogues of `thing` and rules explicit.

This decision consolidates those needs and replaces all incompatible earlier wording within its scope. Modified ADRs retain the history of previous rules. In accordance with D-086, the canonical public name for `A --> B` types is **functional dictionary**.

## Decision

### Auxiliary `subaction` actions

A `subaction` declaration has the same participant, `given`, guard, effect, postcondition, atomicity and anchoring contract as an `action`, with one accessibility difference:

```mud
subaction RemoveMoney for account: Account [mut]
given amount: Money {
    then account.balance -= amount
}
```

- A `subaction` may be invoked from any semantic `then` context, including that of a reactive rule.
- It cannot constitute an external request, a root command or a public API entry point.
- An `action` or `subaction` may invoke ordinary actions and subactions within the same resolution, subject to executable-cycle analysis.
- The entire chain participates in one atomic resolution. An unaccepted result or failure in any internal call also discards the callers' preceding private effects.
- Its anchor retains the `action::*` category; the public or auxiliary class forms part of the descriptor, not the anchor prefix.

The surface AST explicitly retains the `PublicAction` or `Subaction` class. Accessibility is checked after resolving the call.

### Editorial file organisation

Files should preferably group world concepts, places, processes or situations, not syntactic categories. A file such as `battle.mud` may bring together `thing`, aliases, rules, actions, views and messages that jointly describe the battle.

This rule is informative and does not affect resolution, identity, conformance or anchors. A cross-cutting relationship may occupy its own file when that better represents the domain.

### Boolean membership

Boolean membership is written with the container on the left: `container has value`. Its canonical negation is `container has not value`. `has` is a reserved word and `has not` retains two word tokens with their own trivia.

`in` is not a Boolean membership operator: it is reserved for domains, constraints, filters, bindings and conversions where applicable. The AST represents membership through `HasMember` and `HasNotMember`, not through `Membership` or `NotMembership` associated with `in`.

### Exact dictionaries

The ordinary type retains the form:

```mud
A -> B
```

An association is written `a -> b` and is an operational value. Its key is an `ExpressionBlock` and its value a `ValueBlock`; either side may use its short form or braces, and the scopes of both sides are independent. It may appear in a dictionary literal or be added explicitly:

```mud
add (a -> b) to dictionary
```

Parentheses may be omitted when precedence is unambiguous.

Exact-key application is partial:

- a present key produces its associated value;
- a missing key produces `empty` with the declared output form;
- absence does not produce `failed` by itself;
- failure appears only when the empty result does not belong to the type, domain or cardinality required by the context.

Exact dictionaries:

- retain external mutability;
- remain enumerable by keys or associations;
- admit `ordered` with its ordinary semantics;
- admit `unique`, which requires global uniqueness of associated values.

An insertion or replacement that would make the same value appear under more than one key in a `unique` exact dictionary is a complete no-op. It modifies no association and produces no `failed`.

### Functional dictionaries

The type:

```mud
A --> B
```

represents a pure policy defined by branches. A branch is written:

```mud
selector --> result
```

Within the selector and result, `value` is a contextual word bound to the input of type `A`. The selector is a Boolean `ExpressionBlock` and the result a `ValueBlock`; their local scopes are independent.

Every ordinary selector must elaborate directly to `Bool`. MUD does not implicitly insert `value`, `==`, `is` or membership: `value == expression`, `domain has value`, `value is Type` or another pure Boolean condition must be written explicitly. A bare expression that does not produce `Bool` is invalid. `_` is the fallback and is considered only when no applicable ordinary branch has produced a result.

Results and selectors may read external state. Every read must be recorded as a dependency of the branch and dictionary. All transitive calls of an application observe the same stable snapshot of the world.

Branches are externally pure during ordinary execution: they admit no effects on the world, calls to actions/subactions as effects, `create` or `destroy`. The result `ValueBlock` may declare and mutate its own temporary storage, which disappears when evaluation ends. Model editing may create, update, withdraw or move branches within the owning dictionary, but a branch has neither a public anchor nor its own metadata-bearing descriptor. The resolved model uses a local branch key: the normalised selector is the key of an ordinary branch and may not be repeated within the same dictionary; `_` uses its own unique fallback key. Changing only the result preserves the key; changing the selector structurally withdraws the old key and creates the new one. A new branch is inserted before `_` by default; an ordered functional dictionary may declare a specific position.

A functional dictionary:

- admits no external mutability;
- admits no inner `[mut]` capability;
- statically rejects any `mut` applied to its type or location;
- is not a source for `for each`;
- may refer directly or indirectly to other functional dictionaries.

Every recursive component of the call graph must have a well-founded measure that decreases strictly along every edge continuing the cycle. The compiler must prove termination through numeric descent, cardinality reduction, strictly smaller substructures or an equivalent proof. Absence of proof is a static error.

#### `ordered` mode

```mud
A --> B [ordered]
```

- Ordinary branches are tested in source order.
- The first match wins.
- Selectors may overlap and ordering forms part of the value.
- `_` must be the last effective branch; every later branch is unreachable.
- Without a match or fallback, application has derived cardinality `[0..1]` and produces `empty` when there is no result.
- With a fallback, derived cardinality is `[1]`.
- `unique` is valid but redundant; it produces a removal suggestion.

The elaborated mode is called `FirstMatch`.

#### Unordered mode

```mud
A --> B
```

- All ordinary branches are evaluated.
- Each matching branch contributes a result.
- Selectors may overlap.
- Source order is not semantic.
- Without matches, the empty collection is obtained.
- `_` contributes exactly one result only when no ordinary branch matches.
- Derived cardinality is `[0..n]`, where `n` is the demonstrable maximum of matching ordinary branches; with a fallback, the lower bound becomes `1`.
- `unique` deduplicates results produced by different branches.

The elaborated mode is called `AllMatches`.

### Arrows, composition and products

`->` and `-->` accept complete type expressions on both sides. Chains are right-associative:

```mud
A -> B -> C
```

is elaborated as `A -> (B -> C)`. The same applies to mixed chains. Each cardinality or modifier belongs exclusively to the immediately preceding arrow:

```mud
A -> B [2] -> C [3]
```

is elaborated as `A -> (B -> C [3]) [2]`.

Parentheses remain mandatory to change that grouping, to use a complete dictionary as a key, or to apply an outer collection to the complete dictionary value.

No separate function category is introduced. Composition is expressed by applying one dictionary's result as another's input; chained application `table[a][b]` consumes nested dictionaries.

Anonymous structural products are added:

```mud
(A, B)
(a: A, b: B)
```

Their values are written respectively `(x, y)` and `(a = x, b = y)`. They are structural and compared component by component. Variable names occupying a positional product do not create component names. Declared aliases remain nominal even when their representation matches an anonymous product.

Products may act as exact keys or functional inputs.

### `empty`, partial queries and cardinality

`empty` represents absence or an empty collection and is not a failure by itself. Every partial operation must produce `empty` when no result exists. Subsequent checking against the expected type, domain and cardinality decides whether that absence is valid or causes `failed`.

A missing exact query retains output form `B`. A functional `FirstMatch` query without a match produces `empty`; an `AllMatches` query without matches produces a valid empty collection.

### Cardinality omitted from stored fields

Cardinality omission is no longer universally normalised to `[1]` before the field context is known.

- In a stored field without external mutability and with an initialiser, the exact external cardinality of the initial value is inferred.
- A unit value infers `[1]`, a literal collection of three members infers `[3]` and `empty` infers `[0]`.
- The internal contents of a dictionary do not alter external cardinality: a dictionary is one value even when it contains several associations or branches.
- In a field with external mutability, omission retains `[1]`.
- A stored field without an initialiser uses the ordinary rule for its type and default, except for explicit exceptions such as `Any`.
- Calculated fields `:=` retain the form inferred from their expression or the declared form.

When the inferred cardinality of an immutable field differs from `[1]`, the compiler emits a non-blocking suggestion with a correction that materialises the exact cardinality in the source text.

The surface AST retains that cardinality was omitted; typing and elaboration determine effective cardinality and must retain sufficient provenance to distinguish `InferredFromInitializer`, `OrdinaryScalarDefault` and `Explicit`. The subsequent mechanical encoding is not yet fixed.

### Selection

The expression:

```mud
binding in source : predicate
```

is exclusively a filter. The body after `:` must be Boolean. The expression directly returns the accepted original members, without projection, additional wrapping or flattening.

It preserves multiplicity, `unique`, ordering, ordering criterion and the source's conservative cardinality inference. On an exact dictionary, pair binding produces another dictionary with the accepted associations.

### Structured initial activation

D-096 replaces category separation with a single surface. Each module may provide at most one `start with`, either directly or as a block:

```mud
start with {
    Kingdom,
    CanGrow,
    all ActivableDeclarations
}
```

Each expression contributes zero, one or more activatable `thing | rule` declarations: an individual reference contributes one, `empty` contributes zero, a collection contributes its members directly and `all D` explicitly materialises an enumerable domain. A collection of collections is invalid.

Repeated identities are deduplicated and ordering is not observable. Expressions are evaluated only with information available before runtime, and each module may activate only declarations with the same module lifecycle. Contributions from all modules are materialised jointly before initial stabilisation.

The AST retains a single `StartSet(contributions)` sequence; elaboration checks activatable category, depth and static evaluability.

### `Thing` and `Any`

`Thing` remains the built-in root of all `thing`s. It is always effective, does not appear in `start with`, cannot be declared, created or destroyed, and is excluded from the catalogue produced by `all` in a `things` section.

`Any` is the top type of all MUD values. Its open domain includes basic types—including `Money`—, `thing` identities, aliases, family members, magnitudes, intervals, collections, dictionaries, structural products and first-class descriptors of declarations and types in accordance with D-096. Implementation syntax nodes are not MUD values merely by virtue of existing.

`Any`:

- is not enumerable and rejects `all Any`;
- has no universal total ordering;
- compares equality only between compatible effective types and delegates to their equality;
- requires narrowing before a specific operation;
- retains narrowing within the functional branch where it was proven;
- has no universal default.

`Any` is an explicit exception to D-017. Every stored field of type `Any` requires an explicit initialiser.

### Postfix metadata

Metadata access uses the dotless postfix `~` operator:

```mud
value~name
value~path
value~anchor
value~file
```

`value.~name` is invalid. The operator distinguishes nominal or provenance metadata from ordinary world fields and has the same postfix precedence as `.`, `[]` and calls.

The initial built-in types are:

- `Name` for `~name`;
- `MudPath` for `~path`;
- `Anchor` for `~anchor`;
- `MudFile` for `~file`.

They are nominal types, not implicit aliases of `Text`. They may declare explicit conversions to `Text`. Templates may render them contextually without introducing general nominal compatibility.

#### `~name`

The intrinsic `.name` property and special `name = ...` form are removed. Presentation metadata is declared or overridden as:

```mud
~name = "El Castillo Negro"
```

If omitted, its initial value is derived from the unqualified nominal name. `~name` does not modify the source identifier, equality, nominal ordering, `~anchor`, `~path` or `~file`.

D-087 replaces the runtime mutability that this decision had introduced for `~name`. `~name` is configurable model metadata, but every postfix `~` access is read-only during execution. No `~` property may appear as the target of a runtime assignment or update; configurable changes are made through model editing and new elaboration. In aliases and `family` members, metadata remains separate from the immutable payload and does not alter structural equality or associated data.

Ordinary interpolation of these values uses their effective `~name`.

#### Identity and provenance

Every `~` access is runtime-read-only. `~anchor`, `~path` and `~file` are also intrinsic, non-configurable and non-declarable properties: `~anchor` produces the canonical public anchor; `~path` the MUD path; `~file` the physical provenance.

`~file` may participate in any valid expression, but the compiler emits a warning when it escapes presentation or logging, or when its dependency may alter world behaviour. Use remains valid.

For `MudPath` values, `q has p` is reflective and compares complete segments: it is true if `p == q` or if `p` descends from `q`. Negation uses `q has not p`.

#### Magnitudes and units

Special magnitude and unit properties use the same metadata family:

```mud
~name = "metro"
~plural = "metros"
~abbreviation = "m"
~prefixes = all
~format = "{hour:2}:{minute:2}:{second:2}"
```

Each metadata item retains its type, stored or calculated mode and own constraints. The `~` prefix does not imply runtime assignability.

### Templates and anchors

`anchor{expression}` is removed. An anchor is interpolated through an ordinary expression:

```mud
"{expression~anchor}"
```

`~anchor` is also a typed value usable outside templates. The template AST retains only fragments and value interpolations; `AnchorInterpolation` and its corresponding special token disappear.

## Syntactic and semantic model

The grammar and models must distinguish at least:

- `ActionDecl(PublicAction | Subaction, ...)`;
- `ExactDictionaryType` and `DecisionDictionaryType`;
- exact associations and functional branches;
- positional and named products;
- `MetadataAccessExpr` and the absence of assignable metadata targets;
- `HasMember` and `HasNotMember`;
- a single `StartSet(contributions)` for unified activation;
- omitted versus explicit cardinality;
- absence of the former intrinsic name and special anchor interpolation.

`DecisionDictionaryType` retains its historical mechanical name in accordance with D-086; it denotes the surface type of functional dictionaries and does not establish public terminology.

Elaboration must determine for each functional dictionary, and any later representation must retain or allow reconstruction of:

- `FirstMatch` or `AllMatches` mode;
- semantic ordering;
- fallback;
- result uniqueness;
- cardinality derived from application;
- external dependencies of selectors and results;
- stable local key for each branch, without a public anchor;
- termination evidence for each recursive component.

The minimum new diagnostics are:

1. external request for a `subaction`;
2. use of `subaction` as an external root or outside a semantic `then` context;
3. external or inner `mut` in `-->`;
4. non-final `_` or unreachable branches in `FirstMatch`;
5. redundant `unique` in `FirstMatch`;
6. attempt to iterate a functional dictionary;
7. functional-dictionary cycle without a descent proof;
8. inferred immutable cardinality different from `[1]`;
9. `all Any` or enumeration of `Any`;
10. `Any` field without an initialiser;
11. attempt to assign to or update any `~` access at runtime;
12. semantically fragile use of `~file`;
13. removed `.name`, `name =` or `anchor{...}` form;
14. use of the removed `things`/`rules` sections within `start with`.

## Consequences

- MUD gains pure case-based policies without introducing general functions.
- Absence is retained until an external contract requires presence.
- The external API distinguishes public actions from atomic auxiliaries.
- Initial activation gathers activatable `thing | rule` declarations per module into one deduplicated set without semantic ordering.
- Identity, presentation and provenance are separated and typed.
- Arrows and products allow structural keys and policies without weakening alias nominality.
- `Any` serves as a universal value boundary without inventing universal enumeration, ordering or defaults.

## Rejected alternatives

### Fail a partial query immediately

Rejected because it duplicates in the operator a constraint that already expresses expected cardinality and breaks composition with filters, fallbacks and optional types.

### Introduce a general function category

Rejected because the required policies are declarative values that can be inspected and edited by branch. Functional dictionaries retain that explicit structure.

### Retain `.name` and `anchor{...}` as exceptions

Rejected because it would require two parallel mechanisms for information belonging to the same metadata dimension.

### Make `Any` enumerable or give it an arbitrary default

Rejected because the domain depends on the project, mixes categories without universal ordering and contains no stable distinguished value.

## Verification

The suite must cover at least:

1. Exclusive external capability of `action`, invocation of `action`/`subaction` from `then` contexts, shared anchor and complete rollback.
2. Maximal-munch tokenisation of `-->`, `--` and `->`, and parsing of `has` and `has not`.
3. Missing exact query, operational association and `unique` values as a no-op.
4. Functional modes, overlap, fallback, derived cardinality, deduplication and prohibition of mutation or iteration.
5. Accepted and rejected termination of functional-dictionary cycles and reading one snapshot.
6. Pure and mixed arrow chains with modifiers bound to their arrow.
7. Positional and named products, structural equality and use as key or input.
8. `[0]`, `[1]` and `[n]` inference for immutable stored fields, explicitness suggestion and mutable exception.
9. Selection without wrapping, projection or flattening, including dictionary pairs.
10. Module-unified `start with`, direct and block forms, `empty`, one-level collections, deduplication, `all D` when materialising a domain and rejection of nested collections.
11. Permanent effectiveness and catalogue exclusion of `Thing`.
12. `Any`, narrowing, compatible equality, enumeration rejection and initialiser requirement.
13. Metadata reading and types; runtime read-only access for all `~`, separation of identity and `~file` warning.
14. Reflective, segment-wise membership of `MudPath`.
15. Unit and magnitude metadata.
16. Removal of `.name`, `name =` and `anchor{...}`, replaced by `~name` and `~anchor`.

## Current amendment by D-096

The structured activation section requiring separate `things` and `rules` blocks is replaced. `start with` accepts a direct contribution or a unified expression block providing activatable `thing | rule` declarations; identities are deduplicated and ordering is not semantic. Activation is aggregated per module.

`subaction` is also broadened: it may be invoked from any `then` context, not only from another action/subaction, without acquiring external root capability.
