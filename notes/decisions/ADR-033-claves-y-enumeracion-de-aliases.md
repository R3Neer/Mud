---
id: D-033
title: "Composite keys and alias enumeration"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-056"
affects:
  - "futuro `12-aliases.md`, futuro `16-diccionarios.md`, futuro `20-cuantificadores-e-iteracion.md`, futuro `37-finitud-y-enumerabilidad.md`"
---
# ADR-033 — Composite keys and alias enumeration

- Related question: Q-056
- Syntax updated by: [[ADR-088-iteracion-progresiones-y-bloques-de-expresion|D-088]]
- Documents affected: future `12-aliases.md`, future `16-diccionarios.md`, future `20-cuantificadores-e-iteracion.md`, future `37-finitud-y-enumerabilidad.md`

## Context

Structural aliases must be able to act as ordinary composite values: dictionary keys, iteration sources and quantification domains. For two implementations to be equivalent, the finiteness and the order of enumeration cannot be implied.

## Decisión

### Compound keys

A alias it could be the type unique key in a dictionary:

```mud
alias Square {
    file: File
    rank: Rank
}

board: Square -> Piece [0..32 ordered]
```

Ordinary access constructs a single contextual key:

```mud
board[(E, Four)]
```

The form:

```mud
board[E, Four]
```

It is syntactic sugar for the same operation. It does not turn the dictionary into one with multiple keys, nor does it modify the identity nominal value of `Square`.

### Finitud

A structural alias is finite and countable if all its components have finite and countable domains:

```mud
alias Coordinate {
    horizontal: Int in 0..7
    vertical: Int in 0..7
}
```

This alias has $8\cdot 8=64$ values and can be used as a source:

```mud
action VisitCoordinates for mut visits: Nat {
    then for each coordinate in Coordinate :
        visits += 1
}

rule HasLeftEdge {
    exists destination in Coordinate :
        destination.horizontal == 0
}
```

If any component is missing domain finite and countable, the alias it remains a type valid, but its domain It cannot be fully explored or quantified in its entirety.

### Order of numbering

The listing of a structural alias is the lexicographic Cartesian product of the enumerations of its components, in the order of declaration. To `Coordinate`:

```text
(0, 0)
(0, 1)
…
(0, 7)
(1, 0)
…
(7, 7)
```

The enumerability requires that each component provides not only a finite set, but a finite canonical enumeration. The formal normalisation of this property belongs to Q-056.

## Consequences

- Multi-key sugar is generated before resolving access to the dictionary.
- The compiler can calculate the cardinality of a finished product.
- Quantifiers and `for each` share the same canonical numbering of the alias.
- The order of the components affects both structural nominality and comparison and enumeration.

## Future verification

1. Ordinary and ‘sweetened’ access to a password alias.
2. Aversion to sugar when the type The key does not accept that structural form.
3. Cardinality of finished products.
4. Lexicographical order of listing.
5. Rejection of exhaustive iteration when a component is not finite or enumerable.

