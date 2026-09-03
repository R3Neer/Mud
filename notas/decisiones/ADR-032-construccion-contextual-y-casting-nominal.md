---
id: D-032
title: "Contextual construction and nominal casting of aliases"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-056"
affects:
  - "futuro `10-sistema-de-tipos.md`, futuro `12-aliases.md`, futuro `19-expresiones.md`"
---
# ADR-032 — Contextual construction and nominal casting of aliases

- Amended by: [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]]
- Amended by: [[notas/decisiones/ADR-069-literales-char-con-comillas-dobles|D-069]]

- Read more: [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]]
- Related question: Q-056
- Documents affected: future `10-sistema-de-tipos.md`, future `12-aliases.md`, future `19-expresiones.md`

## Context

The nominal nature of aliases requires us to distinguish between:

- The direct construction of a value under a type expected.
- The conversion of a value who already has another one type.
- Comparing literals that have not yet been typed.

Without this separation, writing ordinary values would be unnecessarily cumbersome, or the nominal guarantee would be lost.

## Decisión

### Two families from `to`

`to` It comprises two families that can be distinguished on the basis of their structure:

1. Quantitative conversion, defined as D-030.
2. Nominal casting between one alias and a structurally compatible representation.

```mud
rawText to PlayerName
playerName to Text
cityName to PlayerName
coordinate to Square
```

A list of cast members:

- Keep the value underlying.
- Change the identity nominal value of the type.
- Demand compatibility structural.
- Validate the destination’s restrictions and domains.
- It does not round off or transform the content.

The statement by D-030 that `to` This is not an open casting call – it is an ongoing process current for non-quantitative values that do not feature in this relation nominal. `to` does not allow arbitrary conversions between `thing`, text and numbers or types that are structurally incompatible.

### Compatibility structural

Two representations are compatible when they have the same normalised form. For structural aliases, the following must match, at a minimum:

1. Number of components.
2. Name of each component.
3. Order of the components.
4. Type underlying component of each component.
5. Cardinalities.
6. Structure of collections and dictionaries.
7. Structural modifiers such as `ordered` y `unique`.

Domains and component defaults do not alter this minimal form: they are validated or applied when the target is constructed. The complete inductive definition of normalisation and its possible cycles are set out in Q-056.

### Contextual quotes

A literal The structural form, in and of itself, does not possess identity from alias:

```mud
(E, Four)
```

The type As expected, you can build the value nominal:

```mud
square: Square = (E, Four)
game.Move((E, Four)) # si el `given` esperado es Square
board[E, Four]       # si la clave esperada es Square
```

The same applies to basic literals:

```mud
playerName: PlayerName = "Ada"
```

This contextual construction does not require `to`. By contrast, a type-checked expression retains its type and requires explicit conversion:

```mud
rawName: Text = "Ada"
playerName: PlayerName =
    rawName to PlayerName
```

### Positional and named structural literals

The positional form follows the order of declaration:

```mud
(E, Four)
```

The full form can list all the components in the order of declaration:

```mud
(
    file = E,
    rank = Four
)
```

The positional form must provide all components, even if some are predefined. There is no such thing as a partial positional construction:

```mud
pagination: Pagination = (2, 30) # válido: forma posicional completa
pagination: Pagination = (2)     # inválido: falta size y no está nombrado
```

The named form may omit components. Each omitted component takes its explicit default value or, if it has none, the default value of its type cash in accordance with D-017:

```mud
pagination: Pagination = (size = 30) # page conserva 1
pagination: Pagination = (page = 2)  # size conserva 20
```

Therefore, if not all components are listed, all those that are listed must be named. Positions and names must not be mixed. The components listed retain the relative order of declaration, even if earlier or intermediate components are omitted. Duplicates, unknown components or the reordering of existing components are static errors.

Full construction renders all components before producing the value nominal. The defaults do not alter their equality, lexicographical order or standardised form.

### Context for comparison

Two bare structural literals cannot be compared because neither provides a type expected:

```mud
(E, Four) == (E, Four) # inválido
```

If an operand has already been evaluated as a alias and the other is a literal a syntactically compatible construction that can still be inferred from context, the type The nominal value is passed on as an expectation to the literal:

```mud
(E, Four) to Square == (E, Four)
(E, Four) == (E, Four) to Square
```

Spread is bidirectional with respect to the left or right position and applies to both basic and structural literals. It only constructs literals; it does not silently convert variables, accesses, calls or other expressions that already have type.

For example, if `playerName` has type `PlayerName`, the literal from:

```mud
playerName == "Ada"
```

can be constructed contextually as `PlayerName`. On the other hand, if `rawText` is a variable of type `Text`, `playerName == rawText` remains invalid without `to`.

The text of `Bool` and the basic numeric types have type sufficient contextual basis to allow for a direct comparison. A standard form in double quotation marks is preferred `Text`, but it can be prepared as `Char` when the context requires precisely a scalar in accordance with D-069.

After evaluating the expressions, both operands must be exactly the same type nominal. Compare different aliases or a alias where the expression is already typed as its underlying representation is a error:

```mud
square == coordinate
playerName == rawText
```

One of the operands must be explicitly converted:

```mud
square == coordinate to Square
playerName to Text == rawText
```

### Equality and order

Two values are equal if they have the same nominal alias and the same content.

Simple aliases inherit their order from their type underlying, but they are only compared with values from the same alias. A structural alias It supports order comparisons if all its components are ordered; the order is lexicographical according to the declaration.

Equality `==` and inequality `!=` are available even if the representation is not in any particular order. `<`, `<=`, `>` y `>=` require a structured presentation.

## Consequences

- The typing of literals is controlled by the type expected.
- The elaboration it must distinguish between literals without type setting of pre-typed expressions.
- The elaboration distinguishes the contextual construction guided by the type expected from a nominal conversion `to` explicit.
- The comparison raises expectations in both directions without introducing any implicit coercion.
- The result The work must preserve, or ensure that the contextual structure and the nominal alias even when its representation coincides with another type; its mechanical coding has not yet been finalised.
- D-030 goes on to describe the branch quantitative analysis of `to`; this ADR describes the branch nominal.

## Future verification

1. Simple contextual and structural construction.
2. Casting in both directions between alias and representation.
3. Casting between compatible aliases.
4. Rejection on the grounds of incompatibility or domain of destination.
5. Full positional and nominal forms.
6. A partial form of the name, with the omission of preceding and intermediate components.
7. Partial positional rejection, mixing of positions and names, reordering, duplication and an extra component.
8. Comparison with propagation from both sides.
9. Rejection of two exposed structural members.
10. Rejection of distinct nominal aliases without `to`.
11. Equality and a lexical order independent of the default settings.

## Extension by D-084

The components and fields derived from a alias are only available after a literal structural change has led to that type nominal by context or `to`. `(1, 2).derived` is invalid; `((1, 2) to CosoAlias).derived` is valid. The resolution does not search for candidate aliases by the name of the member.

