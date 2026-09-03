---
title: Gramática concreta
aliases:
  - Concrete syntax from the MUD
tags:
  - mud/especificacion
  - mud/gramatica
status: propuesta
normative: true
depends-on:
  - "[[05-texto-fuente]]"
  - "[[06-lexico]]"
questions:
  - Q-022
  - Q-059
  - Q-062
  - Q-063
decisions:
  - D-102
  - D-101
  - D-015
  - D-025
  - D-028
  - D-029
  - D-031
  - D-035
  - D-036
  - D-037
  - D-038
  - D-039
  - D-041
  - D-042
  - D-044
  - D-047
  - D-048
  - D-049
  - D-050
  - D-054
  - D-055
  - D-056
  - D-057
  - D-058
  - D-059
  - D-061
  - D-062
  - D-063
  - D-064
  - D-065
  - D-066
  - D-067
  - D-068
  - D-069
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
  - D-096
  - D-098
  - D-100
  - D-099
---

# 07. Gramática concreta

## State and purpose

[[gramatica/mud.ebnf]] defines the complete syntax of standard source files `.mud` from MUD 1.0. The additional physical area of `mud.module` is documented separately and its full grammar remains open in Q-062. This chapter It specifies how to read it, how to interpret contextual constructs and how to group expressions. The issues listed in the frontmatter affect semantics However, they do not prevent us from recognising the source form.

## Parsing output

The result The parsing specification is a Lossless CST by file, defined in [[sintaxis/cst-sin-perdidas]]. The EBNF determines the grouping and order of meaningful tokens; the CST also preserves punctuation, terminators and trivia.

The presence of a CST does not confirm that the file is valid. The recovery process may represent missing or unexpected tokens without discarding them.

## Validation prior to the AST

Once the CST has been constructed, the contextual syntactic constraints required to produce a normalised AST are checked, including:

- Modifiers of collection duplicates.
- Duplicate statements by the same person metadata in a owner, including the units.
- A argument a position following that of a named person.
- Specific combinations prohibited by this chapter.

The name resolution, types, domains and effects do not belong to this validation.

A `given` reuses the general expression for type, including dictionaries:

```mud
given prices: Product -> Money
```

The grammar may retain a modifier `mut` written within that expression to diagnostic, but that capacity is statically invalid: `given` It never grants write access.

## Abstract transformation

The AST projection is at [[sintaxis/cst-a-ast-superficial]]. Production is covered mechanically in `sintaxis/cobertura-sintactica.yaml`.

## Programme

A file contains a header of declarations `using` followed by statements from leading figures:

```mud
using world.people
using physics.*
```

There is no declaration from path; it is derived from the path. `using`, no `import`, is the only building in visibility between MUD paths.

All the `using` must appear before the first declaration top-class. Mixing them in is a error and never believe scope local or sequential. The order between several `using` It does not resolve ambiguities.

The top-level categories are:

- `thing`
- `alias`
- `family`
- `magnitude`
- The three ways of `rule`
- `action`
- `subaction`
- `look`
- `message`
- `test`
- `start with`

## `thing`

```mud
thing World

abstract thing Place

thing Alexandria as City, Place {
    ~name = "Alejandría"
}
```

`Thing` is the `thing` an embedded abstract concept that acts as top type. All `thing` meets `is Thing`. A root without `as` It retains zero declared predecessors, but receives an edge semantics implicit towards `Thing`. It is acceptable to write `as Thing`, but it’s redundant: a conforming implementation must issue a diagnostic non-blocking and offer to remove it. `Thing` It cannot be declared, created or destroyed:

```mud
create Thing   # error estático
destroy Thing  # error estático
```

`Thing` is always true without appearing in `start with`, y `all Thing` lists only the `thing` concrete, effective measures, never the abstract concept.

All `thing` displays properties and Postfix metadata separately from their fields. `~identifier` retains the source identifier and `~name` is presentation configurable. All access `~` is read-only during execution; no metadata It is an assignable destination. Metadata are not ordinary fields.

The list following `as` does not indicate priority. `create` It does not accept a body here or anywhere else:

```mud
create Alexandria
destroy Alexandria
```

### Initiators of `thing`

One `thing`, whether concrete or abstract, can initialise a stored field already contributed through its inherited scheme by means of an allocation without re-declaring the field:

```text
fieldName = value-body
```

The objective is retained as the name of field up to the resolution. It does not declare a field new; it does not replace its inheritable default and cannot be addressed as a computed field. It must result in a field inherited: the same `thing` cannot be declared locally `fieldName` and also contain a separate instruction `fieldName = ...`. The form `fieldName: Type = value` it’s just one declaration is set by default and remains valid. The value The initialiser supports a shorthand expression or a `ValueBlock`; the entire body is subject to the contract static of materialisation from the field inherited.

In a `abstract thing`, the initialiser does not materialise own stored data; it is preserved as a legacy contribution to the first materialisation of specific descendants. In a `thing` Specifically, the local initialiser is applied to its own first materialisation and is not inherited by its descendants. A more specific initialiser takes precedence over a less specific inherited one. Multiple specialisation does not take precedence based on the order of `as`: the same source is duplicated, and there are separate and incomparable contributions on the same subject field fall under conflict.

```mud
thing Kingdom {
    mut treasury: Money = 0
}

thing France as Kingdom {
    treasury = 20
}
```

In `France`, `20` initialises the own stored data from `France.treasury` every time it comes to pass `France` since its canonical definition. It does not become the default, nor does it become an inheritable initialiser for descendants of `France`. Confirmed destruction rules that out own stored data and a `create France` subsequently reapplies the initialiser when constructing the new one materialisation. This distinction keeps the inheritable default and the contribution from materialisation.

```mud
abstract thing RichKingdom as Kingdom {
    treasury = 20
}

thing Lydia as RichKingdom
```

`RichKingdom` does not have a specific load of `treasury`, but its initialiser is involved in the first materialisation from `Lydia`.

It is not permitted to mix declaration and its separate initialiser field in a definition:

```mud
thing Broken as Kingdom {
    treasury: Money = 10
    treasury = 20
}
```

`name = valor` has no special intrinsic meaning: if `name` is a stored field Inherited from the existing scheme, it uses this same format; `~name` remains the metadata from presentation.

## Fields

When a owner metadata-bearing with `ValueBlock` use the full form, his statements `~...` may take the form of a preamble incorporated at the beginning of the main text. The preamble forms part of the descriptor, not the `ValueBlock`, and cannot be combined with a second metadata-body. The short form retains the separate metadata-body.


Stored format:

```text
[mut] fieldName: Type [in domain] [collection-specification] [= value-body]
```

Calculated form:

```text
fieldName [derived-value-shape] := value-body
```

`derived-value-shape` it could be `: Type`, `in domain` with collection optional, or a specification from collection alone. Therefore, both are valid: `area: Num in 0..* := width * height` such as `area in 0..* := width * height`. If the type, must be unambiguously inferred from the expression, without any predetermined preference between compatible representations or contextual forms. If there is more than one solution, the type must be written. A computed field does not support `mut` external. Its form may specify domain, specification from collection and interior capacity `[mut]`.

The `mut` 'exterior' is written before the name because it describes the location where it is stored, not the type of its members. `fieldName: mut Type` is not part of the syntax. The names of field and the names of metadata they occupy different syntactic positions: `name: Text` declares a field, whilst `~name = expresión` declares or amends the metadata from presentation.

The value from `=` It can be a short phrase or a `ValueBlock`. In a stored field, the entire body must remain static: it is fully evaluated at compile-time and cannot be read state, participants, `given`, outdoor venues or activities at the world. The mutability temporary structure created within the `ValueBlock` It is valid if the entire structure can be designed statically. For example:

```mud
allowedRange: Int Interval = 1..2 | 3..4
duration: Time = 1 hour + 30 minutes
```

The first method directly produces a normalised discontinuous interval.

```mud
mut population: Population in [0..*] [1] = 10 people
density := population / area
displayDensity: Density := density
```

If the expression of a computed field is also statically closed; the compiler must suggest the immutable stored form. It is not a error nor an automatic rewrite, and the suggestion does not appear when the calculation depends on state runtime.

A comma-separated list forms a collection calculated and inferred type y cardinality where these can be demonstrated:

```mud
numbers := a * b, d, c / a
```

The domain in a calculation, it acts as contract. A potential external output triggers a warning and a check of transition; an output that must be external results in error.

## Expression blocks and value

A `ExpressionBlock` is a declarative form: it contains zero or more pure calculated locals `:=` followed by a final expression. It does not support stored variables or mutation, `for each` as a sentence or `if` internal. It is used by conditions, filters, quantifiers and key sides/selector dictionaries.

A `ValueBlock` build a value and contains zero or more local statements followed by a final expression. Its only statements are evaluated declarations, stored declarations, and assignments whose footprint remains within the block itself, and `for each` local. Does not support `if`, external effects, actions/subactions, `create` nor `destroy`.

```mud
result := {
    mut total: Money = 0
    for each item in items if item.taxable :
        total += item.price
    total
}
```

`ValueBlock` It is not a primary expression. It only appears in owners who explicitly declare it; to use a complex calculation such as argument, index or the right-hand side of a effect It is first linked to a local one.

In `then` Stored local variables are also permitted:

```mud
then {
    mut remaining: Money = account.balance
    remaining -= cost
    account.balance = remaining
}
```

The shape `x := ...` It cannot be allocated. `x: X = ...` creates a non-reallocable local slot and `mut x: X = ...` one that can be reassigned. A `then` it still needs at least one effect observable.

The default of `given` preserves `constant-expression` and does not allow `ValueBlock`.

## Type joints and external arrows

`|` combines non-arrow alternatives and has greater precedence that `->` y `-->`. Both arrows have the same precedence and are grouped from the right:

```mud
A | B -> C | D       # (A | B) -> (C | D)
A | B --> C | D      # (A | B) --> (C | D)
A -> B -> C           # A -> (B -> C)
```

An arrow must be the complete outer shape of the type. A dictionary cannot be regarded as a partial alternative to a union, not even in brackets or by means of a alias whose actual shape is that of an arrow.


### Callable types and types obtained by reflection

Callable types are defined based on the types of receiver/participantes and on the part `given` from the firm:

```mud
Dragon.action(Volume)
(Attacker, Defender).action(Amount)
Dragon.rule(Limit)
Dragon.look(Detail)
```

The category forms part of the construction of type. This surface alone does not determine the variance nor all the rules of compatibility between companies: Q-063 keeps that issue open. The ability to root outside of `action` nor can it be deduced solely from reflective subtyping.

A postfix expression ending in `~type` may hold a position as type when the elaboration proves statically that it produces `Type`. For example `alias Stats := MyDragon.Stats()~type` is valid; the call `MyDragon.Stats()` without `~type` it remains a value and not an expression of type. A callable type such as `Dragon.look(Detail)` already implies `Type` and doesn't need `~type`.
The following are invalid:

```mud
value: A | (B -> C)
value: (A -> B) | C
value: A | (B --> C) | D

alias Lookup := B -> C
value: A | Lookup
```

The following are valid:

```mud
value: (A | B) -> C
value: A -> (B | C)
value: (A | B) --> (C | D)
value: A -> Lookup
```

The alias restriction is checked after the nominal resolution. Each non-arrow alternative may declare domain and just one specification from collection The end belongs to the union full:

```mud
values: Nat in 0..10 | Int in -10..-1 [1..*] = [2 to Nat]
```

Cardinalities by alternative are not permitted. If a contextual expression fits several alternatives, one must be selected using `to`.

## Collections and dictionaries

The cardinality, when it appears, it is placed at the start of the square brackets. Modifiers may be separated by a space or a comma:

```mud
citizens: Person [0..* unique ordered mut]
citizens: Person [0..*, unique, ordered, mut]
```

A final comma is not permitted. In a stored field immutable with an initialiser, a cardinality An omitted element is retained as omitted in the AST and is inferred as the cardinality exact exterior of the value initial:

```mud
one: Nat = 1                 # [1]
three: Nat = [1, 2, 3]      # [3]
none: Nat = empty            # [0]
table: A -> B = AValue -> BValue # [1]: el diccionario completo es un valor
```

A field with `mut` exterior retains `[1]` when it is omitted. Calculated fields `:=` retain the inferred form of their expression. A cardinality an inferred immutable value distinct from `[1]` prompts you to write it out explicitly.

Compatible collections support `|`, `&` y `--`. `^` demands that the result comply with the uniqueness rules. They operate on multiplicities or membership; they do not concatenate:

```mud
leftChars: Char [1..5] = ["a"]
rightChars: Char [0..2] = empty
combinedChars := leftChars | rightChars
```

`empty` it is not a failure by itself. A query partial produces `empty`; the failure appears only when the required external form does not allow for cardinality zero.

### Associations and branches

In an association `->`, the left-hand side is a `ExpressionBlock` and on the right, a `ValueBlock`. In a branch `-->`, the left-hand selector is a `ExpressionBlock` Boolean and the result first `ValueBlock`. The keys only replace the extended side, so all four short combinations are valid/extensa without any auxiliary keywords or external packaging.

```mud
key -> value
key -> { result }
{ key } -> value
{ key } -> { result }
```

The scopes on both sides are independent. The local scopes/selector do not proceed to the value/resultado. The application of the dictionary remains outwardly flawless.

### Precise dictionaries `->`

An accurate dictionary query by key equality, it is countable and admits mutability external. Associations are written using the same arrow:

```mud
capitalOf: Country -> City [2 ordered] =
    Spain -> Madrid,
    France -> Paris
```

A missing key results in `empty`. A complete association can be inserted as value operational:

```mud
then add (Portugal -> Lisbon) to capitalOf
```

`unique` requires the associated values to be globally unique. An insertion or substitution that would duplicate a value A two-key operation is a complete no-op: it does not modify any associations and does not produce `failed`.

Adding an association whose key already exists atomically replaces the previous association when the result respects the contract:

```mud
then add (Spain -> Barcelona) to capitalOf
```

Exact dictionaries are countable. A simple traversal goes through keys, whilst a pairwise traversal goes through associations:

```mud
action CollectCapitalData
for capitalOf: Country -> City [*],
    mut visitedCountries: Country [* unique],
    mut visitedCapitals: City [* unique] {
    then {
        for each country in capitalOf : {
            add country to visitedCountries
        }

        for each (country, capital) in capitalOf : {
            add country to visitedCountries
            add capital to visitedCapitals
        }
    }
}
```

One query 'absent' retains the optional output format:

```mud
capitalOf[Italy] # City [0..1], produce empty si Italy no está
```

The key elements may be structural components:

```mud
distance: (City, City) -> Length =
    (Madrid, Toledo) -> 74 km,
    (Madrid, Segovia) -> 91 km
```

Set-theoretic operators on sets act on keys. For a common key, `|` y `&` retain the value left:

```mud
left: Key -> Nat = AKey -> 1, BKey -> 2
right: Key -> Nat = BKey -> 9, CKey -> 3

left | right   # AKey -> 1, BKey -> 2, CKey -> 3
left & right   # BKey -> 2
left -- right  # AKey -> 1
left ^ right   # AKey -> 1, CKey -> 3
```

`|` y `&` They are not necessarily commutative, as with dictionaries. The insertion order preserves the left-hand content first; `ordered by` normalises after calculating the content.

### Functional dictionaries `-->`

A functional dictionary is a policy case-defined purity. `value` refers to the input within the selector and the result; `_` This is the fallback:

```mud
dangerOf: Creature --> Danger [ordered] =
    value is Dragon --> Extreme,
    value is Predator --> High,
    _ --> Low
```

`ordered` means `FirstMatch`: wins the first one branch applicable, and the application results in `[0..1]`, o `[1]` with a fallback. Without `ordered` all ordinary branches are evaluated and a result is obtained result by chance; `unique` removes duplicates from results:

```mud
traitsOf: Creature --> Trait [unique] =
    value is Flying --> Aerial,
    value is Aquatic --> Aquatic,
    value is Magical --> Magical
```

Selectors are written explicitly. There is no shorthand that implicitly inserts `value`, `==`, `is` o `in`:

```mud
seasonName: Month --> Text [ordered] =
    value == January --> "winter",
    [March..May] has value --> "spring",
    value == June or value == July --> "summer",
    _ --> "other"
```

Therefore, `January --> "winter"`, `[March..May] --> "spring"`, `Dragon --> Extreme` y `shop.discounted --> DiscountedPrice` They do not automatically take on the meaning of a selector. The full comparison or membership must be written out.

Applicability and production from result are recorded separately. One branch whose selector is applicable may produce `empty`; the fallback `_` it merely contributes result when there is none branch The applicable ordinary law has produced one. In `FirstMatch` the order of evidence is retained; in `AllMatches` all the results actually produced are recorded.

You can view the fixtures and results state purely external:

```mud
priceOf: Product --> Money [ordered] =
    value in shop.discounted --> value.basePrice * shop.discount,
    _ --> value.basePrice
```

These readings create explicit dependencies on `shop.discounted`, `shop.discount` y `basePrice`. All transitive calls follow the same snapshot.

Does not support `mut` exterior or `[mut]`, it is not traversed directly via `for each` and every recursion must have a demonstrably well-founded measure. Valid proofs include numerical descent and strict reduction of cardinality or the transition to a strictly minor substructure; a cycle without demonstrable evidence is error.

To iterate through results, you iterate through a domain entries and the dictionary is applied:

```mud
action CollectPrices
for products: Product [*], pricing: Product --> Money,
    mut prices: Money [*] {
    then for each product in products : {
        price := pricing[product]
        add price to prices
    }
}
```

Branches can only be changed by editing the model About the dictionary owner. A structural edit can be inserted before `_` by default, and you can update, remove or move a branch, but none of those operations are directed at a anchor from branch nor does it presuppose identity independent public sphere; its local key is anchored in the resolved representation.

Functional calculus is extensional; it does not merge branches:

```text
(F op G)[x] = F[x] op G[x]
```

`F | G`, `F & G`, `F -- G` y `F ^ G` combine the sets obtained by applying both operands to `x`. Its fallbacks are evaluated independently. The union and the symmetric difference of two functionals `ordered` they can produce two outcomes and lose `ordered` in general; the intersection and the difference may preserve it.

It is not permitted to combine an exact match with a functional match directly.

### `FirstMatch`, `AllMatches`, fallback and cardinality

In a functional `[ordered]`, `unique` It is valid but redundant and triggers a suggestion to remove it. Without a fallback, the application has `[0..1]`; with a fallback, `[1]`.

In an unordered functional, each branch An ordinary coincidence contributes a maximum of one result. With `n` potentially matching branches; the conservative approach is `[0..n]`; a fallback raises the lower bound to `1`. `unique` It deduplicates matching results from different branches without changing which branches were applicable.

```mud
tagsOf: Creature --> Tag [unique] =
    value is Dragon --> Magical,
    value is FireCreature --> Magical,
    value is Flying --> Aerial,
    _ --> Ordinary
```

For a fire-breathing dragon, `Magical` appears only once. The union or the symmetric difference of two functionals `ordered` loses `ordered` when it can produce two different results; the intersection and the difference are preserved when the quota is maintained `[0..1]`.

### Chaining dictionary types

Arrows accept complete types and are right-associative:

```mud
board: Square -> Piece [0..32 ordered]
nested: Name -> Coordinate -> Piece [*]
policyByMode: Mode -> Product --> Money [2..4 ordered]
```

The second example is equivalent to `Name -> (Coordinate -> Piece [*])`. Each specification from collection refers to the immediately preceding arrow. Brackets are only necessary to alter the natural grouping or to delimit another complete construction.

The chained application processes each level in turn:

```mud
piece := boardByGame[game][coordinate]
```

Composition does not introduce an abstract category of function. It is expressed by applying the result from one dictionary as an entry in another:

```mud
weather := weatherOf[capitalOf[country]]
```

### Unbranded structural products

The lads `(A, B)` y `(a: A, b: B)` They are structural products. Their elements are `(x, y)` y `(a = x, b = y)`. They are compared component by component and can act as exact keys or functional entries:

```mud
distance: (City, City) -> Length
label: (name: Text, count: Nat)
routePolicy: (origin: City, destination: City) --> Route
```

Variable names do not create component names: `(x, y)` it remains positional even if the variables are named `x` e `y`. A alias The figure remains nominal, although its payload has the same shape:

```mud
alias Coordinate {
    x: Num
    y: Num
}

raw: (Num, Num) = (1, 2)
nominal: Coordinate = (x = 1, y = 2)
```

`raw` y `nominal` are not interchangeable without an explicit nominal conversion. The compatibility Anonymous products require the same consistency, compatible component names where these exist, and a component-to-component correspondence.

`ordered by ruta` belongs to collections whose members offer a path fixed set of fields, components or associated data. Each intermediate access must be unique and the value The final version must have complete semantic order:

```mud
route: Terrain [* ordered by movementCost]
teams: Team [* ordered by captain.age]
```

One `thing` does not in itself possess total order and cannot be the ultimate key. The whole path it must be transitively stable: mutable stored fields, calculations with mutable dependencies and intermediate accesses whose state subsequent action may alter the key. A path The optional element is also rejected as long as there is no defined position for `empty`.

If the member is a union, the path must exist across all feasible alternatives. Each segment retains its uniqueness and stability, and the final keys must be worked out towards a single type a fully ordered set. A single implicit extension is valid; two purely representational aliases are not unified. When alternatives need to be adapted, a computed field common.

`ordered by` does not allow arbitrary expressions. If the criterion requires a formula, it is declared as field or a calculated value, and is sorted by name. Keys with the same value retain their relative order within provenance stable; in a purely sequential story, it corresponds to the order in which they appear. They are not resolved by anchor, identity nor an order to declaration of a `family`.

It is prohibited `ordered by` for `Char`; its encoding is Unicode. `Text` does not accept specifications for collection.

## Aliases

```mud
alias PlayerName := Text
alias UserName as PlayerName

alias Board := Square -> Piece [0..32 ordered]

alias Square {
    file: File
    rank: Rank
    label: Text := "{file}{rank}"
}

alias Coordinate {
    x: Num
    y: Num
}

alias PositionedCoordinate as Coordinate

alias Pagination {
    page: Nat = 1
    size: Nat = 20
}

alias LargePagination as Pagination {
    size = 100
}
```

One declaration from alias You can write an unordered list of ancestors using `as`. The local definition is optional when the antecedents determine a complete effective form. Therefore, both are valid: `alias UserName as PlayerName` such as `alias PositionedCoordinate as Coordinate`. `alias A` without predecessors or a definition is a error static.

`:= tipo` simply enter the representation of a nominal alias root. A nominal alias Upon succeeding their predecessors, they inherit the effective representation and cannot re-declare it. In particular, `alias UserName as PlayerName := Text` is invalid.

A performance `:= tipo` may be followed by an immediate body containing only metadata from the alias. So a alias A representational model can be documented or configured without incorporating structural components.

The structural body may contain stored components, derived fields and overrides of inherited defaults. An override `nombre = valor` It only changes the default value: it cannot alter type, domain, cardinality, order, uniqueness or inner capacity.

Structural literals are contextual:

```mud
(E, Four)
(file = E, rank = Four)
(size = 30)
```

The positional form must provide all components. If any are omitted, the form must be fully qualified: the omitted components take their explicit default value or the default value of their type. The components listed may skip previous or intermediate components, but those listed retain the relative order of declaration. You are not allowed to mix positions and names:

```mud
pagination: Pagination = (2, 30) # válido
pagination: Pagination = (2)     # inválido: posición parcial
pagination: Pagination = (size = 30) # válido: page conserva 1
```

A component does not support `mut` outside because the value from alias and each of its components is immutable. You can, however, write `[mut]` in his specification from collection to provide internal capacity on the `thing` contained directly; this capacity does not allow the collection.

A derived field from alias It uses the same syntax as the other calculated fields, including an optional declared form:

```mud
alias Squad {
    members: Soldier [*]

    wounded [* mut] := soldier in members :
        soldier.health < MaximumHealth
}
```

The collection A derived collection is not a stored sub-collection of `members`: has contract its own. `[mut]` grants internal capacity even if the source does not. The selection is set for the snapshot under review; once the effects have been consolidated, it is recalculated on the basis of the new state, so members can join or leave automatically. A collection Stored data is never pruned by this reason.

## Families

```mud
family Terrain {
    movementCost: Nat = 1
    passable: Bool = true
    costly := movementCost >= 3

    Plain,
    Forest {
        movementCost = 2
    },
    Water {
        movementCost = 0
        passable = false
    }
}
```

The data appears before the first member. A stored value may be followed, after its optional default, by an immediate body containing only statements `~...`. A calculated value may contain the same immediate metadata body and uses the `derived-value-shape` full list of calculated fields: you can set type, domain or a form of collection compatible without having to buy them mutability no external facilities or on-site storage.

The metadata-body describes the descriptor data standardisation of the `family`, not the value sprayed concrete per member. For example:

```mud
family Terrain {
    movementCost: Nat = 1 {
        ~summary = "Coste base de movimiento"
    }
    costly := movementCost >= 3 {
        ~summary = "Indica terreno costoso"
    }

    Plain,
    Mountain {
        movementCost = 4
    }
}
```

The allocation `movementCost = 4` from the member it is simply an overwrite of value of the stored data. It does not support metadata-body, nor does it introduce any other anchor and does not alter the metadata of the descriptor `movementCost`. The expression of a calculated value is evaluated statically for each member After resolving the stored data, you can query other associated data using unqualified names, and the data must have acyclic dependencies. The block of a member It can only assign stored data.

The items are separated by commas and do not take a final comma. `ordered family` compares its members in order of declaration and allows associated data paths, including stable calculated ones, to be used as keys for `ordered by` in collections.

## Quantities

Magnitude base:

```mud
magnitude Probability: Num in [0..1] {}

magnitude Length: Num in [0..*] {
    root unit meter {
        ~plural = "meters"
        ~abbreviation = "m"
        ~prefixes = all
    }
}
```

Magnitude derived:

```mud
magnitude Speed: Num in [0..*] := Length / Time {
    unit fastie := 1 m/s {
        ~plural = "fasties"
        ~abbreviation = "fst"
    }
}
```

Magnitude from point:

```mud
magnitude RawInstant point over Time {}

magnitude Timestamp point over Time {
    ~format = "{day}:{hour:2}:{minute:2}"
}

magnitude WorkdayTime point over Time in [0..28_800] {
    ~format = "{hour:2}:{minute:2}"
}

magnitude TimeOfDay point over Time in [0..86_400) cycle {
    ~format = "{hour:2}:{minute:2}:{second:2}"
}
```

One magnitude A base can take one of two forms: an empty set with no elements, or exactly one `root unit nombre` followed by zero or more alternative units. You cannot declare an alternative without root. The absence of root it is a choice semantics complete: the magnitude it retains an independent nominal dimension, but its values do not appear unit. It is not the same as its numerical representation, or any other magnitude without units or the dimensional neutral element.

```mud
chance: Probability = 0.75
explicitChance := ratio to Probability
```

A literal A bare numeric value can take the type of a magnitude without units when the expected context uniquely determines them. A general numerical expression requires `to` to bring it into being. Arithmetic retains the nominal factor even if it has no form of unit; the visible projection of units may coincide across statically distinct dimensions. A quantity that does write unit It only takes into account the factors it has identified: the context does not introduce any hidden factors.

One magnitude The derived variable only declares alternative nominal units `unit nombre := equivalencia`; a magnitude from point does not specify units. In the latter, `in` and the domain are optional: without them, the domain The full value of the underlying coordinate; an ordinary interval bounds it without enclosing it, and `[a..b) cycle` adds cyclical normalisation. `cycle` amend the domain 'complete' is not part of the term 'interval', and only one magnitude from point He admits it.

The body of a unit contains only general statements `~...`; it does not exist `unit-property`. `~prefixes: Prefix [* unique] = empty` use the type incorporated `Prefix`: leave it out or write `empty` does not enable any, `all` enables the full decimal SI catalogue and a collection such as `[kilo, milli]` select those pre-set values. `~name`, `~plural` y `~abbreviation` they use the same general metadata system and all runtime access via `~` It is read-only.

A number may omit the space before it unit, but the formatter inserts it: `3m` y `3 m` have the same AST, and the second one is canonical.

`~format` is optional and uses the general template syntax `Text`: the spaces are code and `:2` set two positions here to the left of the point. Without it, there is no special representation of point: the ordinary textual representation of a magnitude, with the coordinate at the unit root and the abbreviation or name of that unit. In this case, the first component is the coordinate at that unit —reduced by the cycle, if it exists— and each subsequent component is extracted within the previous one. A non-obvious container is made explicit, for example `~format = "{week from year:2}"`.

Outside `~format`, extraction requires the point:

```mud
minute from hour in time
picosecond from second in time
week from year in date
```

The form is a single syntactic construction. The receiver it must be a magnitude from point; both units belong to his magnitude underlying; the unit the extracted material does not exceed the capacity of the container; the result is `Nat`. The canonical origin and Euclidean remainder are used, with a possible final partial component when the units do not divide exactly. The extraction does not depend on `~format`.

The shapes produced by `~format` occupy the token contextual `POINT_LITERAL`. The type 'Expected' selects a single magnitude from point and the literal It must exactly reproduce its canonical form. A format that cannot be unambiguously inverted is invalid. Components finer than the last one shown take value zero.

Without `~format`, the literal is written as an ordinary quantity with unit compatible. Everything literal must belong to the domain before applying cyclical normalisation; for example, `26:00:00` is invalid for `TimeOfDay`.

## Activación inicial `start with`

Every module You may declare a maximum of one `start with`. It isn't a `main`, does not call any modules and does not specify an initialisation order. The absence of `start with` in a module is equivalent to an empty contribution.

The declaration accepts a direct contribution or a unified block:

```mud
start with Kingdom
```

```mud
start with {
    Kingdom,
    Place,
    CanEnter,
    empty
}
```

Each expression must be static and may contain zero, one or more activatable statements `thing | rule`. A collection is supplied directly by its members; nested collections are not permitted. Duplicate identities are deduplicated and the source order is retained only as provenance, not as a priority semantics.

A `start with` can only trigger statements with cycle its lifespan module. The contributions from all the modules are combined before the stabilisation initial. `Thing` remains in force at all times and does not form part of the collection can be enabled.

`all D` can bring about a domain countable when a contribution requires a collection explicit; `all` Without an operand, it retains its contextual meaning.

## Participants

`for` links predefined roles from any type from value declared. A role may be individual or collective; its values may be restricted by `in dominio` and acknowledge the specification full list of collection. The domain is written after the type and before the collection. `on nombre: Tipo` uses the implicit universe of `thing` specific and proactive measures compatible with that type; on the other hand `on nombre[: Tipo] in fuente` It links from a finite, countable source and can therefore relate other values. The related form can write the type to refine the source elements nominally.

```mud
rule CanAttack for attacker: Army, defender: Army
given maximumDistance: Length {
    distance <= maximumDistance
}

rule AllAdults for people: Person in EligibleCitizens [1..*, unique] {
    forall person in people : person.age >= 18
}

rule IsWeekend for day: Day {
    day == Saturday or day == Sunday
}

rule Starve on
    world: World,
    kingdom in world.kingdoms [mut]
{
    when kingdom.food == empty
    then kingdom.population -= 1
}
```

The type can be inferred from a participant related: that is usually enough `kingdom in world.kingdoms`.

It can also be written as the type to refine, in name only, the members of the collection, not necessarily to repeat his type stated:

```mud
rule MutualFriends on
    alice: Person in bob.friends,
    bob in alice.friends
{
    when alice.mood changes or bob.mood changes
    then create FriendshipChanged
}
```

All the names in a header `on` are visible throughout the entire header. Their types and constraints are resolved jointly, so that forward references and cycles are permitted where there is a unique nominal solution. Each role starts from the `thing` concrete and active actions on the part of its type effective; the relationships are the finite join that satisfies all membership conditions on the same snapshot. It is not the case that different roles must be assigned different identities, nor do two symmetrical orientations constitute different relationships.

Everything participant `for`, `on` y `given` has an explicit identifier. It does not exist participant anonymous, nor with cardinality effective `[1]`. A header can group together identifiers that share type and metadata-body, for example `for attacker, target: Fighter { ... }`; the group is sugar and each descriptor retains its own anchor.

In a action, `mut` before the name of any role `for`, including the cardinality `[1]`, grants mutability external on the collection supplied. The receiver The relevant location must be a storage facility with that capacity; a literal or a collection calculated values do not meet the contract. The `mut` of the specification from collection continues to provide internal capacity on the `thing` member:

```mud
action Treat for
    mut patients: Person [1..10, unique, mut]
{
    then for each patient in patients : {
        patient.health += 10
    }
}
```

The declaration The previous one may change the membership or an order from the collection received stored data and modify its members. `mut patients: Person [*]` grants only the first capacity; `patients: Person [*, mut]`, only the second one.

Declaring an internal capacity based on immutable values is valid, but the compiler suggests removing it when it can demonstrate that it will never be exercisable. The suggestion preserves the meaning and does not constitute a warning. In a strict dictionary, the `mut` external changes associations and `[mut]` only grants authorisation in respect of securities `thing` materially associated; never on keys, aliases, nested levels or the value absent. A functional dictionary prohibits both forms of `mut`.

The mutability 'exterior' can indeed be applied to a collection of any type:

```mud
action Record for mut observations: Num [*]
given value: Num {
    then add value to observations
}
```

Boolean rules and `look`, because they are pure, they do not allow `mut` exterior. None `given` supports mutability neither outside nor inside: its specification from collection may state cardinality, `unique` y `ordered`, but his production excludes `mut`.

An ordinary reference to `World` refers to the identity exact. `on World` and a role `for World` reflectively select the `thing` specific, active measures that meet `is World`, including the one itself `World` if it is specific. This selection only applies when the type of the role is a `thing`.

The link depends on the role category:

- one `thing` is linked by identity;
- a staple, alias, member from `family`, dictionary or other value 'immutable' is linked to value;
- a role with `mut` exterior is linked by identity from the storage location and also retains its value current.

## Rules

### Boolean

The body culminates in a single expression `Bool` and it can declare immutable local bindings beforehand:

```mud
rule IsAdult for person: Person {
    person.age >= 18
}

rule CanAfford for person: Person given price: Money {
    available := person.money
    available >= price
}
```

It doesn’t have `if`.

### Reactivate

```mud
rule OpenGate on gate: Gate [mut] {
    when gate.unlocked
    if not gate.open
    then gate.open = true
}
```

`changes` is a temporal suffix used in expressions:

```mud
when position + offset changes

when {
    calendar.day changes or
        alarm.enabled
}
```

On the other hand, starting the second line with `or` is invalid:

```mud
when {
    calendar.day changes
    or alarm.enabled
}
```

The subsequent jump to `changes` ends a complete expression; curly brackets do not suppress terminators, and the `or` there is no left-hand operand. To place the operator at the start of the second line, the expression would need to be kept open using brackets.

It has fewer precedence than arithmetic, conversions and comparisons, but more than `and` y `or`. Therefore:

```text
position + offset changes  ≡  (position + offset) changes
temperature > limit changes  ≡  (temperature > limit) changes
position changes or ready  ≡  (position changes) or ready
```

Within `when`, every `e changes` produces a temporary trigger that pulses when `e` has different values in the two consecutive start snapshots. The standard Boolean operands of `and` y `or` amount to transition `false` → `true`; this allows changes and conditions to be combined so that they become true without missing any consecutive pulses. Only the words `and` y `or` consist of temporal activators; their symbolic variants and the other logical operators retain their ordinary meaning when applied to values.

A `when e` Purely Boolean detects the transition `false` → `true` of the full expression. `old e` may appear in `when` and in `if` of a reactive rule when `e` It is pure and can be evaluated in both snapshots; see the previous one. It is not permitted in its `then`. To measure a variation, an explicit condition is written; for example `position - old position >= 10 meters`; it does not exist `changes by`.

```mud
when position changes and velocity changes

when price changes or outOfStock
if price > old price and stock < old stock

when position - old position >= 10 meters
```


`when` It also supports declarative sources. A occurrence from `message`, the effective firing of a rule reactive and the assessment of a rule `always` for a link, they can act as a trigger. Actions, sub-actions, `look`, Boolean rules and tests are not declarative sources of triggers.

A declarative reference used as a trigger does not take parentheses: `when Damaged`, `when Dragon.Damaged` or a local variable containing that descriptor. Receptors restrict their binding sites `on`; they do not turn the trigger into a call ordinary.

A trigger produces zero or more causal matches. Each match retains its bindings/testigos and the identities of occurrence. `and` performs a natural join on compatible matches and, where they do not share bindings, a Cartesian product; `or` carries out union. Two causally distinct events are not considered duplicates simply because they share payload. The purely Boolean case described above is the temporary rise in voltage that triggers these matches when the corresponding edge occurs.
The links found in the first snapshot as evidenced by `start with` compare `old` and the value current one against the same one snapshot: `changes` does not fire. The elevated Boolean branches, on the other hand, retain the previous false virtual value and may fire if they are already true. Any link created subsequently takes its first wave active as baseline Complete it without taking a shot, and start comparing on the next one.

### `always`

```mud
always rule ValidPopulation on kingdom: Kingdom {
    population := kingdom.population
    population >= 0 people
}
otherwise "Population cannot be negative: {population}"
```

The body directly contains the condition, without `if`. The `otherwise` An optional element is written after the closing brace; it forms part of the complete rule and can take the form of an expression `Text`. The diagnostic it is only evaluated if the condition is false, on the same tentative state and with the same links that breached the rule. Their value becomes the reason from the result `failed`. Omitting it is legal, but it triggers a warning and a reason default. Writing it inside the curly brackets is a error.

## Shares

```mud
action Recruit for kingdom: Kingdom [mut]
given amount: Nat in 1..100 {
    if kingdom.treasury >= amount * recruitmentCost
    otherwise "The kingdom cannot afford {amount} recruits"
    then {
        kingdom.treasury -= amount * recruitmentCost
        kingdom.soldiers += amount
    }
    after kingdom.soldiers >= old kingdom.soldiers
    otherwise "Recruitment did not increase the army"
}
```

There is no classification semantics elementary actions as opposed to compound actions. A `then` is an ordered sequence of consequences and may incorporate local connections `:=`, direct effects, calls to `action` o `subaction` and routes `for each`. A call The internal function is executed at its textual position on the delta deprived of the resolution: observe the visible effects shown above, and add your own effects to them resolution and subsequent judgements comply with them.

One `action` it could be root exterior. A `subaction` It can never be the case, but both are omissible and can be invoked from any semantic context `then`, including the `then` of a rule reactive or a test when the context allows. The call The internal process does not open a transaction or a resolution root independent.

The `after` of all the shares/subactions The executed operations are checked against the stable state final attempt at the resolution complete. A `failed` 'nested' reverses the entire resolution; a `rejected` internal processes also abort and reverse it, whilst retaining the category `rejected`. The `otherwise` optional from `if` o `after` explains the rejection and the associated `then` explains the `failed` of the transition complete.

```mud
subaction RemoveMoney for account: Account [mut]
given amount: Money {
    then account.balance -= amount
}

action Transfer
for source: Account [mut], destination: Account [mut]
given amount: Money {
    then {
        source.RemoveMoney(amount)
        destination.AddMoney(amount)
    }
}
```

External capacity and reflective subtyping are distinct properties: `subaction <: action`, but to expand a descriptor does not provide an alternative `subaction` in root safe outdoor space.

## Point of exit

```mud
look RealmSummary for kingdom: Kingdom
given locale: Locale {
    name := kingdom~name
    population: Population := kingdom.population in people
}

message KingChanged on kingdom: Kingdom {
    when kingdom.king changes
    if kingdom.visible

    kingdomName := kingdom~name
    kingName: Text := kingdom.king~name
    time := kingdom.clock in second
    timeText := "{kingdom.clock}"
}
```

`look` It is a pure callable. It can be accessed by the host, another module whose contract make it visible and MUD code in contexts suitable for reading, including a `then`. Its fields read a single, coherent view inherited from the caller: stable state from the host, a snapshot from a rule y delta private, visible on the point verbatim from a `then`. Supports `for` y `given` and returns exactly one value from the anonymous type comprising its public fields.

A `message` It isn't called that. Every instance of its `when` which exceeds `if` create a occurrence causal with identity, declaration, bindings `on` and birth certificate. That very same occurrence can feed triggers into the wave next. Within the MUD, its payload is projected onto the view causal; after a commit, it is projected to the host via the stable state final. A rollback cancels the delivery outdoors.

The outer casing keeps the bindings separate `on` which identify the participants and the payload public; it does not merge the two namespaces. Confirmed occurrences retain their order causal between waves and, within the same wave, a stable and reproducible technical order that does not introduce any priority semantics among them.

A field audience whose value 'direct' is a magnitude which supports drives should preferably select its presentation with `in`. Omitting it is legal and uses the canonical unit projection, but triggers a warning because it implies a decision of the API. A magnitude Without units, it displays the numerical value directly and does not produce that warning. A magnitude from point directa publishes its coordinates on the unit chosen, and not his `~format`; to publish the format, a field `Text`.

## Clauses and keys

`when`, `if`, `then` y `after` You can always use keys. You can omit them when there is only one element. A `then` with more than one effect and a `after` from test If there is more than one assertion, they must be used.

```mud
if ready

if {
    available := player.money
    available >= price
}
otherwise "Available: {available}"
```

Braces do not suppress terminators between elements within a block.

### Local values under the right conditions

Boolean rule blocks, `when`, `if`, rules `always` y `after` Action expressions may contain zero or more local bindings followed by exactly one final expression:

```mud
when {
    wasOpen := old door.open
    isOpen := door.open
    wasOpen != isOpen
}
```

Links use `nombre [: Tipo] := expresión`, are pure, immutable and sequential, and do not allow forward references, loops, redeclaration or shading. They are recalculated on every evaluation of the clause and do not store state between waves.

His scope reaches the `otherwise` associated, but not `then` nor any other clause. In a `when`, `changes` y `old` they evaluate the defining expression of a local variable in each snapshot necessary.

An unstructured expression of declaration It must be the last one. It must be drawn up to `Bool`, except in `when`, where you must create an activator supported by your contract temporal. An empty block, a block consisting solely of local variables, or a second non-declarative expression are invalid.

The block `after` of a test retains one or more assertions. It may begin with common locals, visible in all assertions and their `otherwise`; after the first assertion, no further local assertions may be declared:

```mud
after {
    expected := before + amount
    kingdom.soldiers == expected
    kingdom.treasury >= 0
}
```

### Local values in `then`

A block `then`, including that of an iteration, can interleave effects with computed local bindings:

```mud
then {
    cost := amount * price
    remaining: Money := kingdom.money - cost
    kingdom.money -= cost
}
```

The shape `name [derived-value-shape] := value-expression` declares a value immutable local variable. The derived form allows `: Type`, `in domain` with collection optional, or a collection alone. The type and the cardinality are inferred when there is a unique solution; otherwise, they must be written out. It does not allow `mut` outdoors.

The expression is pure and is evaluated only once when execution reaches the declaration. Read the previous sequential effects of the same delta private and retains its value even if subsequent instructions change their dependencies.

The name has only been available since its declaration until the end of the block. It may be used in subsequent statements, but not before it appears; there are no forward references, loops, redeclarations or shading. Each iteration creates a scope new. A `then` must retain at least one effect o call: a block consisting solely of local variables is invalid.

## Calls

The participants take up the receiver; the `given`, the brackets:

```mud
army.IsDestroyed()
(attacker, defender).CanAttack()
(
    attacker = leftArmy,
    defender = rightArmy
).CanAttack()
```

The named receivers may reorder roles provided they are accurate and exhaustive.

An expression of collection holds a single position as receiver when the relevant role is a collective role; it is not broken down into several roles. If the role declares `mut` externally, that expression must also be a compatible, mutable space.

That a type may appear in `for` does not require all the arguments in that type as roles. `for` identifies the semantic subjects of the operation; `given`, its auxiliary parameters.

The `given` They must have a name, are read-only, and can declare a closed static default:

```mud
given origin: Square = Capital,
      depth: Nat,
      exhaustive: Bool = false
```

Arguments can be positional, named or a prefix positional, followed by nouns. After the first argument A positional form cannot appear in a named form. In positional usage, only a complete suffix can be omitted with a default; in named forms, intermediate defaults may be omitted and the order rearranged:

```mud
game.Search(Capital, 3)
game.Search(depth = 3)
game.Search(exhaustive = true, depth = 3)
```

The latter form is valid, but the compiler suggests writing `depth` before `exhaustive` to follow the order of declaration. A name cannot be repeated or be unknown, and every `given` If no default value is specified, it must remain linked.

Fully-qualified multi-part receivers can also reorder roles and are subject to the same canonical order suggestion. They remain exact and exhaustive, and are not mixed with positional receivers.

## Effects

Grammar recognises:

```mud
target = value
target += amount
target -= amount
target *= factor
target /= divisor
target |= values
target &= values
target ^= uniqueValues
target --= values

add value to collection
remove value from collection

add mut morale: Nat to Army
remove morale from Army

create Declaration
destroy Declaration
```

`destroy` retains the identity and canonical definitions, but the materialisation the runtime specific to a `thing` specific. Confirmed destruction discards its stored values and any runtime structural modifications, the owner whichever that may be identity; a `create` the latter constructs a materialisation frees itself from the standard scheme and reapplies defaults and initialisers. This self-destruction does not delete loads belonging to other owners that are merely suspended by an inactive dependency. To destroy a rule Reactiva also rules out the temporary storage of that activation; if it is created again, its first wave activa establishes a baseline new without firing, simply as a result of the reactivation.

One path An assignable value can traverse stored components of immutable aliases and exact dictionary indexings when it terminates at a location root externally writable. This write operation does not alter the intermediate aliases: the elaboration constructs new values from it type exact nominal value, retains its other stored components, recalculates the derivatives and propagates the substitutions outwards to the storage root. For example:

```mud
shop.orders[id].status = Shipped
shop.orders[id].retryCount += 1
```

A local that contains a alias it remains a value and does not take on a path back to storage, so `order.status = Shipped` is invalid when `order` It is just a local link. Nor can you write a derived field from the alias.

If an exact dictionary lookup used as an intermediate step fails to find the key, the absence is `empty` and the effect partial is a no-op: it does not create the association, nor does it generate a value using default settings and does not produce `failed` because of that absence. This does not affect the direct allocation `shop.orders[id] = order`, which replaces an entire association and can generate a missing key when the contract allows it.

The shape `remove name from Owner` is different from removing a value by means of resolution and types. In both cases, the parser retains the same provenance; the AST produced must generate the correct variant or a diagnostic.

`|=`, `&=`, `^=` y `--=` retain their update class in the AST. They require an externally mutable location or a path a reconstructible assignable whose write-back ends in one, plus a result assignable to the sheet. `^=` only accepts collections `unique`. With regard to collections, uniform updates are consolidated by union, intersection, parity or sum of removed multiplicities; mixing different classes is conflict unless otherwise expressly stated. Regarding `Text`, `|=` Chaining operations and several concurrent updates require a specific overall order.

## `for each`, progressions, selection and quantifiers

`for each` accepts any finite and countable source: sets, exact dictionaries, countable intervals, finite countable domains and any other value with canonical enumeration. An interval does not become collection because it can be explored.

```mud
for each person in kingdom.people if person.hungry :
    person.health -= 1

for each value in [0..100] by 5 : {
    doubled := value * 2
    total += doubled
}
```

The `:` is mandatory. The brackets form part of the main body and do not replace the separator. The main body may begin on the same line or after one or more terminators; this physical separation does not alter its abstract structure. In a `for each` executable; the short body must be a effect o call a action and the block uses `EffectBlock`. Within `ValueBlock`, `LocalForEach` use a `ValueStatement` brief or a `LocalStatementBlock`, accepts only local statements and cannot extend beyond the scope of the block’s value.

### Iteration filter

`by` precedes `if`. The filter can be an expression or a block of expressions with local variables. It is pure and non-stochastic. With semantic order, it is evaluated immediately before each iteration and takes into account the sequential projection left by previous iterations; without semantic order, all filters start from the same initial projection and the accepted modifications are consolidated simultaneously in accordance with the contract of the body. An accurate dictionary can link `(key, value)`.

### Progression `by`

`by` A signed, compatible difference is received and evaluated once before runtime. Positive anchor at the lower boundary and negative at the upper boundary. An open initial boundary advances once before the first candidate. The progression ends before the first external candidate and does not need to reach the opposite end. The inverted ends continue to produce `empty`.

```text
[1..8] by 2   -> 1, 3, 5, 7
[1..8] by -3  -> 8, 5, 2
(1..8] by 2   -> 3, 5, 7
[1..8) by -2  -> 6, 4, 2
```

A demonstrably zero runtime step is error static; if it can vary and ultimately equals zero, it produces the failure assessment `progression-step-zero`. In a action that one failure ends as `failed` and rollback; in a pure expression, it propagates as failure evaluation and never becomes `false`. In a domain zero-stage is always error static. The compatibility uses the advance operation and exact implicit conversions, not identity nominal: `Nat` can proceed via `Int`, `Num` by exact differences that are compatible, and quantities in compatible units. In a magnitude from point The step is a linear difference.

`by` It is not a stride over arbitrary collections. `ordered by ruta` keeps another one semantics.

### Default steps and numbers

A source with its own numbering does not need `by`. When the enumeration is based on a sequence, `Nat` e `Int` are used by default `1` y `Money`, `0.01`; omit `by` Always choose that positive difference. Other types of exact progression require an explicit step, unless a canonical successor is defined. `Num` supports explicit exact steps and a general range of `Num` without a step is invalid. The intervals of `Rum` they never allow progression `by`, neither in iteration nor in staggered domains; a collection explicit statement of values `Rum` it is countable without `by`.

### Tiered domains

`interval by step` It uses the same progression to define membership, and the static step may be negative. The sign may change the terms, but the order is not part of the type. `all` is realised in canonical order; `Nat in [1..8] by -2 = all` produces `2, 4, 6, 8`. In discontinuous intervals, the iteration is restarted for each segment; for positive values, the segments are traversed from smallest to largest, and for negative values, the order is reversed. A domain cyclical point It covers no more than one fundamental period.

### Selection and quantifiers

Selection and `exists`, `forall`, `count`, `min`, `max` accept `by` when the source defines progression and maintains it `:` even if the body has keys. Everyone uses `ExpressionBlock`: the block contains premises `:=` followed by a final Boolean expression. In `min` y `max` that predicate filters witnesses, and the operation returns the first or the last, respectively, according to the semantic order of the source; a source `ordered` without an explicit key is also valid; a source without a usable order is rejected, and no accepted witness produces `empty`. `sum` does not belong to language.

A selection produces a collection and therefore does not directly consume a domain naked: if the conceptual source is a domain `D`, it should be written as `all D`. Iterations and quantifiers that do not produce a collection they can eat a domain finite and countable.

```mud
selected := x in source by step : {
    threshold := limit
    x < threshold
}
```

A selection directly returns the accepted instances and preserves provable multiplicity, uniqueness and order. Its predicate remains pure and deterministic.

### `take` and indexing

`take amount from source` retains its semantics existing. As it produces a collection, a domain `D` he cannot appear naked as `source`: it must be explicitly implemented as `all D`. On a collection sorted or a materialisation with canonical numbering, it takes the prefix; on collection/diccionario A non-ordered sample drawn from a random sample is reproducible without replacement. Positional indexing still requires an observable order.

## Tipo superior `Any`

`Any` is the top type open view of the project’s MUD values. This includes basic values and incorporated values such as the members of `Prefix`, identities `thing`, aliases, members of `family`, magnitudes, intervals, collections, dictionaries, structural products and first-class descriptors of statements and types. AST nodes are not MUD values simply by virtue of existing as a compiler representation.

`Any` It is not countable; it has no universal or predetermined order. The following are invalid:

```mud
all Any
unknown: Any
```

A stored field `Any` You must write an initialiser. The equality operator requires compatible effective types and relies on the equality of the type effective. Any specific operation requires narrowing:

```mud
rule Positive given value: Any {
    value is Nat and value > 0
}
```

Inside a functional branch, `is` e `iis` retain the narrowing in the result:

```mud
describeAny: Any --> Text [ordered] =
    value iis PersonId --> "Person id {value}",
    value is Nat --> "Natural {value}",
    _ --> "Other"
```

`Money` It remains a staple, incorporated because of its rules of materialisation, not an exception to the opening of `Any`.

## Contextual values

Collections may be written in square brackets. In places where a comma does not conflict with another construction, the contextual form may omit them:

```mud
[A, B, C]
```

Brackets are required for nesting and for using the collection as a single argument. `empty` needs a type expected; compare `empty == empty` Without context, it is invalid.

A dictionary with a key structural alias supports:

```mud
board[(E, Four)]
board[E, Four]
```

## Intervals

The specific form of a type The interval operator first writes the type of its limits and then the contextual word `Interval`:

```mud
Nat Interval
Int Interval
Num Interval
Rum Interval
Money Interval
```

The grammar retains any `type-reference` in that position; the static phase requires that it be resolved to an accepted numerical representation. `Interval` it is not a declaration nominal amount checked via name resolution in this building.

Forms:

```mud
[a..b]
(a..b)
[a..b)
(a..b]
a..b
[a]
```

`a..b` is equivalent to `[a..b]`; `[a]`, a `[a..a]`. A winger `*` must be closed on its side. The exclusive cyclic form of magnitudes of point is a full range followed by the modifier: `[a..b) cycle`.

Finite terms are complete expressions and must be evaluated in the same way type sorted. Within an interval of magnitude They may be expressed in local units – even different ones – which are standardised before comparison:

```mud
[1 m..5 km]
[minimumDistance..5 m]
[1 km..maximumDistance]
[minimumDistance..maximumDistance]
```

A literal located next to a field from magnitude must bring their own unit. Therefore, `[minimumDistance..5] m` is invalid and is written as `[minimumDistance..5 m]`.

When all finite endpoints are numeric literals without unit, just one unit may follow the interval:

```mud
[1..5] m
1..5 m
[1..5) km
[*..5] m
[1] m
[] m
```

`1..5 m` is categorised as `(1..5) m`. The unit 'exterior' is not distributed across fields or quantities that already have unit. `[1..5 m]` is invalid because it conflicts with `Num` with a magnitude, y `[1 m..5 m] m` add a second one unit Invalid external link.

The canonical serialisation of literals that share unit use `[1..5] m`, although `[1 m..5 m]` is also valid. If the units differ or one side is an expression that has already been typed, local units are used.

After evaluating and normalising the effective extremes of a linear interval:

- a lower bound that is less than the upper bound preserves the written sides;
- Two equal boundaries form a single unit only if both sides are closed and produce `empty` otherwise;
- a lower bound greater than the upper bound results in `empty`.

The investment does not imply a downward trend or cycle. Filling that gap never fails to resolution on their own; they only produce `failed` restrictions that render the tentative state, such as a value stored in such a way that it is outside its domain or a ruler `always` unfulfilled. A `given` outside domain and a `if` o `after` Fakes retain their result `rejected`.

The domains declared in the header of a magnitude retain the bare numerical bounds as interpreted in their canonical representation: in the unit root when it exists, and directly in the numerical representation when there are no units. The form `[a..b) cycle` It also retains this restriction and requires a strictly positive period. Other sides, such as infinities or empty intervals, are invalid with `cycle`.

## Precedence and grouping

From highest to lowest:

| Level | Shapes | Group |
| ---: | --- | --- |
| 1 | access `.`, metadata `~`, index `[]`, call `()` y `unit from container in point` | left or full form |
| 2 | prefixes `old`, `allowed`, `not`, sign | right |
| 3 | `*`, `/`, `%` | left |
| 4 | `+`, `-`, `--` | left |
| 5 | suffixes `to Type`, `in unit` and restriction `in Domain` | cumulative |
| 6 | `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `is not`, `iis`, `iis not`, `has`, `has not` | restricted |
| 7 | temporal suffix `changes` | non-membership-based |
| 8 | `and`, `&` | left |
| 9 | `or`, `|` | left |
| 10 | `xor`, `^` | left |
| 11 | `=>` | right |
| 12 | `<=>` | adjacent chain |
| 13 | `eventually ... through ...` | outdoor |

Shapes `take amount from source`, `binding in source : predicate` and the quantifiers contain complete expressions in their delimited positions. The first `from` non-nested that can limit the number of `take` separates quantity and source; the non-nested colon separates source and predicate. The `from` o `:` words enclosed in brackets or within another complete construction belong to that construction. This rule of contextual delimitation prevents the `from` the component extraction process accidentally absorbs the separator from `take`. Therefore:

```mud
take n from player in players : player.ready
```

is categorised as `take n from (player in players : player.ready)` without brackets.

`to` and the `in` from unit transform the value cumulative tail on its left. The parser then continues with the result:

```mud
population / regions to Population
distance + offset in km
value to A to B
```

are grouped as follows:

```text
(population / regions) to Population
(distance + offset) in km
(value to A) to B
```

If another operator appears next, use the result already converted. This rule is naturally implemented using a Pratt parser that allows for a shorter postfix precedence followed by new operators.

`in` from unit consumes the expression of unit complete, including products, quotients and parentheses:

```mud
speed in km/h
acceleration in m/(s*s)
```

As `to` is applied to each quantitative operand before the comparison, `3 m == 3 m to Length` is categorised as `3 m == (3 m to Length)`, not as an adaptation of the result Boolean.

## Chains

Homogeneous chains of the order:

```mud
a < b < c
```

are produced as follows:

```mud
a < b and b < c
```

Chained equality follows the same rule. `<=>` It produces combinations of adjacent pairs. They do not form chains:

- `!=`
- `is` e `is not`
- `iis` e `iis not`
- belonging `has` y `has not`
- `=>`

Different operators are not combined within the same chain without explicit conjunctions.

`iis` check the exact effective nominal type; `is` includes specialisations. For:

```mud
alias Identifier := Nat
alias PersonId as Identifier
alias EmployeeId as PersonId
```

a `EmployeeId` meets `value is PersonId`, but no `value iis PersonId`. `value iis not PersonId` eliminates only the exact possibility `PersonId` during the narrowing. The right-hand operand of `iis` it must be a type nominal; products, dictionaries and the identity singleton `Madrid` are invalid.

About `MudPath`, Boolean membership uses the container on the left, is reflexive and compares entire segments:

```mud
world.combat has world.combat          # true
world.combat has world.combat.melee    # true
world.combat has world.combatant       # false
```

## Postfix metadata

The access is written `owner~metadata`, never `owner.~metadata`. All access `~` is runtime-readonly; the write operation exists only as declaration from the model within the relevant metadata-bearing preamble.

| Metadata | Type | Principal owners | Reportable |
| --- | --- | --- | --- |
| `~identifier` | `Name` | anchored elements | no, intrinsic |
| `~name` | `Name` | compatible metadata-bearing elements | yes |
| `~path` | `MudPath` | statements and anchored elements | no, intrinsic |
| `~anchor` | `Anchor` | statements and anchored elements | no, intrinsic |
| `~file` | `MudFile` | elements with provenance physics | no, intrinsic |
| `~kind` | a reflective family, according to receiver | compatible statements and descriptors | no, intrinsic |
| `~type` | `Type` | everything value MUD | no, intrinsic |
| `~metadata` | `Metadata [* unique]` | metadata-bearing elements | no, intrinsic |
| `~for` | `Participant [* unique ordered]` | Boolean rule, `action`, `subaction`, `look` | no, intrinsic |
| `~on` | `Participant [* unique ordered]` | reactive rule, ruler `always`, `message` | no, intrinsic |
| `~given` | `Participant [* unique ordered]` | Boolean rule, `action`, `subaction`, `look` | no, intrinsic |
| `~clauses` | `ClauseKind [* unique]` | statements containing clauses | no, intrinsic |
| `~plural` | `Text` | units | yes |
| `~abbreviation` | `Text` | units | yes |
| `~prefixes` | `Prefix [* unique]` | units | yes; default `empty` |
| `~format` | `Text` | magnitudes of point | yes |
| `~summary` | `Text` | compatible metadata-bearing elements | yes; default `""` |
| `~description` | `Text` | compatible metadata-bearing elements | yes; default `""` |
| `~deprecated` | `Text [0..1]` | compatible metadata-bearing elements | yes; default `empty` |

The ‘Owners’ column is a restriction semantics availability information, not a description of when the result is non-empty. After solving and classifying the receiver, an access to a property that is not supported by its static category is error. In particular, `thing A` invalidates `A~for`; a `action` it does support `~for` even if you omit the clause, in which case you get `empty`. The very distinction between non-existent property and value 'empty' refers to `~on` y `~given`.

The production `metadata-name ::= identifier | "for" | "on" | "given"` only allows those ‘hard’ keywords to appear syntactically after `~`. The parser cannot determine the textual name of the receiver if the entry exists: construct the postfix form and the resolution and the typing process applies the above matrix.

The table summarises the common and configurable properties that affect the syntax of this chapter. The reflective system also defines the specific properties of each descriptor, such as specialisation relationships, fields, components and structural properties of collections and dictionaries; these are not duplicated here as a second authoritative catalogue.

`Prefix` is a type built-in. Its SI values are written as ordinary identifiers (`kilo`, `milli`, ...), so `~prefixes = [kilo, milli]` It doesn’t require any special grammar.

General conversions are explicit when the following apply:

```mud
pathText: Text = Alexandria~path to Text
```

Templates can render metadata types directly without creating compatibility overall nominal figure with `Text`. `~file` It is valid in any expression, but triggers a warning when it appears outside text or purely informative public output, and its value may affect behaviour:

```mud
look SourceInfo {
    source := "Loaded from {Alexandria~file}"
}

rule Fragile given expected: MudFile {
    Alexandria~file == expected # válido con advertencia
}
```

`~name` and any other metadata These settings can be changed by editing the model and reworking it; never by means of a effect runtime. This edition remains unchanged payload, equality, path nor anchor unless the source identifier is changed by some other means.

## `Text` and operators

`|` concatenates `Text`:

```mud
"Hello, " | name
```

The following are not permitted `&`, `^` nor `-` on `Text`. `xor` is entirely logical and `^` exclusively conjunctive. The nominal aliases of `Text` do not undergo implicit concatenation.

Everything literal `Text`, whether standard or multi-line, is a template. `{e}` assesses `e` and insert the canonical textual representation of the value. Metadata are ordinary expressions:

```mud
"Kingdom: {kingdom}"
"Population: {kingdom.population:6}"
"Rule: {CanRecruit~anchor}"
"Path: {CanRecruit~path}"
"Literal braces: \{example\}"
```

`anchor{...}` does not belong to the language. Render `Name`, `MudPath`, `Anchor` o `MudFile` in a template does not implicitly convert them to `Text` outside that context.

They can be rendered directly `Text`, `Char`, `Bool`, basic numbers, values `thing`, the members of `family`, intervals, sets and magnitudes. A call a Boolean rule It is also so because it produces `Bool`. Statement and type descriptors are first-class MUD values, but this does not mean they have an implicit textual representation. Actions, reactive rules, rules `always`, `look`, `message`, tests, types and declarations `family` produce error static within `{...}` as long as there is no applicable explicit textual conversion or projection.

One `thing`, a nominal alias and a member from `family` are represented by their `~name` effective. Its anchor A canonical form is obtained by `~anchor`; edit `~name` does not change equality, path nor anchor. A member from `family` Without overwriting, it initially uses its nominal name. An interval uses its normalised canonical form. A collection It omits only the outer square brackets and separates elements using `, `; all collection if it appears as an element, it retains its own square brackets:

```mud
"{[1, 2, 3]}"          # 1, 2, 3
"{[[1, 2], [3, 4]]}"   # [1, 2], [3, 4]
```

A numeric gap allows for `{e:izquierda}`, `{e::derecha}` y `{e:izquierda:derecha}`. The left-hand precision is the minimum of the figures preceding the point and pads with zeros without taking the sign into account or truncating. The right-hand side precisely determines the subsequent digits, adds zeros or rounds to the nearest whole number, with ties being treated as even:

```mud
"{count:4}"     # 0012
"{ratio::2}"    # 12.30
"{ratio:4:2}"   # 0012.30
```

Left-hand precision is supported for all basic numeric types. Right-hand precision is supported for types that can display a fractional part: `Num`, `Rum` y `Money`. Any numeric format over another type is a error static.

One magnitude linear without `in` represents the number followed by the canonical projection of units of its dimension. If that projection is empty, it represents only the number. Nominal factors without unit they are not printed, but remain in the type. A magnitude from point use its `~format` if it has one, and if not, the standard rule for its magnitude underlying. `{magnitude in unit}` select one presentation available and, for a point, avoid the `~format` and represents the complete coordinate. It is invalid to apply `in` to a magnitude base without units. When there is unit, the abbreviation is used if one exists; otherwise, the singular form of `1` y `-1`, and the plural for the other values.

`time in picosecond` expresses the total coordinate; `picosecond from second in time` extracts the part within the second. The second method is valid even if the displayed format does not include picoseconds.

## `eventually`, `allowed` and chance

```mud
allowed game.Move(origin, destination)

eventually game.Checkmate(White)
    through game.Move, game.Pass

eventually game.Checkmate(White)
    through [game.Move, game.Pass]

Rand([1..6])
```

Tickets for `through` These are references to actions, not specific calls. The list, with or without square brackets, represents the same thing collection contextual. MUD 1.0 only supports `Rand(source)`; it does not yet include syntax for weights or distributions.

## Open endings and prefixes

`TERMINATOR` comes from `;` or of `NEWLINE`. A jump continues when the following appears:

1. Within `()` o `[]`.
2. After `,`.
3. Following an incomplete binary operator or assignment.
4. After `:`, `:=`, `->`, `-->`, `.` o `~` when its operand is missing or member.
5. After `using`, `as`, `for`, `on`, `given`, `when`, `if`, `then`, `after`, `otherwise`, `to`, `in`, `through`, `by`, `from`, `over`, `root` o `point` when the production requires content.
6. Within a header which, according to the EBNF, it can’t be over yet.
7. Inside a literal o comment multi-line.

A jump after a unit That one’s already finished unit. The bleeding never decides.

> [!example]
> In `value = first` The jump terminates the assignment. In `value = first +` It doesn't complete the operation because the right-hand operand is missing.

## Contextual distinctions

The parser or the elaboration The following issues must be resolved without arbitrary decision-making:

| Area | Distinction |
| --- | --- |
| `in` | domain, participant related, restriction/filtro o unit |
| `has` | Boolean membership |
| `call()` | regla booleana o acción |
| `remove x from y` | value from collection or dynamic property |
| `UNIT_FORM` | unit enabled or invalid name |
| shared operators | logical, arithmetic, textual or set-theoretic operation |
| literal structural | alias expected |
| `[expression]` | collection unitary or unit interval |
| `1..5 unit` | unit common to the interval or right-hand end of an invalid lead |

If the names, types and constraints of the expression do not determine a single valid interpretation, the programme is invalid and must provide the type is missing. No implicit preference applies. For example, a derivation without sufficient context cannot arbitrarily choose whether `[3]` is a collection or the interval `[3..3]`. The grammar expressly states `1..5 m` as a way of unit common `(1..5) m`; it is not up to the parser to decide.

## Error recovery

An implementation may synchronise after a error in:

- `TERMINATOR`
- `}`
- A clear-cut start to a declaration higher

Recovery only improves diagnoses. It cannot be carried out silently semantics nor accept a form that does not conform to the rules of grammar.

## Preserved contextual structures

The parser does not decide on matters that require resolution:

- If a path with dots intersects MUD paths, statements or members.
- If a literal structural, used before a call represents a receiver one or more recipients.
- If a `postfix-expression` of a effect is a call from action.
- What type contextual selects a literal structural, of unit, by point or a literal consisting of a single scalar.

The CST retains the specific form and the Surface AST an unresolved form. The subsequent stages carry out the classification.

## Representation of quantities

The optional entry of a magnitude use the general syntax `declared-type`. A subsequent static rule requires that the type provided that it is a permitted numerical representation. The grammar does not maintain a duplicate, closed list of numerical types.

## Empty bodies omitted

The body of a `thing` is optional. These forms produce the same AST and IR, although the CST retains the notation:

```mud
thing A
thing A {}
thing A;
abstract thing Root
thing B as Root
```

The point and a comma does not introduce a new rule: it is already a `TERMINATOR` explicit and allows, for example, `thing A; thing B; thing C as A`.

## Nominal access for members of alias

Derived components and fields belong to the type nominal value of the alias. A bare structure does not acquire members by coincidence of form:

```mud
(1, 2).derived                    # inválido
((1, 2) to CosoAlias).derived     # válido
```

The context of type you can also build the alias without `to`. The compiler does not look for candidate aliases based on the name of the member.

## Reflective metadata

The `~...` Configurable elements appear before the standard content. Fields, components and participants may contain an immediate metadata-only block. All `for`, `on` y `given` has a required name; a grouped header shares type and metadata-body amongst its identifiers. The file defaults precede `using`. `start with` and the bodies of `when`/`if`/`then`/`after`/`otherwise` They are not metadata-bearing owners.
## Belonging, restriction and local transformations

Boolean membership uses `contenedor has valor` y `contenedor has not valor`. `in` It is not a Boolean membership operator. `valor in Dominio` locally restricts or filters the value; `binding in source : predicate` It remains a selection.

One collection can be transformed locally using `values [unique]`, `values [ordered]`, `values [ordered by score]` o `values [1..10, unique, ordered]`. Does not support `mut`. The elaboration normalises domain, `unique`, order and cardinality. `[n]` is still indexing; a cardinality An exact local without any other modifiers is written as `[n..n]`.

