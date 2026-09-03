---
title: Concrete grammar
aliases:
  - MUD concrete syntax
tags:
  - mud/specification
  - mud/gramatica
status: proposed
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

# 07. Concrete grammar

## State and purpose

[[gramatica/mud.ebnf]] defines the complete syntax of standard `.mud` source files in MUD 1.0. The additional physical format of `mud.module` is documented separately, and its complete grammar remains open in Q-062. This chapter specifies how to read the grammar, interpret contextual constructs and group expressions. The questions listed in the frontmatter affect semantics, but do not prevent the source form from being recognised.

## Parsing output

The normative parsing result is a lossless CST per file, defined in [[sintaxis/cst-sin-perdidas]]. The EBNF determines grouping and the order of meaningful tokens; the CST also preserves punctuation, terminators and trivia.

The presence of a CST does not confirm that the file is valid. The recovery process may represent missing or unexpected tokens without discarding them.

## Validation prior to the AST

Once the CST has been constructed, the contextual syntactic constraints required to produce a normalised AST are checked, including:

- Duplicate collection modifiers.
- Duplicate declarations of the same metadata on an owner, including units.
- A positional argument following a named argument.
- Specific combinations prohibited by this chapter.

The name resolution, types, domains and effects do not belong to this validation.

A `given` reuses the general expression for type, including dictionaries:

```mud
given prices: Product -> Money
```

The grammar may retain a `mut` modifier written within that expression for diagnostics, but the capability is statically invalid: `given` never grants write access.

## AST projection

The AST projection is defined in [[sintaxis/cst-a-ast-superficial]]. Production coverage is recorded mechanically in `sintaxis/cobertura-sintactica.yaml`.

## Programme

A file contains a header of declarations `using` followed by statements from leading figures:

```mud
using world.people
using physics.*
```

There is no path declaration; the path is derived from the file path. `using`, not `import`, is the only construct that establishes visibility between MUD paths.

All `using` declarations must appear before the first top-level declaration. Mixing them in is an error and never creates local or sequential scope. The order of multiple `using` declarations does not resolve ambiguities.

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
    ~name = "Alexandria"
}
```

`Thing` is the intrinsic abstract `thing` that acts as the top type. Every `thing` satisfies `is Thing`. A root without `as` retains no declared ancestors, but receives an implicit semantic edge to `Thing`. Writing `as Thing` is accepted but redundant: a conforming implementation must issue a non-blocking diagnostic and offer to remove it. `Thing` cannot be declared, created or destroyed:

```mud
create Thing   # static error
destroy Thing  # static error
```

`Thing` is always active without appearing in `start with`, and `all Thing` lists only effective concrete `thing` values, never the abstract concept.

Every `thing` exposes postfix properties and metadata separately from its fields. `~identifier` retains the source identifier and `~name` is configurable presentation text. Every `~` access is read-only during execution; metadata cannot be an assignable destination. Metadata are not ordinary fields.

The list following `as` does not indicate priority. `create` accepts no body here or anywhere else:

```mud
create Alexandria
destroy Alexandria
```

### `thing` initialisers

A `thing`, whether concrete or abstract, can initialise a stored field already contributed by its inherited schema through an assignment without redeclaring the field:

```text
fieldName = value-body
```

The target is retained as a field name until resolution. It does not declare a new field, replace its inheritable default, or target a calculated field. It must resolve to an inherited field: the same `thing` cannot locally declare `fieldName` and also contain a separate `fieldName = ...` initialiser. The form `fieldName: Type = value` is a single declaration with a default and remains valid. The initialiser value accepts a short expression or `ValueBlock`; the entire body is subject to the inherited field's static materialisation contract.

In an `abstract thing`, the initialiser does not materialise its own stored data; it is preserved as an inherited contribution to the first materialisation of concrete descendants. In a concrete `thing`, the local initialiser applies to its own first materialisation and is not inherited by its descendants. A more specific initialiser takes precedence over a less specific inherited one. Multiple specialisation does not establish precedence from the order of `as`: if the same source is duplicated and separate, incomparable contributions target the same field, they conflict.

```mud
thing Kingdom {
    mut treasury: Money = 0
}

thing France as Kingdom {
    treasury = 20
}
```

In `France`, `20` initialises `France.treasury` whenever `France` is materialised from its canonical definition. It does not become the field default or an inheritable initialiser for descendants of `France`. Confirmed destruction removes that stored data, and a subsequent `create France` reapplies the initialiser when constructing the new materialisation. This distinction keeps inheritable defaults separate from materialisation contributions.

```mud
abstract thing RichKingdom as Kingdom {
    treasury = 20
}

thing Lydia as RichKingdom
```

`RichKingdom` has no concrete `treasury` storage, but its initialiser contributes to `Lydia`'s first materialisation.

Mixing a field declaration with its separate initialiser in one definition is not permitted:

```mud
thing Broken as Kingdom {
    treasury: Money = 10
    treasury = 20
}
```

`name = value` has no special intrinsic meaning: if `name` is a stored field inherited from the effective schema, it uses this same form; `~name` remains presentation metadata.

## Fields

When a metadata-bearing owner with a `ValueBlock` uses the expanded form, its initial `~...` declarations may form an integrated preamble at the beginning of the same body. The preamble belongs to the descriptor, not to the `ValueBlock`, and cannot be combined with a second metadata body. The short form retains the separate metadata body.


Stored format:

```text
[mut] fieldName: Type [in domain] [collection-specification] [= value-body]
```

Calculated form:

```text
fieldName [derived-value-shape] := value-body
```

`derived-value-shape` may be `: Type`, `in domain` with an optional collection specification, or a collection specification alone. Therefore, both `area: Num in 0..* := width * height` and `area in 0..* := width * height` are valid. If the type is omitted, it must be inferred unambiguously from the expression, without a predetermined preference between compatible representations or contextual forms. If more than one solution exists, the type must be written. A calculated field does not support outer `mut`; its shape may specify a domain, a collection specification and internal `[mut]` capability.

Outer `mut` is written before the name because it describes the storage location, not the type of its members. `fieldName: mut Type` is not part of the syntax. Field names and metadata names occupy different syntactic positions: `name: Text` declares a field, whereas `~name = expression` declares or amends presentation metadata.

The value after `=` may be a short expression or a `ValueBlock`. In a stored field, the complete body must remain static: it is fully evaluated at compile time and cannot read world state, participants, `given` values, external locations or activities. Temporary mutable structures created within the `ValueBlock` are valid when the complete structure can be constructed statically. For example:

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

If a calculated field's expression is also statically closed, the compiler must suggest the immutable stored form. This is neither an error nor an automatic rewrite, and the suggestion does not appear when the calculation depends on runtime state.

A comma-separated list forms a calculated collection and infers type and cardinality where they can be proven:

```mud
numbers := a * b, d, c / a
```

The domain on a calculated value acts as a contract. A potentially out-of-domain result triggers a warning and a runtime transition check; a result that is provably outside the domain is an error.

## Expression blocks and value

An `ExpressionBlock` is a declarative form: it contains zero or more pure calculated locals declared with `:=`, followed by a final expression. It does not support stored variables, mutation, `for each` as a statement or an internal `if`. It is used by conditions, filters, quantifiers and dictionary key or selector sides.

A `ValueBlock` constructs a value and contains zero or more local statements followed by a final expression. Its only statements are calculated declarations, stored declarations, assignments whose footprint remains within the block, and local `for each`. It does not support `if`, external effects, actions, subactions, `create` or `destroy`.

```mud
result := {
    mut total: Money = 0
    for each item in items if item.taxable :
        total += item.price
    total
}
```

`ValueBlock` is not a primary expression. It appears only in owners that explicitly declare it; to use a complex calculation as an argument, index or effect RHS, bind it to a local first.

Stored local variables are also permitted in `then`:

```mud
then {
    mut remaining: Money = account.balance
    remaining -= cost
    account.balance = remaining
}
```

The form `x := ...` cannot be assigned to. `x: X = ...` creates a local slot that cannot be reassigned, and `mut x: X = ...` creates one that can. A `then` still requires at least one observable effect.

The default of `given` preserves `constant-expression` and does not allow `ValueBlock`.

## Type unions and outer arrows

`|` combines non-arrow alternatives and has greater precedence than `->` and `-->`. Both arrows have the same precedence and group from the right:

```mud
A | B -> C | D       # (A | B) -> (C | D)
A | B --> C | D      # (A | B) --> (C | D)
A -> B -> C           # A -> (B -> C)
```

An arrow must be the complete outer shape of a type. A dictionary cannot be a partial union alternative, even inside parentheses or through an alias whose effective shape is an arrow.


### Callable types and types obtained by reflection

Callable types are defined based on the types of receiver/participantes and on the part `given` from the firm:

```mud
Dragon.action(Volume)
(Attacker, Defender).action(Amount)
Dragon.rule(Limit)
Dragon.look(Detail)
```

The category forms part of the type construction. This surface alone determines neither variance nor every compatibility rule between callables: Q-063 keeps that issue open. The ability to root outside `action` likewise cannot be deduced solely from reflective subtyping.

A postfix expression ending in `~type` may occupy a type position when elaboration proves statically that it produces `Type`. For example, `alias Stats := MyDragon.Stats()~type` is valid; the call `MyDragon.Stats()` without `~type` remains a value rather than a type expression. A callable type such as `Dragon.look(Detail)` already denotes `Type` and does not need `~type`.
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

The alias restriction is checked after nominal resolution. Each non-arrow alternative may declare a domain and at most one collection specification. The final collection specification belongs to the complete union:

```mud
values: Nat in 0..10 | Int in -10..-1 [1..*] = [2 to Nat]
```

Cardinalities by alternative are not permitted. If a contextual expression fits several alternatives, one must be selected using `to`.

## Collections and dictionaries

Cardinality, when present, is placed at the start of the square brackets. Modifiers may be separated by spaces or commas:

```mud
citizens: Person [0..* unique ordered mut]
citizens: Person [0..*, unique, ordered, mut]
```

A trailing comma is not permitted. In an immutable stored field with an initialiser, an omitted cardinality remains omitted in the AST and is inferred as the initial value's exact outer cardinality:

```mud
one: Nat = 1                 # [1]
three: Nat = [1, 2, 3]      # [3]
none: Nat = empty            # [0]
table: A -> B = AValue -> BValue # [1]: the complete dictionary is one value
```

A field with outer `mut` retains `[1]` when cardinality is omitted. Calculated fields declared with `:=` retain the inferred shape of their expression. An inferred immutable cardinality other than `[1]` prompts the author to write it explicitly.

Compatible collections support `|`, `&` and `--`. `^` requires the result to comply with uniqueness rules. They operate on multiplicities or membership; they do not concatenate:

```mud
leftChars: Char [1..5] = ["a"]
rightChars: Char [0..2] = empty
combinedChars := leftChars | rightChars
```

`empty` is not a failure by itself. A partial query produces `empty`; failure appears only when the required outer shape does not permit cardinality zero.

### Associations and branches

In an association `->`, the left side is an `ExpressionBlock` and the right side a `ValueBlock`. In a branch `-->`, the left selector is a Boolean `ExpressionBlock` and the result is a `ValueBlock`. Braces replace only the expanded side, so all four short and expanded combinations are valid without auxiliary keywords or outer wrapping.

```mud
key -> value
key -> { result }
{ key } -> value
{ key } -> { result }
```

The scopes on both sides are independent. Key or selector locals do not flow into the value or result. Dictionary application remains externally pure.

### Exact dictionaries `->`

An exact dictionary is queried by key equality, is countable and permits outer mutability. Associations are written with the same arrow:

```mud
capitalOf: Country -> City [2 ordered] =
    Spain -> Madrid,
    France -> Paris
```

A missing key produces `empty`. A complete association may be inserted as a runtime value:

```mud
then add (Portugal -> Lisbon) to capitalOf
```

`unique` requires associated values to be globally unique. An insertion or replacement that would duplicate one value under two keys is a complete no-op: it changes no association and does not produce `failed`.

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

An absent lookup retains the optional result shape:

```mud
capitalOf[Italy] # City [0..1], produces empty if Italy is absent
```

The key elements may be structural components:

```mud
distance: (City, City) -> Length =
    (Madrid, Toledo) -> 74 km,
    (Madrid, Segovia) -> 91 km
```

Set-theoretic operators on dictionaries act on keys. For a common key, `|` and `&` retain the left-hand value:

```mud
left: Key -> Nat = AKey -> 1, BKey -> 2
right: Key -> Nat = BKey -> 9, CKey -> 3

left | right   # AKey -> 1, BKey -> 2, CKey -> 3
left & right   # BKey -> 2
left -- right  # AKey -> 1
left ^ right   # AKey -> 1, CKey -> 3
```

`|` and `&` are not necessarily commutative, as with dictionaries. Insertion order preserves left-hand content first; `ordered by` normalises after calculating the content.

### Functional dictionaries `-->`

A functional dictionary is a pure case-defined policy. `value` refers to the input within both the selector and the result; `_` is the fallback:

```mud
dangerOf: Creature --> Danger [ordered] =
    value is Dragon --> Extreme,
    value is Predator --> High,
    _ --> Low
```

`ordered` means `FirstMatch`: the first applicable branch wins, and application yields `[0..1]`, or `[1]` with a fallback. Without `ordered`, every ordinary branch is evaluated and all results are obtained; `unique` removes duplicate results:

```mud
traitsOf: Creature --> Trait [unique] =
    value is Flying --> Aerial,
    value is Aquatic --> Aquatic,
    value is Magical --> Magical
```

Selectors are written explicitly. No shorthand implicitly inserts `value`, `==`, `is` or `in`:

```mud
seasonName: Month --> Text [ordered] =
    value == January --> "winter",
    [March..May] has value --> "spring",
    value == June or value == July --> "summer",
    _ --> "other"
```

Therefore, `January --> "winter"`, `[March..May] --> "spring"`, `Dragon --> Extreme` and `shop.discounted --> DiscountedPrice` do not automatically acquire selector meaning. The complete comparison or membership must be written.

Applicability and result production are tracked separately. A branch whose selector applies may produce `empty`; the `_` fallback contributes a result only when no applicable ordinary branch has produced one. `FirstMatch` preserves evidence order; `AllMatches` records every result actually produced.

Selectors and results may read external state purely:

```mud
priceOf: Product --> Money [ordered] =
    value in shop.discounted --> value.basePrice * shop.discount,
    _ --> value.basePrice
```

These readings create explicit dependencies on `shop.discounted`, `shop.discount` and `basePrice`. All transitive calls use the same snapshot.

It supports neither outer `mut` nor `[mut]`, is not traversed directly with `for each`, and every recursion must have a demonstrably well-founded measure. Valid proofs include numeric descent, strict cardinality reduction, or transition to a strict substructure; a cycle without such evidence is an error.

To iterate over results, iterate over an input domain and apply the dictionary:

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

Branches can be changed only by editing the model at the owning dictionary. By default, a structural edit may insert before `_`, and may update, remove or move a branch, but none of these operations targets a branch anchor or assumes an independent public identity; the local key is grounded in the resolved representation.

Functional calculus is extensional; it does not merge branches:

```text
(F op G)[x] = F[x] op G[x]
```

`F | G`, `F & G`, `F -- G` and `F ^ G` combine the sets obtained by applying both operands to `x`. Their fallbacks are evaluated independently. The union and symmetric difference of two `ordered` functionals may produce two outcomes and generally lose `ordered`; intersection and difference may preserve it.

It is not permitted to combine an exact match with a functional match directly.

### `FirstMatch`, `AllMatches`, fallback and cardinality

In a functional `[ordered]` dictionary, `unique` is valid but redundant and triggers a suggestion to remove it. Without a fallback, application has cardinality `[0..1]`; with a fallback, `[1]`.

In an unordered functional dictionary, each matching ordinary branch contributes at most one result. With `n` potentially matching branches, the conservative cardinality is `[0..n]`; a fallback raises the lower bound to `1`. `unique` deduplicates equal results from different branches without changing which branches applied.

```mud
tagsOf: Creature --> Tag [unique] =
    value is Dragon --> Magical,
    value is FireCreature --> Magical,
    value is Flying --> Aerial,
    _ --> Ordinary
```

For a fire-breathing dragon, `Magical` appears only once. The union or symmetric difference of two `ordered` functional dictionaries loses `ordered` when it may produce two distinct results; intersection and difference preserve it when cardinality remains `[0..1]`.

### Chaining dictionary types

Arrows accept complete types and are right-associative:

```mud
board: Square -> Piece [0..32 ordered]
nested: Name -> Coordinate -> Piece [*]
policyByMode: Mode -> Product --> Money [2..4 ordered]
```

The second example is equivalent to `Name -> (Coordinate -> Piece [*])`. Each collection specification applies to the immediately preceding arrow. Parentheses are needed only to alter the natural grouping or delimit another complete construction.

The chained application processes each level in turn:

```mud
piece := boardByGame[game][coordinate]
```

Composition does not introduce an abstract function category. It is expressed by applying one dictionary's result as input to another:

```mud
weather := weatherOf[capitalOf[country]]
```

### Anonymous structural products

`(A, B)` and `(a: A, b: B)` are structural products. Their values are `(x, y)` and `(a = x, b = y)`. They are compared component by component and can act as exact keys or functional entries:

```mud
distance: (City, City) -> Length
label: (name: Text, count: Nat)
routePolicy: (origin: City, destination: City) --> Route
```

Variable names do not create component names: `(x, y)` remains positional even when its variables are named `x` and `y`. An alias remains nominal even when its payload has the same shape:

```mud
alias Coordinate {
    x: Num
    y: Num
}

raw: (Num, Num) = (1, 2)
nominal: Coordinate = (x = 1, y = 2)
```

`raw` and `nominal` are not interchangeable without an explicit nominal conversion. Anonymous-product compatibility requires the same arity, compatible component names where present, and component-by-component correspondence.

`ordered by path` applies to collections whose members expose a fixed path of fields, components or associated data. Every intermediate access must be unique and the final value must have a total semantic order:

```mud
route: Terrain [* ordered by movementCost]
teams: Team [* ordered by captain.age]
```

A `thing` has no total order by itself and cannot be the final key. The complete path must be transitively stable: mutable stored fields, calculations with mutable dependencies and intermediate accesses whose state a later action may alter are invalid keys. An optional path is also rejected unless a defined position exists for `empty`.

If a member is a union, the path must exist across all feasible alternatives. Every segment must remain unique and stable, and the final key must elaborate to a single totally ordered type. A single implicit widening is valid; two purely representational aliases are not unified. When alternatives need adaptation, a common calculated field must be provided.

`ordered by` does not permit arbitrary expressions. If the criterion requires a formula, it is declared as a field or calculated value and referenced by name. Keys with the same value retain their relative order under stable provenance; in a purely sequential source, this is their order of appearance. Ties are not resolved by anchor, identity or `family` declaration order.

`ordered by` is prohibited for `Char`; its encoding is Unicode. `Text` does not accept collection specifications.

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

An alias declaration may write an unordered list of ancestors using `as`. The local definition is optional when the ancestors determine a complete effective form. Therefore, both `alias UserName as PlayerName` and `alias PositionedCoordinate as Coordinate` are valid. `alias A` without ancestors or a definition is a static error.

`:= type` introduces the representation of a root nominal alias. Nominal aliases with ancestors inherit the effective representation and cannot redeclare it. In particular, `alias UserName as PlayerName := Text` is invalid.

A `:= type` representation may be followed by an immediate body containing only alias metadata. A representational alias can therefore be documented or configured without acquiring structural components.

The structural body may contain stored components, calculated fields and inherited-default overrides. An override `name = value` changes only the default value: it cannot alter type, domain, cardinality, order, uniqueness or inner capability.

Structural literals are contextual:

```mud
(E, Four)
(file = E, rank = Four)
(size = 30)
```

The positional form must provide all components. If any are omitted, the form must be fully qualified: the omitted components take their explicit default value or the default value of their type. The components listed may skip previous or intermediate components, but those listed retain the relative order of declaration. You are not allowed to mix positions and names:

```mud
pagination: Pagination = (2, 30) # valid
pagination: Pagination = (2)     # invalid: partial positional form
pagination: Pagination = (size = 30) # valid: page retains 1
```

A component does not support outer `mut` because the alias value and each component are immutable. Its collection specification may nevertheless contain `[mut]` to grant internal capability over directly contained `thing` values; this capability does not make the collection itself assignable.

A calculated alias component uses the same syntax as other calculated fields, including an optional declared shape:

```mud
alias Squad {
    members: Soldier [*]

    wounded [* mut] := soldier in members :
        soldier.health < MaximumHealth
}
```

A calculated collection is not a stored subcollection of `members`: it has its own contract. `[mut]` grants internal capability even if the source does not. The selection is fixed for the snapshot being evaluated; once effects have been consolidated, it is recalculated from the new state, so members can join or leave automatically. A stored collection is never pruned for this reason.

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

Data declarations appear before the first member. A stored datum may be followed, after its optional default, by an immediate body containing only `~...` statements. A calculated datum may contain the same immediate metadata body and uses the complete `derived-value-shape` of calculated fields: it may specify a compatible type, domain or collection shape without acquiring outer mutability or local storage.

The metadata body describes the canonical `family` data descriptor, not the concrete value supplied by each member. For example:

```mud
family Terrain {
    movementCost: Nat = 1 {
        ~summary = "Base movement cost"
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

The member assignment `movementCost = 4` simply overrides the stored datum's value. It does not support a metadata body, introduce another anchor or alter the metadata of the `movementCost` descriptor. A calculated value expression is evaluated statically for each member after stored data have been resolved; it may query other associated data through unqualified names, and those data must have acyclic dependencies. A member block may assign only stored data.

Members are separated by commas and do not permit a trailing comma. `ordered family` makes its members comparable by declaration order and allows associated-data paths, including stable calculated data, to serve as `ordered by` keys in collections.

## Magnitudes

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

Point magnitude:

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

A base magnitude has one of two forms: an empty body, or exactly one `root unit name` followed by zero or more alternative units. An alternative cannot be declared without a root. Absence of a root is a complete semantic choice: the magnitude retains an independent nominal dimension, but its values display no unit. It is not identical to its numeric representation, another unitless magnitude, or the dimensionless element.

```mud
chance: Probability = 0.75
explicitChance := ratio to Probability
```

A bare numeric literal may take the type of a unitless magnitude when the expected context determines it uniquely. A general numeric expression requires `to` to construct that magnitude. Arithmetic retains the nominal factor even when it has no unit form; the visible unit projection may coincide across statically distinct dimensions. A quantity that explicitly writes a unit includes only the factors that unit identifies: context introduces no hidden factors.

A derived magnitude declares only nominal alternative units as `unit name := equivalence`; a point magnitude declares no units. For the latter, `in` and its domain are optional: without them, the domain is the full underlying coordinate space; an ordinary interval bounds it without wrapping, and `[a..b) cycle` adds cyclic normalisation. `cycle` modifies the complete domain rather than the interval term, and only a point magnitude accepts it.

A unit body contains only ordinary `~...` statements; there is no `unit-property`. `~prefixes: Prefix [* unique] = empty` uses the built-in `Prefix` type: omitting it or writing `empty` enables none, `all` enables the full decimal SI catalogue, and a collection such as `[kilo, milli]` selects those predefined values. `~name`, `~plural` and `~abbreviation` use the same general metadata system, and every runtime `~` access is read-only.

A number may omit the space before its unit, but the formatter inserts it: `3m` and `3 m` have the same AST, and the latter is canonical.

`~format` is optional and uses the general `Text` template syntax: spaces are literal, and `:2` sets two places to the left of the point here. Without it, a point has no special representation: it uses the ordinary textual representation of a magnitude, with the coordinate in the root unit and that unit's abbreviation or name. In this case, the first component is the coordinate in that unit—reduced by the cycle, if one exists—and each subsequent component is extracted within the preceding one. A non-obvious container is made explicit, for example `~format = "{week from year:2}"`.

Outside `~format`, extraction requires the point:

```mud
minute from hour in time
picosecond from second in time
week from year in date
```

The form is one syntactic construct. Its receiver must be a point magnitude; both units belong to its underlying magnitude; the extracted unit is no larger than the container unit; and the result is `Nat`. It uses the canonical origin and Euclidean remainder, with a possible final partial component when the units do not divide exactly. Extraction does not depend on `~format`.

Forms produced by `~format` occupy the contextual token `POINT_LITERAL`. The expected type selects a single point magnitude, and the literal must reproduce its canonical form exactly. A format that cannot be inverted unambiguously is invalid. Components finer than the last one shown take the value zero.

Without `~format`, the literal is written as an ordinary quantity with a compatible unit. Every literal must belong to the domain before cyclic normalisation is applied; for example, `26:00:00` is invalid for `TimeOfDay`.

## Initial activation with `start with`

Each module may declare at most one `start with`. It is not a `main`, does not invoke modules and does not specify an initialisation order. Omitting `start with` from a module is equivalent to an empty contribution.

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

Each expression must be static and may contain zero, one or more activatable `thing | rule` declarations. A collection contributes its members directly; nested collections are not permitted. Duplicate identities are deduplicated, and source order is retained only as provenance, not as priority.

A `start with` may activate only declarations whose lifecycle is module-scoped. Contributions from all modules are combined before initial stabilisation. `Thing` is always active and is not part of the activatable collection.

`all D` may materialise a countable domain when a contribution requires an explicit collection; `all` without an operand retains its contextual meaning.

## Participants

`for` binds predefined roles of any declared value type. A role may be individual or collective; its values may be restricted by `in domain` and may use the complete collection specification. The domain is written after the type and before the collection specification. `on name: Type` uses the implicit universe of concrete, active `thing` values compatible with that type, whereas `on name[: Type] in source` binds from a finite, countable source and may therefore relate other values. The related form may write the type to refine the source elements nominally.

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

The type may be inferred from a related participant: `kingdom in world.kingdoms` is usually sufficient.

The type may also be written only to refine the names of collection members, without necessarily repeating their declared type:

```mud
rule MutualFriends on
    alice: Person in bob.friends,
    bob in alice.friends
{
    when alice.mood changes or bob.mood changes
    then create FriendshipChanged
}
```

All names in an `on` header are visible throughout that header. Their types and constraints are resolved jointly, so forward references and cycles are permitted when they have a unique nominal solution. Each role ranges over active concrete `thing` values of its effective type; relationships are the finite join satisfying all membership conditions in the same snapshot. Different roles need not bind different identities, and two symmetric orientations do not constitute different relationships.

Every `for`, `on` and `given` participant has an explicit identifier. There is no anonymous participant, nor one with effective cardinality `[1]`. A header may group identifiers sharing a type and metadata body, for example `for attacker, target: Fighter { ... }`; the group is sugar and each descriptor retains its own anchor.

In an action, `mut` before any `for` role name, including cardinality `[1]`, grants outer mutability over the supplied collection. The corresponding receiver must be a stored location with that capability; a literal or calculated collection does not satisfy the contract. The `mut` in the collection specification continues to grant internal capability over member `thing` values:

```mud
action Treat for
    mut patients: Person [1..10, unique, mut]
{
    then for each patient in patients : {
        patient.health += 10
    }
}
```

The preceding declaration may change membership or order in the stored collection and may modify its members. `mut patients: Person [*]` grants only the first capability; `patients: Person [*, mut]` grants only the second.

Declaring internal capability over immutable values is valid, but the compiler suggests removing it when it can prove that the capability can never be exercised. The suggestion preserves meaning and is not a warning. In an exact dictionary, outer `mut` changes associations, while `[mut]` grants authority only over materially associated `thing` values—never over keys, aliases, nested levels or an absent value. A functional dictionary prohibits both forms of `mut`.

Outer mutability can be applied to a collection of any type:

```mud
action Record for mut observations: Num [*]
given value: Num {
    then add value to observations
}
```

Boolean rules and `look`, being pure, do not allow outer `mut`. No `given` supports mutability outside or inside: its collection specification may state cardinality, `unique` and `ordered`, but its production excludes `mut`.

An ordinary reference to `World` denotes that exact identity. `on World` and a `for World` role reflectively select the concrete, active `thing` values that satisfy `is World`, including `World` itself if it is concrete. This selection applies only when the role's type is a `thing`.

The link depends on the role category:

- one `thing` is linked by identity;
- a built-in value, alias, `family` member, dictionary or other immutable value is bound by value;
- a role with outer `mut` is bound by storage-location identity and also retains its current value.

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

### Reactive

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

The newline after `changes` ends a complete expression; braces do not suppress terminators, so `or` has no left operand. To place the operator at the start of the second line, the expression must be kept open with parentheses.

It has lower precedence than arithmetic, conversions and comparisons, but higher precedence than `and` and `or`. Therefore:

```text
position + offset changes  ≡  (position + offset) changes
temperature > limit changes  ≡  (temperature > limit) changes
position changes or ready  ≡  (position changes) or ready
```

Within `when`, every `e changes` produces a temporal trigger that pulses when `e` has different values in two consecutive initial snapshots. Ordinary Boolean operands of `and` and `or` represent a `false` → `true` transition; this allows changes and conditions to be combined without missing consecutive pulses. Only the words `and` and `or` compose temporal triggers; their symbolic variants and the other logical operators retain their ordinary value meaning.

A purely Boolean `when e` detects the complete expression's `false` → `true` transition. `old e` may appear in a reactive rule's `when` and `if` when `e` is pure and evaluable in both snapshots; it is not permitted in `then`. A variation is measured with an explicit condition such as `position - old position >= 10 meters`; `changes by` does not exist.

```mud
when position changes and velocity changes

when price changes or outOfStock
if price > old price and stock < old stock

when position - old position >= 10 meters
```


`when` also supports declarative sources. A `message` occurrence, the effective firing of a reactive rule and the evaluation of an `always` rule for a binding may act as triggers. Actions, subactions, `look`, Boolean rules and tests are not declarative trigger sources.

A declarative reference used as a trigger takes no parentheses: `when Damaged`, `when Dragon.Damaged`, or a local containing that descriptor. Receivers restrict its `on` bindings; they do not turn the trigger into an ordinary call.

A trigger produces zero or more causal matches. Each match retains its bindings or witnesses and occurrence identities. `and` performs a natural join on compatible matches and, where they share no bindings, a Cartesian product; `or` performs union. Two causally distinct events are not duplicates merely because they share a payload. The purely Boolean case described above is the temporal rising edge that creates these matches when the corresponding transition occurs.
Bindings found in the first snapshot established by `start with` compare `old` and the current value against that same snapshot, so `changes` does not fire. Rising Boolean branches instead retain a virtual previous value of `false` and may fire when already true. Any binding created later takes its first active wave as a complete baseline without firing, and begins comparison on the next wave.

### `always`

```mud
always rule ValidPopulation on kingdom: Kingdom {
    population := kingdom.population
    population >= 0 people
}
otherwise "Population cannot be negative: {population}"
```

The body directly contains the condition, without `if`. The optional `otherwise` is written after the closing brace, forms part of the complete rule, and accepts a `Text` expression. Its diagnostic is evaluated only when the condition is false, over the same tentative state and bindings that breached the rule. Its value becomes the reason for the `failed` result. Omitting it is legal, but produces a warning and a default reason. Writing it inside the braces is an error.

## Actions

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

There is no semantic classification of elementary versus compound actions. A `then` is an ordered sequence of consequences and may contain local `:=` bindings, direct effects, `action` or `subaction` calls, and `for each` iteration. An internal call executes at its textual position over the resolution's private delta: it observes preceding visible effects, adds its own effects to that resolution, and its subsequent judgements observe them.

An `action` may be an external root. A `subaction` never can, but both may be omitted and may be invoked from any semantic `then` context, including the `then` of a reactive rule or test when the context permits it. An internal call does not open an independent transaction or root resolution.

The `after` clauses of every executed action and subaction are checked against the final stable state of the complete tentative resolution. A nested `failed` reverses the entire resolution; an internal `rejected` also aborts and reverses it while retaining the `rejected` category. The optional `otherwise` of `if` or `after` explains rejection, and the associated `then` explains failure of the complete transition.

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

External eligibility and reflective subtyping are distinct properties: `subaction <: action`, but widening a descriptor does not make a `subaction` a safe external root.

## `look` and `message`

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

`look` is a pure callable. It may be accessed by the host, by another module whose contract makes it visible, and by MUD code in reading contexts, including `then`. Its fields read one coherent view inherited from the caller: host stable state, a rule snapshot, or the private delta visible at that point in `then`. It supports `for` and `given` and returns exactly one value of the anonymous type made from its public fields.

A `message` is not called directly. Every instance of its `when` that passes `if` creates a causal occurrence with an identity, declaration, `on` bindings and birth wave. That occurrence may feed triggers in the next wave. Within MUD, its payload is projected onto the causal view; after commit, it is projected to the host from the final stable state. A rollback cancels external delivery.

The outer envelope keeps the `on` bindings that identify participants separate from the public payload; it does not merge the two namespaces. Confirmed occurrences retain causal order between waves and, within one wave, a stable reproducible technical order that introduces no priority semantics among them.

A public field whose direct value is a magnitude supporting units should preferably select its representation with `in`. Omitting it is legal and uses the canonical unit projection, but triggers a warning because it implies an API decision. A unitless magnitude displays its numeric value directly without that warning. A direct point magnitude publishes its coordinate in the chosen unit, not its `~format`; publishing the format requires a `Text` field.

## Clauses and keys

`when`, `if`, `then` and `after` may always use braces. They may omit them when there is only one element. A `then` with more than one effect and a test `after` with more than one assertion must use them.

```mud
if ready

if {
    available := player.money
    available >= price
}
otherwise "Available: {available}"
```

Braces do not suppress terminators between elements within a block.

### Local values in conditions

Boolean-rule blocks, `when`, `if`, `always` rules and action `after` expressions may contain zero or more local bindings followed by exactly one final expression:

```mud
when {
    wasOpen := old door.open
    isOpen := door.open
    wasOpen != isOpen
}
```

Bindings use `name [: Type] := expression`, are pure, immutable and sequential, and permit no forward references, cycles, redeclaration or shadowing. They are recalculated on every evaluation of the clause and store no state between waves.

Its scope reaches the associated `otherwise`, but not `then` or any other clause. In a `when`, `changes` and `old` evaluate a local's defining expression in every required snapshot.

The single non-declaration expression must come last. It must elaborate to `Bool`, except in `when`, where it must produce an activator supported by the temporal contract. An empty block, a block containing only local bindings or a second non-declaration expression is invalid.

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

The form `name [derived-value-shape] := value-expression` declares an immutable local value. The derived shape permits `: Type`, `in domain` with an optional collection specification, or a collection specification alone. Type and cardinality are inferred when a unique solution exists; otherwise, they must be written explicitly. Outer `mut` is not permitted.

The expression is pure and evaluated only once when execution reaches the declaration. It reads preceding sequential effects from the same private delta and retains its value even if later statements change its dependencies.

The name is available only from its declaration to the end of the block. It may be used in later statements, but not before it appears; there are no forward references, cycles, redeclarations or shadowing. Each iteration creates a new scope. A `then` must retain at least one effect or call: a block containing only locals is invalid.

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

Named receivers may reorder roles provided their names are exact and exhaustive.

A collection expression occupies a single receiver position when the corresponding role is collective; it is not split across several roles. If the role declares outer `mut`, that expression must also denote a compatible mutable location.

A type's appearance in `for` does not require every argument of that type to be a role. `for` identifies the operation's semantic subjects; `given` identifies its auxiliary parameters.

Every `given` must have a name, is read-only and may declare a closed static default:

```mud
given origin: Square = Capital,
      depth: Nat,
      exhaustive: Bool = false
```

Arguments may be positional, named or a positional prefix followed by named arguments. After the first named argument, no positional argument may appear. In positional use, only a complete suffix with defaults may be omitted; in named use, intermediate defaults may be omitted and arguments reordered:

```mud
game.Search(Capital, 3)
game.Search(depth = 3)
game.Search(exhaustive = true, depth = 3)
```

The latter form is valid, but the compiler suggests writing `depth` before `exhaustive` to follow declaration order. A name cannot be repeated or unknown, and every `given` without a default must remain bound.

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

`destroy` preserves identity and canonical definitions, but removes the runtime materialisation of a concrete `thing`. Confirmed destruction discards its stored values and runtime structural modifications regardless of owner identity; a later `create` constructs a fresh materialisation from the effective schema and reapplies defaults and initialisers. This destruction does not delete capabilities owned elsewhere that are merely suspended by an inactive dependency. Destroying a reactive rule also discards that activation's temporal memory; if recreated, its first active wave establishes a new baseline without firing solely because of reactivation.

An assignable path may traverse stored components of immutable aliases and exact-dictionary indices when it ends at an externally writable root location. This write does not mutate intermediate aliases: elaboration constructs new values of the exact nominal type, preserves their other stored components, recalculates derived values, and propagates replacements outwards to the storage root. For example:

```mud
shop.orders[id].status = Shipped
shop.orders[id].retryCount += 1
```

A local containing an alias remains a value and acquires no path back to storage, so `order.status = Shipped` is invalid when `order` is merely a local binding. A derived alias field is likewise not writable.

If an exact dictionary lookup used as an intermediate step does not find its key, the absence is `empty` and the partial effect is a no-op: it neither creates the association nor synthesises a default value, and does not produce `failed` merely because of that absence. This does not affect the direct assignment `shop.orders[id] = order`, which replaces a complete association and may create a missing key when the contract permits it.

Resolution and typing distinguish `remove name from Owner` from removing a value. In both cases the parser retains the same provenance; AST construction must produce the correct variant or a diagnostic.

`|=`, `&=`, `^=` and `--=` retain their update class in the AST. They require an externally mutable location or a reconstructible assignable path whose write-back ends in one, and a result assignable to the location. `^=` accepts only `unique` collections. For collections, homogeneous updates consolidate by union, intersection, parity or summed removed multiplicities; mixing different classes is a conflict unless explicitly specified otherwise. For `Text`, `|=` is concatenation and multiple concurrent updates require a defined global order.

## `for each`, progressions, selection and quantifiers

`for each` accepts any finite, countable source: collections, exact dictionaries, countable intervals, finite countable domains and any other value with canonical enumeration. An interval does not become a collection merely because it can be traversed.

```mud
for each person in kingdom.people if person.hungry :
    person.health -= 1

for each value in [0..100] by 5 : {
    doubled := value * 2
    total += doubled
}
```

The `:` is mandatory. Braces form part of the body and do not replace the separator. The body may begin on the same line or after one or more terminators; this physical separation does not alter its abstract structure. In executable `for each`, the short body must be an effect or action call and the braced body uses `EffectBlock`. Within `ValueBlock`, `LocalForEach` uses a short `ValueStatement` or a `LocalStatementBlock`, accepts only local statements, and cannot outlive the value block's scope.

### Iteration filter

`by` precedes `if`. The filter may be an expression or an expression block with local values. It is pure and non-stochastic. With semantic order, it is evaluated immediately before each iteration and observes the sequential projection left by preceding iterations; without semantic order, all filters start from the same initial projection and accepted modifications are consolidated simultaneously under the body's contract. An exact dictionary may bind `(key, value)`.

### Progression `by`

`by` takes a signed compatible difference that is evaluated once before runtime. A positive step anchors at the lower bound and a negative step at the upper bound. An open initial bound advances once before the first candidate. The progression ends before the first out-of-range candidate and need not reach the opposite bound. Inverted endpoints still produce `empty`.

```text
[1..8] by 2   -> 1, 3, 5, 7
[1..8] by -3  -> 8, 5, 2
(1..8] by 2   -> 3, 5, 7
[1..8) by -2  -> 6, 4, 2
```

A provably zero runtime step is a static error; if it may vary and evaluates to zero, it produces the evaluation failure `progression-step-zero`. In an action that failure yields `failed` and rollback; in a pure expression it propagates as evaluation failure and never becomes `false`. A zero domain step is always a static error. Compatibility uses the advance operation and exact implicit conversions rather than nominal identity: `Nat` may advance through `Int`, `Num` through compatible exact differences, and quantities through compatible units. For a point magnitude, the step is a linear difference.

`by` is not a stride over arbitrary collections. `ordered by path` has separate semantics.

### Default steps and numbers

A source with its own enumeration order does not need `by`. For sequence-based enumeration, `Nat` and `Int` default to `1`, and `Money` to `0.01`; omitting `by` always selects that positive difference. Other exact progression types require an explicit step unless they define a canonical successor. `Num` supports explicit exact steps, and a general `Num` interval without a step is invalid. `Rum` intervals never permit `by` progression, in iteration or stepped domains; an explicit collection of `Rum` values is enumerable without `by`.

### Stepped domains

`interval by step` uses the same progression to define membership, and a static step may be negative. Its sign may change the members, but order is not part of the type. `all` materialises in canonical order; `Nat in [1..8] by -2 = all` produces `2, 4, 6, 8`. In discontinuous intervals, iteration restarts for each segment; positive steps traverse segments from lowest to highest, while negative steps reverse that order. A cyclic point domain covers at most one fundamental period.

### Selection and quantifiers

Selections and `exists`, `forall`, `count`, `min` and `max` accept `by` when the source defines a progression, and retain `:` even when the body uses braces. All use `ExpressionBlock`: the block contains `:=` premises followed by a final Boolean expression. For `min` and `max`, that predicate filters witnesses and the operation returns the first or last respectively in the source's semantic order; an `ordered` source without an explicit key is also valid. A source without usable order is rejected, and no accepted witness produces `empty`. `sum` is not part of the language.

A selection produces a collection and therefore does not consume a bare domain directly: if the conceptual source is a domain `D`, it must be written `all D`. Iterations and quantifiers that do not produce a collection may consume a finite, countable domain directly.

```mud
selected := x in source by step : {
    threshold := limit
    x < threshold
}
```

A selection directly returns the accepted instances and preserves provable multiplicity, uniqueness and order. Its predicate remains pure and deterministic.

### `take` and indexing

`take amount from source` retains its existing semantics. Because it produces a collection, a domain `D` cannot appear bare as `source`: it must be explicitly materialised as `all D`. On an ordered collection or a materialisation with canonical enumeration, it takes the prefix; on an unordered collection or dictionary, it takes a reproducible sample without replacement. Positional indexing still requires an observable order.

## Top type `Any`

`Any` is the open top type over the project's MUD values. This includes basic and built-in values such as `Prefix` members, `thing` identities, aliases, `family` members, magnitudes, intervals, collections, dictionaries, structural products and first-class declaration and type descriptors. AST nodes are not MUD values merely because they exist as compiler representations.

`Any` is not enumerable; it has no universal or predefined order. The following are invalid:

```mud
all Any
unknown: Any
```

A stored field of type `Any` must provide an initialiser. Equality requires compatible effective types and uses the effective type's equality relation. Any more specific operation requires narrowing:

```mud
rule Positive given value: Any {
    value is Nat and value > 0
}
```

Inside a functional branch, `is` and `iis` retain their narrowing in the result:

```mud
describeAny: Any --> Text [ordered] =
    value iis PersonId --> "Person id {value}",
    value is Nat --> "Natural {value}",
    _ --> "Other"
```

`Money` remains a built-in type because of its materialisation rules, not as an exception to the openness of `Any`.

## Contextual literals

Collections may be written in square brackets. In places where a comma does not conflict with another construction, the contextual form may omit them:

```mud
[A, B, C]
```

Brackets are required for nesting and for using the collection as a single argument. `empty` needs an expected type; `empty == empty` is invalid without context.

A dictionary with a key structural alias supports:

```mud
board[(E, Four)]
board[E, Four]
```

## Intervals

The type form for an interval first writes the endpoint type and then the contextual word `Interval`:

```mud
Nat Interval
Int Interval
Num Interval
Rum Interval
Money Interval
```

The grammar retains any `type-reference` in that position; the static phase requires it to resolve to an accepted numeric representation. `Interval` is not a nominal declaration looked up by name resolution in this construct.

Forms:

```mud
[a..b]
(a..b)
[a..b)
(a..b]
a..b
[a]
```

`a..b` is equivalent to `[a..b]`; `[a]` is equivalent to `[a..a]`. A `*` endpoint must be open on its side. The only cyclic form for point magnitudes is a complete interval followed by the modifier: `[a..b) cycle`.

Finite endpoints are complete expressions and must elaborate to the same ordered type. Within a magnitude interval, they may be expressed in local units—even different ones—which are normalised before comparison:

```mud
[1 m..5 km]
[minimumDistance..5 m]
[1 km..maximumDistance]
[minimumDistance..maximumDistance]
```

A literal next to a magnitude-valued expression must carry its own unit. Therefore, `[minimumDistance..5] m` is invalid and must be written `[minimumDistance..5 m]`.

When all finite endpoints are numeric literals without unit, just one unit may follow the interval:

```mud
[1..5] m
1..5 m
[1..5) km
[*..5] m
[1] m
[] m
```

`1..5 m` is grouped as `(1..5) m`. The outer unit is not distributed over fields or quantities that already carry a unit. `[1..5 m]` is invalid because it combines `Num` with a magnitude, and `[1 m..5 m] m` adds an invalid second outer unit.

The canonical serialisation of literal endpoints that share a unit uses `[1..5] m`, although `[1 m..5 m]` is also valid. If the units differ or one endpoint is an expression that already has a type, local units are used.

After evaluating and normalising the effective extremes of a linear interval:

- a lower bound that is less than the upper bound preserves the written sides;
- equal endpoints form a singleton only if both sides are closed, and produce `empty` otherwise;
- a lower bound greater than the upper bound results in `empty`.

Inversion does not imply descending traversal or a cycle. Producing that empty interval never fails a resolution by itself; only constraints that make the tentative state invalid produce `failed`, such as a stored value outside its domain or an unsatisfied `always` rule. An out-of-domain `given` and a false `if` or `after` retain the `rejected` result.

Domains declared in a magnitude header retain bare numeric bounds interpreted in their canonical representation: in the root unit when one exists, and directly in the numeric representation when there are no units. The form `[a..b) cycle` retains this restriction and requires a strictly positive period. Other endpoint forms, such as infinities or empty intervals, are invalid with `cycle`.

## Precedence and grouping

From highest to lowest:

| Level | Shapes | Group |
| ---: | --- | --- |
| 1 | access `.`, metadata `~`, index `[]`, call `()` and `unit from container in point` | left or complete form |
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
| 13 | `eventually ... through ...` | outer |

The forms `take amount from source`, `binding in source : predicate` and the quantifiers contain complete expressions in their delimited positions. The first unnested `from` that can delimit `take` separates amount from source; the unnested colon separates source from predicate. A `from` or `:` inside delimiters or another complete construct belongs to that construct. This contextual delimitation prevents the `from` in component extraction from accidentally consuming the `take` separator. Therefore:

```mud
take n from player in players : player.ready
```

is categorised as `take n from (player in players : player.ready)` without brackets.

`to` and unit conversion with `in` transform the accumulated value on their left. The parser then continues with the result:

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

If another operator follows, it consumes the already converted result. A Pratt parser can implement this rule by ending the postfix parse at the appropriate precedence before accepting subsequent operators.

Unit conversion with `in` consumes the complete unit expression, including products, quotients and parentheses:

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

Chained equality follows the same rule. `<=>` produces comparisons between adjacent pairs. The following do not form chains:

- `!=`
- `is` and `is not`
- `iis` and `iis not`
- membership `has` and `has not`
- `=>`

Different operators are not combined within the same chain without explicit conjunctions.

`iis` checks the exact effective nominal type; `is` includes specialisations. Given:

```mud
alias Identifier := Nat
alias PersonId as Identifier
alias EmployeeId as PersonId
```

an `EmployeeId` satisfies `value is PersonId`, but not `value iis PersonId`. `value iis not PersonId` eliminates only the exact `PersonId` possibility during narrowing. The right operand of `iis` must be a nominal type; products, dictionaries and the singleton identity `Madrid` are invalid.

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
| `~format` | `Text` | point magnitudes | yes |
| `~summary` | `Text` | compatible metadata-bearing elements | yes; default `""` |
| `~description` | `Text` | compatible metadata-bearing elements | yes; default `""` |
| `~deprecated` | `Text [0..1]` | compatible metadata-bearing elements | yes; default `empty` |

The “Owners” column is a semantic availability restriction, not a description of when the result is non-empty. After resolving and classifying the receiver, accessing a property unsupported by its static category is an error. In particular, `thing A` makes `A~for` invalid; an `action` supports `~for` even when it omits the clause, in which case the result is `empty`. The same distinction between an unavailable property and an `empty` value applies to `~on` and `~given`.

The production `metadata-name ::= identifier | "for" | "on" | "given"` merely allows those hard keywords to appear syntactically after `~`. The parser cannot determine whether the receiver has the named entry: it constructs the postfix form, and resolution and typing apply the matrix above.

The table summarises the common and configurable properties that affect the syntax of this chapter. The reflective system also defines the specific properties of each descriptor, such as specialisation relationships, fields, components and structural properties of collections and dictionaries; these are not duplicated here as a second authoritative catalogue.

`Prefix` is a built-in type. Its SI values are written as ordinary identifiers (`kilo`, `milli`, ...), so `~prefixes = [kilo, milli]` requires no special grammar.

General conversions are explicit when the following apply:

```mud
pathText: Text = Alexandria~path to Text
```

Templates can render metadata types directly without establishing general nominal compatibility with `Text`. `~file` is valid in any expression, but triggers a warning when it appears outside text or purely informative public output and its value may affect behaviour:

```mud
look SourceInfo {
    source := "Loaded from {Alexandria~file}"
}

rule Fragile given expected: MudFile {
    Alexandria~file == expected # valid with a warning
}
```

`~name` and any other configurable metadata may be changed by editing and re-elaborating the model, never by a runtime effect. Such an edit changes neither payload, equality, path nor anchor unless the source identifier is changed separately.

## `Text` and operators

`|` concatenates `Text`:

```mud
"Hello, " | name
```

The operators `&`, `^` and `-` are not permitted on `Text`. `xor` is exclusively logical and `^` exclusively set-like. Nominal aliases of `Text` do not undergo implicit concatenation.

Every `Text` literal, whether ordinary or multiline, is a template. `{e}` evaluates `e` and inserts the value's canonical textual representation. Metadata are ordinary expressions:

```mud
"Kingdom: {kingdom}"
"Population: {kingdom.population:6}"
"Rule: {CanRecruit~anchor}"
"Path: {CanRecruit~path}"
"Literal braces: \{example\}"
```

`anchor{...}` is not part of the language. Rendering `Name`, `MudPath`, `Anchor` or `MudFile` in a template does not implicitly convert it to `Text` outside that context.

`Text`, `Char`, `Bool`, basic numbers, `thing` values, `family` members, intervals, collections and magnitudes can be rendered directly. A call to a Boolean rule can also be rendered because it produces `Bool`. Statement and type descriptors are first-class MUD values, but that does not give them an implicit textual representation. Actions, reactive rules, `always` rules, `look`, `message`, tests, types and `family` declarations produce a static error inside `{...}` unless an applicable explicit textual conversion or projection exists.

A `thing`, a nominal alias and a `family` member are represented by their effective `~name`. Their canonical anchor is obtained through `~anchor`; editing `~name` changes neither equality, path nor anchor. A `family` member without an override initially uses its nominal name. An interval uses its normalised canonical form. A collection omits only its outer square brackets and separates elements with `, `; any collection that appears as an element retains its own square brackets:

```mud
"{[1, 2, 3]}"          # 1, 2, 3
"{[[1, 2], [3, 4]]}"   # [1, 2], [3, 4]
```

A numeric placeholder accepts `{e:left}`, `{e::right}` and `{e:left:right}`. Left precision is the minimum number of digits before the point and pads with zeroes without counting the sign or truncating. Right precision determines the following digits, adding zeroes or rounding to nearest with ties to even:

```mud
"{count:4}"     # 0012
"{ratio::2}"    # 12.30
"{ratio:4:2}"   # 0012.30
```

Left-hand precision is supported for all basic numeric types. Right-hand precision is supported for types that can display a fractional part: `Num`, `Rum` and `Money`. A numeric format over any other type is a static error.

A linear magnitude without `in` renders the number followed by the canonical unit projection of its dimension. If that projection is empty, it renders only the number. Unitless nominal factors are not printed, but remain in the type. A point magnitude uses its `~format` when present and otherwise follows the ordinary rule for its underlying magnitude. `{magnitude in unit}` selects an available representation and, for a point, bypasses `~format` to render the complete coordinate. Applying `in` to a unitless base magnitude is invalid. When a unit is present, its abbreviation is used if available; otherwise, the singular name is used for `1` and `-1`, and the plural for all other values.

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

Operands of `through` are action references, not concrete calls. The list, with or without square brackets, represents the same contextual collection. MUD 1.0 supports only `Rand(source)`; it does not yet include syntax for weights or distributions.

## Open line endings and prefixes

`TERMINATOR` comes from `;` or `NEWLINE`. A line break continues the expression when it follows:

1. Within `()` or `[]`.
2. After `,`.
3. Following an incomplete binary operator or assignment.
4. After `:`, `:=`, `->`, `-->`, `.` or `~` when its operand or member is missing.
5. After `using`, `as`, `for`, `on`, `given`, `when`, `if`, `then`, `after`, `otherwise`, `to`, `in`, `through`, `by`, `from`, `over`, `root` or `point` when the production requires content.
6. Within a header which, according to the EBNF, it can’t be over yet.
7. Inside a literal or multiline comment.

A newline after a unit terminates that unit. Line wrapping never determines semantics.

> [!example]
> In `value = first`, the newline terminates the assignment. In `value = first +`, it does not complete the operation because the right-hand operand is missing.

## Contextual distinctions

The parser or elaborator must resolve the following issues without arbitrary choices:

| Area | Distinction |
| --- | --- |
| `in` | domain, related participant, restriction/filter or unit |
| `has` | Boolean membership |
| `call()` | Boolean rule or action |
| `remove x from y` | collection value or dynamic property |
| `UNIT_FORM` | unit enabled or invalid name |
| shared operators | logical, arithmetic, textual or set-theoretic operation |
| literal structural | alias expected |
| `[expression]` | collection unitary or unit interval |
| `1..5 unit` | unit shared by the interval, or the right endpoint of an invalid construction |

If the names, types and constraints of an expression do not determine a single valid interpretation, the programme is invalid and must supply the missing type information. No implicit preference applies. For example, elaboration without sufficient context cannot arbitrarily choose whether `[3]` is a collection or the interval `[3..3]`. The grammar explicitly defines `1..5 m` as the common-unit form `(1..5) m`; the parser does not choose between them.

## Error recovery

An implementation may synchronise after an error at:

- `TERMINATOR`
- `}`
- A clear-cut start to a declaration higher

Recovery only improves diagnostics. It cannot silently change semantics or accept a form that does not conform to the grammar.

## Preserved contextual structures

The parser does not decide on matters that require resolution:

- Whether a dotted path traverses MUD paths, declarations or members.
- Whether a structural literal before a call represents one receiver or several receivers.
- Whether an effect's `postfix-expression` is an action call.
- Which contextual type selects a structural, unit, point or single-scalar literal.

The CST retains the concrete form and the Surface AST retains an unresolved form. Later stages perform the classification.

## Magnitude representation

A magnitude's optional representation uses the general `declared-type` syntax. A later static rule requires the resolved type to be a permitted numeric representation. The grammar does not maintain a duplicate closed list of numeric types.

## Empty bodies omitted

The body of a `thing` is optional. These forms produce the same AST and IR, although the CST retains the notation:

```mud
thing A
thing A {}
thing A;
abstract thing Root
thing B as Root
```

The semicolon introduces no new rule: it is already an explicit `TERMINATOR` and permits, for example, `thing A; thing B; thing C as A`.

## Nominal access to alias members

Calculated components and fields belong to the alias's nominal value type. A bare structure does not acquire members merely by matching its shape:

```mud
(1, 2).derived                    # invalid
((1, 2) to CosoAlias).derived     # valid
```

An expected type may also construct the alias without `to`. The compiler does not search for candidate aliases by member name.

## Reflective metadata

Configurable `~...` elements appear before ordinary content. Fields, components and participants may contain an immediate metadata-only body. Every `for`, `on` and `given` has a required name; a grouped header shares its type and metadata body among its identifiers. File defaults precede `using`. `start with` and the bodies of `when`/`if`/`then`/`after`/`otherwise` are not metadata-bearing owners.
## Membership, restriction and local transformations

Boolean membership uses `container has value` and `container has not value`. `in` is not a Boolean membership operator. `value in Domain` locally restricts or filters the value; `binding in source : predicate` remains a selection.

A collection may be transformed locally with `values [unique]`, `values [ordered]`, `values [ordered by score]` or `values [1..10, unique, ordered]`. This form does not support `mut`. Elaboration normalises domain, `unique`, order and cardinality. `[n]` remains indexing; an exact local cardinality without other modifiers is written `[n..n]`.
