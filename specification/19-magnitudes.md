---
title: Magnitudes units and points
tags:
  - mud/specification
status: current
normative: true
depends-on:
  - "[[07-lexicon]]"
  - "[[10-names-and-anchors]]"
  - "[[11-type-system]]"
  - "[[18-domains-and-intervals]]"
  - "[[21-expressions]]"
questions:
  - Q-033
  - Q-070
decisions:
  - D-028
  - D-029
  - D-030
  - D-034
  - D-040
  - D-059
  - D-061
  - D-062
  - D-076
  - D-082
  - D-083
  - D-087
  - D-089
  - D-129
  - D-157
  - D-158
  - D-160
  - D-161
  - D-163
---

# 19. Magnitudes, units and points

## Nominal quantitative declarations

A magnitude gives numeric coordinates an independent nominal quantitative
contract. Its representation, dimension, domain, units and linear/point category
are separate information. Unit text cannot remove or invent dimensional factors.

```mud
magnitude Length {
    root unit meter { ~abbreviation = "m"; ~prefixes = all }
}
magnitude Time { root unit second { ~abbreviation = "s" } }
magnitude Speed := Length / Time
distance: Length = 3 m
```

Only Nat, Int, Num, Rum and Money can represent magnitudes; Num is the default.
Magnitudes are not arbitrary payload aliases, generic constructors or activatable
identities. They have nominal declarations/metadata and fixed dimensions.

## Bases, derived factors and representations

> [!rule] MUD-QUANT-001 — Independent bases and checked composition
> A base magnitude contributes its original nominal factor even without units.
> A derived magnitude composes factors by its declared product/quotient, while
> checking each original numeric operation's representation signature before
> dimensional cancellation. Equal factors do not erase nominal identity or
> create an implicit conversion.

A base with units declares exactly one root unit and may declare positive
alternative equivalences. A unitless base has an empty unit body and no alternative
units. For example Probability and Opacity, both Num in [0..1], remain distinct
nominal dimensions. A unitless numeric literal can construct a base with one
unique expected context; a typed numeric expression requires admitted explicit
`to`. A quantity with units supplies only the factors those units denote, never
additional hidden unitless factors from context.

Derived `:=` is dimensional definition, not specialization or conversion.
A derived magnitude cannot declare root unit; its canonical unit projection is
the product/quotient of underlying root projections. It may name dimensionally
valid alternative units. Products/quotients of admitted units require no separate
declaration for each combination.

MUD-TYPE-037 in [[11-type-system#Dimensional normalization]] defines the finite
anchor-to-integer-exponent map, sorted nonzero factors, acyclic topological
unit equivalences and exact canonical scales. A base's scale is one, prefix
factors are powers of ten and compound scales multiply/divide. Unit scale
normalization is distinct from coordinate computation rounding.

Select representation at each original operation. Nat/Int/Num products follow
exact widening, division produces Num, and exact remainder follows MUD-TYPE-039.
Money signatures and hundredth ties-to-even rounding are
[[21-expressions#4. Numeric, dimensional and Boolean operators]]. Money*Money is
unsupported even when surrounding factors later cancel. Rum-only products/quotients
produce Rum with MUD-TYPE-038's binary64 sites; implicit exact/Rum and Money/Rum
mixing remains invalid. An explicit derived representation needs the existing
representability evidence and adds no hidden rounding/conversion signature.

Header domains use bare canonical coordinate bounds, after the optional numeric
representation. They contain no explicit unit suffix. Ordinary interval
expressions retain their local/shared-unit forms under [[18-domains-and-intervals]].
Canonical-coordinate domain checking follows supported numeric construction;
unit presentation does not change which domain is checked.

## Units, forms and source classification

> [!rule] MUD-QUANT-002 — Named unit catalogue
> Every root/alternative unit has a lowerCamel identifier and stable subordinate
> anchor. Its equivalence must be positive, compatible with the magnitude and
> acyclic to the canonical unit. Source forms and enabled prefixes must not
> collide between distinct units of the same magnitude.

`~name`, `~plural`, `~abbreviation` and `~prefixes` use ordinary read-only
descriptor metadata. Prefixes default to empty. Identifier/name/plural/abbreviation
and enabled prefixed forms constitute the admitted source catalogue. Enabled
presentation forms may contain spaces/punctuation but must contain an alphabetic
character; an exact keyword cannot be a source unit form. Cross-magnitude
collisions require expected context or qualification, such as Length.meter;
without a unique resolution they are errors.

Unit anchors use `unit::<qualified-magnitude>::<identifier>`. Changing metadata
does not change identity; renaming an identifier does. Prefixed forms are
structurally elaborated and create no extra unit anchors. Unit descriptors can
be reflected where available, but first-class unit values are outside MUD 1.0.

The base scanner does not consult the catalogue. Contextual source classification
resolves unit/point forms after ordinary lexing. Adjacent `3m`, `90km/h` and
`r0.1m` are admitted with sufficient context; canonical formatting writes
`3 m`, `90 km/h`, `r0.1 m`. The formatter inserts one number/unit space and
keeps compound products/quotients compact. A quantity can be a collection member.

## Prefix family

Prefix is the fixed SI Family. Its builtin names resolve as ordinary identifiers,
not reserved words. `~prefixes = all` enables the complete catalogue; an explicit
unique collection selects a subset. There are no binary prefixes or composed
prefixes. Micro accepts µ, μ or u input, normalized to µ.

| Name | Symbol | Exact factor |
| --- | --- | --- |
| quecto | q | 10^-30 |
| ronto | r | 10^-27 |
| yocto | y | 10^-24 |
| zepto | z | 10^-21 |
| atto | a | 10^-18 |
| femto | f | 10^-15 |
| pico | p | 10^-12 |
| nano | n | 10^-9 |
| micro | µ | 10^-6 |
| milli | m | 10^-3 |
| centi | c | 10^-2 |
| deci | d | 10^-1 |
| deca | da | 10^1 |
| hecto | h | 10^2 |
| kilo | k | 10^3 |
| mega | M | 10^6 |
| giga | G | 10^9 |
| tera | T | 10^12 |
| peta | P | 10^15 |
| exa | E | 10^18 |
| zetta | Z | 10^21 |
| yotta | Y | 10^24 |
| ronna | R | 10^27 |
| quetta | Q | 10^30 |

## Points, differences and domains

A point magnitude `P point over M` describes coordinates on linear M.
It inherits M's numeric representation and units, declares no root/alternative
units of its own, and has independent nominal point identity. Its optional
domain is either ordinary linear or a finite [a..b) cycle with positive period.

| Admitted compatible operation | Result |
| --- | --- |
| P - P | Underlying linear difference M. |
| P + M; M + P | P. |
| P - M | P. |
| P + P | Unsupported. |

Numeric representation checks and source rounding sites remain required for
each operation. For a cycle of period p=b-a, the mathematical coordinate
normalization lies in [a,b), relative to a, using Euclidean remainder. This
differs from truncating numeric %. Cyclic normalization does not redefine
ordinary intervals or authorize an infinite traversal. Source coordinate
literals must meet the domain before cycle correction.

> [!rule] MUD-QUANT-003 — Contextual point construction
> A point literal requires one unique expected point type before format
> interpretation. With ~format, it must match the exact canonical rendering
> and the format must have a statically unique inverse. Without ~format use
> a compatible inherited unit, or the unitless coordinate rule MUD-TYPE-041.

Canonical formatted literals retain every fixed fragment, separator, component
order and numeric width/precision. Reconstruct and render again, requiring
exact source equality. Omitted lower precision is zero, not hidden information
or implicit rounding. A noninvertible format is invalid. Two point types may
have the same visible spelling when expected context selects one.

Without format, a point over a unitless magnitude admits a contextual numeric
literal, such as `position: Cursor = 0.5`, and typed numbers require explicit
`to Cursor`. Conversion checks representation/domain without silently repairing
invalid coordinates. No synthetic unit, unit presentation, unit extraction or
conversion from an unrelated nominal magnitude is introduced. Rum's r prefix
remains required without an inherited unit context.

## Presentation, extraction and public fields

`quantity in unit` selects presentation of its complete canonical coordinate;
it does not change magnitude/dimension. On points it bypasses ~format:
13:30 in hour presents 13.5 h, not the hour component 13. Unitless factors remain
in the type and add no unit text; a completely unitless projection prints only
the number. A unitless base has no `in unit` presentation.

`smallUnit from containingUnit in point` extracts a Nat component by Euclidean
remainder relative to the canonical origin. Both units belong to the underlying
magnitude and smallUnit cannot exceed containingUnit. Partial final components
are possible where the containment ratio is not integral. Extraction is independent
of units displayed by ~format. The short `smallUnit from containingUnit` exists
only inside a point-format hole. Successive `{hour:2}:{minute:2}:{second:2}`
holes use the complete initial coordinate then components within preceding units.

Numeric Text holes `{e:left}`, `{e::right}`, `{e:left:right}` use natural decimal
widths. Left pads to a minimum without removing digits or counting the sign;
right fixes fractional digits with ties-to-even text rounding, available for
Num/Rum/Money. Zero right precision removes the point. Formatting changes Text,
never the numeric value. Point formats reuse this syntax with the additional
invertibility requirement.

A direct public magnitude field can explicitly select units with in. Omitting
it is legal but warns when units are selectable; no warning is needed for a
unitless magnitude. A direct point field publishes its numeric coordinate;
publishing ~format requires a Text field such as `timeText := "{clock.time}"`.
Recursive foreign serialization of contained magnitudes remains
[[../notes/questions/Q-070-foreign-value-conversion-lifetime-and-errors|Q-070]] and is
not an implied host protocol here.

## Counterexamples and scope boundaries

90 km/h normalizes to 25 m/s under exact Num coordinates. Different independent
unitless Probability/Opacity factors do not become interchangeable. Money
products cannot be rescued by dimensional cancellation. Mixed Rum/exact derived
operands require admitted explicit conversion, not merely a result annotation.
An unformatted unitless Cursor is valid; a Cursor literal 2 outside [0..1) cycle
is invalid. `7:05:00` is invalid where canonical format requires `07:05:00`.

Irregular calendar APIs, localization and related standard-library choices
remain [[../notes/questions/Q-033-c-calendars-and-localisation|Q-033]], outside this
numeric magnitude core. No Gregorian calendar, timezone or host encoding is
selected by a point's mathematical coordinate contract.

[[types/typing-cases.yaml]], [[types/test_dimension_witnesses.py]] and
[[types/test_rum_witnesses.py]] cover supplied factor/scale normalization,
representation signature boundaries, binary64 sites and unitless coordinates.
Lexical/CST/AST coverage retains contextual unit and point forms. Finite
certificates are not a compiler, general format-inversion solver or runtime.
