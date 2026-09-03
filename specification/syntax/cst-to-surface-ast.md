---
title: Conversion from CST to Surface AST
aliases:
  - CST to AST
  - Syntactic normalisation
tags:
  - mud/specification
  - mud/sintaxis
status: proposed
normative: true
depends-on:
  - cst-lossless
  - ../08-abstract-syntax
  - mud-surface-ast.asdl
  - syntax-coverage.yaml
questions:
  - Q-063
decisions:
  - D-102
  - D-015
  - D-054
  - D-066
  - D-070
  - D-071
  - D-072
  - D-073
  - D-085
  - D-086
  - D-087
  - D-096
  - D-097
  - D-100
---

# Conversion from CST to Surface AST

## State and purpose

This document defines the normative projection from a validated CST to the normalised Surface AST. It does not define name resolution, inference, static analysis or dynamic semantics.

The exhaustive production-by-production matrix is in `syntax-coverage.yaml`. This document sets out the required general rules and conventions.

## Precondition

The transformation takes the following form:

- A complete `MudFileSyntax`.
- Tokens and nodes with consistent spans.
- Absence of blocking syntactic errors in the transformed sub-tree.
- Contextual validation of duplicates and prohibited combinations.
- Physical metadata of the file.

The presence of `MissingForRecovery`, `ErrorSyntax` or `SkippedTokensSyntax` inside a declaration prevents the corresponding normative node from being generated, unless an implementation also provides a non-normative fault-tolerant AST.

## Result

The transformation produces a `MudFile` featuring:

```text
physical metadata
metadataDefaults[]
usings[]
declarations[]
origin
```

The metadata for fields, components, participants, units and other stable entities is stored directly in the constructor of the owner. There is no side table for `MetadataAttachment` by span.

The build aggregator then constructs `MudProject` and orders its files by normalised path for canonical serialisation.

## Common rules

### Trivia

All trivia is ignored. Ordinary comments do not produce AST nodes.

### Punctuation

The following are excluded:

- Commas.
- Colons.
- Braces, square brackets and round brackets.
- Terminators.
- Keywords whose presence is encoded by the constructor.

A keyword that distinguishes operators or variants is converted to the corresponding enum.

### Order

The source order of all elements that are converted into AST sequences is preserved. The transformation does not reorder lists based on their meaning.

### Provenance

A directly represented node uses the span of the complete CST structure, excluding leading trivia.

A synthesised node uses:

```text
Synthetic(anchorSpan, reason)
```

The `anchorSpan` is the narrowest specific position that explains the synthesis.

## File and `using`

```text
mud-file → MudFile
using-declaration → UsingDecl
```

The concrete body `using-file-body` or `declaration-file-body` disappears. The transformation separates file metadata defaults from the `using` header and declarations. Subordinate metadata remains in its owner's constructor, not in a side table.

```mud
using physics.*
```

produces:

```text
UsingDecl(path = [physics], recursive = Enabled)
```

The absence of `.*` produces `Disabled`.

## Names

Every nominal production generates its corresponding wrapper. Qualified names retain segments rather than a dotted string.

```mud
world.people.Person
```

conceptually produces:

```text
QualifiedName([world, people, Person])
```

An expression path made solely of dotted segments produces `DottedPathExpr` until resolution determines its category.

## `thing`

```ebnf
thing-declaration
```

produces `ThingDecl`:

- `abstract` → `Enabled`; omission → `Disabled`.
- Name → `NominalName`.
- Predecessors → sequence of `TypeRef`.
- Stored or calculated `~...` statements → `metadata_assignment` sequence, normalised to `StoredMetadataAssignment` or `CalculatedMetadataAssignment`.
- Body → metadata, fields and specific initialisers.

`thing-body` and `thing-body-declaration` do not generate independent AST nodes. `metadata-assignment` does produce its own node and does not become a field. Each `field-declaration` feeds the `fields` sequence; every `thing-initializer`, in either a concrete or abstract `thing`, produces `ThingInitializer(fieldName, value)` in `initializers`, without being folded into `StoredFieldDecl.defaultValue`. A definition that locally declares a field and contains a `thing-initializer` with the same name is rejected during validation before AST construction. Omitting the body and writing an explicit empty body produce the same empty sequences; the terminator is discarded as layout.

A `name = value` form does not trigger any specific syntactic rejection. It is treated like any other `ThingInitializer`; later resolution determines whether `name` actually refers to a stored field inherited from the effective schema. If the same `thing` declares an ordinary `name` field, the combination is rejected by the general rule preventing the same field from being declared and initialised separately. Presentation metadata is still written as `~name = value`.

An explicit `Thing` predecessor remains at the surface level. It does not hinder transformation: later resolution reports the redundancy, normalises the effective root, and may offer a code action that removes the text.

## Fields

### Stored

```mud
mut population: Population in [0..*] [1] = 10 people
```

is projected to:

```text
StoredFieldDecl(
    collectionMutable = Enabled,
    name = population,
    shape = ValueShape(
        type = NamedType(Population),
        domain = [0..*],
        collection = CollectionSpec([1..1], ...)
    ),
    defaultValue = 10 people
)
```

The value-form domain and collection specification are normalised nodes, not text fragments.

### Calculated and public

An omitted type entry remains absent. The type is inferred.

## Collection normalisation

### Cardinality omitted

```mud
value: Nat
values: Nat = [1, 2, 3]
```

Both forms produce a `CollectionSpec` with `OmittedCardinality`. The Surface AST neither manufactures `[1]` nor infers `[3]`. Later elaboration uses the owner and initialiser: an ordinary scalar without evidence to the contrary preserves `[1]`; an immutable stored field with a finite initialiser may yield an exact cardinality with provenance `InferredFromInitializer`.

### Exact cardinality

```mud
values: Nat [5]
```

produces:

```text
[5..5]
```

### Bare star

```mud
values: Nat [*]
```

produces:

```text
[EffectiveCardinality..EffectiveCardinality]
```

The left-hand end is not yet replaced by zero.

### Modifiers

The two concrete forms:

```mud
[0..* unique ordered mut]
[0..*, unique, ordered, mut]
```

produce the same `CollectionSpec`.

Omitting modifiers results in:

```text
isUnique = Disabled
order = Unordered
elementsMutable = Disabled
```

`ordered` produces `OrdinaryOrdered`, a neutral surface feature whose semantic meaning is determined during the elaboration. `ordered by a.b` produces `OrderedBy([a,b])`.

Pre-AST validation rejects:

- Repeated `unique`.
- Repeated `mut`.
- More than one `ordered`.
- Simultaneous `ordered` and `ordered by`.

### `given`

`given-declaration` represents its input with the same surface `TypeExpr` used by other type contexts. This preserves complete dictionary types without introducing a second read-only type hierarchy. A written `mut` capability may be represented in the Surface AST, but later validation and typing reject it statically for `given`.

## Types

### Nominal

Every `type-reference` produces `NamedType(TypeRef(...))`. The AST has not yet classified the name.

### Callables and reflected types

`callable-type` produces `CallableType(kind, receivers, givens)` and retains the specified category and types; Q-063 keeps signature compatibility and variance open. `reflected-type` consumes a `postfix-expression` followed by `~type` and produces `ReflectedType(value)`; later elaboration requires the expression to statically denote `Type` and obtains the represented type. The mechanical form after typing and elaboration remains undecided.

### Products and dictionaries

```mud
Name -> Coordinate -> Piece [*]
A -> B [2] --> C [3 ordered]
```

Arrow chains fold inwards from the right. The first shape produces `ExactDictionaryType(Name, ExactDictionaryType(Coordinate, Piece, [*]), ...)`; the second produces an outer dictionary whose value is `DecisionDictionaryType(B, C, FirstMatch, [3])`, and `[2]` belongs to the outer arrow.

`(A, B)` and `(name: A, value: B)` produce `PositionalProductType` and `NamedProductType`, respectively. Parentheses forming the product are retained by the constructor; parentheses used solely for grouping are discarded.

The CST can recognise a parenthesised arrow inside an alternative, but contextual validation or resolution rejects an arrow as one branch of a `|` alternative, even when the outer form derives from an alias.

## Aliases

The list written after `as` is preserved as `direct_ancestors`. The `:= type-expression` alternative produces `AliasRepresentation`; combining it with ancestors is rejected before AST construction. An absent definition produces `definition = None` and is valid only when at least one ancestor exists. A metadata-only body following `:= type-expression` feeds `AliasDecl.metadata` and creates no structural members.

`type-expression` normalises one or more `type-alternative` values separated by `|` into a single `TypeExpr`. Redundant groupings are removed, identical alternatives are deduplicated, and every nominal alternative is retained even when its domain is contained within another. The outer collection specification is associated with the complete `TypeExpr`.

`derived-value-shape` with `: type-expression` produces `ExplicitDerivedShape`. Shapes without a type, `in domain [collection]` and `collection`, produce `InferredDerivedShape`; when the collection is omitted, it defaults to scalar cardinality and the type is deferred to inference.

A restriction `interval-expression by constant-expression` produces `SteppedDomain`; the other restrictions result in `ExpressionDomain`. Brackets that do not alter the grouping do not reach the Surface AST.

The structural body produces `StructuralAlias` with `AliasMember` in source order. A `component-declaration` produces `AliasComponentDecl`; a `calculated-field-declaration` produces `AliasCalculatedFieldDecl`; and `inherited-default-override` produces `AliasDefaultOverride`.

A component cannot produce outer mutability. Its collection specification may produce `elementsMutable = Enabled`. A calculated field may also state `elementsMutable = Enabled`; that capability belongs to the calculated collection and is not inferred from the sources used by its expression.

## Families

The word `ordered` produces `isOrdered = Enabled`.

Data declarations are divided into stored and calculated declarations. Each may consist of an immediate body containing only `metadata-assignment`; that sequence is preserved in `StoredFamilyDataDecl.metadata` or `CalculatedFamilyDataDecl.metadata`. A calculated declaration retains `derived_value_shape?` using the same normalisation as a calculated field: `ExplicitDerivedShape` for a written type and `InferredDerivedShape` for a domain or collection without an invented surface type.

In a member preamble, each `metadata-assignment` produces `StoredMetadataAssignment` or `CalculatedMetadataAssignment` on the member's descriptor; subsequent ordinary assignments are retained as `FamilyDataAssignment`. These replace the value of stored data for that member, but do not create a descriptor, anchor or metadata body of their own. A metadata-only member body produces `assignments = []` and retains its `metadata` sequence.

The comma between clauses is removed. The absence of a final comma has already been validated by the grammar rules.

## Magnitudes

### Representation

The optional annotation uses `DeclaredType`. The numerical representation check is deferred.

### Base

The body is divided into:

- Optional root unit.
- Subsequent alternative units.

### Derived

The dimensional expression is expanded from left to right into `DimensionProduct` and `DimensionLink`, retaining multiplication and division.

### Point

An ordinary domain produces `OrdinaryPointDomain`; `cycle` after the interval expression produces `CyclicPointDomain`. The token is not included in the range as a delimiter or as part of its endpoints.

An omitted `~format` remains absent.

## Units

Units are not normalised into separate `UnitProperties`. `unit-body` is discarded as a specific wrapper, and each `metadata-assignment` is preserved in the `metadata` sequence of `RootUnitDecl` or `AlternativeUnitDecl`.

`~prefixes = empty`, `~prefixes = all` and `~prefixes = [kilo, milli]` follow ordinary expression transformation. The Surface AST does not manufacture `NoPrefixes`, `AllPrefixes` or `SelectedPrefixes`; later elaboration applies the expected type `Prefix [* unique]` and default `empty`.

A root unit produces `RootUnitDecl(name, metadata)` and an alternative unit produces `AlternativeUnitDecl(name, equivalence, metadata)`. Omitted presentation metadata remains absent at this stage.

## Participants

A grouped header produces one node per identifier and copies to each descriptor the same metadata declarations with provenance `NormalizedSugar`.

### `for`

Every participant has a required name. The outer `mut`, `ValueShape` and descriptor metadata sequence are converted. A grouped header produces one `ForParticipant` per identifier and copies the same metadata body to each.

### `on`

The direct variant produces `DirectOnParticipant(name, type, elementsMutable, metadata)`. The related variant produces `RelatedOnParticipant(name, refinement?, source, elementsMutable, metadata)`. The cross-references remain unresolved at this stage.

### `given`

The name, `TypeExpr`, default and metadata are converted. A dictionary type uses the ordinary `ExactDictionaryType` or `DecisionDictionaryType` constructors. The default remains an `expr` and does not acquire a `ValueBlock`; its static nature and the prohibition of any `mut` capability in `given` are checked later.

## Rules and actions

The metadata-bearing preamble of every rule, action, subaction, look, message and test is retained in the `metadata` field of the corresponding parent constructor. `start with` does not generate metadata of its own.

Default metadata written at the start of the file uses `FileMetadataAssignment(name, type?, value?)`. Its value remains a static `expr?` and is not normalised to `ValueBlock`; this is a deliberate exception for file defaults.

### Boolean rule

The body becomes `ExpressionBlock(locals, result)`. The form without local declarations produces `locals = []`.

### Reactive rule

`local-value-declaration` forms preceding behavioural clauses become `leading_locals`. `when` produces an `ExpressionBlock` in `activator`; `if` produces another in `guard?`; `then` produces `EffectBlock`.

### `always` rule

`InvariantBodySyntax`, enclosed in braces, produces an `ExpressionBlock`. The outer `DiagnosticTailSyntax` produces the `AlwaysRuleDecl` diagnostic; if absent, the AST retains `diagnostic = absent`. The warning's default text is not inserted here.

### Action

`action` and `subaction` produce `ActionDecl` with `PublicAction` or `Subaction`. `local-value-declaration` forms preceding behavioural clauses become `leading_locals`. `if` produces `ActionGuard` with an `ExpressionBlock`; `after` produces `ActionPostcondition` with another.

The action is not classified as either elementary or compound.

### `look` and `message`

`look-declaration` projects its optional `given-clause` to `LookDecl.givens`. In `message`, local-value declarations preceding behavioural clauses become `leading_locals`. Public fields are converted to `PublicFieldDecl` and retain their order.

## Expression blocks, value blocks and tests

A `local-value-declaration` inside an `ExpressionBlock`, a shared preamble or a `TestAfterBlock` produces `LocalValueDecl(name, shape?, value)`. Its RHS remains an ordinary expression: these positions cannot acquire a `ValueBlock` through nesting.

The short form `if ready` produces `ExpressionBlock([], ready)`. The brace form contains only pure local `:=` declarations and requires a single final expression. `otherwise` lies outside the AST block, although resolution extends those locals' environment to it.

A short `value-body` normalises to `ValueBlock([], value)`. The expanded form produces `ValueBlock(statements, result)`. Calculated statements produce `LocalCalculatedDecl`, stored ones `LocalStoredDecl`, mutations `LocalAssignment`/`LocalAdd`/`LocalRemove`, and local iteration `LocalForEach`. Later validation and elaboration verify that every `LocalMutation` stays within storage created by the `ValueBlock`.

`LocalForEach` preserves `source`, `step?` and the filter as `ExpressionBlock?`; its short body or text in brackets normalises to `LocalStatementBlock` and never to `EffectBlock`.

When a metadata-bearing owner uses the integrated expanded form, its initial `~...` declarations are extracted to the descriptor's `metadata` field and the following statements form its `ValueBlock`. The preamble does not produce `ValueStatement`. The short form with a separate metadata body converges on the same AST. Validation before AST construction rejects a declaration that combines metadata from both locations.

In tests, `after expr` produces `TestAfterBlock([], [TestAssertion(expr)])`. The braced form retains its pure calculated values before the assertions and does not become a `ValueBlock`.

## `then` and blocks

```mud
then effect
```

and:

```mud
then {
    effect
}
```

both produce `EffectBlock`, with one statement in equivalent cases.

All block statements are retained in order. Calculated declarations produce `LocalCalculatedStatement`, stored declarations `LocalStoredStatement`, and effects `EffectStatement`. Later validation requires at least one observable effect; a block made solely of local values is therefore not a valid `then`.

## Effects

### Assignment

The concrete operator is converted to:

- `Assign`.
- `AddAssign`.
- `SubtractAssign`.
- `MultiplyAssign`.
- `DivideAssign`.
- `UnionAssign`.
- `IntersectionAssign`.
- `SymmetricDifferenceAssign`.
- `DifferenceAssign`.

### `add`

The alternative using an expression produces `AddValueEffect`.

The alternative with a field declaration produces `AddFieldEffect`. The nested declaration is transformed as a stored field.

### Call candidate

`action-call-effect` produces `ActionCallCandidateEffect(expr)`. Later resolution must confirm that the expression ends in a valid action call.

### Iteration

Simple binding produces `ValueIterationBinding`. The bracketed pair yields `DictionaryIterationBinding`. Executable `for each` retains `by` as `step?`, normalises `if` to `ExpressionBlock`, and converts both its short effect and the block after `:` to `EffectBlock`. Iteration inside a `ValueBlock` is another production and produces `LocalForEach` with `LocalStatementBlock`. Addressability, compatibility and zero steps belong to later phases.

## Expressions

### Folding of precedence

Each precedence level is folded according to [[07-concrete-grammar]]:

- Ordinary binary operators: left.
- Implication: right.
- Chainable comparisons: `ComparisonChainExpr`.

### Word and symbolic operators

`has not` produces `HasNotMember`. `e iis T` produces `ExactTypeTestExpr(e, T, Disabled)` and `e iis not T` produces `ExactTypeTestExpr(e, T, Enabled)`.

Various enums are retained:

| Concrete | AST |
|---|---|
| `and` | `WordAnd` |
| `&` | `SymbolAnd` |
| `or` | `WordOr` |
| `|` | `SymbolOr` |
| `xor` | `WordXor` |
| `^` | `SymbolXor` |
| `--` | `CollectionDifference` |

### `changes`

The presence of the suffix results in `ChangesExpr(operand)`.

### `all` materialisation

The prefix `all D` produces `PrefixExpr(EnumerateAll, D)`; the contextual literal without an operand remains `AllLiteral`.

### Selection and `take`

`binding in source [by step] : predicate` produces `SelectionExpr(binding, source, step?, predicate)`. Simple or dictionary binding reuses `ValueIterationBinding` or `DictionaryIterationBinding`; its scope is limited to the predicate. The short form and `{ locals*; result }` converge on `ExpressionBlock`.

`exists`, `forall`, `count`, `min` and `max` produce `QuantifierExpr(kind, variable, source, step?, body)`, with an `ExpressionBlock` body. `sum` is no longer in the catalogue. The transformation does not determine the Boolean contract or, for `min`/`max`, the validity of the source order; these checks occur later.

`take amount from source` produces `TakeExpr(amount, source)`. The node's shape does not determine whether the selection is an ordered prefix or a reproducible sample: that distinction depends on the type and resolved properties of `source`.

Both constructs contain complete expressions. Therefore, composition is preserved through explicit nesting of the AST:

```text
take n from player in players : player.score == 2
→ TakeExpr(n, SelectionExpr(player, players, ...))

player in take m from players : player.score == 2
→ SelectionExpr(player, TakeExpr(m, players), ...)
```

### Dictionary associations and branches

`a -> b` produces `ExactAssociationExpr(ExpressionBlock([], a), ValueBlock([], b))`; `selector --> result` produces `DecisionBranchExpr(ExpressionBlock([], selector), ValueBlock([], result))`. The brace-form `mapping-key-body` retains its premises in `ExpressionBlock`; the expanded RHS uses `value-block-body` and stores its statements in `ValueBlock`. The short RHS remains `mapping-expression`, so an outer comma continues to separate clauses rather than becoming part of the first value. `_` produces `FallbackLiteral`. Operations `|`, `&`, `--` and `^` are initially retained as `BinaryExpr`; elaboration specialises them according to resolved types. A functional operation preserves both operands and does not become a merged branch list.

### Conversions

`to T` produces `TypeConversion`. `in u` produces `UnitConversion`.

### Postfix

`element~metadata` produces `MetadataAccessExpr`; no access `~` is part of a runtime-assignable target. The other suffixes are applied in order:

```text
base.a[i](x)
```

produces:

```text
CallExpr(
  IndexExpr(
    MemberAccessExpr(base, a),
    [i]
  ),
  [x]
)
```

### Arguments

Unlabelled arguments form the `positionalArguments` prefix. Arguments written with `name =` form the `NamedCallArgument` suffix.

Contextual syntax validation rejects a positional argument following the first named argument, so `CallExpr` need not represent that invalid state.

### Receiver ambiguity

`receiver-tuple` and `structural-literal` converge on one of two forms: `PositionalStructuralLiteralExpr` or `NamedStructuralLiteralExpr`. Subsequent `MemberAccessExpr` and `CallExpr` retain the complete form. Resolution selects a signature and then chooses between one structural receiver and multiple receivers.

### Paths

A `qualified-name` used as an expression produces `DottedPathExpr`, not a resolved reference.

## Literal expressions

### Exact and `Rum`

Underscores are removed and exponent and mantissa are normalised to canonical form. Provenance to the CST lexeme is retained.

### `Char` and `Text`

Every ordinary double-quoted literal initially produces `TextTemplateExpr`. Later contextual elaboration turns it into `Char` when the expected type is `Char` and the decoded text contains exactly one Unicode scalar value. Single quotation marks do not produce a character literal.

### Booleans

`true` → `BoolLiteral(Enabled)`.

`false` → `BoolLiteral(Disabled)`.

### `empty`

Produces `EmptyLiteral`.

### `POINT_LITERAL`

It retains its original form in `PointLiteral`; its magnitude remains unresolved, as expected.

## Templates

`TEXT_FRAGMENT` is decoded after escape processing and margin normalisation.

The difference between explicit and implicit closure disappears.

Every interpolation produces `ValueInterpolation`; `anchor{...}` does not belong to the language.

Within a point magnitude's `format`, `unit from container` produces `ContextualPointComponentExpr`; no unwritten receiver is invented.

## Structural literals

The positional form produces `PositionalStructuralLiteralExpr` with two mandatory elements and the rest.

The named form produces `NamedStructuralLiteralExpr` with one or more `NamedStructuralElement`.

Alias selection, positional completeness and component defaults belong to later validation and resolution, guided by the expected type.

## Values separated by commas

The production:

```ebnf
value-expression ::= expression , [ "," , expression , { "," , expression } ] ;
```

is transformed as follows:

- No comma: the original expression.
- With one or more commas: `CollectionLiteralExpr` of all expressions.

## Intervals

### Closed shorthand

```mud
a..b
```

produces closed boundaries.

### Singleton

```mud
[a]
```

produces `lower = a`, `upper = a`, both of which are closed.

### Empty with unit

```mud
[] meters
```

produces `EmptyInterval(UnitProduct(...))`.

### Shared unit

The final unit moves to the `sharedUnit` field; it is not duplicated on either endpoint.

### Cyclic

The `cycle` following `PointDomainSyntax` selects `CyclicPointDomain`; it does not alter the `Interval` content. Pre-AST validation requires the preceding interval to be finite, non-empty, closed on the left and open on the right.

### `*` endpoints

`*` produces `EffectiveIntervalBound`, without yet converting it to infinity or to a value dependent on the domain.

## Quantity values and units

A numeric literal followed by a unit produces `QuantityValueExpr(Quantity(...))`.

Unit and dimension expressions remove grouping parentheses but retain the tree structure imposed by multiplication and division.

## `start with` and tests

The expression form and block form of `start with` produce a single `StartSet(contributions)`. Source order is retained only as provenance, not as activation semantics.

The module-level declaration adds `ModuleStartDecl`. Within a test, the same `StartSet` is a field of `TestDecl`.

`after assertion` and `after { assertion... }` produce a uniform `TestAfterBlock`.

## Elements not yet normalised

The following are still pending for subsequent phases:

- Qualified names versus semantic access.
- Specific alias selected for a structural literal.
- Multiple receivers versus a structural receiver.
- Ordinary call versus rule or action call.
- Type of a contextual literal.
- Evidence of a declared static expression.
- Compatibility of domains and cardinalities.
- Resolution of units and prefixes.

## Transformation diagnostics

The transformation can only generate its own diagnostics when:

- The CST violates a contextual invariant required for normalisation.
- A property required to build an AST product is missing.
- Two concrete spellings normalise to the same field.
- A grammar production has no transformation rule.

A failure of names or types is not a diagnostic of this phase.

## Mechanical table

`syntax-coverage.yaml` is exhaustive. Each production states:

- `cst`: specific category.
- `ast.disposition`.
- `ast.target` or a reason for discarding/folding.

The possible dispositions are:

- `constructor`.
- `wrapper`.
- `normalized`.
- `enum-or-property`.
- `folded`.
- `inlined`.
- `discarded`.

## Minimum tests

Each normalisation rule must include at least:

- Minimum valid form.
- Equivalent variant.
- Borderline case.
- Invalid case prior to the AST, where applicable.

The initial corpus is in `cases/cst-ast.yaml`.

## Membership, restriction and local transformations

`a has b` projects to `HasMember`; `a has not b` projects to `HasNotMember`. `value in Domain` projects to `DomainRestrictionExpr`; `binding in source : predicate` preserves `SelectionExpr`. `collection-transform-suffix` folds to `CollectionTransformExpr`; local transforms provide no internal `mut` capability.
