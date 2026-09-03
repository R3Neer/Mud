---
title: Surface abstract syntax
aliases:
  - Surface AST
  - Surface abstract syntax tree
tags:
  - mud/especificacion
  - mud/sintaxis
status: proposed
normative: true
depends-on:
  - 03-notacion
  - 05-texto-fuente
  - 06-lexico
  - 07-gramatica-concreta
  - sintaxis/cst-sin-perdidas
  - sintaxis/mud-surface-ast.asdl
questions:
  - Q-063
decisions:
  - D-102
  - D-101
  - D-015
  - D-032
  - D-054
  - D-066
  - D-095
  - D-070
  - D-071
  - D-072
  - D-073
  - D-074
  - D-075
  - D-076
  - D-077
  - D-079
  - D-080
  - D-081
  - D-082
  - D-084
  - D-085
  - D-086
  - D-087
  - D-088
  - D-090
  - D-091
  - D-092
  - D-093
  - D-096
  - D-097
  - D-100
  - D-098
---

# 08. Surface abstract syntax

## State and purpose

This chapter defines the normalised Surface AST for MUD 1.0. The AST preserves syntactic distinctions that affect later stages and removes punctuation, trivia, concrete grouping and sugar whose interpretation does not depend on name or type resolution.

The standard mechanical diagram is [[mud-surface-ast]]. This chapter explains its invariants and how it relates to other representations.

Nominal resolution operates on this AST and produces the normative HIR `nombres/mud-nominal-hir.asdl`, which instantiates symbols, scopes, bindings, anchors and a partial nominal graph without duplicating source syntax. Effective types, domains, cardinalities, dependencies and other inferred conclusions belong to later typing and elaboration stages whose mechanical representation is not yet finalised.

## Representation pipeline

```text
source text
→ tokens and trivia
→ lossless CST
→ contextual syntactic validation
→ normalised Surface AST
→ nominal resolution
→ Nominal HIR: symbols + scopes + bindings + anchors + partial graph
→ typing and elaboration
→ later semantic representation, not yet formalised
```

> [!rule] MUD-AST-001 — Surface responsibility
> The Surface AST does not contain resolved symbols, anchors, inferred types, computed effects or decisions that depend on a declaration found by name.

> [!rule] MUD-AST-003 — Border of the Nominal HIR
> The Nominal HIR may add identity and resolution, but no type semantics: it contains symbols, scopes, bindings, anchors and named edges. Effect types, effect domains, cardinalities, elaborated conversions and termination evidence are excluded from the Nominal HIR and belong to later typing and elaboration stages.

> [!rule] MUD-AST-002 — Standardisation
> Two concrete forms declared equivalent by this chapter produce the same AST form, except for their provenance.

## Relation with the CST

The CST preserves:

- Keywords.
- Delimiters.
- Commas and terminators.
- Grouping brackets.
- Comments and spaces.
- Exact notation of literals.
- Missing or unexpected recovery tokens.

The AST preserves:

- Category of declaration.
- Written names, still unresolved.
- Source order of semantically relevant lists.
- Domains, cardinalities and permissions.
- Structure of expressions and effects.
- Lexical distinctions that carry meaning, such as `and` versus `&`.
- Provenance sufficient for diagnostics and transformations.

A file containing syntactic errors may have a CST without producing a complete AST.

## Roots

### `MudProject`

`MudProject` aggregates the files that make up a compilation. It does not arise from a single-file production and has no single `SourceSpan`.

Its files are canonically serialised by normalised `relativePath`. This arrangement does not alter each file's internal order or assign semantic meaning to physical file order.

### `MudFile`

Every `MudFile` contains:

- Physical metadata.
- The default file metadata in source order.
- The list of `using`.
- The list of top-level declarations.

Metadata for subordinate owners is stored directly in their AST constructors, not in a `SourceSpan` side table. `using` directives are stored separately from declarations because the grammar requires them to form a header. Both groups retain source order.

The MUD path derived from the source path is metadata, not another AST declaration.

## Provenance

All nodes except `MudProject` possess `SourceOrigin`:

```text
Written(span)
Synthetic(basis, reason)
```

`Written` identifies a concrete region. `Synthetic` is used for elements genuinely introduced by normalisation. An omitted cardinality does not become `[1..1]` in the Surface AST: it remains `OmittedCardinality`, and elaboration determines its shape from the owner and initialiser.

The positions:

- They begin at zero.
- They use UTF-8 byte offsets.
- They have a unique exclusive end.
- Columns are counted using Unicode scalar values.

## Names

The AST uses distinct wrappers to prevent categories being mixed before resolution:

- `MudPath`.
- `QualifiedName`.
- `NominalName`.
- `FieldName`.
- `MemberName`.
- `RoleName`.
- `GivenName`.
- `ComponentName`.
- `VariableName`.
- `TypeRef`.
- `DeclarationRef`.

Capitalisation is adjusted according to the context, but the original text of the identifier is retained.

### Dotted paths

A sequence of identifiers linked solely by `.` is represented as `DottedPathExpr`. Later resolution determines whether its segments denote:

- MUD path and declaration.
- Declaration and member.
- Participant and field.
- A combination of the above.

When the chain contains calls, indices or other postfixes, it uses `MemberAccessExpr`, `IndexExpr` and `CallExpr`.

## Flags

MUD ASDL defines:

```text
flag = Disabled | Enabled
```

It is used for conceptually Boolean properties such as:

- `isAbstract`.
- `isOrdered` of a `family`.
- Outer mutability.
- Capability over members.
- Uniqueness.
- Whether an interval is cyclic.

It cannot be represented as an integer or a string.

## Metadata in stable owners

Every surface builder that directly represents a metadata-bearing owner preserves a `metadata_assignment*` sequence. This includes metadata-bearing nominal declarations, units, fields, components and participants. The specific bodies merely delimit the preamble; a separate `MetadataAttachment` is not produced, nor is the owner's identity or `SourceSpan` lost.

A grouped participant header is normalised into several descriptors, and the same metadata sequence is copied to each. `ModuleStartDecl` and `start with` inside a test do not receive their own sequence.

## `thing` declarations

A `ThingDecl` contains:

- `isAbstract`.
- Nominal name from the source.
- Direct predecessors in source order.
- Metadata assignments such as `~name`.
- Fields.
- Inherited field initialisers.

The AST does not sort ancestors alphabetically. Their order does not establish semantic priority, but is retained for provenance, formatting and diagnostics.

The Surface AST retains an explicit `Thing` in `as`. Later resolution treats it as a valid but redundant root; tooling may offer to remove it, but the formatter does not silently do so.

The preamble contains metadata declarations, while the remainder contains specific fields and initialisers. `metadata_assignment` distinguishes `StoredMetadataAssignment` and `CalculatedMetadataAssignment`; it retains only written or syntactically normalised information, without inventing intrinsic properties. Metadata is resolved and categorised by owner category and does not become ordinary fields.

### Concrete initialiser

```text
ThingInitializer(name, valueBlock)
```

It retains the written `fieldName = value-body` shape in a concrete or abstract `thing` body. It is not a `StoredFieldDecl` and is not included in `defaultValue`: the AST keeps schema defaults separate from initialisation contributions. `name` remains an unresolved `FieldName`, and the RHS normalises to `ValueBlock`; later resolution and elaboration ensure that the target is an inherited stored field and that the value satisfies its type and domain.

Validation before AST construction rejects a definition that contains both a field declaration and a `ThingInitializer` with the same name. A `fieldName: Type = value` declaration retains its `defaultValue` inside `StoredFieldDecl` and does not generate `ThingInitializer`.

The initialiser sequence remains separate from the field sequence. In an abstract `thing`, it represents inheritable initialisation contributions that do not instantiate the abstract thing's own stored data; in a concrete `thing`, it represents contributions to that thing's first materialisation. The CST continues to preserve the body's natural interleaved physical structure.

## Fields

### Stored field

```text
StoredFieldDecl(
    collectionMutable,
    name,
    shape,
    defaultValueBlock?,
    metadata*
)
```

`ValueShape` contains a `TypeExpr` normalised using nominal alternatives, an optional domain per alternative, and one outer collection specification.

### Calculated field

```text
CalculatedFieldDecl(name, shape?, valueBlock, metadata*)
```

It contains no outer mutability. An absent `shape` delegates type, domain and collection to inference. `ExplicitDerivedShape` retains a complete `TypeExpr`; `InferredDerivedShape` retains a written domain or collection without inventing a surface type. Elaboration combines these restrictions with the inferred type.

### Public fields

`PublicFieldDecl(name, shape?, valueBlock, metadata*)` shares the calculated form, but retains its own category because it belongs to the interface of `look` and `message`.

## Value shape

`ValueShape` is a structure reused by:

- Stored fields.
- Alias components.
- Stored `family` data.
- Participants `for`.

It contains the complete type expression, but not a default value or outer mutability. Those aspects belong to the owning context.

`GivenDecl` uses the same surface `TypeExpr` as other type contexts, so it can represent exact or functional dictionaries. `given` is a read-only parameter: any `mut` appearing in that form is retained solely for diagnostics and rejected statically during later validation and typing.

## Types

### Nominal unions

`TypeExpr` contains a non-empty sequence of `TypeAlternative` and a single outer collection specification. The Surface AST flattens groupings, removes identical duplicates and retains first-occurrence order for provenance and formatting. Union is associative, commutative and idempotent, but does not eliminate an alternative whose domain is contained by another. Redundant parentheses are not preserved.

Every `TypeAlternative` contains a `DeclaredType` and an optional `DomainExpr`. `SteppedDomain` retains interval and step separately; other surface domains use `ExpressionDomain` until semantic elaboration.

### Nominal type

```text
NamedType(TypeRef)
```

It includes both built-in types and programme-declared types. Whether a name denotes `Nat`, a `thing`, a `family`, an alias or a magnitude is decided later.


### Callable and reflected types

`CallableType(kind, receivers, givens)` retains types such as `Dragon.action(Volume)`, `(Attacker, Defender).action(Amount)` and `Dragon.look(Detail)`. At this stage `receivers` remain unresolved `TypeRef` values and `givens` are `TypeExpr`; the AST does not decide signature compatibility or variance, which remain open in Q-063.

`ReflectedType(value)` contains a written expression in type position whose form ends in `~type`, such as `MyDragon.Stats()~type`. Resolution and typing must prove that `value` statically produces `Type`; later elaboration obtains the represented type. The mechanical form of that elaboration is not yet fixed. An ordinary call without `~type` remains a value.
### Dictionary

```text
DictionaryType(keyType, valueTypeExpression)
```

The value retains its `TypeExpr`, so it may contain its own domain and collection. The collection written after the complete dictionary belongs to the outer `TypeExpr`.

The brackets required by the grammar for a nested dictionary are not preserved by the AST.

Functional-dictionary branches remain value nodes in the Surface AST and receive neither `AnchoredSymbol` nor a synthetic anchor. Resolution preserves source order and derives a dictionary-local `decision_branch_key` from the normalised selector; that key is used for reconstruction and internal dependencies, not for nominal resolution or metadata.

## Collections

The standard form is:

```text
CollectionSpec(
    cardinality,
    isUnique,
    order,
    elementsMutable
)
```

The order is a sum:

```text
Unordered
OrdinaryOrdered
OrderedBy(path)
```

An optional Boolean flag is not used because it would permit invalid states.

### Cardinality

`CollectionSpec` retains cardinality provenance. When none is written, `cardinalityOrigin = OmittedCardinality`: the Surface AST neither synthesises `[1..1]` nor infers an effective cardinality. Later elaboration determines it from the owner and, where applicable, its initialiser.

Explicit forms are normalised as follows:

- `[a]` → `[a..a]`.
- `[*]` → `[*..*]`.
- `[a..b]` retains both ends.

A written `*` remains `EffectiveCardinality` in the Surface AST. Later elaboration applies its effective value according to perspective and context.

### Duplicate modifiers

The CST can represent `unique unique`; pre-AST validation rejects it. The AST contains only one `isUnique` property.

## Aliases

`AliasDecl` contains:

- Nominal name.
- Sequence of direct ancestors that have not yet been resolved.
- Optional local definition.
- Metadata for the alias in source order.

The local definition is one of the following:

```text
AliasRepresentation(TypeExpr)
StructuralAlias(AliasMember*)
```

Structural members may include:

```text
AliasComponentDecl(AliasComponent)
AliasCalculatedFieldDecl(name, shape?, expression)
AliasDefaultOverride(name, value)
```

The absence of a definition is preserved when `as` is present; pre-AST validation rejects `alias A` without ancestors or a definition. An explicit empty body and an omitted body are distinct concrete forms, but both produce an empty local sequence.

A structural component:

- Does not support outer mutability.
- May have internal `[mut]` capability in its collection.
- It may have domain and static default.

A calculated field has no assignable storage; it may specify its shape and internal capability, and its value is recalculated from the expression. A local override may target only an inherited stored component and replaces only its default value.

Structural literals remain contextual. `PositionalStructuralLiteralExpr` requires at least two values and `NamedStructuralLiteralExpr` retains one or more named components; neither names a specific alias. Alias members therefore become available only after contextual elaboration or an explicit nominal conversion.

The same rule applies to basic literals. If the context expects a nominal alias whose representation the literal supports, elaboration constructs that alias directly without introducing a general implicit conversion. For example, with `alias PlayerName := Text`, `name: PlayerName = "Ada"` is valid. By contrast, an expression already typed as `Text`, such as `rawName`, does not silently become `PlayerName`; it requires `rawName to PlayerName`.

Later elaboration must distinguish alias construction guided by an expected type from an explicit nominal `to` conversion. The Surface AST does not add a contextual-alias node because it still retains the literal and its expected context; the mechanical representation of the resolved distinction is fixed at that later stage.

## Families

`FamilyDecl` contains:

- Declaration-order flag.
- Metadata for the family in source order.
- Stored or calculated data.
- Members.

Associated data do not support outer mutability. Stored data retain `metadata_assignment*` together with their shape and default value. Calculated data retain `derived_value_shape?`, `ValueBlock` and `metadata_assignment*`; their derived form matches calculated fields and can express a compatible type, domain or collection form.

Every declaration of associated data is a stable metadata-bearing owner and produces a `Field` descriptor belonging to the `family`, with `FieldKind.Stored` or `FieldKind.Calculated`. The `member.data` selection is a value, not a copy of the descriptor. Metadata therefore belongs to data declared only once and is not duplicated per member.

Every `FamilyMember` retains metadata assignments, such as `~name`, and assignments to stored data. `FamilyDataAssignment` deliberately has no `metadata` field: a member override merely selects the actual value of the stored slot and does not create a metadata-bearing owner. An omitted block makes both sequences empty.

## Result of `min` and `max`

`QuantifierExpr(Min|Max, ...)` needs no special default constructor. Elaboration assigns the element type and conservative cardinality `[0..1]` to its result; evaluation without candidates produces the ordinary `empty` value. Only a later context incompatible with zero elements introduces the normal cardinality failure.

## Magnitudes

There are separate constructors:

- `BaseMagnitudeDecl`.
- `DerivedMagnitudeDecl`.
- `PointMagnitudeDecl`.

The optional numeric representation is stored as a `DeclaredType`, rather than through a closed enumeration. A later static rule requires the resolved type to be a valid numeric representation.

In `BaseMagnitudeDecl`, absent `root_unit` deliberately represents a unitless base magnitude; it is not an incomplete node and does not request later unit synthesis. In that case `units` must be empty. The nominal dimension is incorporated during elaboration and cannot be inferred from the presence of a unit form.

### Dimensions

Dimensional expressions use dedicated nodes rather than general arithmetic expressions:

```text
DimensionProduct(first, links)
DimensionLink(MultiplyDimension | DivideDimension, term)
```

### Units

A root unit and an alternative unit use different variants because the latter has a quantitative equivalence:

```text
RootUnitDecl(name, metadata*)
AlternativeUnitDecl(name, equivalence, metadata*)
```

Neither `UnitProperties` nor `PrefixPolicy` exists in the Surface AST. A unit body is a general `metadata_assignment` preamble, and every declaration is retained without conversion to a parallel structure.

`~prefixes` is stored metadata of type `Prefix [* unique]` whose language default is `empty`. `empty`, `all` and `[kilo, milli]` remain ordinary MUD expressions in the AST; later resolution identifies `kilo`, `milli`, etc. as intrinsic `Prefix` values. The absence of `~plural` or `~abbreviation` is also preserved without synthesising presentation at this stage.

## Participants

### `for`

`ForParticipant` contains:

- Outer mutability.
- Required name.
- Complete `ValueShape`.
- Metadata for the descriptor in source order.

Does not support a default value.

### `on`

There are two variants:

```text
DirectOnParticipant(name, type, elementsMutable, metadata*)
RelatedOnParticipant(name, refinement?, source, elementsMutable, metadata*)
```

References between participants, including forward references and cycles, are preserved as expressions. Their joint resolution does not belong to the Surface AST.

### `given`

`GivenDecl` contains:

- Name is required.
- Read-only value shape.
- Optional default.
- Metadata for the descriptor in source order.

It can represent neither outer nor inner mutability.

### Clauses

`ForClause`, `OnClause` and `GivenClause` are distinct nodes. An omitted clause is absence, not an empty synthetic clause.

## Rules

The three classes have different constructors:

- `BooleanRuleDecl`.
- `ReactiveRuleDecl`.
- `AlwaysRuleDecl`.

A reactive rule stores:

- Pure local variables preceding their behaviour clauses.
- `when` activator as an `ExpressionBlock` with a temporal contract.
- Optional `if` guard as an `ExpressionBlock` with a Boolean contract.
- Effect block.

`changes` is an expression node, not a separate `when` clause variant.

In `always`, `InvariantBodySyntax` produces only the `ExpressionBlock`; the following `DiagnosticTailSyntax` becomes the `diagnostic` field of `AlwaysRuleDecl`. The rule may omit it, in which case the AST retains `diagnostic = absent`. Default warning and diagnostic text belong to validation and elaboration.

Default file metadata assignments do not use `ValueBlock`: they retain a static `FileMetadataAssignment`.

## Expression blocks and value blocks

`ExpressionBlock(locals, result)` contains only pure `LocalValueDecl` calculations and a final expression. A shorthand form normalises to `ExpressionBlock([], expression)`. It contains no stored variables, mutation, `LocalForEach` or `ValueBlock` nested as a primary expression.

`ValueBlock(statements, result)` contains `ValueStatement*` and a final expression. `ValueStatement` distinguishes calculated declarations, stored declarations, local mutation and `LocalForEach`. Calculated and stored declarations inside a `ValueBlock` in turn retain their initialisers as `ValueBlock`, so short and expanded forms converge without turning the block into an `expr`.

`LocalMutation` retains the unresolved surface destination; typing and elaboration later prove that the complete footprint belongs to storage created within the `ValueBlock`. `LocalForEach` uses `LocalStatementBlock`, not `EffectBlock`, and retains the `ExpressionBlock?` filter.

The owners of `ExpressionBlock` are Boolean rules, `always`, `when`, guards, action `after`, `for each` filters, selections, `exists`, `forall`, `count`, `min`, `max`, exact keys and functional selectors. The owners of `ValueBlock` are the value slots declared by the grammar: locals, fields, data/components, initialisers, dictionary values/results and metadata. `given` retains `expr? defaultValue` because its default does not accept a value block.

`min` and `max` retain `QuantifierExpr` and a Boolean `ExpressionBlock`. Elaboration returns the first or last accepted witness according to `source`'s semantic order; `Sum` does not exist in `quantifier_kind`.

When metadata and `ValueBlock` physically share a compatible descriptor body, the AST extracts metadata into the owner's `metadata` field and retains only value statements in `ValueBlock`.

## Actions

The Surface AST uses a single `ActionDecl`.

There is no semantic classification of elementary versus compound actions. `ActionCallCandidateEffect` retains only a `postfix-expression` occupying an effect position whose callable nature must be resolved later; that resolution decides its meaning, not an alleged elementary or compound class of the action owner.

An action contains:

- Optional `for` participants.
- Optional `given` parameters.
- Pure local values preceding the behavioural clauses.
- Optional Boolean guard and diagnostic.
- Effects block.
- Optional Boolean `after` postcondition and diagnostic.

## `look` and `message`

`LookDecl` retains `for` participants, `given` parameters and public fields.

`MessageDecl` retains `on` participants, pure local values preceding its behavioural clauses, a Boolean activator, an optional Boolean guard and public fields.

They cannot be reduced to generic rules or actions because their subsequent contracts are different.

## Tests

`TestDecl` contains:

- Local `StartSet`.
- Effects block.
- A `TestAfterBlock` with initial local declarations and a non-empty sequence of assertions.

The shape `after expr` produces a block with no statements and an assertion. In the form `after { ... }`, all local declarations precede the first assertion.

Module and test `start with` forms share `StartSet`, which retains a single contribution sequence; only the module form is wrapped in `ModuleStartDecl`.

## Effect blocks

A short `then` and a braced `then` normalise to the same `EffectBlock`. The block retains a non-empty source-ordered `then_statement` sequence and an optional failure diagnostic. Each statement is `EffectStatement`, `LocalCalculatedStatement` or `LocalStoredStatement`; later validation requires at least one observable effect.

The AST does not assume sequential or simultaneous execution other than that defined in subsequent chapters; it merely preserves the declared structure.

## Effects

There are specific nodes for:

- Assignment.
- Addition of a value.
- Addition of a field.
- Removal.
- Creation.
- Destruction.
- Action-call candidate.
- Iteration `for each`.

### Comma-separated values

A `value-expression` with several elements normalises to:

```text
CollectionLiteralExpr(elements)
```

A single-element form remains that expression rather than becoming a synthetic collection.

### Assignable expressions

`AssignableExpr` retains a root and member or index suffixes. Verifying that the path ends in a writable location belongs to resolution, typing and effects. The Surface AST does not expand a path crossing immutable aliases: it retains its suffixes, and later elaboration decides whether it can rebuild intermediate values and propagate write-back to externally writable storage. A missing exact key at an intermediate stage is likewise not rewritten in the AST.

### Iteration `for each`

`ForEachEffect(binding, source, step?, filter?, body)` retains the `by` expression and the filter as an `ExpressionBlock`, and normalises either a short effect or the block following `:` to an `EffectBlock`. Addressability, default steps, compatibility, filter order and zero steps belong to elaboration.

## Expressions

### Operators

The AST preserves lexically distinct operators when MUD assigns them different contracts:

- `WordAnd` opposite `SymbolAnd`.
- `WordOr` opposite `SymbolOr`.
- `WordXor` opposite `SymbolXor`.

This allows `when` to distinguish temporal composition written with ordinary Boolean words from composition written with symbols.

### Comparisons

A string such as:

```mud
0 <= x < 10
```

is represented by `ComparisonChainExpr`, rather than arbitrary binary pairings.

Non-chainable comparisons result in a single edge in the chain or an equivalent validated node.

`is not` produces `IsNotRelation`; it is not reduced to an outer `not`, because nominal narrowing must directly record the negative test.

### Selection and quantifiers

`SelectionExpr(binding, source, step?, predicate)` preserves `step?` and normalises the predicate to `ExpressionBlock`. `QuantifierExpr(kind, variable, source, step?, body)` does the same for the five quantifiers `exists`, `forall`, `count`, `min` and `max`. The AST does not decide the Boolean contract of `body` or the validity of the required source order.

### Conversions

`to Type` and `in unit` produce `ConversionExpr` with different destinations. The grammar's postfix barrier already determines their grouping, but not compatibility.

### Postfix and calls

`MemberAccessExpr`, `IndexExpr` and `CallExpr` are constructed from left to right.

`CallExpr` retains:

- The called expression.
- The prefix of positional arguments.
- The named-argument suffix.

The separator prevents a positional element from being placed after a named element.

A possible interpretation of:

```mud
(attacker, defender).CanAttack()
```

Whether this denotes several receivers or a single structural value remains pending signature resolution. The Surface AST retains the structural form and postfix chain.

### `Rand`

`Rand(expr)` produces `RandomExpr`; it is neither a type nor an ordinary call.

### Selection and `take`

`binding in source [by step] : predicate` produces `SelectionExpr`. It retains the binding, source, optional step and predicate as an `ExpressionBlock` without materialising the resulting collection. The binding introduces names only into the predicate.

`take amount from source` produces `TakeExpr`. The Surface AST does not determine whether the source is a list, text, dictionary, enumerable domain or unordered collection; later resolution determines whether to take a canonical prefix or a reproducible sample.

The composition of both forms is structural. `take n from player in players : condition` contains a `SelectionExpr` as a source of `TakeExpr`; `player in take m from players : condition` contains a `TakeExpr` as a source of `SelectionExpr`.

### `all`

The contextual literal `all` produces `AllLiteral`. Its domain and whether it is static or dynamic are determined during type checking; the Surface AST does not enumerate its values. The prefix form `all D` produces `PrefixExpr(EnumerateAll, D)` and explicitly preserves the requested materialisation.

### Quantifiers

`exists`, `forall`, `count`, `min` and `max` share `QuantifierExpr` with their own enum, an optional `step?`, and an `ExpressionBlock` body.

### Collection operators

`--` produces `CollectionDifference`, distinct from `Subtract`. The updates `|=`, `&=`, `^=` and `--=` produce `UnionAssign`, `IntersectionAssign`, `SymmetricDifferenceAssign` and `DifferenceAssign`, respectively; they are not reduced to `Assign` because update class participates in concurrent consolidation.

## Templates `Text`

A template is an ordered sequence of:

- `TextFragment` with decoded text.
- `ValueInterpolation`.

The AST does not retain:

- Explicit or implicit closing quotation marks.
- Physical margin of the multiline literal.
- Escape sequences used to achieve the same effect.

The CST does keep them.

Ordinary double-quoted text always appears in the Surface AST as `TextTemplateExpr`. Later elaboration may turn it into a `Char` value when the context requires `Char`, it contains no interpolations, and its decoded value is exactly one Unicode scalar. The Surface AST therefore has no separate lexical `CharLiteral` constructor.

`NumericTextFormat` displays whole and optional fractional widths without retaining the specific colons.

Within a point magnitude's `format`, `unit from container` produces `ContextualPointComponentExpr`; it does not invent an explicit receiver absent from the source.

## Intervals

All forms are standardised to:

```text
Interval(lower, lowerBoundary, upper, upperBoundary, sharedUnit?)
EmptyInterval(sharedUnit?)
```

Standardisation:

- `a..b` → closed interval.
- `[a]` → a closed interval with both endpoints included.
- Shapes with unit shared → unit in `sharedUnit`.
- `[] unit` → `EmptyInterval(unit)`.
- `[a..b) cycle` → `CyclicPointDomain` over the specified semi-open interval.

Parentheses and square brackets survive only as `OpenBoundary` or `ClosedBoundary`.

`*` endpoints remain `EffectiveIntervalBound` values until elaboration.

## Quantity values and units

`QuantityValueExpr` contains a numeric literal and a `UnitProduct`.

Unit expressions and dimensional expressions have separate trees, even though both use `*`, `/` and parentheses in concrete syntax.

A `UNIT_FORM` is preserved as contextual source text. Its catalogue resolution belongs to later phases.

The absence of a space between number and unit does not affect the AST. `3m` and `3 m` produce the same output; the exact source form remains available in the CST and the formatter outputs the latter.

## Numeric literals

The AST holds a canonical representation of the value, not necessarily the exact lexeme. For example:

```mud
1_000
1000
```

may produce the same `ExactNumberLiteral("1000")`.

The mathematical precision of `Num` and the binary64 interpretation of `Rum` are established later.

## Preserved order and canonical order

The source order is preserved:

- Statements within a file.
- Predecessors.
- Fields and components.
- Family data and members.
- Participants and `given`.
- Arguments.
- Effects and assertions.

Only `MudProject` defines canonical file serialisation by path. No other list is automatically sorted in the Surface AST unless a specific rule states otherwise.

## Invalid states excluded

A Surface AST must not contain:

- A missing cardinality value.
- Two modifiers `unique`.
- Two collection-order modifiers.
- Mutable `given` parameters.
- Duplicate metadata declarations within the same unit.
- Resolved symbol or anchor.
- An inferred type inserted as though it had been written.
- Ordinary comments.
- Recovery tokens.

## Structural serialisation

Canonical AST serialisation:

1. Sort files by normalised path.
2. Preserve the order of internal sequences.
3. Use ASDL constructor names.
4. Skip trivia and punctuation.
5. Include `SourceOrigin` except in comparison views that expressly exclude it.
6. Serialise enums by their canonical name.

This serialisation is used for snapshots, caching and tooling. It is not MUD code and does not replace the pretty-printer.

## Coverage

Every production from [[mud]] must appear in:

- `mud-syntax-kinds.yaml`.
- `cobertura-sintactica.yaml`.

The coverage specifies whether the production:

- It builds a node.
- It is normalised.
- It is returned to its parent.
- It is discarded as layout.
- It remains contextual up to resolution.

`validate_syntax_model.py` checks that it matches.

## Conformance

A conforming Surface AST implementation must:

1. Generate constructors equivalent to `mud-surface-ast.asdl`.
2. Apply all standardisations from [[cst-a-ast-superficial]].
3. Reject the excluded states before the AST.
4. Preserve provenance.
5. Do not anticipate resolution, typing or IR.
6. Maintain the required operator differences.
7. Enable the creation of a stable structural form for testing.

## Normalisation of empty bodies of `thing`

`thing A`, `thing A;` and `thing A {}` produce the same `ThingDecl` with zero fields and no intrinsic overrides. The CST preserves the written body and terminator; the AST creates no empty body node.


## Source examples → AST

```mud
A -> B -> C
```

is normalised as `ExactDictionaryType(A, ExactDictionaryType(B, C))`.

```mud
value iis not PersonId
```

produces `ExactTypeTestExpr(value, PersonId, Enabled)`.

```mud
"{value~anchor}"
```

produces `TextTemplateExpr([ValueInterpolation(MetadataAccessExpr(value, anchor))])`.

```mud
values: Nat = [1, 2, 3]
```

preserves `OmittedCardinality` in the Surface AST and obtains `[3]` only during field elaboration.

```mud
start with {
    all,
    empty
}
```

produces `StartSet(contributions=[AllLiteral, EmptyLiteral])`.

## Product types and dictionary types

`PositionalProductType` and `NamedProductType` retain the components of anonymous structural products. `ExactDictionaryType` and `DecisionDictionaryType` represent exact dictionaries and branch-defined functional dictionaries, respectively. The mechanical name `Decision` is retained for schema stability.

A chain folds inwards from the right:

```text
A -> B [2] --> C [3 ordered]
```

conceptually produces:

```text
ExactDictionaryType(
    A,
    DecisionDictionaryType(B, C, FirstMatch, [3]),
    [2]
)
```

Validation after resolution rejects an arrow as a partial union alternative, even when introduced through an alias.

## Cardinality omitted

`CollectionSpec` preserves `WrittenCardinality` or `OmittedCardinality`. Thus:

```mud
values: Nat = [1, 2, 3]
```

the Surface AST retains the omission. Later elaboration of an immutable stored field infers `[3]` and records `InferredFromInitializer`; parsing does not generate that information.

## Nominal comparisons

`is` remains represented by transitive nominal comparison. `iis` produces its own node because its narrowing behaviour differs:

```text
ExactTypeTestExpr(value, PersonId, negated=Disabled)
ExactTypeTestExpr(value, PersonId, negated=Enabled)
```

The second form corresponds to `value iis not PersonId`. Resolution requires the right-hand operand to be a nominal type.

## Dictionary set operations

The Surface AST preserves `|`, `&`, `--` and `^` as `BinaryExpr`, because their exact category depends on resolved types. Elaboration specialises them as exact or functional dictionary operations. A functional operation preserves its operands; it does not create a new branch list.

## Metadata, text and activation

`element~metadata` always produces `MetadataAccessExpr`. There is no assignable `MetadataSuffix`: `AssignableExpr` retains only `MemberSuffix` and `IndexSuffix`, so no `~` access may be an effect destination. The Surface AST also does not determine whether the receiver supports the property; that check is deferred until the receiver's static category is resolved. Every interpolation produces `ValueInterpolation`, including:

```mud
"{value~anchor}"
```

`AnchorInterpolation` does not exist. `start with` produces `StartSet(contributions)` with one contribution sequence. `ActionDecl` preserves `PublicAction` or `Subaction`.

## Ownership, restrictions and local adaptation of collections

`has` and `has not` normalise to `HasMember` and `HasNotMember`. `value in Domain` produces `DomainRestrictionExpr`; a selection retains `SelectionExpr` with its original binding. Local specifications produce `CollectionTransformExpr` with `LocalCollectionTransform`, without `mut` capability.
