---
id: D-083
title: "Unitless base quantities"
status: current
date: 2026-08-04
supersedes: []
superseded-by: []
questions: []
affects:
  - "magnitudes, types, quantitative conversions, `Text` templates and public boundary"
---
# ADR-083 — Unitless base quantities

- Modified by: [[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]]
- Modifies: [[notes/decisions/ADR-027-departures-from-the-model-by-means-of-look-and-message|D-027]], [[notes/decisions/ADR-028-system-of-quantities-and-units|D-028]], [[notes/decisions/ADR-030-explicit-quantitative-conversion-using-to|D-030]] and [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]].
- Affected documents: magnitudes, types, quantitative conversions, `Text` templates and public boundary.

## Context

The grammar and AST already allowed `root unit` to be omitted from a base magnitude, and `Probability` appeared as a normative example. However, presentation and public-field rules then assumed that every linear magnitude had a root unit or a composition of root units. It remained undefined whether the omission was deliberate, how such a value was constructed, and whether losing unit notation also removed its dimensional identity.

Requiring a root unit would force ceremonial labels for quantities such as probability, opacity or difficulty. Treating all of them as the same dimensionless number, on the other hand, would lose the nominal separation that justifies declaring them as different magnitudes.

## Decision

### Declaration

A base magnitude declares one of these two forms:

1. **With units**: it contains exactly one `root unit` and may contain alternative units.
2. **Unitless**: its body is empty and it cannot contain alternative units.

```mud
magnitude Probability: Num in [0..1] {}

magnitude Length: Num in [0..*] {
    root unit meter {}
}
```

The absence of `root unit` is a complete semantic choice, not an anonymous unit or an incomplete declaration.

### Quantitative identity

A unitless base magnitude retains an independent nominal dimension. It is not identified with its numeric representation or with another unitless magnitude:

```mud
magnitude Probability: Num in [0..1] {}
magnitude Opacity: Num in [0..1] {}
```

`Probability`, `Opacity` and `Num` remain distinct types and are not implicitly converted between one another. The absence of a visible unit does not mean that the factor disappears from dimensional algebra. A multiplication or division retains the magnitude's nominal factor, and normalisation does not confuse it with the dimensional identity element.

The internal representation of a dimension therefore distinguishes its nominal factors from its **unit projection**. Factors whose magnitudes have a root unit contribute to that projection; unitless factors remain in the dimension but produce no unit text. Two dimensions with the same visible projection may still be incompatible.

### Construction and conversion

A bare numeric literal may be elaborated as a unitless magnitude when the expected context determines a single magnitude:

```mud
chance: Probability = 0.75
```

Without that context, the literal retains a basic numeric type. An ordinary numeric expression does not implicitly acquire a magnitude. Explicit materialisation uses `to`:

```mud
chance := ratio to Probability
```

This branch of `to` requires a compatible numeric representation and checks the target domain. It does not authorise converting a different nominal magnitude merely because both are unitless.

A quantity that writes a unit, such as `5 m`, acquires only the factors determined by that unit. The context does not silently add unitless factors. Those factors must come from an already typed operand or a valid explicit conversion.

### Presentation

The canonical form of a unitless base magnitude is the canonical form of its numeric value, without a suffix or trailing space:

```mud
chance: Probability = 0.75
text := "Chance: {chance}"  # Chance: 0.75
```

For a derived magnitude, canonical presentation writes the unit projection of its dimension. Factors from unitless magnitudes retain their static meaning but add no visible label. If the projection is empty, only the number is written.

The presentation operator `in` cannot be applied to a unitless base magnitude. On a derived magnitude it may change the projection expressible through units without removing or replacing its unitless nominal factors.

A public field whose direct value is a unitless magnitude does not receive the warning for omitting `in`: there is no unit choice to make explicit. The ordinary warning rule continues to apply when the magnitude does admit presentation through units.

## Alternatives

### Always require a root unit

Rejected because it would make labels such as `probability` or `scorePoint` mandatory ceremony and make the usual notation of those quantities less natural.

### Treat unit absence as the neutral dimension

Rejected because it would make nominally distinct magnitudes such as `Probability` and `Opacity` dimensionally compatible, and would erase factors when they participate in derived expressions.

### Use aliases for every unitless case

Rejected as an obligation. An alias remains appropriate for wrapping data without quantitative dimensional semantics, but a unitless magnitude retains domains, numeric representation and participation in magnitude algebra.

## Consequences

- The optionality of `root_unit` in `BaseMagnitudeDecl` is semantic and intentional.
- The dimensional resolver must retain nominal factors even when they have no unit form.
- Presentation of a dimension is a projection and does not by itself determine its identity.
- API diagnostics suggest `in` only when a selectable unit exists.
- An implementation cannot invent an observable synthetic unit to complete a unitless magnitude.

## Verification

1. Acceptance of a base magnitude with an empty body and rejection of alternative units without a root.
2. Contextual elaboration of `0.75` as `Probability` and numeric retention without context.
3. Explicit materialisation `ratio to Probability`, including domain checking.
4. Rejection of implicit conversion between two unitless magnitudes.
5. Retention of the unitless nominal factor in derived products and quotients.
6. Rendering without a suffix of a magnitude whose unit projection is empty.
7. Absence of a unit warning on a public field of a unitless magnitude.
8. Rejection of `chance in unit` for a unitless base magnitude.
