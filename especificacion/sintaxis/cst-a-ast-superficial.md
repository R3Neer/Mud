---
title: Conversion from CST to Surface AST
aliases:
  - CST to AST
  - Syntactic normalisation
tags:
  - mud/especificacion
  - mud/sintaxis
status: propuesta
normative: true
depends-on:
  - cst-sin-perdidas
  - ../08-sintaxis-abstracta
  - mud-surface-ast.asdl
  - cobertura-sintactica.yaml
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

This document defines the regulatory projection based on a validated CST to the Surface AST normalised. It does not define name resolution, inference, static assessment or semantics dynamics.

The exhaustive matrix production by production is in `cobertura-sintactica.yaml`. This document sets out the general rules and standards required explanation.

## Precondition

The transformation takes the following form:

- One `MudFileSyntax` complete.
- Tokens and nodes with consistent spans.
- Absence of blocking syntactic errors in the transformed sub-tree.
- Contextual validation duplicates and prohibited combinations.
- Physical metadata of the file.

The existence of tokens `MissingForRecovery`, `ErrorSyntax` o `SkippedTokensSyntax` inside a declaration prevents the corresponding policy node from being generated, unless an implementation also provides a non-policy-based, fault-tolerant AST.

## Resultado

The transformation produces a `MudFile` featuring:

```text
metadata físico
metadataDefaults[]
usings[]
declarations[]
origin
```

The metadata for fields, components, participants, units and other stable entities is stored directly in the constructor of the owner. There is no side table for `MetadataAttachment` by span.

The build aggregator then builds `MudProject` and organises its files by path normalised for canonical serialisation.

## Common rules

### Trivia

All trivia is ignored. Ordinary comments do not produce AST nodes.

### Score

The following are excluded:

- Commas.
- Two points on syntax.
- Braces, square brackets and round brackets.
- Terminators.
- Keywords whose presence is encoded by the constructor.

A keyword that distinguishes operators or variants is converted to the corresponding enum.

### Order

The source order of all elements that are converted into AST sequences is preserved. The transformation does not reorder lists based on their meaning.

### Procedencia

A directly represented node uses the span of the complete CST structure, excluding the trivia initial.

A synthesised node uses:

```text
Synthetic(anchorSpan, reason)
```

The `anchorSpan` is the narrowest specific position that explains the synthesis.

## Archive and `using`

```text
mud-file → MudFile
using-declaration → UsingDecl
```

The concrete body `using-file-body` o `declaration-file-body` disappears. The transformation separates the file metadata defaults from the header `using` and the declarations. The subordinate metadata remains in the constructor of its owner, not in a side table.

```mud
using physics.*
```

produces:

```text
UsingDecl(path = [physics], recursive = Enabled)
```

The absence of `.*` produces `Disabled`.

## Names

Every production A nominal generates its corresponding wrapper. Qualified names retain segments, not a string with dots.

```mud
world.people.Person
```

conceptually produces:

```text
QualifiedName([world, people, Person])
```

A path of expression consisting solely of segments with point produces `DottedPathExpr` until the resolution determine its category.

## `thing`

```ebnf
thing-declaration
```

produces `ThingDecl`:

- `abstract` → `Enabled`; omission → `Disabled`.
- Name → `NominalName`.
- Predecessors → sequence of `TypeRef`.
- Statements `~...` stored or calculated → sequence of `metadata_assignment`, normalised to `StoredMetadataAssignment` o `CalculatedMetadataAssignment`.
- Body → metadata, fields and specific initialisers.

`thing-body` y `thing-body-declaration` do not generate independent AST nodes. `metadata-assignment` it does produce its own node and does not become field. Each `field-declaration` feed the sequence `fields`; every `thing-initializer`, both in a `thing` whether concrete or abstract, it produces `ThingInitializer(fieldName, value)` in the sequence `initializers`, without folding in on itself `StoredFieldDecl.defaultValue`. If the same definition locally declares a field and contains a `thing-initializer` of the same name, is rejected during the validation prior to the AST. Omitting the body and an explicit empty body produce the same empty sequences; the terminator is discarded as a layout.

A way `name = valor` It does not trigger any specific syntactic rejection. It is treated like any other `ThingInitializer`; the resolution The latter decides whether `name` actually refers to a stored field inherited from the existing scheme. If the same `thing` declares a field ordinary `name`, the combination is rejected under the general rule that prevents the same variable from being declared and initialised separately field. The metadata from presentation it is still being written `~name = valor`.

An explicit predecessor `Thing` remains at that superficial level. It does not hinder the transformation: the resolution the latter outputs the redundancy, normalises the root effective and can offer a action a piece of code that removes the text.

## Fields

### In stock

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

The domain in the form of value and the specification from collection They are standardised nodes, not text fragments.

### Calculated and public

The entry for type What is missing remains missing. The type inferred.

## Standardisation of collections

### Cardinality omitted

```mud
value: Nat
values: Nat = [1, 2, 3]
```

Both forms produce a `CollectionSpec` with `OmittedCardinality`. The Surface AST does not manufacture `[1]` nor does it imply `[3]`. The elaboration the latter uses the owner and the initialiser: an ordinary scalar with no evidence of conservation `[1]`; a stored field An immutable type with a finite initialiser can yield a cardinality exact with provenance `InferredFromInitializer`.

### Cardinality exact

```mud
values: Nat [5]
```

produces:

```text
[5..5]
```

### Exact star

```mud
values: Nat [*]
```

produces:

```text
[EffectiveCardinality..EffectiveCardinality]
```

The left-hand end is not yet replaced by zero.

### Modifiers

The two specific forms:

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

The validation previous rejection:

- Repeat of `unique`.
- Repeat of `mut`.
- More than one `ordered`.
- `ordered` y `ordered by` simultaneous.

### `given`

`given-declaration` displays its entry using the same method `TypeExpr` more superficial than other contexts of type. This makes it possible to preserve complete dictionary types without introducing a second, read-only type hierarchy. The presence of capacity `mut` can be represented in the Surface AST, but that capacity is statically rejected for `given` during the later stages of validation and typed.

## Types

### Nominal

Everything `type-reference` produces `NamedType(TypeRef(...))`. The AST has not yet classified the name.

### Callables and reflected types

`callable-type` produces `CallableType(kind, receivers, givens)` and retains the category and the types specified; Q-063 keeps the compatibility y variance between companies. `reflected-type` consumes one `postfix-expression` followed by `~type` and produces `ReflectedType(value)`; the elaboration The latter requires that the property be statically denoted `Type` and obtains the type represented. The mechanical form following typing and elaboration It has not yet been decided.

### Products and dictionaries

```mud
Name -> Coordinate -> Piece [*]
A -> B [2] --> C [3 ordered]
```

The arrow chains fold inwards from the right. The first shape produces a `ExactDictionaryType(Name, ExactDictionaryType(Coordinate, Piece, [*]), ...)`; the second produces a number whose value is a `DecisionDictionaryType(B, C, FirstMatch, [3])`, y `[2]` belongs to the outer arrow.

`(A, B)` y `(name: A, value: B)` produce, respectively `PositionalProductType` y `NamedProductType`. The parentheses forming the product are retained by the constructor; parentheses used purely for grouping are discarded.

CST can recognise a parented arrow within an alternative, but the contextual validation or the resolution rejects the idea that an arrow is a partial alternative to `|`, even when the external form derives from a alias.

## Aliases

The list drawn up after `as` is preserved as `direct_ancestors`. The alternative `:= type-expression` produces `AliasRepresentation`; its combination with predecessors is rejected prior to the AST. The lack of definition results in `definition = None` and it is only valid if there is at least one ancestor. A metadata-only body following `:= type-expression` feeds `AliasDecl.metadata` and does not create structural members.

`type-expression` normalises one or more `type-alternative` separated by `|` in a single `TypeExpr`. Redundant groupings are removed, identical alternatives are deduplicated, and each nominal alternative is retained even if its domain is contained within another. The specification from collection external is associated with the `TypeExpr` complete.

`derived-value-shape` with `: type-expression` produces `ExplicitDerivedShape`. Shapes without type, `in domain [collection]` y `collection`, produce `InferredDerivedShape`; a collection If omitted, it defaults to the cardinality climbing and the type is not devised until the stage of inference.

A restriction `interval-expression by constant-expression` produces `SteppedDomain`; the other restrictions result in `ExpressionDomain`. Brackets that do not alter the grouping do not reach the Surface AST.

The structural body produces `StructuralAlias` with `AliasMember` in source order. A `component-declaration` produces `AliasComponentDecl`; a `calculated-field-declaration`, `AliasCalculatedFieldDecl`; y `inherited-default-override`, `AliasDefaultOverride`.

A component cannot produce mutability exterior. Its collection In general, it can produce `elementsMutable = Enabled`. A derived field may also state `elementsMutable = Enabled`; that capacity belongs to the collection derived and not inferred from the sources from which it is expressed.

## Families

The word `ordered` produces `isOrdered = Enabled`.

Data declarations are divided into stored and calculated declarations. Each declaration may consist of an immediate body comprising solely `metadata-assignment`; that sequence is preserved in `StoredFamilyDataDecl.metadata` o `CalculatedFamilyDataDecl.metadata`. The calculated figure retains `derived_value_shape? shape` using the same standardisation as a computed field: `ExplicitDerivedShape` for type written and `InferredDerivedShape` for domain o collection without type a made-up superficiality.

In the preamble to a member, any `metadata-assignment` produces `StoredMetadataAssignment` o `CalculatedMetadataAssignment` from the descriptor from the member; subsequent ordinary allocations are retained as `FamilyDataAssignment`. These assignments replace the value of a piece of data stored for that member, but don’t believe it descriptor, anchor nor their own metadata-body. A body of member metadata-only produces `assignments = []` and retains its sequence `metadata`.

The comma between clauses is removed. The absence of a final comma has already been validated by the grammar rules.

## Quantities

### Representation

The optional annotation uses `DeclaredType`. The numerical representation check is deferred.

### Base

The body is divided into:

- Unit root optional.
- Subsequent alternative units.

### Derivative

The dimensional expression is expanded from left to right in `DimensionProduct` y `DimensionLink` whilst retaining multiplication and division.

### Punto

The domain ordinary produces `OrdinaryPointDomain`; the presence of `cycle` after the expression ‘interval’ comes `CyclicPointDomain`. The token is not included in the range as a delimiter nor as part of its ends.

`~format` What is absent remains absent.

## Units

The units are not standardised `UnitProperties` separate. `unit-body` is ruled out as a specific packaging material, and each `metadata-assignment` is preserved in the sequence `metadata` from `RootUnitDecl` o `AlternativeUnitDecl`.

`~prefixes = empty`, `~prefixes = all` y `~prefixes = [kilo, milli]` follow the standard transformation of expressions. The Surface AST does not manufacture `NoPrefixes`, `AllPrefixes` nor `SelectedPrefixes`; the elaboration the following applies type expected `Prefix [* unique]` and the default `empty`.

One unit root produces `RootUnitDecl(name, metadata)` and an alternative `AlternativeUnitDecl(name, equivalence, metadata)`. The metadata for presentation Those omitted are still missing at this stage.

## Participants

A grouped header produces one node per identifier and copies to each descriptor the same metadata declarations with provenance `NormalizedSugar`.

### `for`

Every participant has a required name. They are converted `mut` outdoor, `ValueShape` and the metadata sequence of the descriptor. A grouped header produces a `ForParticipant` by identifier, and copies the same metadata body to each one.

### `on`

The direct variant produces `DirectOnParticipant(name, type, elementsMutable, metadata)`. The related variant produces `RelatedOnParticipant(name, refinement?, source, elementsMutable, metadata)`. The cross-references remain unresolved at this stage.

### `given`

The name is converted, `TypeExpr`, default and metadata. A type The dictionary is maintained using the standard constructors `ExactDictionaryType` o `DecisionDictionaryType`. The default remains `expr` and does not acquire `ValueBlock`; its permanent nature and the prohibition of any capacity `mut` from the `given` are checked afterwards.

## Rules and actions

The metadata-bearing preamble of each rule, action, subaction, look, message y test is kept in the field `metadata` of the corresponding parent constructor. `start with` It does not generate its own metadata.

The default metadata written at the start of the file uses `FileMetadataAssignment(name, type?, value?)`. His value remains `expr?` constant and is not normalised to `ValueBlock`; this is a deliberate exception to the file defaults.

### Regla booleana

The body becomes `ExpressionBlock(locals, result)`. The form without local declarations produces `locals = []`.

### Regla reactiva

The `local-value-declaration` The provisions preceding the conduct clauses apply to `leading_locals`. `when` produces a `ExpressionBlock` in `activator`; `if` produces another one in `guard?`; `then` produces `EffectBlock`.

### Ruler `always`

`InvariantBodySyntax`, enclosed in brackets, produces a `ExpressionBlock`. The `DiagnosticTailSyntax` The exterior produces the diagnostic from `AlwaysRuleDecl`; if it is missing, it is retained `diagnostic = absent`. The default text of the warning is not inserted here.

### Acción

`action` y `subaction` produce `ActionDecl` with `PublicAction` o `Subaction`. The `local-value-declaration` The provisions preceding the conduct clauses apply to `leading_locals`. `if` produces `ActionGuard` with a `ExpressionBlock`; `after` produces `ActionPostcondition` with another.

The following is not classified as action as either elementary or compound.

### `look` y `message`

`look-declaration` projects its `given-clause` optional to `LookDecl.givens`. In `message`, the `local-value-declaration` The provisions preceding the conduct clauses apply to `leading_locals`. Public properties are converted to `PublicFieldDecl` and remain in the same order.

## Expression blocks, value and tests

One `local-value-declaration` inside `ExpressionBlock`, of the shared preambles and of `TestAfterBlock` produces `LocalValueDecl(name, shape?, value)`. Its RHS remains an ordinary expression: these positions cannot recover a `ValueBlock` by nesting.

A short way of saying `if ready` produces `ExpressionBlock([], ready)`. The expression in curly brackets contains only pure local derivatives `:=` and requires a single final expression. `otherwise` is outside the AST block, although the resolution extends to him the environment of those local ones.

A `value-body` briefly normalises to `ValueBlock([], value)`. The full form produces `ValueBlock(statements, result)`. The bloc’s calculated statements result in `LocalCalculatedDecl`, those stored `LocalStoredDecl`, mutations `LocalAssignment`/`LocalAdd`/`LocalRemove` and the local route `LocalForEach`. The validation/elaboración subsequently verifies that every deed of `LocalMutation` remain within the storage created by the `ValueBlock`.

`LocalForEach` preserves `source`, `step?` and the filter as `ExpressionBlock?`; its short body or text in brackets normalises to `LocalStatementBlock` and never to `EffectBlock`.

When a owner metadata-bearing uses the built-in expanded form; the declarations `~...` The initials are extracted towards the field `metadata` from the descriptor and the following sentences make up its `ValueBlock`. The preamble does not produce `ValueStatement`. The short form with a separate metadata-body converges to the same AST. The validation prior to the AST, it rejects the idea that the same declaration Combine the metadata from both locations.

In tests, `after expr` produces `TestAfterBlock([], [TestAssertion(expr)])`. The expression in curly brackets retains its pure calculated values prior to the assertions and does not take on `ValueBlock`.

## `then` and blocks

```mud
then effect
```

y:

```mud
then {
    effect
}
```

both produce `EffectBlock`, with a judgement in similar cases.

All the statements in the block are kept in order. The calculated expressions produce `LocalCalculatedStatement`, those stored `LocalStoredStatement` and the effects `EffectStatement`. The validation The latter requires that there be at least one effect observable; therefore, a block consisting solely of local variables is not a `then` valid.

## Effects

### Allocation

The specific operator is converted to:

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

The alternative with declaration from field produces `AddFieldEffect`. The declaration nested is transformed as stored field.

### Candidate for call

`action-call-effect` produces `ActionCallCandidateEffect(expr)`. The resolution The following must confirm that the expression ends with a call a action valid.

### Iteration

Simple linking produces `ValueIterationBinding`. The pair in brackets yields `DictionaryIterationBinding`. The `for each` executable retains `by` such as `step?`, normalise `if` a `ExpressionBlock` and converts both the effect as short as the block behind `:` in `EffectBlock`. The route written inside `ValueBlock` is another one production and produces `LocalForEach` with `LocalStatementBlock`. Address, compatibility and step zero belong to later phases.

## Expressions

### Folding of precedence

Output by level is broken down in accordance with [[07-gramatica-concreta]]:

- Ordinary iterative operators: left.
- Implication: right.
- Chainable comparisons: `ComparisonChainExpr`.

### Word operators and symbol

`has not` produces `HasNotMember`. `e iis T` produces `ExactTypeTestExpr(e, T, Disabled)` y `e iis not T`, `ExactTypeTestExpr(e, T, Enabled)`.

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

### Materialización `all`

The prefix `all D` produces `PrefixExpr(EnumerateAll, D)`; the literal contextual without an operand is retained `AllLiteral`.

### Selection and `take`

`binding in source [by step] : predicate` produces `SelectionExpr(binding, source, step?, predicate)`. Simple or dictionary linking reuses `ValueIterationBinding` o `DictionaryIterationBinding`; his scope is limited to the predicate. The short form and `{ locales*; resultado }` converge on `ExpressionBlock`.

`exists`, `forall`, `count`, `min` y `max` produce `QuantifierExpr(kind, variable, source, step?, body)`, with `body` such as `ExpressionBlock`. `sum` It is no longer in the catalogue. The transformation does not determine the contract Boolean nor, for `min`/`max`, the validity of the source order; these checks are carried out at a later stage.

`take amount from source` produces `TakeExpr(amount, source)`. The shape of the node does not determine whether the selection will be a prefix ordered or a reproducible sample: that distinction depends on the type and the resolved cases of `source`.

Both constructs contain complete expressions. Therefore, composition is preserved through explicit nesting of the AST:

```text
take n from player in players : player.score == 2
→ TakeExpr(n, SelectionExpr(player, players, ...))

player in take m from players : player.score == 2
→ SelectionExpr(player, TakeExpr(m, players), ...)
```

### Dictionary associations and branches

`a -> b` produces `ExactAssociationExpr(ExpressionBlock([], a), ValueBlock([], b))`; `selector --> resultado` produces `DecisionBranchExpr(ExpressionBlock([], selector), ValueBlock([], resultado))`. The `mapping-key-body` 'entre llaves' retains its premises at `ExpressionBlock`; the extended RHS uses `value-block-body` and stores its judgements in `ValueBlock`. The short RHS remains `mapping-expression`, so that an external comma continues to separate clauses and does not become part of the value of the first and `_` produces `FallbackLiteral`. Operations `|`, `&`, `--` y `^` are initially retained `BinaryExpr`; the elaboration It specialises them according to the resolved types. A functional operation preserves both operands and does not transform into a merged list of branches.

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

Unlabelled arguments form the prefix `positionalArguments`. Arguments with `name =` form the suffix of `NamedCallArgument`.

The validation Contextual syntax rejects a position following the first element mentioned, so `CallExpr` you don’t need to represent that state invalid.

### Ambiguity regarding recipients

`receiver-tuple` y `structural-literal` converge in one of two ways: `PositionalStructuralLiteralExpr` o `NamedStructuralLiteralExpr`. The `MemberAccessExpr` y `CallExpr` subsequent ones retain their full form. The resolution select a signature, then choose from receiver a single structural unit and multiple receptors.

### Roads

A `qualified-name` When used as an expression, it produces `DottedPathExpr`, not a resolved reference.

## Literal expressions

### Exact and `Rum`

They are deleted `_` and the exponent and mantissa are normalised to canonical form. The provenance to the lexeme CST.

### `Char` y `Text`

Everything literal The word ‘ordinary’ in double quotation marks initially produces `TextTemplateExpr`. The elaboration subsequent contextual information turns it into `Char` when the type as expected, and the decoded text contains exactly one Unicode scalar. Single quotation marks do not produce any token literal.

### Booleans

`true` → `BoolLiteral(Enabled)`.

`false` → `BoolLiteral(Disabled)`.

### `empty`

Produces `EmptyLiteral`.

### `POINT_LITERAL`

It retains its original shape in `PointLiteral`; his magnitude The issue has still not been resolved, as expected.

## Templates

`TEXT_FRAGMENT` It is decoded after escape sequences and margin normalisation.

The difference between explicit and implicit closure disappears.

Any interpolation produces `ValueInterpolation`; `anchor{...}` does not belong to language.

Within the `format` of a magnitude from point, `unidad from contenedor` produces `ContextualPointComponentExpr`; you don’t just make up a receiver which wasn’t written.

## Structural literals

The positional form produces `PositionalStructuralLiteralExpr` with two mandatory elements and the rest.

The named form produces `NamedStructuralLiteralExpr` with one or more `NamedStructuralElement`.

The selection of alias, positional completeness and component defaults belong to validation/resolución later, as required type expected.

## Values separated by commas

The production:

```ebnf
value-expression ::= expression , [ "," , expression , { "," , expression } ] ;
```

is transformed as follows:

- No comma: original wording.
- With one or more commas: `CollectionLiteralExpr` of all expressions.

## Intervals

### Closed (abbreviated)

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

### Unit shared

The unit The final moves to the field `sharedUnit`; it is not duplicated at either end.

### Cyclical

The `cycle` behind the `PointDomainSyntax` select `CyclicPointDomain`; it does not alter the `Interval` content. The validation The condition prior to the AST requires that the preceding interval be finite, non-empty, closed on the left and open on the right.

### Stars

`*` produces `EffectiveIntervalBound`, without yet converting it to infinity or to a value dependent on the domain.

## Quantities and units

A literal a number followed by unit produces `QuantityValueExpr(Quantity(...))`.

Expressions of unit and dimension remove grouping brackets, but retain the tree structure imposed by multiplication and division.

## `start with` and tests

The form of an expression and the contributions block of `start with` produce a single `StartSet(contributions)`. The source order is retained only as provenance, not like semantics from activation.

The declaration top-tier of the module add `ModuleStartDecl`. Within a test, the same `StartSet` is a field from `TestDecl`.

`after assertion` y `after { assertion... }` produce a `TestAfterBlock` uniform.

## Elements that have not yet been standardised

The following are still pending for subsequent phases:

- Qualified names versus semantic access.
- Alias specific example of a literal structural.
- Multiple receivers versus receiver structural.
- Call ordinary versus call as a rule, or action.
- Type of a literal contextual.
- Evidence of a declared static expression.
- Compatibility of domains and cardinalities.
- Resolution units and prefixes.

## Transformation diagnostics

The transformation can only generate its own diagnostics when:

- The CST violates a invariant context required for normalisation.
- A property required to build an AST product is missing.
- Two specific ways of writing the same thing field standardised.
- One production The deck has no transformation rule.

A failure of names or types is not a diagnostic of this phase.

## Mechanical table

`cobertura-sintactica.yaml` It is comprehensive. Each production states:

- `cst`: specific category.
- `ast.disposition`.
- `ast.target` o reason discard/pliegue.

The provisions are as follows:

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

The initial corpus is in `casos/cst-ast.yaml`.

## Belonging, restriction and local transformations

`a has b` is projected onto `HasMember`; `a has not b`, a `HasNotMember`. `value in Domain` is projected onto `DomainRestrictionExpr`; `binding in source : predicate` preserve `SelectionExpr`. `collection-transform-suffix` folds like `CollectionTransformExpr`; there is no local in-house capacity.

