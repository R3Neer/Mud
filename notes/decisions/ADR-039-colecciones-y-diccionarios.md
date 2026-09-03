---
id: D-039
title: "Collections and dictionaries"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-006"
  - "Q-047"
affects:
  - "futuro `15-colecciones.md`, futuro `16-diccionarios.md`, futuro `20-cuantificadores-e-iteracion.md`"
---
# ADR-039 — Collections and dictionaries

- Amended by: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Amended by: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]] y [[ADR-098-rutas-asignables-y-write-back-de-aliases|D-098]]
- Amended by: [[notes/decisions/ADR-064-orden-por-ruta-estable|D-064]]
- Amended by: [[ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]] y [[ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]]
- Read more: D-019, D-026, D-033
- Related questions: Q-006, Q-047
- Documents affected: future `15-colecciones.md`, future `16-diccionarios.md`, future `20-cuantificadores-e-iteracion.md`
- Amended by: [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].

## Decisión

### Collections

The cardinality uses whole-note intervals:

```mud
T[n]
T[min..max]
T[min..*]
T[*]
```

To omit it is tantamount to `[1]`; `[n]` is equivalent to `[n..n]`; `[*]` use the semantics effective limit of D-029 and is usually equivalent to `[0..*]`.

`empty` means 'absence of' `null`.

Collections allow duplicates, except `unique`. `ordered` retains an observable order and `ordered by ruta` declare a key semantics stable in accordance with D-064.

Add to a collection `unique` a value if it is already present, it is a no-op. The operation is idempotent: one or more additions of the same value they produce a single presence, even when they result from compatible concurrent effects.

When a literal intended for a collection `unique` contains duplicates whose equality can be proven statically, the compiler normalises them to a single occurrence and issues a non-blocking warning. If the collection standardised fails to comply with its cardinality, the programme also includes a error static of cardinality and the following is not valid:

```mud
members: Person [* unique] = [Alice, Alice]  # aviso; equivale a [Alice]
pair: Person [2 unique] = [Alice, Alice]     # error; tras normalizar solo queda un valor
```

Initial sources of information:

- When the type The whole possesses an intrinsic semantic order, `ordered` Use that order. This includes the orders defined for basic items, `Char`, `ordered family` and aliases where applicable.
- When the type The complete version does not have a common overall comparator, `ordered` use the provenance a stable record of occurrences; collections of `thing` are the usual cases.
- `Char` use value ascending Unicode scale and does not support `ordered by`.
- You don’t invent a comparator between branches of a union by means of text position, tags, proper nouns or identity implementation.

In a collection values with associated fields, components or data, `ordered by ruta` may replace the standard sort order with a key derived from unique accesses from each member. The key must have full semantic order and the entire path must be transitively stable. A `thing` It is not a sortable primary key. Keys that are equal retain the relative order of provenance stable. In a purely sequential narrative, this provenance corresponds to the order of insertion. This order of collection it does not alter the intrinsic comparison between its members.

When the type o `ordered by ruta` determines the main order, a literal When written in a different order, it is normalised and produces a non-blocking warning. Among identical keys, the provenance stable; in a literal written sequentially, the order in which it is written conveys that provenance. This notice does not apply to a collection `thing [ordered]` whose usual order stems entirely from his own ideas.

### Set Algebra

Set operators also apply to compatible sets:

| Operation | Form |
| --- | --- |
| Unión | `A | B` |
| Intersection | `A & B` |
| Difference | `A -- B` |
| Symmetric difference of sets `unique` | `A ^ B` |

Two operands are compatible when they have the same type number of member. The refinements of domain and the modifiers for collection They may differ and are combined in accordance with the following rules; no implicit conversions are performed between different types.

Be $\mu_C(v)\in\mathbb N$ the multiplicity of the value $v$ in the collection $C$. Operations are defined point a point:

$$
\begin{aligned}
\mu_{A\mid B}(v) &= \max(\mu_A(v),\mu_B(v)),\\
\mu_{A\mathbin{\&}B}(v) &= \min(\mu_A(v),\mu_B(v)),\\
\mu_{A\mathbin{--}B}(v) &= \max(\mu_A(v)-\mu_B(v),0).
\end{aligned}
$$

Therefore, the union it is idempotent even without `unique`: `A | A == A`. It is neither concatenation nor the sum of bags. If both operands are `unique`, these definitions correspond to the union, ordinary intersection and difference of sets.

`^` requires both operands to be `unique` and applies the ordinary symmetric difference. It is not defined via the absolute difference of multiplicities because that operation is not associative. The equivalent binary form on multisets is written as `(A -- B) | (B -- A)`.

#### Cardinality y domain inferred

Sean $[a..b]$ y $[c..d]$ the static cardinalities of $A$ y $B$. Without further information on overlap, the compiler can guarantee:

| Result | Cardinality conservative |
| --- | --- |
| `A | B` | $[\max(a,c)..b+d]$ |
| `A & B` | $[0..\min(b,d)]$ |
| `A -- B` | $[\max(0,a-d)..b]$ |
| `A ^ B` (`unique`) | $[\max(0,a-d,c-b)..b+d]$ |

The arithmetic of limits is conservative `*` as an effective upper bound. The analysis must narrow these intervals where it can demonstrate disjunction, inclusion, equality, or a domain finite or any other relevant restriction.

Yes $D_A$ y $D_B$ These are the semantic domains of the members:

| Result | Domain from member |
| --- | --- |
| `A | B` | $D_A\cup D_B$ |
| `A & B` | $D_A\cap D_B$ |
| `A -- B` | $D_A$ |
| `A ^ B` (`unique`) | $D_A\cup D_B$ |

The IR retains the domain resulting form, even though its most precise form does not have an abbreviated surface script.

#### Propagation of modifiers

For each modifier $m$ from `unique`, `ordered` or interior capacity `mut`, its presence in the result is obtained from the same table:

| Result | Presence of $m$ |
| --- | --- |
| `A | B` | $m(A)\land m(B)$ |
| `A & B` | $m(A)\lor m(B)$ |
| `A -- B` | $m(A)$ |
| `A ^ B` | $m(A)\land m(B)$; `unique` it is guaranteed |

For `unique`, the table follows directly from the multiplicities: the intersection is unique if any of the operands restricts each multiplicity to one and the union It needs that guarantee on both sides. The symmetric difference already requires `unique` in its operands.

For `mut`, the table refers exclusively to the internal load-bearing capacity of members, never to the mutability outside of a stored field. A union A mixed symmetric difference could contain a member accessible only from the operand without capacity; an intersection, on the other hand, contains only members that are also accessible from the operand with capacity. A difference `--` It only retains elements from the left-hand operand. A computed field does not acquire mutability outdoors.

For `ordered`, if only the intersection preserves the order, the ordered operand is filtered; the difference `--` filters the left-hand operand. Union and mixed symmetric differences are unordered because they may contain elements that are exclusive to the unordered operand.

When both operands are `ordered`, must use compatible sort criteria. If their sort keys or sort modes are incompatible, the operation is a error static. An order by type or by the same one path `ordered by` normalises the result based on that criterion and preserves provenance stable amongst ties. When the operation retains a sequence constructed by composing the operands rather than replacing it with one of those criteria, the result it is stable with respect to the left-hand operand:

- The union go through first $A$ and then adds, in the order of $B$, only the additional occurrences required to achieve each maximum multiplicity.
- The intersection and the difference `--` leak $A$ without rearranging it.
- The symmetric difference first preserves the excess occurrences of $A$ and then those from $B$.

In consequence, when a binary operation constructs its observable sequence through stable composition of the operands, commutative operations retain the same multiset when the operands are swapped, but may produce different observable sequences. The ordered equality continues to compare the complete sequence.

Example of inference:

```mud
leftChars: Char [1..5] = ["a"]
rightChars: Char [0..2] = empty
combinedChars := leftChars | rightChars
```

The type static of `combinedChars` is `Char [1..7]`: it isn't `unique`, `ordered` nor `mut`, and its domain from member is the domain full list of `Char`.

`Text` is not the same as `Char [* ordered]`: retains the positional order of its characters and does not support modifiers for collection. D-056 establishes this distinction.

Compatible concurrent insertions that need to complete an order of provenance They respect causality and resolve ties only between concurrent events by means of a reproducible pseudo-random selection using identity semantics stable. In a collection `unique`, equivalent insertions are merged before that order is completed.

### Dictionaries

The form:

```mud
Key -> Value [cardinality modifiers]
```

declares a dictionary with intrinsically unique keys. The modifier `unique`, when written, applies to the **associated values** in accordance with D-085: requires that the same value is not associated with more than one key. An insertion or replacement that would violate this uniqueness is a complete no-op and does not produce `failed`.

```mud
stock =
    Grain -> 2_000,
    Bronze -> 500
```

Assigning a key replaces its value; entering a missing key triggers the input if type, domain, capacity and cardinality if permitted; removing a missing key is a no-op.

Reading a missing key results in `empty` in accordance with the declared exit procedure. Absence does not result in `failed` in its own right; merely a later context whose type, domain o cardinality If it does not accept zero elements, it may fail. It is not used `null` nor is it quietly replaced by the default setting from the type from value.

A dictionary lookup may be followed by access to members of the value obtained when its type allows this. Another chained indexing method requires that the result the intermediate dictionary is itself a compatible dictionary.

When exact indexing is an intermediate step in a path allocable that passes through a alias unchangeable, the elaboration can reconstruct the alias and extend the substitution to the dictionary and the externally mutable location that contains it. If the intermediate key is absent, the query produces `empty` and the partial write-back is a no-op: it does not commit the key, does not apply defaults and does not produce `failed` because of that absence. The direct allocation `dictionary[key] = wholeValue` It remains distinct and may provide a missing clue.

### Order and iteration

A dictionary `ordered` It iterates through keys in their canonical order. It can be iterated through by keys or by pairs `(key, value)`.

A structural alias it can act as a single composite key and use the sugar defined in D-033:

```mud
board[(E, Four)]
board[E, Four]
```

### Equality

- Collection ordered: same sequence and multiplicity.
- Collection unordered: same multiset.
- Dictionary: the same key associations–value; the order in which they are stored does not affect equality.

## Consequences

- Cardinality, order, uniqueness and mutability They are separate axes.
- Dictionaries do not explain `null`.
- The iteration does not depend on the hash or internal structure of the materialiser.
- Operations relating to collection and the dictionary must be complete; where is it? decision as indicated.

## Option ruled out

### Default uniqueness

It has been ruled out that `unique` implicit, both for all collections and depending on the type from member. Multiplicity is observable and necessary information in collections such as `Num [*]`; removing it by default would alter the meaning of data representing observations, runs or frequencies. A default value depending on the type It would also mean that the same form of collection change from semantics between generic code, aliases and conversions.

The general rule is that the absence of `unique` It retains its multiplicity, yet its presence commands a singular occurrence by value.

## Future verification

1. Cardinality omitted and `empty`.
2. Duplicates, normalisation, notice and idempotence of `unique`.
3. Intrinsic semantic order, by provenance stable and `ordered by`, including one path stable on associated data and ties by provenance.
4. Missing reading such as `empty`, writing and retrieval of a missing password, and `unique` global values.
5. Equality irrespective of internal representation.
6. Key alias plain and sweetened.
7. Multitudes of union, intersection and difference; rejection of `^` without `unique`.
8. Inference conservative and narrow-minded cardinality y domain.
9. Propagation of `unique`, `ordered` and interior capacity `mut` in the four permitted operations.
10. Canonical order and stable sequence constructed by composing operands, including any possible sequential difference resulting from swapping them.
11. Absence of mutability external in calculated results.

