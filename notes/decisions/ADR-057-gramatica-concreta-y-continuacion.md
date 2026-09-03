---
id: D-057
title: "Concrete grammar, precedence and continuation"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-001"
affects:
  - "[[specification/05-texto-fuente]], [[specification/06-lexico]], [[specification/07-gramatica-concreta]], `specification/grammar/`"
---
# ADR-057 — Concrete grammar, precedence and continuation

- Amended by: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]

- Amended by: [[notes/decisions/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]], [[notes/decisions/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]]
- Further amended by: [[notes/decisions/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]]
- Also amended by: [[notes/decisions/ADR-064-orden-por-ruta-estable|D-064]]
- Also amended by: [[notes/decisions/ADR-065-cabecera-using-de-fichero|D-065]]
- Finally amended by: [[notes/decisions/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]
- Amended by: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]
- Amended by: [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].
- Subsequently amended by: [[ADR-074-uniones-nominales-y-estrechamiento|D-074]], [[ADR-075-dominios-enumerables-all-y-valores-derivados|D-075]], [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]], [[ADR-077-destruccion-cardinalidad-y-diagnostico-de-transicion|D-077]] and [[ADR-079-diagnostico-exterior-de-reglas-always|D-079]]
- Closes: [[notes/questions/Q-001-gramatica-y-saltos-de-linea|Q-001]]
- Affected documents: [[specification/05-texto-fuente]], [[specification/06-lexico]], [[specification/07-gramatica-concreta]], `specification/grammar/`

## Context

MUD decisions had already established the principal constructions, but no consolidated grammar existed. This left no single answer to the following questions:

- Which forms belong to the source language.
- Which words are reserved or contextual.
- When a line break terminates a construction.
- How operators, conversions and chains are grouped.
- Which distinctions are resolved by syntax and which by static analysis.

## Decision

The syntax of MUD 1.0 is defined by:

1. [[specification/grammar/mud-lexico.ebnf|The lexical grammar]].
2. [[specification/grammar/mud.ebnf|The concrete grammar]].
3. The contextual constraints and grouping algorithm in [[specification/07-gramatica-concreta]].

The EBNF grammars define the set of syntactic forms. They do not attempt to decide matters that require name or type resolution, including the distinction between:

- A rule call and an action call.
- Boolean membership through `has`/`has not` and the display of units through `in`.
- A recognised unit name and an ordinary identifier.
- The semantic variant of an overloaded operator.
- A singleton collection `[e]` and a unit interval `[e]`.

These distinctions produce distinct nodes during elaboration and must be diagnosed statically when they are ambiguous or invalid.

D-059 adds another contextual distinction: `1..5 m` is elaborated as a numeric interval with a common unit, whereas `1 m..5 km` contains two ordinary magnitude endpoints. A common unit may follow only a form whose finite endpoints are unitless numeric literals.

Headers use distinct productions for `for`, `on` and `given` participants. The EBNF permits `for` to use any `declared-type`, declare an `in` domain, write a collection specification and declare an outer `mut`. `given` also permits domain, cardinality, uniqueness and ordering, but its production excludes both outer `mut` and inner capacity. `on` retains only an individual type reference and its optional inner capacity. Static analysis requires the type in `on` to resolve to a `thing`; the required-name, purity and receiver-place constraints also belong to D-036.

### Terminators

The lexer emits `NEWLINE` and `SEMICOLON`. The parser turns them into `TERMINATOR`, except where a line break occurs:

- Within `()`, `[]` or another delimited construction that remains open.
- After a comma.
- After an operator that requires an operand.
- After an introductory word that requires content.
- Within a literal or multiline comment.

The exhaustive list of introductory words and operators is derived from the grammar itself. Indentation plays no part in this decision.

### Operators

Precedence and chaining are set out in [[specification/07-gramatica-concreta#Precedencia y agrupación]]. `to` and the display form of `in` are postfix operators that transform the entire value accumulated to their left; new operators may then be applied to the converted result. `changes` is a temporal suffix below comparisons and above `and` and `or`, in accordance with D-058.

Permitted chains are elaborated as adjacent pairs:

```mud
a < b < c
```

is equivalent to:

```mud
a < b and b < c
```

The same rule applies to homogeneous chains of equality and `<=>`. The operators `!=`, `is`, `iis`, `has`, `has not` and `=>` are not chainable.

### Error recovery

Concrete error recovery is not part of the accepted language. An implementation may recover at `TERMINATOR`, `}` or the unambiguous beginning of a declaration, but it may not use recovery to accept a form rejected by the grammar.

## Consequences

- Q-001 is no longer an open design question.
- The grammar may evolve through explicit normative changes and conformance tests.
- A parser may use recursive descent, Pratt parsing, PEG or another technique, provided that it accepts and groups exactly the same forms.
- Semantic decisions that remain open do not prevent programs from being recognised or their surface AST from being constructed.

## Verification

1. Every referenced production is defined.
2. Every reachable symbol starts from `mud-file`.
3. Valid and invalid examples for each declaration.
4. Termination and continuation for every prefix class.
5. Grouping at every precedence level.
6. Diagnostics for contextual ambiguities.
7. Syntactic separation between collective `for` roles and individual `on` bindings.
8. Elaboration of intervals with a shared unit rather than local units.
9. Syntactic rejection of inner `mut` capacity in `given`.
10. A domain placed between the type and collection of a `for` role.

## Amendment by D-088

`:` is the required separator in every construction that uses it to introduce a subordinate body; braces do not replace it. `for each` must always write `:` before its effect or block. Selections and quantifiers retain `:` even with `{ ... }`. The grammar adds optional `by` to selections and quantifiers, and generalises `boolean-block` to `expression-block`.
