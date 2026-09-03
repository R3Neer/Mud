---
id: D-086
title: "Exact nominal identity, outer arrows and dictionary algebra"
status: current
date: 2026-08-05
supersedes: []
superseded-by: []
questions: []
affects:
  - "type operators, nominal narrowing, exact and functional dictionaries, cardinality, ordering, uniqueness, AST, IR, diagnostics and normative examples"
---

# ADR-086 — Exact nominal identity, outer arrows and dictionary algebra

- Modifies: [[ADR-038-close-knit-families-with-strong-values|D-038]], [[ADR-039-collections-and-dictionaries|D-039]], [[ADR-049-operators-precedence-and-standardised-intervals|D-049]], [[ADR-057-concrete-grammar-precedence-and-continuation|D-057]], [[ADR-068-universal-thing-and-intrinsic-name|D-068]], [[ADR-070-lossless-cst-and-normalised-surface-ast|D-070]], [[ADR-074-nominal-unions-and-type-narrowing|D-074]], [[ADR-076-named-units-prefixes-and-adjacent-notation|D-076]], [[ADR-080-higher-order-collection-algebra-and-updates|D-080]], [[ADR-084-alias-specialisation-inherited-members-and-derived-views|D-084]] and [[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]].
- Extends: [[ADR-051-graph-future-semantics-and-reconstructable-information|D-051]] and [[ADR-052-pipelines-renderers-and-conformance|D-052]].
- Affected documents: chapters 02 and 04 to 09; future chapters 10, 12, 15, 16, 19, 20, 34, 38, 40, 41, 44 and 47; grammar; CST; Surface AST; semantic representation after typing and elaboration; conformance cases.

## Context

D-085 introduced exact dictionary types `A -> B` and branch-defined dictionaries `A --> B`, together with anonymous products, absence through `empty`, postfix metadata and right-associative arrows. The first integration left three issues incomplete:

1. The relationship between unions and arrows did not expressly prevent a dictionary from appearing as a partial alternative of a union, even after aliases were resolved.
2. `is` cannot distinguish transitive nominal membership from exact nominal identity, a distinction needed when ordering branches that refine specialised aliases.
3. The existing conjunctive operators lacked semantics specific to exact dictionaries and branch-defined dictionaries.

In addition, the numbered documentation retained examples and explanations incompatible with D-085. This decision fixes the new semantics; correcting those examples is part of its documentary integration, but creates no additional decisions.

## Terminology

The canonical public name of `A --> B` becomes **functional dictionary**. The expression **decision dictionary** remains as D-085's historical term and as a description of its branch-based implementation, but is not the preferred name in the current specification.

The mechanical identifiers `DecisionDictionaryType`, `DecisionBranchExpr` and `DecisionApplyExpr` are retained in the first version of the schemas to avoid introducing a nominal migration without semantic value. They should be understood as the representation of case-defined functional dictionaries.

## Decision

### Precedence of `|`, `->` and `-->` in types

The type-union operator `|` has higher precedence than `->` and `-->`. The two arrows have the same precedence and are right-associative.

```mud
A | B -> C | D
```

is equivalent to:

```mud
(A | B) -> (C | D)
```

```mud
A | B --> C | D
```

is equivalent to:

```mud
(A | B) --> (C | D)
```

```mud
A -> B -> C
```

is equivalent to:

```mud
A -> (B -> C)
```

Each cardinality, ordering, uniqueness or capability specification belongs exclusively to the immediately preceding arrow:

```mud
A -> B [2] --> C [3 ordered]
```

is elaborated as:

```mud
A -> (B --> C [3 ordered]) [2]
```

### The arrow as a complete outer form

An arrow must constitute the complete outer form of the type in which it appears. An exact or functional dictionary cannot be a partial alternative of a union. Parentheses do not bypass this restriction.

The following are invalid:

```mud
value: A | (B -> C)
value: (A -> B) | C
value: A | (B --> C) | D
value: (A -> B) | (C -> D)
```

The following are valid:

```mud
value: (A | B) -> C
value: A -> (B | C)
value: (A | B) --> (C | D)
value: A -> (B -> C)
```

The restriction is checked after resolving aliases. If an alias's effective outer form is an arrow, it likewise cannot be used as a union alternative:

```mud
alias Lookup := B -> C

value: A | Lookup       # invalid
value: A -> Lookup      # valid
```

The EBNF may retain parenthesised groupings to produce a useful CST; validation after resolution rejects the prohibited outer forms.

### Exact nominal operator `iis`

`iis` is a non-chainable infix operator whose result is `Bool`. The left operand is a value and the right operand must resolve to a nominal type.

```mud
value iis PersonId
```

is true only when the value's effective nominal type is exactly `PersonId`.

`is` and `iis` are distinct:

```mud
value is T
```

checks membership in `T`, including its specialisations.

```mud
value iis T
```

checks exact nominal identity.

Let:

```mud
alias Identifier := Nat
alias PersonId as Identifier
alias EmployeeId as PersonId
```

For a value whose exact type is `EmployeeId`:

```mud
value is Identifier    # true
value is PersonId      # true
value is EmployeeId    # true

value iis Identifier   # false
value iis PersonId     # false
value iis EmployeeId   # true
```

The same rule applies with multiple specialisation. For `alias C as A, B`, an exact `C` value satisfies `is A`, `is B` and `is C`, but only `iis C`.

### Exact negation `iis not`

`iis not` is the direct derived form of negating the exact test:

```mud
value iis not PersonId
```

is equivalent to:

```mud
not (value iis PersonId)
```

`not iis` is not added. The parser retains whether `iis` or `iis not` was written through the polarity of the exact node; the formatter may preserve the source form.

### Narrowing

- `value is T` retains `T` and its possible specialisations.
- `value iis T` retains only the exact nominal possibility `T`.
- `not (value is T)` removes `T` and all its specialisations.
- `not (value iis T)` and `value iis not T` remove only the exact possibility `T`; specialisations remain possible.

Flow analysis must apply these rules to nominal unions and multiple specialisation.

`iis` does not replace `==`. Equality compares values according to their type and content; `iis` only inspects the left operand's effective nominal type.

The exact identity of a singleton `thing` continues to be checked through `==`:

```mud
place == Madrid
```

Membership of a `thing` in a category is checked through `is`:

```mud
place is City
```

The right operand of `iis` cannot be an anonymous product, structural union, dictionary, non-nominal type expression or singleton identity such as `Madrid`.

### `iis` in functional dictionaries

`iis` may select a branch and narrow `value` within its result:

```mud
describe: Identifier --> Text [ordered] =
    value iis EmployeeId --> "Employee {value}",
    value iis PersonId --> "Person {value}",
    value is Identifier --> "Identifier {value}"
```

Order is significant because an `EmployeeId` also satisfies `value is PersonId`.

## Exact-dictionary algebra

The `|`, `&`, `--` and `^` operators act on the key domains of two compatible exact dictionaries. When an operation retains a key present in both operands, the left operand's association prevails.

Let:

```mud
left: Key -> Value =
    a -> 1,
    b -> 2

right: Key -> Value =
    b -> 9,
    c -> 3
```

### Exact union `|`

```mud
left | right
```

produces:

```mud
a -> 1,
b -> 2,
c -> 3
```

Formally:

```text
domain(L | R) = domain(L) ∪ domain(R)
(L | R)[k] = L[k] if k ∈ domain(L); R[k] otherwise
```

It is not necessarily commutative as a dictionary value.

### Exact intersection `&`

```mud
left & right
```

produces:

```mud
b -> 2
```

Formally:

```text
domain(L & R) = domain(L) ∩ domain(R)
(L & R)[k] = L[k]
```

It has the same key set as `R & L`, but not necessarily the same associations.

### Exact difference `--`

```mud
left -- right
```

produces:

```mud
a -> 1
```

It retains left associations whose keys do not appear on the right.

### Exact symmetric difference `^`

```mud
left ^ right
```

produces:

```mud
a -> 1,
c -> 3
```

It retains only keys present in exactly one operand. `^` is admitted on exact dictionaries even though their keys are inherently unique, because it operates on key membership and does not require reinterpreting value uniqueness.

### Properties and ordering

- `|` and `&` are associative and commutative with respect to the key set, but not necessarily as dictionary values because of left precedence.
- `--` is neither associative nor commutative.
- `^` is associative and commutative.
- `L | R` retains `L` associations first and then adds `R`'s new keys.
- `L & R` and `L -- R` filter `L` without reordering it.
- `L ^ R` retains `L`'s exclusive associations first and then `R`'s exclusive associations.
- An `ordered by` criterion normalises the content after calculating it.

### Interaction with `unique`

In an exact `[unique]` dictionary, no value may be associated with two different keys. The operation incorporates left associations first and then the corresponding right associations. A right association that would violate `unique` is omitted as a no-op and produces no `failed`.

```mud
left: Person -> Room [unique] =
    Ana -> BlueRoom

right: Person -> Room [unique] =
    Luis -> BlueRoom,
    Marta -> RedRoom
```

`left | right` produces `Ana -> BlueRoom, Marta -> RedRoom`.

The key and value types of both operands must be compatible. The result retains common types, required uniqueness, demonstrable ordering and conservatively derived cardinality.

## Functional-dictionary algebra

Set operators do not compare or merge branches, selectors, fallbacks or source orderings. Their semantics are extensional and pointwise over the result of applying both dictionaries to the same input.

For any operator `op` among `|`, `&`, `--` and `^`:

```text
(F op G)[x] = F[x] op G[x]
```

The right-hand operation is the ordinary collection operator. `F[x]` and `G[x]` are computed on the same input and snapshot of the world before being combined.

### Functional union `|`

```text
(F | G)[x] = F[x] | G[x]
```

It includes results produced by either operand. There is no left precedence between functional results.

### Functional intersection `&`

```text
(F & G)[x] = F[x] & G[x]
```

It retains results produced by both.

### Functional difference `--`

```text
(F -- G)[x] = F[x] -- G[x]
```

It removes from `F`'s results the multiplicities produced by `G`.

### Functional symmetric difference `^`

```text
(F ^ G)[x] = F[x] ^ G[x]
```

It retains results produced by exactly one of the operands and preserves the ordinary uniqueness constraints of collection symmetric difference.

### Ordering and cardinality

Two `ordered` functionals individually produce at most one result. Their combination retains `ordered` only when maximum cardinality per application remains `[0..1]`.

- `F | G` may produce two distinct results and generally loses `ordered`.
- `F & G` produces at most one and may retain `ordered`.
- `F -- G` produces at most `F`'s result and may retain `ordered`.
- `F ^ G` may produce two and generally loses `ordered`.

If one or both operands are not `ordered`, the compiler may retain it only when it proves the same maximum bound.

For:

```text
F[x] : B [fmin..fmax]
G[x] : B [gmin..gmax]
```

the following conservative approximations are initially admitted:

```text
F | G  : B [max(fmin, gmin)..fmax + gmax]
F & G  : B [0..min(fmax, gmax)]
F -- G : B [0..fmax]
F ^ G  : B [0..fmax + gmax]
```

Analysis may narrow them using `unique`, finite domains or demonstrable overlap information.

### `unique`, fallback and dependencies

`unique` deduplicates the collection produced by each application. It may matter when combining two `ordered` functionals, even if redundant on each isolated operand.

Fallbacks belong to each operand. `F[x]` and `G[x]` are first evaluated with their own branches and `_`; the results are then combined. No joint fallback is created or merged.

The compound's external dependencies are the union of both operands' transitive dependencies:

```text
dependencies(F op G) = dependencies(F) ∪ dependencies(G)
```

The operation remains pure and deterministic with respect to the common snapshot.

### Equality

Defining the algebra extensionally does not turn general functional equality into an equivalence proof for every input. `F == G` remains subject to nominal or structural rules defined separately.

## Common restrictions

- Only dictionaries of the same class are combined: exact with exact and functional with functional.
- `->` and `-->` are not combined directly.
- Input and output types must be compatible.
- Operators are pure and produce no effects.
- Evaluation retains ordinary snapshot and atomicity.
- No operator is introduced that selects the left side if it produces something and the right side otherwise.

## Syntactic and semantic representation

The surface AST retains `iis` through:

```text
ExactTypeTestExpr(valueExpression, nominalTypeReference, negated)
```

- `negated = false` for `iis`.
- `negated = true` for `iis not`.

The right operand is resolved during elaboration. Structural types and singleton identities are rejected during typing/elaboration before a valid elaborated result is obtained.

Set operations may remain `BinaryExpr` in the surface AST because their class depends on resolved types. Elaboration must distinguish operations on exact dictionaries from operations on functional dictionaries and determine their result type. The subsequent mechanical form of that distinction is not yet fixed.

A set operation on functionals is equivalent to applying both operands in the same snapshot and then applying the collection operation to their results. A merged list of branches is never materialised and no attempt is made to prove logical equivalence between selectors.

Elaboration must likewise distinguish the transitive nominal membership of `is` from the exact nominal identity of `iis`. The surface AST retains both forms; any later representation must preserve or allow reconstruction of that distinction without this decision fixing concrete node names.

## Required diagnostics

An implementation must diagnose at least:

- an arrow used as a partial union alternative;
- an alias whose effective outer form is an arrow inside a union;
- a non-nominal right operand of `iis`;
- a singleton identity to the right of `iis`;
- chaining `iis` or `iis not`;
- combining an exact and a functional dictionary;
- incompatible input types;
- incompatible output types;
- demonstrated loss of `ordered` when a declared form requires it;
- use of `^` when the resulting collection type does not satisfy its uniqueness requirements.

Inferred loss of `ordered` is not a failure by itself when the context permits an unordered type; it must, however, be explained in the incompatibility diagnostic when an outer annotation requires retaining it.

## D-085 coverage closure

This version incorporates, as part of the same normative unit, the documentary and mechanical gaps left outside D-085's first integration. In particular, conformance must also cover:

- internal calls, root inaccessibility and atomic rollback of `subaction`;
- `has` and `has not` on `MudPath`, with the container on the left, and rejection of invalid chains;
- querying, replacement, key and association iteration, product keys and `unique` no-op in exact dictionaries;
- explicit equality, membership and Boolean-condition selectors; rejection of implicit selectors; fallback, external reads, domain application and functional termination;
- cardinalities and deduplication of `FirstMatch` and `AllMatches`;
- chained application and dictionary composition;
- structural product compatibility and separation from nominal aliases;
- selection as a direct filter that neither projects, flattens nor wraps and that preserves exact associations;
- `create Thing`, `destroy Thing` and `all Any` errors;
- catalogue, typing, mutability and warnings for postfix metadata;
- inference of `[0]`, `[1]` and greater cardinalities, including dictionaries as one outer value;
- `iis` with multiple specialisation and exact narrowing.

The corresponding normative examples belong to numbered chapters 05 to 09. Future chapters listed in the index must retain or refine them when drafted, but may not refer only to this ADR.

## Consequences

- Arrows retain a uniform reading and cannot be hidden inside unions through aliases.
- `iis` allows branches to be ordered from exact nominal cases to more general membership without confusing value equality.
- Exact algebra follows key identity and retains left precedence.
- Functional algebra composes policies without inspecting their branch implementation.
- Ordering and cardinality inference form part of the result's elaborated type.
- Normative examples in numbered chapters must show positive, combined and invalid cases.

## Rejected alternatives

### Interpret `F | G` as left preference

Rejected because it would confuse union with a fallback operation. Functional union combines result collections.

### Merge functional branches

Rejected because it would require logical equivalence of selectors, special handling of `_` and source-order normalisation.

### Represent `iis` as `==` on exposed type descriptors

Rejected because it would expose an implementation representation and lose `iis`-specific narrowing rules.

### Allow parenthesised arrows inside unions

Rejected because it would make dictionary queryability depend on groupings that are difficult to elaborate and would allow the restriction to be bypassed through aliases.

## Verification

The suite must cover:

1. arrow precedence and associativity;
2. rejection at the surface and after alias resolution;
3. `is`, `iis`, `iis not` and `==` over specialisation chains and diamonds;
4. positive and negative exact narrowing;
5. the four operations on exact dictionaries with collisions;
6. ordering and interaction with `unique`;
7. the four functional operations on results with and without overlap;
8. loss and retention of `ordered`;
9. dependency union and the same snapshot;
10. rejection of exact/functional mixing;
11. expected AST and IR without branch merging;
12. absence of constructions removed by D-085 in valid examples and schemas;
13. `subaction` calls and rollback;
14. selectors, fallback, dependencies and functional termination;
15. direct selection, `Any`, metadata and the omitted-cardinality matrix;
16. positive and negative cases enumerated by the D-086 v4 coverage validator.
