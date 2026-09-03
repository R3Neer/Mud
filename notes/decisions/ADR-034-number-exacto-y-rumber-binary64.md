---
id: D-034
title: "`Num` exactly and `Rum` binary64"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-019"
  - "Q-058"
affects:
  - "futuro `06-lexicon.md`, futuro `10-sistema-de-tipos.md`, futuro `17-dominios-e-intervalos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`, futuro `20-cuantificadores-e-iteracion.md`"
---
# ADR-034 — `Num` exactly and `Rum` binary64

- Edit: [[notes/decisions/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notes/decisions/ADR-030-conversion-cuantitativa-explicita|D-030]]
- Related questions: Q-019, Q-058
- Syntax updated by: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]
- Documents affected: future `06-lexicon.md`, future `10-sistema-de-tipos.md`, future `17-dominios-e-intervalos.md`, future `18-magnitudes.md`, future `19-expresiones.md`, future `20-cuantificadores-e-iteracion.md`

## Context

A single type A general number cannot offer the following at the same time:

- Intuitive decimal equality and exact arithmetic.
- Direct floating-point performance for simulation.
- Visibility syntactic rules governing when approximation is accepted.

MUD distinguishes between these needs. `Num` is the type default and exact general; `Rum`, short for *rapid number*, is a deliberate choice to use approximate arithmetic.

## Decisión

### `Num`

`Num` denotes the set of rational numbers:

$$
\llbracket\mathsf{Num}\rrbracket=\mathbb Q
$$

Every value has a canonical representation:

$$
\frac{n}{d}
\qquad
n\in\mathbb Z
\quad
d\in\mathbb N_{>0}
$$

such that:

$$
\gcd(|n|,d)=1
$$

The denominator is always positive, and zero is represented as $0/1$.

The operations are accurate as long as their result be rational. In context `Num`, in particular:

```mud
0.1 + 0.2 == 0.3
1 / 3 * 3 == 1
1 == 1.0
```

are true.

The semantics It does not use binary floating-point numbers. An implementation may start with native integers, but must promote to arbitrary-precision integers before any observable overflow occurs. Resource limits fall within the category of technical faults, not the domain mathematician from `Num`.

### `Rum`

`Rum` represents approximate values in IEEE 754 format `binary64`. A materialisation You can only use the native float if you play the contract set for MUD.

```mud
value: Rum = r0.1
```

The approach is part of the meaning:

```mud
r0.1 + r0.2 == r0.3
```

its accuracy is not guaranteed; the approximation forms part of the contract.

The binary64 evaluation parameters required for bit-for-bit portability will be finalised in Q-058. No implementation may exploit this to use a different width or display extended precision as result observable or replace the semantics as a decimal.

### Literal expressions

A literal `Rum` 'puro' requires the prefix vocabulary `r`:

```mud
r10
r0.1
r1.25
r1_000
r1e-6
```

Negation is an external operator:

```mud
-r10
```

`r-10` is invalid.

The prefix It remains compulsory even if there is a type expected `Rum`:

```mud
value: Rum = 0.1
```

is invalid. It should be written as:

```mud
value: Rum = r0.1
```

Nor are exact and rapid literals mixed together:

```mud
r0.1 + 0.2 # inválido
```

### Quantities based on `Rum`

One magnitude you can select `Rum` as a representation:

```mud
magnitude SimulationDistance: Rum {
    ...
}
```

When a literal takes a unit of a magnitude based on `Rum`, the unit provides a rough context and `r` is optional:

```mud
10 meters
0.5 meters
r10 meters
r0.5 meters
```

It is recommended that you omit `r` in quantities of unit because the magnitude already makes the representation visible. The omission does not turn the value in `Num`.

### Separation and conversions

`Num` y `Rum` They are not implicitly combined in arithmetic or comparison:

```mud
exactValue + rapidValue
exactValue == rapidValue
```

These are static errors.

A must be chosen domain calculation:

```mud
exactValue to Rum + rapidValue
exactValue + rapidValue to Num

exactValue to Rum == rapidValue
exactValue == rapidValue to Num
```

`Num to Rum` is produced by the value `binary64` the nearest value, rounded to the nearest whole number.

`Rum to Num` It produces the exact rational number represented by the stored finite binary pattern. It does not necessarily reconstruct the decimal number that appeared in the programme.

### Policy overall rounding

The policy MUD’s global value is rounded to the nearest whole number, with ties treated as a tie, equivalent to `roundTiesToEven`. This applies to any narrow quantitative conversion that requires rounding. There is no local selection of policy.

### Special values and errors

`Rum` does not contain any observable values `NaN`, `Infinity` nor `-Infinity`. Division by zero, a result infinity and overflow beyond the permitted finite range result in error.

The negative zero of `binary64` is normalised to zero and does not constitute a value a different observable.

### Intervals

A range of `Rum` you can declare a domain:

```mud
value: Rum in [r0..r1]
```

It is uncountable. Therefore, it cannot be a source of `for each` nor any other construction that requires an exhaustive list:

```mud
action InvalidRumIteration for mut total: Rum {
    then for each value in [r0..r1] by r0.1 :
        total += value
}
```

That loop is invalid. The restriction prevents the approximate accumulation from defining membership, traversal order or termination.

## Consequences

- `Rum` is added to the basic numeric types.
- `Num` It remains the default general numerical representation.
- The lexer incorporates its own set of literals prefixed with `r`.
- The AST distinguishes between exact rational literals and literals `binary64`.
- The IR of `Num` It requires a standard, rational form that is independent of the implementation.
- The IR of `Rum` requires a canonical representation of the value `binary64` finite.
- The analysis of enumerability always rejects intervals of `Rum`.
- D-030 the option to select the policy overall rounding.

## Future verification

1. Sign normalisation, greatest common divisor and rational zero.
2. Exact equalities involving decimals and fractions.
3. Promotion before an observable integer overflow.
4. Recognition and rejection of literal forms with `r`.
5. Omission of `r` only under a unit from magnitude `Rum`.
6. Rejection of implicit mixtures between `Num` y `Rum`.
7. Conversions in both directions with known exact results.
8. Close conversion ties were settled as draws.
9. Division by zero error and non-finite results.
10. Normalisation of negative zero.
11. Use of intervals `Rum` such as domain and rejection as a countable source.

