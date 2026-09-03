---
id: D-075
title: "Enumerable domains, `all` and derived-value form"
status: current
date: 2026-08-03
supersedes: []
superseded-by: []
questions:
  - "Q-047"
affects:
  - "domains, collections, fields, local bindings, AST and conformance"
---
# ADR-075 — Enumerable domains, `all` and derived-value form

- Extended by: [[ADR-081-filtrado-take-and-indexacion-de-colecciones|D-081]]
- Amended by: [[ADR-088-iteracion-progresiones-firmadas-and-bloques-de-expresion|D-088]]

## Context

Intervals alone cannot constrain enumerated, stepped or nominal values. The collection form of a computed value must also be expressible and inferable in the same way as for a stored value.

## Decision

### Domains

The model distinguishes interval, finite, stepped and named domains, and compositions using union, intersection, difference and symmetric difference.

```mud
colors: Color in [Red, White] [2] = all
numbers: Num in 0..1 by 0.2 [6] = all
```

`by` turns a linear interval into a discrete domain. Its step is static, signed, non-zero, exact and compatible with the type or dimension. A positive step anchors at the lower bound and a negative step at the upper bound, in accordance with D-088. `Num` uses exact rational arithmetic; a `Rum` domain is not enumerable. Cardinality always uses square brackets and is independent of the domain.

### Contextual `all` literal

`all` denotes the canonical complete enumeration of its expected domain and requires context. It is admitted for `Bool`, families, finite aliases, finite and stepped domains, the prefix catalogue and `thing` types. For a `thing` type it gathers compatible active strict descendants; with `Thing` it gathers every active `thing` declaration except the built-in type itself. Each identity appears once.

When enumeration depends on the world, such as `all` over `thing`, it may feed only a computed `:=` value. Cardinality is checked on each evaluation's result.

### Derived values

Computed fields, computed family data, local bindings and public `look` and `message` fields share this form:

```text
name [derived-form] ":=" expression
```

The derived form is a complete `: type` annotation, an `in domain` constraint optionally followed by a collection specification, or a collection without type or domain. Thus both `a: A in [B, C] := expression` and `a in [B, C] := expression` are possible without fabricating a superficial type annotation.

The declared domain in a derived form is coercive: it filters the result with the same semantics as a local domain constraint. Cardinality is checked after that transformation; an unsatisfiable lower bound produces the corresponding obligation or failure and never fabricates members.

A comma-separated list of expressions constructs a derived collection:

```mud
numbers := a * b, d, c / a
```

Its common type and cardinality are inferred. Arity is exact cardinality for ordinary multiplicity collections; under `unique` it is exact only when element distinction can be proved. A collection included as an element is not implicitly flattened.

A selection `value in source : predicate` and `take amount from source` also produce derived collection values. They retain demonstrable source contracts and allow the derived form to declare a more precise domain or cardinality as an independent obligation.

## Conversion diagnostics

When `to` supplies only a type context, tooling suggests moving it to the declaration. If the conversion is constant and safe, it also normalises the value:

```mud
value := 3.7 to Nat
value: Nat := 4
value: Nat = 4
```

Each transformation is an independent suggestion and is offered only when it preserves domains and failure behaviour.

## Verification

1. Finite domains of families, things and quantities.
2. Exact grids and rejection of invalid steps.
3. Static and dynamic `all` with cardinality.
4. Domains and collections in every computed declaration.
5. Inference of computed lists, multiplicity and `unique`.
6. Three outcomes of derived-domain analysis.
7. Staged `to` suggestions.

## Amendment by D-088

The step of a stepped domain no longer has to be positive. It remains static, exact, compatible and non-zero, but may be signed. Positive steps anchor at the lower bound and negative steps at the upper; an open initial bound advances once before the first candidate. The sign may change membership but does not introduce order into the type; `all` uses canonical order. `Rum` remains excluded.

## Current amendment by D-096

Alongside the contextual `all` literal, `all D` materialises the canonical complete enumeration of an explicit enumerable domain. Visible reflective domains admit forms such as `all action`, `all rule`, `all look` and `all A.action(B)`. `all` without an operand retains contextual elaboration.
