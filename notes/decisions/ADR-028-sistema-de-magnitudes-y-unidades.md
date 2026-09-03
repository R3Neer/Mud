---
id: D-028
title: "System of quantities and units"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-019"
  - "Q-034"
  - "Q-054"
  - "Q-055"
affects:
  - "futuro `10-sistema-de-tipos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`"
---
# ADR-028 — System of quantities and units

- Amended by: [[notes/decisions/ADR-034-number-exacto-y-rumber-binary64|D-034]], [[notes/decisions/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] y [[notes/decisions/ADR-083-magnitudes-base-sin-unidades|D-083]]
- Expanded by: [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]]
- Related questions: Q-019, Q-034, Q-054, [[notes/questions/Q-055-literales-de-magnitudes-de-punto|Q-055]]
- Documents affected: future `10-sistema-de-tipos.md`, future `18-magnitudes.md`, future `19-expresiones.md`

## Context

The original reference combined numerical representation, dimension, unit and lexical syntax. It also dealt with `Percentage` such as type In its basic form, it used suffixes for certain types and required users to manually declare compound units that could be deduced from the dimensions.

MUD needs to distinguish between:

- How a number is represented.
- What physical or conceptual quantity does it represent?
- What unit It is written.
- What dimension results from combining quantities?

## Decisión

### Basic types

The basic non-numeric data types are:

```mud
Text
Bool
Char
```

The basic numeric types are:

```mud
Nat
Int
Num
Rum
Money
```

The five numerical types are representations, not magnitudes. They can be used directly or serve as the numerical representation of a magnitude:

```mud
attempts: Nat
factor: Num

magnitude Population: Nat {
    ...
}
```

`Percentage` is no longer a type basic. A percentage concept must be modelled using the system of quantities and domains. D-034 fixed `Num` as an exact rational number, and adds `Rum` as an approximate representation `binary64`.

Numeric literals do not have suffixes of type. There aren't any `30N`, `30I`, `30M` or equivalent forms. The type context determines the exact representation. Literals `Rum` Cigars form a distinct family with prefix `r`, according to D-034:

```mud
balance: Money = 30
population: Population = 30 people
rapid: Rum = r0.1
```

### Non-derived quantities

One magnitude A non-derivative represents an independent quantity:

```mud
magnitude Length {
    ...
}
```

If you omit the numerical representation, use `Num`. You can declare it via `:`:

```mud
magnitude Population: Nat {
    ...
}

magnitude Temperature: Int {
    ...
}
```

You can restrict your domain by means of `in`, situated after the optional numerical representation and before the block:

```mud
magnitude Probability: Num in [0..1] {
    ...
}

magnitude Population: Nat in [*] {
    ...
}
```

Its header therefore follows this order:

```text
magnitude nombre [: representación-numérica] [in intervalo] bloque
```

The endpoints of the header interval are plain numbers in the canonical representation of the magnitude. When there is a unit root, are performed there; the unit It is not written within the interval. This restriction on declaration does not prevent ordinary interval expressions from using local units or a unit common in accordance with D-059.

One magnitude a non-derivative function that declares units contains exactly one `root unit`. D-076 requires an identifier `lowerCamel` in its header:

```mud
magnitude Length {
    root unit meter {
        ~name = "meter"
        ~plural = "meters"
        ~abbreviation = "m"
    }
}
```

The identifier determines `~identifier` and the anchor. `~name`, `~plural`, `~abbreviation` y `~prefixes` are configurable metadata in accordance with D-076 y D-087.

One unit An alternative is stated by means of a positive equivalence:

```mud
unit minute := 60 seconds {
    ~name = "minute"
    ~plural = "minutes"
    ~abbreviation = "min"
}
```

Any equivalence of unit must:

1. To be strictly positive.
2. To belong to the same magnitude.
3. To be reduced to the unit root.
4. Do not participate in cycles.

`~prefixes` has type `Prefix [* unique]` y default value `empty`. `~prefixes = all` select the domain fully integrated and `~prefixes = [p1, p2, ...]` one collection explicit. There is no special sub-grammar of properties of unit.

### Derived quantities

`:=` define a relation dimensional, not inheritance or conversion:

```mud
magnitude Speed :=
    Length / Time

magnitude Area :=
    Length * Length
```

One magnitude A derived class cannot declare `root unit`. His unit The canonical form is obtained by combining the units root of the component quantities. The expressions for unit that are dimensionally compatible are automatically valid:

```mud
10 m/s
90 km/h
3 Mm/ps
5 cm/min
```

The prefixes enabled in the component units remain available in these expressions. It is not necessary to specify each product or quotient by name.

One magnitude A derived quantity may be expressed in terms of a nominal quantity for an equivalence that is already dimensionally valid:

```mud
magnitude Speed :=
    Length / Time
{
    unit fastie := 1 m/s {
        ~name = "fastie"
        ~plural = "fasties"
        ~abbreviation = "fst"
    }
}
```

That unit does not become root nor does it restrict other compatible forms of expression.

### Inference representative

One magnitude derived without type Explicitly choose the least expanded representation capable of representing the operation. For the ordinary hierarchy:

$$
\mathsf{Nat}
\prec
\mathsf{Int}
\prec
\mathsf{Num}
$$

The following rules are initially applied:

| Representation operations | Result |
| --- | --- |
| `Nat * Nat` | `Nat` |
| `Nat * Int` | `Int` |
| `Int * Int` | `Int` |
| Any transaction involving `Num` | `Num` |
| Any division | `Num` |

An explicit representation can be declared as follows:

```mud
magnitude DiscreteArea: Nat :=
    Width * Height
```

The table describes exact operations. Operations in which all operands are `Rum` produce `Rum`; `Rum` is not implicitly conflated with exact representations. The inference of derived quantities that combine components `Rum` will be completed in Q-058.

Explicit annotation does not introduce rounding. The programme must satisfy the corresponding static representability rules. The rules for `Money` and the complete matrix of operators remains open in Q-019.

## Consequences

- The AST will separate `NumericType`, `MagnitudeDecl`, `UnitDecl` and dimensional expressions.
- The static analysis You will need to normalise dimensions and scale factors.
- Derived units are structural expressions, not a nominal list.
- The lexer and the resolver must distinguish between identifiers, names, plurals, abbreviations and prefixes within the context of magnitude.
- `r` is a prefix from literal approximate.

## Future verification

1. Magnitude non-derivative with a predetermined, explicit representation and domain optional in the canonical order.
2. Zero rejection, negative signs and cycles in equivalences.
3. Standardisation of `km/h` to the unit canonical of `Speed`.
4. Inference of each ordinary combination of numeric types.
5. Rejection of `root unit` in a magnitude derived.
6. Equivalence between a unit Derived noun and its structural form.
7. None prefix by default or `empty`, full catalogue available via `all` and subset using a collection explicit.

