---
id: D-076
title: "Named units, prefixes and adjacent notation"
status: current
date: 2026-08-03
supersedes: []
superseded-by: []
questions:
  - "Q-054"
affects:
  - "magnitudes, units, lexicon, names, anchors and editing tooling"
---
# ADR-076 — Named units, prefixes and adjacent notation

- Amended by: [[ADR-086-identidad-nominal-exacta-flechas-exteriores-and-algebra-de-diccionarios|D-086]], [[ADR-087-metadatos-reflectivos-descriptores-estables-and-visibilidad-exterior|D-087]] and [[ADR-089-clasificacion-contextual-de-formas-fuente-sin-dependencia-circular-del-scanner|D-089]].
- Closes with D-089: [[notes/questions/Q-054-c-catalogue-and-lexical-resolution-of-units-and-prefixes|Q-054]].

## Decision

Every unit declares a `lowerCamel` identifier that participates in its anchor. D-087 integrates unit configuration into the general metadata system: `~name: Name`, `~plural: Text`, `~abbreviation: Text` and `~prefixes: Prefix [* unique] = empty`. None of these properties uses a special unit syntax production.

```mud
root unit meter {
    ~name = "meter"
    ~plural = "meters"
    ~abbreviation = "m"
    ~prefixes = all
}
```

The declared identifier retains ordinary unit-identifier rules. `~name`, `~plural` and `~abbreviation` share the same criteria when enabled as source forms: they may contain U+0020 spaces and punctuation but must contain at least one alphabetic character; they therefore may not consist entirely of digits or entirely of non-alphabetic characters. A complete form that exactly matches a MUD keyword is not admissible as source spelling, although the same value may remain a presentation.

Uniqueness within a magnitude is checked over identifier, name, plural, abbreviation and every form obtained by applying each permitted prefix. Two distinct units of one magnitude may not generate the same form, directly or through prefixing. A collision between different magnitudes is resolved by expected type or qualification such as `Length.meter`; without sufficient context it is an error.

The contextual identifier form is valid and tooling may suggest an unambiguous shorter abbreviation. An override of `~name` identical to the default receives a removal suggestion. `family` members likewise use standard `~name` metadata without changing their identity.

### Prefixes

`Prefix` is a built-in nominal type. SI catalogue names (`quecto`, `ronto`, ..., `quetta`) are built-in `Prefix` values; they tokenise as ordinary identifiers and resolve at the built-in level, not as new reserved words.

`~prefixes` has type `Prefix [* unique]` and language default `empty`. Omitting it and writing `~prefixes = empty` therefore admit none; `~prefixes = all` uses every built-in `Prefix`; a collection such as `~prefixes = [kilo, milli]` selects exactly that subset. Micro accepts `µ`, `μ` and `u` as unit-form input and normalises to `µ`. Binary prefixes and prefix composition do not exist.

The normative catalogue is:

| Name | Canonical symbol | Factor |
|---|---:|---:|
| `quecto` | `q` | 10^-30 |
| `ronto` | `r` | 10^-27 |
| `yocto` | `y` | 10^-24 |
| `zepto` | `z` | 10^-21 |
| `atto` | `a` | 10^-18 |
| `femto` | `f` | 10^-15 |
| `pico` | `p` | 10^-12 |
| `nano` | `n` | 10^-9 |
| `micro` | `µ` | 10^-6 |
| `milli` | `m` | 10^-3 |
| `centi` | `c` | 10^-2 |
| `deci` | `d` | 10^-1 |
| `deca` | `da` | 10^1 |
| `hecto` | `h` | 10^2 |
| `kilo` | `k` | 10^3 |
| `mega` | `M` | 10^6 |
| `giga` | `G` | 10^9 |
| `tera` | `T` | 10^12 |
| `peta` | `P` | 10^15 |
| `exa` | `E` | 10^18 |
| `zetta` | `Z` | 10^21 |
| `yotta` | `Y` | 10^24 |
| `ronna` | `R` | 10^27 |
| `quetta` | `Q` | 10^30 |

Prefixed units are elaborated structurally and receive no additional anchors. `Prefix` values are not unit declarations.

### Adjacency and formatting

D-089's contextual classifier accepts a unit immediately after a numeric literal without requiring the base scanner to know the catalogue:

```mud
3m
90km/h
r0.1m
```

Canonical form inserts exactly one space after the number and keeps products and quotients compact:

```mud
3 m
90 km/h
r0.1 m
```

The contextual view recognises number and unit as separate tokens even without a space; base tokenisation remains independent of the catalogue. Smart editing and the formatter insert the space; highlighting alone never modifies the file.

Quantities with units may be collection members. Unit declarations as first-class values are outside MUD 1.0.

## Anchors

A unit uses a stable form derived from magnitude and identifier, for example:

```text
unit::physics.Length::meter
```

Changing metadata does not change the anchor; renaming the identifier does and requires explicit migration.

## Verification

1. Optional metadata and local or contextual collisions.
2. Complete SI catalogue and three micro inputs.
3. `empty`, `all` and prefix subsets.
4. Exact adjacent literals, `Rum` and compound expressions.
5. Space normalisation without splitting identifiers containing digits.
6. Stable anchor and no anchors for prefixed units.
