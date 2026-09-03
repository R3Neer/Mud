---
id: D-030
title: "Explicit quantitative conversion using `to`"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-019"
  - "Q-053"
affects:
  - "futuro `10-sistema-de-tipos.md`, futuro `18-magnitudes.md`, futuro `19-expresiones.md`"
---
# ADR-030 — Explicit quantitative conversion using `to`

- Related questions: Q-019, Q-053
- Expanded by: [[notas/decisiones/ADR-032-construccion-contextual-y-casting-nominal|D-032]]
- Amended by: [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|D-034]]
- As further amended by: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Subsequently amended by: [[notas/decisiones/ADR-083-magnitudes-base-sin-unidades|D-083]]
- Documents affected: future `10-sistema-de-tipos.md`, future `18-magnitudes.md`, future `19-expresiones.md`

## Context

`as` reserves the right to declare specialisation in `thing`, so it cannot continue to express conversions. MUD needs to distinguish the change from unit of a quantity obtained by converting its numerical representation.

## Decisión

`to` is the explicit quantitative conversion operator:

```mud
value to Int
value to Nat
value to Money
value to Population
value to Price
```

You can convert:

1. Between compatible numerical representations.
2. One amount to one magnitude dimensionally compatible.
3. A more general quantitative expression of the representation stated by the magnitude of destination.
4. A basic numerical expression to one magnitude a base without units, such as materialisation explicit nominal.

The fourth form, as set out by D-083, check the compatibility of representation and the domain of destination. It does not allow conversion between two different nominal quantities simply because neither has unit.

```mud
averagePopulation: Population :=
    population / regions to Population
```

In his branch quantitative, `to` It is not an open casting call. D-032 It adds the nominal casting of structurally compatible aliases separately. Conversions such as the following continue to be rejected:

```mud
army to Kingdom
place to House
text to Num
distance to Time
Bool to Nat
```

### Rounding and validation

When the target representation cannot retain a fractional part, `to` apply the only one policy MUD rounding rule. The syntax does not allow you to select a policy local:

```mud
value to Int
```

The policy global, set by D-034, is rounding to the nearest whole number, with ties treated as even (`roundTiesToEven`).

After rounding, the result must belong to the domain of destination. `to` It does not automatically saturate or correct a value outside domain.

`Num to Rum` round up to value `binary64` nearest. `Rum to Num` accurately reproduces the rationale represented by the value stored binary. Both forms are explicit.

### Difference from `in`

`in` change the unit which is used to express a quantity, without changing its magnitude:

```mud
distance in kilometers
speed in km/h
```

It applies to both linear quantities and quantities of point. In a magnitude from point transforms the full coordinate and prevents its `format`: yes `time` is 1.30 pm, `time in hour` expresses `13.5 h`, not the time component `13`.

The presentation The selected data can be observed by subsequently converting it to a numerical representation and interpolating it in `Text` or publish it in a field from `look` o `message`:

```mud
speed in km/h to Rum
"{distance in kilometer}"
```

If no subsequent operation observes the presentation, the compiler may suggest removing a `in` redundant. Extracting part of a point use the alternative form `picosecond from second in time`, set by D-061.

`to` changes the numerical representation or renders a magnitude quantitatively compatible:

```mud
average to Int
averagePopulation to Population
amount to Money
```

## Consequences

- The AST distinguishes `UnitPresentationExpr` from `QuantitativeConversionExpr`.
- The type system must verify compatibility numerical and dimensional checks before acceptance `to`.
- A statically known invalid conversion is detected at compile-time; a violation dependent on the value must have a result explicit dynamic, yet to be integrated with the semantics overview of faults.
- `as` stops taking part in conversions altogether.
- D-032 adds the branch nominal, without altering these quantitative rules.

## Future verification

1. Extensions and contractions between numerical representations.
2. Conversion to a magnitude compatible.
3. Rejection of incompatible dimensions.
4. Rejection of values outside the domain after rounding.
5. A noticeable difference between `quantity in unit` y `quantity to type`.
6. Presentation of a magnitude from point in a unit without applying its `format`.
7. Materialisation of a magnitude unitless basis and rejection between different nominal quantities.

