---
title: Abstract syntax superficial
aliases:
  - AST superficial
  - Surface AST
tags:
  - mud/especificacion
  - mud/sintaxis
status: propuesta
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

# 08. Abstract syntax superficial

## State and purpose

This chapter defines the Surface AST standardised MUD 1.0. The AST preserves the syntactic distinctions that affect subsequent stages and removes punctuation, trivia, specific groups and sugars whose interpretation does not depend on name resolution or types.

The standard mechanical diagram is [[mud-surface-ast]]. This chapter explains its invariants and how it relates to other representations.

The nominal resolution operates on this AST and produces the regulatory HIR `nombres/mud-nominal-hir.asdl`, which instantiates symbols, scopes, bindings, anchors and a nominal graph partial without duplicating the source syntax. Effective types, domains, cardinalities, dependencies and other inferred conclusions belong to later stages of typing and elaboration the mechanical representation of which has not yet been finalised.

## A series of performances

```text
texto fuente
→ tokens y trivia
→ CST sin pérdidas
→ validación sintáctica contextual
→ AST superficial normalizado
→ resolución nominal
→ HIR nominal: símbolos + scopes + bindings + anclas + grafo parcial
→ tipado y elaboración
→ representación semántica posterior todavía no formalizada
```

> [!rule] MUD-AST-001 — Superficial responsibility
> The Surface AST does not contain resolved symbols, anchors, inferred types, computed effects or decisions that depend on a declaration found by name.

> [!rule] MUD-AST-003 — Border of the Nominal HIR
> The Nominal HIR you can add identity y resolution, but no type semantics: it contains symbols, scopes, bindings, anchors and named edges. Effect types, effect domains, cardinalities, elaborate conversions and evidence of termination are excluded from the Nominal HIR and belong to later stages of typology and elaboration.

> [!rule] MUD-AST-002 — Standardisation
> Two specific forms declared equivalent by this chapter produce the same AST form, except for their provenance.

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
- Names written down, still unresolved.
- Order semantically relevant lists.
- Domains, cardinalities and permissions.
- Structure of expressions and effects.
- Lexical differences that carry meaning, such as `and` opposite `&`.
- Provenance sufficient for diagnostics and transformations.

A file containing syntactic errors may have a CST without producing a complete AST.

## Roots

### `MudProject`

`MudProject` adds the files that make up a compilation. It does not come from a production consists of a single file and does not have a `SourceSpan` unique.

Its files are serialised canonically by `relativePath` standardised. This arrangement does not alter the internal order of each file, nor does it attribute any semantic meaning to the physical order of the files.

### `MudFile`

Every `MudFile` contains:

- Physical metadata.
- The default file metadata in source order.
- The list of `using`.
- The list of top-level declarations.

Metadata for subordinate owners is stored directly in their AST constructors, not in a side table because `SourceSpan`. The `using` They are stored separately from the declarations because the grammar requires them to form a header. Both groups retain their source order.

The path from the MUD derived from the path is metadata and not just one declaration AST.

## Procedencia

All nodes except `MudProject` possess `SourceOrigin`:

```text
Written(span)
Synthetic(basis, reason)
```

`Written` indicates a specific region. `Synthetic` is used for elements that are actually introduced by standardisation. A cardinality omitted does not become `[1..1]` in the Surface AST: preserve `OmittedCardinality` and the elaboration determines its shape according to the owner and the initialiser.

The positions:

- They start from scratch.
- They use UTF-8 byte offsets.
- They have a unique end cap.
- Columns are counted using Unicode scalar values.

## Names

AST uses different wrappers to prevent categories from being mixed up before the resolution:

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

### We walk with point

A sequence of identifiers linked exclusively by means of `.` is written as `DottedPathExpr`. The resolution It will then determine whether its segments denote:

- MUD path and declaration.
- Declaración y miembro.
- Participante y campo.
- A combination of the above.

When the string contains calls, indices or other postfixes, the following are used `MemberAccessExpr`, `IndexExpr` y `CallExpr`.

## Flags

ASDL- The MUD defines:

```text
flag = Disabled | Enabled
```

It is used for conceptually Boolean properties such as:

- `isAbstract`.
- `isOrdered` of a `family`.
- Mutability outdoors.
- Capacity regarding members.
- Uniqueness.
- The periodicity of an interval.

It cannot be represented as an integer or a string.

## Metadata in stable owners

Any superficial builder who directly represents a owner metadata-bearing preserves a sequence `metadata_assignment* metadata`. This includes metadata-bearing nominal declarations, units, fields, components and participants. The specific bodies merely delimit the preamble; a `MetadataAttachment` side, nor is the `SourceSpan` such as identity from the owner.

A grouped header of participants is standardised across several descriptors and the same metadata sequence is copied to each one. `ModuleStartDecl` and the `start with` inside a test do not receive their own sequence.

## Statements by `thing`

One `ThingDecl` contains:

- `isAbstract`.
- Nominal source name.
- Direct predecessors in source order.
- Metadata assignments such as `~name`.
- Fields.
- Inherited field initialisers.

The AST does not list predecessors in alphabetical order. The order in which they appear is not ranked in order of priority semantics does not remove its value such as provenance, format and diagnostic.

The Surface AST retains a `Thing` explicitly stated in `as`. The resolution The latter treats it as a redundancy of the root It is valid, and the tooling allows it to be removed; the formatter does not silently remove it.

The preamble contains metadata declarations, whilst the rest of the body contains specific fields and initialisers. `metadata_assignment` distinguish `StoredMetadataAssignment` y `CalculatedMetadataAssignment`; it retains only written or syntactically standardised information, without inventing any intrinsic properties. Metadata is resolved and categorised by category of owner and do not become ordinary fields.

### Concrete initialiser

```text
ThingInitializer(name, valueBlock)
```

It retains its shape `fieldName = value-body` written on the body of a `thing`, whether concrete or abstract. It is not a `StoredFieldDecl` and is not included in `defaultValue`: AST keeps the schema default and the initialisation contribution separate. `name` remains as `FieldName` unresolved, and the RHS normalises to `ValueBlock`;  the resolution y elaboration Subsequent checks ensure that the target is a stored field inherited and that the value satisfy his type y domain.

The validation The AST preliminary ruling rejects the idea that a single definition could contain a declaration premises of field and a `ThingInitializer` of the same name. A declaration `fieldName: Type = value` retains its `defaultValue` inside the `StoredFieldDecl` and does not generate `ThingInitializer`.

The sequence of initialisers is kept separate from that of the fields. In a `thing` abstracta represents inheritable initialisation contributions that are not instantiated own stored data; in one particular instance, it shows contributions to his first materialisation. The CST continues to preserve the body’s natural, interwoven physical structure.

## Fields

### Campo almacenado

```text
StoredFieldDecl(
    collectionMutable,
    name,
    shape,
    defaultValueBlock?,
    metadata*
)
```

`ValueShape` contains a `TypeExpr` normalised using nominal alternatives, domain optional per alternative and a single one specification from collection outdoors.

### Campo calculado

```text
CalculatedFieldDecl(name, shape?, valueBlock, metadata*)
```

Does not contain mutability outdoors. `shape` absent proxy type, domain y collection to the inference. `ExplicitDerivedShape` retains a `TypeExpr` complete; `InferredDerivedShape` retains a domain o collection written without making up a type superficial. The elaboration combines these restrictions with the type inferred.

### Public fields

`PublicFieldDecl(name, shape?, valueBlock, metadata*)` It shares the calculated form, but retains its own category because it belongs to the interface of `look` y `message`.

## How to value

`ValueShape` is a structure reused by:

- Stored fields.
- Components of alias.
- Data stored from `family`.
- Participants `for`.

It contains the expression of type complete, but not predetermined or mutability external. These aspects form part of the context owner.

`GivenDecl` use the same one `TypeExpr` more superficial than other contexts of type, so it can represent exact or functional dictionaries. `given` is a read-only parameter: any `mut` the fact that it appears in that form is retained solely for diagnostic and is statically rejected during the subsequent stages of validation and typed.

## Types

### Nominal joints

`TypeExpr` contains a non-empty sequence of `TypeAlternative` and just one specification from collection exterior. The Surface AST flattens groupings, removes identical duplicates and retains the order of the first occurrence for provenance and format. The union The operation is associative, commutative and idempotent, but it does not eliminate an alternative by inclusion of domain. Redundant brackets are not preserved.

Every `TypeAlternative` contains a `DeclaredType` and a `DomainExpr` optional. `SteppedDomain` separately retains the interval and step; the other surface domains use `ExpressionDomain` until his elaboration semantics.

### Type nominal

```text
NamedType(TypeRef)
```

It includes both built-in types and types declared by the programme. Whether a name is `Nat`, a `thing`, a `family`, a alias or a magnitude That will be decided later.


### Callable and reflected types

`CallableType(kind, receivers, givens)` retains the form of types such as `Dragon.action(Volume)`, `(Attacker, Defender).action(Amount)` o `Dragon.look(Detail)`. At this stage `receivers` remain `TypeRef` unresolved and `givens` are `TypeExpr`; the AST does not decide compatibility nor variance signatures, open question in Q-063.

`ReflectedType(value)` contains a written expression in the position of type whose form ends in `~type`, such as `MyDragon.Stats()~type`. The resolution and the typing must demonstrate that `value` generates statically `Type`; the elaboration The latter obtains the type represented. The mechanical form of that elaboration has not yet been set. A call ordinary without `~type` remains a value.
### Dictionary

```text
DictionaryType(keyType, valueTypeExpression)
```

The value retains its `TypeExpr`, so it may contain domain y collection their own. The collection written after the comprehensive dictionary belongs to the `TypeExpr` outdoors.

The brackets required by the grammar for a nested dictionary are not preserved by the AST.

The branches of a functional dictionary remain nodes of value in the Surface AST and do not receive `AnchoredSymbol` nor anchor synthetic. The resolution retains its source order and derives a `decision_branch_key` local to the dictionary based on the normalised selector; that key is used for reconstruction and internal dependencies, not for nominal resolution nor metadata.

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

A Boolean ‘plus’ operator is not used path optional because it would allow invalid states.

### Cardinalidad

`CollectionSpec` retains the provenance of the cardinality. If none is entered, `cardinalityOrigin = OmittedCardinality`: the Surface AST does not summarise `[1..1]` nor does it yet imply a cardinality effective. The elaboration The latter determines it according to the owner and, where applicable, its initialiser.

Explicit forms are normalised as follows:

- `[a]` → `[a..a]`.
- `[*]` → `[*..*]`.
- `[a..b]` retains both ends.

A winger `*` the text remains as `EffectiveCardinality` in the Surface AST. The elaboration The latter applies its value effective depending on the perspective and context.

### Duplicate modifiers

The CST can represent `unique unique`; the validation prior to the AST rejects it. The AST contains only one property `isUnique`.

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
AliasCalculatedFieldDecl(nombre, forma?, expresión)
AliasDefaultOverride(nombre, valor)
```

The lack of definition persists when it exists `as`; the validation prior to the AST, rejects `alias A` without antecedents or definition. An explicit empty body and the omission of a body are distinct concrete forms, but both produce a local empty sequence.

A structural component:

- Does not support mutability outdoors.
- It may have internal capacity `[mut]` in his collection.
- It may have domain and static default.

A derived field If it has no assignable load, it can specify the shape and internal capacity, and the value is recalculated based on this expression. A local override can only target a legacy stored component and only replaces its default value.

Structural literals remain contextual. `PositionalStructuralLiteralExpr` requires at least two values and `NamedStructuralLiteralExpr` retains one or more named components; a alias specifically. Therefore, the members of the alias are only available after elaboration contextual or the result of an explicit nominal conversion.

The same rule applies to basic literals. If the context expects a nominal alias whose representation is supported by the literal, the elaboration builds that directly alias without introducing a general implicit conversion. For example, with `alias PlayerName := Text`, `name: PlayerName = "Ada"` is valid. On the other hand, an expression that already contains type `Text`, as a variable `rawName`, it does not silently switch to `PlayerName`; requires `rawName to PlayerName`.

The elaboration The latter must distinguish the construction of alias led by the type expected nominal conversion `to` explicitly stated. The Surface AST does not add a node of alias contextual because it still retains the literal and the context that awaits it; the mechanical representation of the distinction that has been established will be fixed at that stage.

## Families

`FamilyDecl` contains:

- Order flag for declaration.
- Metadata for the family in source order.
- Stored or calculated data.
- Members.

The associated data do not support mutability external. The stored data retains `metadata_assignment* metadata` along with its format and default value. The calculated data retains `derived_value_shape? shape`, his `ValueBlock` y `metadata_assignment* metadata`; the derived form is the same as in calculated fields and can express type, domain or a way of collection compatible.

Every declaration An associated data item is a owner stable metadata-bearing and is produced as descriptor `Field` subject to the `family`, with `FieldKind.Stored` o `FieldKind.Calculated`. The screening `member.data` is a value, not a copy of the descriptor. Therefore, metadata relates to data that is declared only once and is not duplicated because member.

Every `FamilyMember` retains metadata assignments, such as `~name`, and assignments to stored data. `FamilyDataAssignment` deliberately remains without field `metadata`: a rewriting of member just select the value the actual value of the stored slot and does not create a owner metadata-bearing. An omitted block results in both sequences being empty.

## Result from `min` y `max`

`QuantifierExpr(Min|Max, ...)` It does not require a special default constructor. The elaboration assigns to the result the type element and a cardinality conservative `[0..1]`; a round without candidates results in the value ordinary `empty`. Only a subsequent context that is incompatible with zero elements introduces the failure normal for cardinality.

## Quantities

There are separate constructors:

- `BaseMagnitudeDecl`.
- `DerivedMagnitudeDecl`.
- `PointMagnitudeDecl`.

The optional numerical representation is stored using `DeclaredType`, rather than through a closed enumeration. A subsequent static rule requires that the type provided that the solution is a valid numerical representation.

In `BaseMagnitudeDecl`, `root_unit` 'absent' deliberately represents a magnitude base without units; it is not an incomplete node nor does it request a unit subsequent synthesis. In that case `units` must be empty. The nominal dimension is incorporated during the elaboration and it cannot be inferred from the presence of a form of unit.

### Dimensions

Dimensional expressions use dedicated nodes rather than general arithmetic expressions:

```text
DimensionProduct(first, links)
DimensionLink(MultiplyDimension | DivideDimension, term)
```

### Units

One unit root and one alternative consists of different variants because the second has quantitative equivalence:

```text
RootUnitDecl(name, metadata*)
AlternativeUnitDecl(name, equivalence, metadata*)
```

It does not exist `UnitProperties` nor `PrefixPolicy` in the Surface AST. The body of unit is a general introduction to `metadata_assignment` and every declaration is retained without being converted to a parallel structure.

`~prefixes` is metadata stored from type `Prefix [* unique]` whose default language is `empty`. `empty`, `all` y `[kilo, milli]` Ordinary MUD expressions remain in the AST; the resolution the following identifies `kilo`, `milli`, etc., as inherent values of `Prefix`. The absence of `~plural` o `~abbreviation` it is also preserved, without being synthesised presentation at this stage.

## Participants

### `for`

`ForParticipant` contains:

- Mutability outdoors.
- Name is required.
- `ValueShape` complete.
- Metadata for the descriptor in source order.

Does not support a default value.

### `on`

There are two variants:

```text
DirectOnParticipant(name, type, elementsMutable, metadata*)
RelatedOnParticipant(name, refinement?, source, elementsMutable, metadata*)
```

References between participants, including forward references and cycles, are preserved as expressions. Their resolution joint does not belong to the Surface AST.

### `given`

`GivenDecl` contains:

- Name is required.
- How to value read-only.
- Optional default.
- Metadata for the descriptor in source order.

It cannot represent mutability neither outside nor inside.

### Clauses

`ForClause`, `OnClause` y `GivenClause` are distinct nodes. An omitted clause is an absence, not an empty synthetic clause.

## Rules

The three classes have different constructors:

- `BooleanRuleDecl`.
- `ReactiveRuleDecl`.
- `AlwaysRuleDecl`.

One reactive rule stores:

- Pure local variables preceding their behaviour clauses.
- Activator `when` such as `ExpressionBlock` with contract temporary.
- Guard `if` optional, such as `ExpressionBlock` with contract Boolean.
- Effects block.

`changes` It is a node of expression, not a separate clause variant `when`.

In a nutshell `always`, `InvariantBodySyntax` is produced exclusively by the `ExpressionBlock`; the `DiagnosticTailSyntax` following the locking mechanism, this results in the field `diagnostic` from `AlwaysRuleDecl`. The rule may omit it, and the AST retains `diagnostic = absent`. The warning and the diagnostic The default settings belong to validation y elaboration.

The default file metadata settings do not use `ValueBlock`: they retain a constant stored allocation `FileMetadataAssignment`.

## Expression blocks and value

`ExpressionBlock(locals, result)` contains only `LocalValueDecl` pure calculations and a final expression. A shorthand form normalises to `ExpressionBlock([], expression)`. It contains no stored variables, mutation, `LocalForEach` nor `ValueBlock` nested as a primary expression.

`ValueBlock(statements, result)` contains `ValueStatement*` and a final remark. `ValueStatement` distinguish declaration calculated, declaration stored, local mutation and `LocalForEach`. The calculated and stored expressions of a `ValueBlock` in turn retain their initialiser as `ValueBlock`, so that the short and long forms converge without turning the block into `expr`.

`LocalMutation` retains the unresolved surface destination; typed/elaboración They then demonstrate that the complete footprint belongs to the storage created within the `ValueBlock`. `LocalForEach` use `LocalStatementBlock`, no `EffectBlock`, and keep the filter `ExpressionBlock?`.

The owners of `ExpressionBlock` these are Boolean rules, `always`, `when`, guards, `after` from action, filters for `for each`, selection, `exists`, `forall`, `count`, `min`, `max`, exact keys and functional selectors. The owners of `ValueBlock` are the slots from value declared by the grammar: locals, fields, data/componentes, initialisers, values/resultados dictionary and metadata. `given` retains a `expr? defaultValue` because its default value does not take a block of value.

`min` y `max` retain `QuantifierExpr` y `ExpressionBlock` Boolean. The elaboration returns the first/último witness accepted in accordance with the semantic order of `source`; `Sum` does not exist in `quantifier_kind`.

When metadata and `ValueBlock` physically share the body of a descriptor If compatible, AST extracts the metadata from the field `metadata` from the owner and retains only the sentences from value in `ValueBlock`.

## Shares

The Surface AST use a single `ActionDecl`.

There is no classification semantics elementary actions versus compound actions. `ActionCallCandidateEffect` it only retains one `postfix-expression` holds a position as effect whose callable nature must be resolved later; the resolution It is you who decide your own destiny, not some so-called elemental class/compuesta of the action owner.

One action contains:

- Participants `for` optional.
- `given` optional.
- Pure local functions preceding their behavioural clauses.
- Optional Boolean guard and diagnostic.
- Effects block.
- Boolean postcondition `after` optional and diagnostic.

## `look` y `message`

`LookDecl` retains participants `for`, `given` and public property.

`MessageDecl` retains participants `on`, pure local variables preceding their behaviour clauses, Boolean activator, optional Boolean guard and public properties.

They cannot be reduced to generic rules or actions because their subsequent contracts are different.

## Tests

`TestDecl` contains:

- Home starting line-up.
- Effects block.
- A `TestAfterBlock` with initial local declarations and a non-empty sequence of assertions.

The shape `after expr` produces a block with no statements and an assertion. In the form `after { ... }`, all local declarations precede the first assertion.

`start with` from module and from test share `StartSet`, which retains a single sequence of contributions; only the first one is wrapped in `ModuleStartDecl`.

## Effect blocks

A `then` brief and a `then` those in brackets are standardised to the same `EffectBlock`. The block retains a non-empty sequence of `then_statement` in source order and a diagnostic from failure optional. Each statement is `EffectStatement`, `LocalCalculatedStatement` o `LocalStoredStatement`; the validation The latter requires at least one effect observable.

The AST does not assume sequential or simultaneous execution other than that defined in subsequent chapters; it merely preserves the declared structure.

## Effects

There are specific nodes for:

- Allocation.
- Addition of value.
- Addition of field.
- Deletion.
- Creation.
- Destruction.
- Candidate for call from action.
- Iteration `for each`.

### Values separated by commas

`value-expression` with several elements, it is normalised to:

```text
CollectionLiteralExpr(elements)
```

The form of a single element remains as that expression, not as a collection synthetic.

### Allocable

`AssignableExpr` retains a root and suffixes of member o index. The verification that the path ends in a writable location belongs to resolution, types and effects. The Surface AST does not expand a path which traverses immutable aliases: it retains their suffixes, and the elaboration The subsequent stage decides whether it can reconstruct the intermediate values and propagate the write-back to externally writable storage. If an exact key is missing at an intermediate stage, this is not rewritten in the AST either.

### Iteration `for each`

`ForEachEffect(binding, source, step?, filter?, body)` retains the expression `by`, the filter as `ExpressionBlock` and normalises effect brief/bloque following `:` a `EffectBlock`. Address, default step, compatibility, filter order and zero-pass belong to elaboration.

## Expressions

### Operators

The AST preserves lexically distinct operators when MUD assigns them different contracts:

- `WordAnd` opposite `SymbolAnd`.
- `WordOr` opposite `SymbolOr`.
- `WordXor` opposite `SymbolXor`.

This allows `when` distinguish between temporal composition using ordinary Boolean words and that using symbols.

### Comparisons

A string such as:

```mud
0 <= x < 10
```

is represented by `ComparisonChainExpr`, rather than arbitrary binary pairings.

Non-chainable comparisons result in a single edge in the chain or an equivalent validated node.

`is not` produces `IsNotRelation`; it doesn’t get lost like a `not` external, because the nominal narrowing must directly confirm the negative test result.

### Selection and quantifiers

`SelectionExpr(binding, source, step?, predicate)` preserves `step?` and normalises the predicate to `ExpressionBlock`. `QuantifierExpr(kind, variable, source, step?, body)` Do the same for all five quantifiers `exists`, `forall`, `count`, `min` y `max`. The AST does not decide on the contract Boolean of `body` nor the validity of the order required by the provisions.

### Conversions

`to Type` y `in unit` produce `ConversionExpr` with different destinations. The postfix barrier in the grammar has already determined their grouping, but not the compatibility.

### Postfix and calls

`MemberAccessExpr`, `IndexExpr` y `CallExpr` They are constructed from left to right.

`CallExpr` retains:

- The expression call.
- The prefix of positional arguments.
- The named-argument suffix.

The separator prevents a positional element from being placed after a named element.

A possible interpretation of:

```mud
(attacker, defender).CanAttack()
```

as several receivers or as a single one structural value is still pending resolution signature. The Surface AST retains the structural form and the postfix chaining.

### `Rand`

`Rand(expr)` has `RandomExpr`; it is not a type not even one call ordinary.

### Selection and `take`

`binding in source [by step] : predicate` has `SelectionExpr`. It retains the link, the source, the optional step and the predicate as `ExpressionBlock` without realising the collection resulting. Binding only introduces names into the predicate.

`take amount from source` has `TakeExpr`. The Surface AST does not determine whether the source is a list, text or dictionary, domain countable or one collection in no particular order; that resolution It then determines whether to take a prefix canonical or a reproducible sample.

The composition of both forms is structural. `take n from player in players : condition` contains a `SelectionExpr` as a source of `TakeExpr`; `player in take m from players : condition` contains a `TakeExpr` as a source of `SelectionExpr`.

### `all`

The literal contextual `all` produces `AllLiteral`. His domain and whether they are static or dynamic is determined during type checking; the Surface AST does not list its values. The prefix form `all D` produces `PrefixExpr(EnumerateAll, D)` and explicitly preserves the materialisation requested.

### Quantifiers

`exists`, `forall`, `count`, `min` y `max` share `QuantifierExpr` with its own enum, a `step?` optional and a `ExpressionBlock` as a body.

### Operators of collection

`--` produces `CollectionDifference`, other than `Subtract`. The updates `|=`, `&=`, `^=` y `--=` produce, respectively `UnionAssign`, `IntersectionAssign`, `SymmetricDifferenceAssign` y `DifferenceAssign`; they are not limited to `Assign` because the update class participates in the consolidation concurrent.

## Templates `Text`

A template is an ordered sequence of:

- `TextFragment` with decoded text.
- `ValueInterpolation`.

The AST does not retain:

- Explicit or implicit closing quotation marks.
- Physical margin of the literal multi-line.
- Escape sequences used to achieve the same effect.

The CST does keep them.

Ordinary text enclosed in double quotation marks always appears in the Surface AST such as `TextTemplateExpr`. The elaboration subsequent action may turn it into a value `Char` when the context requires it `Char`, contains no interpolations and its value The decoded value is exactly a Unicode scalar. Therefore, the Surface AST it does not have a separate lexical constructor `CharLiteral`.

`NumericTextFormat` displays whole and optional fractional widths without retaining the specific colons.

Within the `format` of a magnitude from point, `unidad from contenedor` produces `ContextualPointComponentExpr`; you don’t just make up a receiver explicit information that does not appear in the source.

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

Parentheses and square brackets only survive as `OpenBoundary` o `ClosedBoundary`.

The wingers `*` remain as `EffectiveIntervalBound` up to elaboration.

## Quantities and units

`QuantityValueExpr` contains a literal numerical and a `UnitProduct`.

The expression of unit and the dimensional one has separate trees, even though both use `*`, `/` and parentheses in the concrete syntax.

A way `UNIT_FORM` is preserved as source text contextual. Its resolution The catalogue entry relates to later phases.

The absence of a space between the number and unit does not affect AST. `3m` y `3 m` produce the same output; the exact source form remains available in the CST and the formatter outputs the second one.

## Numeric literals

The AST holds a canonical document from the value, not necessarily the exact lexeme. For example:

```mud
1_000
1000
```

may produce the same `ExactNumberLiteral("1000")`.

The mathematical accuracy of `Num` and the binary64 interpretation of `Rum` are prepared afterwards.

## Preserved order and canonical order

The source order is preserved:

- Statements within a file.
- Predecessors.
- Fields and components.
- Family details and members.
- Participants and `given`.
- Arguments.
- Effects and assertions.

Alone `MudProject` defines a canonical file serialisation by path. No other list is automatically sorted in the Surface AST unless a specific standard states otherwise.

## Invalid states excluded

A Surface AST It must not contain:

- Cardinality absent.
- Two modifiers `unique`.
- Two orders of collection.
- `given` changeable.
- Duplicate metadata declarations within the same unit.
- Symbol o anchor resolved.
- Type implied, inserted as if it had been written.
- Ordinary comments.
- Recovery tokens.

## Structural serialisation

The canonical serialisation of AST:

1. Sort files by path standardised.
2. It preserves the order of the internal sequences.
3. Use constructor names ASDL.
4. Skip trivia and punctuation.
5. Includes `SourceOrigin` except in comparison views where this is expressly excluded.
6. Serialise enums by their canonical name.

This serialisation is used for snapshots, caching and tooling. It is not MUD code and does not replace the pretty-printer.

## Coverage

All production from [[mud]] must appear in:

- `mud-syntax-kinds.yaml`.
- `cobertura-sintactica.yaml`.

The coverage specifies whether the production:

- Build a node.
- It’s returning to normal.
- He turns to his father.
- It is ruled out as a layout.
- It remains contextual up to resolution.

`validate_syntax_model.py` Check that it matches.

## Conformidad

One conforming implementation from the Surface AST must:

1. Generate constructors equivalent to `mud-surface-ast.asdl`.
2. Apply all standardisations from [[cst-a-ast-superficial]].
3. Reject the excluded states before the AST.
4. Preserve provenance.
5. Do not anticipate resolution, typed or IR.
6. Maintain the required operator differences.
7. Enable the creation of a stable structural form for testing.

## Normalisation of empty bodies of `thing`

`thing A`, `thing A;` y `thing A {}` produce the same `ThingDecl` with zero fields and no intrinsic overwriting. The CST preserves the written body and terminator; the AST does not create an empty body node.


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

preserves `OmittedCardinality` in the Surface AST and buy `[3]` only during the elaboration from the field.

```mud
start with {
    all,
    empty
}
```

produces `StartSet(contributions=[AllLiteral, EmptyLiteral])`.

## Product types and dictionary types

`PositionalProductType` y `NamedProductType` retain the components of the anonymous structural products. `ExactDictionaryType` y `DecisionDictionaryType` represent, respectively, exact dictionaries and functional dictionaries defined by branches. The mechanical name `Decision` is retained for the sake of the scheme’s stability.

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

The validation following the resolution rejects an arrow as a partial alternative to a union, even when it appears via a alias.

## Cardinality omitted

`CollectionSpec` preserves `WrittenCardinality` u `OmittedCardinality`. To:

```mud
values: Nat = [1, 2, 3]
```

the Surface AST retains the omission. The elaboration of a stored field 'immutable' implies subsequently `[3]` and log in `InferredFromInitializer`; it does not generate that information during parsing.

## Nominal comparisons

`is` It continues to be represented by means of transitive nominal comparison. `iis` It produces its own node because its narrowing is different:

```text
ExactTypeTestExpr(value, PersonId, negated=Disabled)
ExactTypeTestExpr(value, PersonId, negated=Enabled)
```

The second form corresponds to `value iis not PersonId`. The resolution requires the right-hand operand to be a type nominal.

## Dictionary set operations

The Surface AST preserves `|`, `&`, `--` y `^` such as `BinaryExpr`, because the exact category depends on the resolved types. The elaboration This specialises them as exact or functional dictionary operations. A functional operation preserves its operands; it does not create a new list of branches.

## Metadata, text and activation

`element~metadata` always produces `MetadataAccessExpr`. It does not exist `MetadataSuffix` allocable: `AssignableExpr` only retains `MemberSuffix` e `IndexSuffix`, so that no access `~` may be the destination of a effect. The Surface AST nor does it determine whether the property exists for the receiver; that check is deferred until the static category of the receiver has been resolved. Any interpolation produces `ValueInterpolation`, including:

```mud
"{value~anchor}"
```

It does not exist `AnchorInterpolation`. `start with` produces `StartSet(contributions)` with a single series of contributions. `ActionDecl` preserves `PublicAction` o `Subaction`.

## Ownership, restrictions and local adaptation of collections

`has` y `has not` are normalised as `HasMember` y `HasNotMember`. `value in Domain` produces `DomainRestrictionExpr`; a selection with the original binding `SelectionExpr`. Local specifications result in `CollectionTransformExpr` with `LocalCollectionTransform`, without capacity `mut`.

