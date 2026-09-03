---
id: D-101
title: "Value blocks, stored local variables and witness extrema"
status: current
date: 2026-08-29
supersedes: []
superseded-by: []
questions: []
affects:
  - "ExpressionBlock, ValueBlock, EffectBlock, local variables, for each, fields, aliases, family, dictionaries, metadata, participants, min, max, grammar, CST, AST, resolution and consolidation"
---
# ADR-101 — Value blocks, stored local variables and witness extrema

- Modifies: [[ADR-036-participants-recipients-and-calls|D-036]], [[ADR-037-fields-and-declarative-domains|D-037]], [[ADR-038-close-knit-families-with-strong-values|D-038]], [[ADR-047-quantifiers-and-finite-iteration|D-047]], [[ADR-066-static-values-and-local-bindings-in-then|D-066]], [[ADR-071-local-bindings-in-boolean-blocks|D-071]], [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]], [[ADR-087-metadatos-reflectivos-descriptores-estables-and-visibilidad-exterior|D-087]], [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]], [[ADR-095-empty-extrema-as-ordinary-absence|D-095]], [[ADR-096-modulos-callables-look-message-and-activation|D-096]] and [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].
- Retains the `given` default as a closed static expression in accordance with D-063 and D-066.

## Context

MUD already distinguished declarative expression blocks and executable effect blocks, but that division left no dedicated form for constructing a value through temporary local storage. It also did not allow stored local variables in `then`, forced every `for each` to be modelled as an effect, and left `sum`, `min` and `max` in an overly heterogeneous aggregation family.

The extension must preserve two deliberate language boundaries: a value computation cannot acquire observable effects, and `if` does not become a general statement inside calculation blocks.

## Decision

### Three body contracts

`ExpressionBlock` contains zero or more pure calculated locals `:=` and exactly one final expression. It admits no stored variables, mutation, `for each` as a statement or inner `if`.

`ValueBlock` constructs exactly one value through zero or more `ValueStatement` items and a final expression. Its statement catalogue is closed to:

1. local calculated declaration;
2. local stored declaration, mutable or immutable;
3. local mutation;
4. `LocalForEach`.

`EffectBlock` executes observable consequences. It admits the calculated and stored local declarations above, in addition to ordinary effects. A `then` remains invalid if it contains neither an observable effect nor an executable call.

Blocks are not general primary expressions. They appear only in explicit owner slots. Arguments, indices, literal elements, ordinary effect RHSs and other `expression` positions do not acquire inline blocks.

### Outer purity of `ValueBlock`

A `ValueBlock` may modify only storage created within its own boundary. The check uses the target's final footprint, not merely the initial identifier: a local leading to external state does not authorise writing that state.

It admits no effects on the world, `create`, `destroy` or calls to actions/subactions as effects. A local variable declared in an enclosing scope of the same `ValueBlock` may be modified from an inner `LocalForEach`.

There is no `if` statement inside `ExpressionBlock`, `ValueBlock` or `LocalStatementBlock`. Value choice, filtering, extrema, absence and narrowing continue to be expressed with MUD's declarative constructs.

### Stored local variables

In addition to `x := value-body`, the following are admitted:

```mud
x: X = value-body
mut x: X = value-body
```

`:=` does not create an assignable location. `x: X =` creates a non-reassignable stored local slot and `mut x: X =` a reassignable one. The local initialiser is evaluated when the declaration is reached and may read runtime state when the context permits.

Stored variables admit the complete type/value form compatible with their owner. Slot mutability and the inner capability of its value are orthogonal.

A calculated local may be a `given` or a readonly `for` participant. An immutable stored local may be a `given` or readonly `for`. A mutable stored local may also satisfy `for mut`. The call temporarily binds the participant to the slot; it introduces neither first-class references nor copy-in/copy-out, and a failure also reverts modifications to that slot under ordinary atomicity.

### Local `for each`

Within `ValueBlock`, `for each` uses `LocalStatementBlock`, which contains only `ValueStatement` items and has no final expression of its own. Its filter remains a Boolean `ExpressionBlock`.

In an iteration with semantic order, a mutable outside the loop but inside the owning body is observed sequentially between iterations. In an iteration without semantic order, all iterations start from the same prior projection and their modifications to an outer mutable are consolidated as concurrent. A set of compatible `+=` operations uses general arithmetic consolidation; several absolute `=` assignments do not thereby acquire accumulator semantics.

Each iteration retains an independent local scope.

### `ExpressionBlock` owners

The following use `ExpressionBlock`: Boolean rules, `always`, `when`, `if` guards, action `after`, `for each` filters, selection, `exists`, `forall`, `count`, `min`, `max`, exact-dictionary keys and functional-dictionary selectors. Functional selectors and the bodies of the five quantifiers listed elaborate to `Bool`, except for the temporally distinct contracts already fixed for `when`.

### Witness extrema

`min` and `max` use an `ExpressionBlock` as a Boolean predicate. Among accepted witnesses, `min` returns the first and `max` the last according to the source's semantic order. An `ordered` source, even without an explicit key, provides sufficient order. A source without usable semantic order is invalid. No accepted candidate produces `empty` with the ordinary partial cardinality of extrema.

`by` retains exclusively its progression meaning when the source admits it; `min` and `max` introduce no ordering criterion of their own.

### `ValueBlock` owners

The following may use a short form or `ValueBlock`: calculated and stored locals; stored, computed and public fields; inherited `thing` initialisers; stored/computed `family` data; member-data assignments; alias-component defaults and overrides; alias computed fields; exact-dictionary values; functional-dictionary results; stored or computed metadata.

The owner's constraints remain in force. When a field, component, datum, member assignment or other slot requires static initialisation, its entire `ValueBlock` must be statically evaluable. The `given` default is a deliberate exception: it remains a `constant-expression` and does not admit `ValueBlock`.

### Dictionaries

An exact association has `ExpressionBlock` on the left and `ValueBlock` on the right. A functional branch has `ExpressionBlock<Bool>` on the left and `ValueBlock` on the right. The scopes on both sides are independent; locals on the left do not pass to the right. The common outer environment and contextual functional `value` remain available under their contracts.

Braces replace only the extended operand. All four short/extended combinations are freely admitted:

```mud
key -> value
key -> { result }
{ key } -> value
{ key } -> { result }
```

and their `-->` equivalents. No auxiliary keywords or mandatory outer wrapper are introduced. A trivial single-expression block is valid even if tooling may suggest shortening it.

Applying a dictionary remains externally pure even when the result uses temporary local mutability.

### Integrated metadata

Any owner that simultaneously has its own metadata-bearing descriptor and `ValueBlock` may write its `~...` declarations as a contiguous preamble at the start of the extended body. That preamble is projected to the descriptor and is not part of `ValueBlock`.

This applies to stored/computed/public fields, alias components and computed fields, and stored/computed `family` data. It does not apply to `ThingInitializer`, overrides, member assignments, locals, `given` or `Metadata` itself. `Metadata` remains terminal.

A declaration does not combine the integrated preamble with a second metadata body. The short form may retain the existing separate metadata body. File metadata defaults retain their constant contract and do not acquire `ValueBlock`.

## Consequences

- `ExpressionBlock` remains declarative and cannot regain mutability by nesting a value block as a primary expression.
- Imperative local construction of a value does not require turning the computation into a world effect.
- `EffectBlock` and `ValueBlock` share local declarations but differ in their writing boundary and in the second block's mandatory result.
- Mutable local slots may satisfy `for mut` participants without creating a general reference system.
- `min` and `max` compose existing filtering and order instead of inventing their own key expression.
- Integrated metadata is surface sugar; the AST retains metadata and value in separate fields of the same owner.

## Verification

1. Short and extended forms of every `ExpressionBlock` and `ValueBlock` owner.
2. Rejection of `if`, outer effects and mutation escaping `ValueBlock`.
3. Local `:=`, `=` and `mut ... =` declarations with correct scopes and shadowing.
4. Nested `LocalForEach`, pure filter and body without a mandatory result.
5. Sequential ordered accumulator and consolidated unordered accumulator; distinction between `+=` and `=`.
6. Readonly binding and `for mut` for each local class, including rollback.
7. Boolean `min`/`max` returning witnesses, ordered source without a key and `empty` without candidates.
8. All four short/extended combinations of `->` and `-->`, with independent scopes.
9. Integrated metadata projected to the descriptor and rejection of a second metadata body.
10. `given` default remains constant.
11. `TestAfterBlock`, `start with`, metadata-only bodies and shared behaviour preambles retain their special contracts.
