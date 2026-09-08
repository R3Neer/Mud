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
  - "future `15-collections.md`, future `16-dictionaries.md`, future `20-quantifiers-and-iteration.md`"
---
# ADR-039 — Collections and dictionaries

- Modified by: [[ADR-105-keyed-uniqueness-by-stable-path|D-105]].

- Amended by: [[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]]
- Amended by: [[ADR-086-exact-nominal-identity-external-arrows-and-dictionary-algebra|D-086]] and [[ADR-098-assignable-paths-and-write-back-of-immutable-aliases|D-098]]
- Amended by: [[notes/decisions/ADR-064-ordering-by-stable-path|D-064]]
- Amended by: [[ADR-080-higher-order-collection-algebra-and-updates|D-080]] and [[ADR-081-collection-filtering-take-and-indexing|D-081]]
- Read more: D-019, D-026, D-033
- Related questions: Q-006, Q-047
- Documents affected: future `15-collections.md`, future `16-dictionaries.md`, future `20-quantifiers-and-iteration.md`
- Amended by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].

## Decision

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

Collections allow duplicates unless a uniqueness mode is present. `unique` retains at most one occurrence of each whole value. `unique by path` retains at most one occurrence for each semantically equal key obtained from the stable path, with the first occurrence by stable provenance surviving. `unique` and `unique by path` are alternative forms of one uniqueness axis. `ordered` retains an observable order and `ordered by path` declares stable key semantics in accordance with D-064.

Adding a value already present in a `unique` collection is a no-op. Adding to a `unique by path` collection is also a no-op when an existing occurrence has the same projected key. The operations are idempotent under their respective criteria, including compatible concurrent effects; distinct concurrent values with one keyed-uniqueness key are resolved by stable provenance rather than by conflict or replacement.

When a literal intended for a collection with uniqueness contains a collision that can be proven statically, the compiler normalises it and issues a non-blocking warning. Ordinary `unique` compares whole values; `unique by path` compares the projected semantic key. In both cases the first occurrence by stable provenance survives, and the warning identifies the exact retained source occurrence and the colliding later occurrence or occurrences. If the normalised collection fails its cardinality, the programme also has a static cardinality error:

```mud
members: Person [* unique] = [Alice, Alice]  # warning; retains the first Alice
pair: Person [2 unique] = [Alice, Alice]     # error; normalisation leaves one value
contacts: Person [* unique by email] = [Alice, Bob]  # if the e-mails are provably equal, warning; retains Alice
```

Initial sources of information:

- When the type The whole possesses an intrinsic semantic order, `ordered` Use that order. This includes the orders defined for basic items, `Char`, `ordered family` and aliases where applicable.
- When the type The complete version does not have a common overall comparator, `ordered` use the provenance a stable record of occurrences; collections of `thing` are the usual cases.
- `Char` use value ascending Unicode scale and does not support `ordered by`.
- You don’t invent a comparator between branches of a union by means of text position, tags, proper nouns or identity implementation.

In a collection values with associated fields, components or data, `ordered by ruta` may replace the standard sort order with a key derived from unique accesses from each member. The key must have full semantic order and the entire path must be transitively stable. A `thing` It is not a sortable primary key. Keys that are equal retain the relative order of provenance stable. In a purely sequential narrative, this provenance corresponds to the order of insertion. This order of collection it does not alter the intrinsic comparison between its members.

When the type or `ordered by path` determines the main order, a literal written in a different order is normalised and produces a non-blocking warning. Among identical keys, provenance remains stable; in a sequentially written literal, the writing order conveys that provenance. This notice does not apply to a `thing [ordered]` collection whose ordinary order derives entirely from its own values.

### Set Algebra

Set operators also apply to compatible sets:

| Operation | Form |
| --- | --- |
| Union | `A | B` |
| Intersection | `A & B` |
| Difference | `A -- B` |
| Symmetric difference of whole-value-unique sets | `A ^ B` |

Two operands are compatible when they have the same type number of member. The refinements of domain and the modifiers for collection They may differ and are combined in accordance with the following rules; no implicit conversions are performed between different types.

Be $\mu_C(v)\in\mathbb N$ the multiplicity of the value $v$ in the collection $C$. Operations are defined point a point:

$$
\begin{aligned}
\mu_{A\mid B}(v) &= \max(\mu_A(v),\mu_B(v)),\\
\mu_{A\mathbin{\&}B}(v) &= \min(\mu_A(v),\mu_B(v)),\\
\mu_{A\mathbin{--}B}(v) &= \max(\mu_A(v)-\mu_B(v),0).
\end{aligned}
$$

Therefore, the union it is idempotent even without `unique`: `A | A == A`. It is neither concatenation nor the sum of bags. If both operands guarantee whole-value uniqueness, these definitions correspond to the union, ordinary intersection and difference of sets.

`^` requires both operands to guarantee whole-value uniqueness. Ordinary `unique` and `unique by path` both provide that guarantee. The operation applies ordinary symmetric difference by whole value; it is not defined via the absolute difference of multiplicities because that operation is not associative. The equivalent binary form on multisets is written as `(A -- B) | (B -- A)`.

#### Cardinality and domain inferred

Let $[a..b]$ and $[c..d]$ be the static cardinalities of $A$ and $B$. Without further information about overlap, the compiler can guarantee:

| Result | Cardinality conservative |
| --- | --- |
| `A | B` | $[\max(a,c)..b+d]$ |
| `A & B` | $[0..\min(b,d)]$ |
| `A -- B` | $[\max(0,a-d)..b]$ |
| `A ^ B` (whole-value-unique) | $[\max(0,a-d,c-b)..b+d]$ |

The arithmetic of limits is conservative `*` as an effective upper bound. The analysis must narrow these intervals where it can demonstrate disjunction, inclusion, equality, or a domain finite or any other relevant restriction.

Let $D_A$ and $D_B$ be the semantic domains of the members:

| Result | Domain from member |
| --- | --- |
| `A | B` | $D_A\cup D_B$ |
| `A & B` | $D_A\cap D_B$ |
| `A -- B` | $D_A$ |
| `A ^ B` (whole-value-unique) | $D_A\cup D_B$ |

The IR retains the domain resulting form, even though its most precise form does not have an abbreviated surface script.

#### Propagation of modifiers

Uniqueness is not a Boolean modifier after D-105. Let `N` be no uniqueness guarantee, `V` ordinary whole-value uniqueness and `K(p)` keyed uniqueness by resolved path `p`; every `K(p)` also guarantees `V`. Collection algebra remains defined by whole-value multiplicity and uses these conservative result guarantees:

- `A | B` yields at least `V` exactly when both operands guarantee at least `V`; it does not automatically retain `K(p)` because distinct cross-operand values may share a key.
- `A & B` preserves a sole keyed criterion `K(p)` because the result is a subset of that operand. Equal keyed criteria also remain `K(p)`. Different keyed criteria conservatively expose `V` rather than arbitrarily preferring one. Without a keyed criterion, `V` is guaranteed when either operand guarantees it.
- `A -- B` preserves the exact uniqueness mode of `A`.
- `A ^ B` requires both operands to guarantee at least `V` and conservatively yields `V`.

Analysis may strengthen these results when it proves that cross-operand key collisions are impossible. It never keyed-normalises `|` or `^` merely to keep a modifier.

For `ordered` and interior capability `mut`, presence in the result continues to follow this table:

| Result | Presence of the modifier |
| --- | --- |
| `A | B` | $m(A)\land m(B)$ |
| `A & B` | $m(A)\lor m(B)$ |
| `A -- B` | $m(A)$ |
| `A ^ B` | $m(A)\land m(B)$ |

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

declares a dictionary with intrinsically unique keys. A written uniqueness modifier applies to the **associated values** in accordance with D-085. `unique` requires that the same whole value is not associated with more than one key; `unique by path` requires that no two associated values have the same projected semantic key, with `path` interpreted from the value rather than the dictionary key. An insertion or replacement that would violate the effective value-uniqueness criterion is a complete no-op and does not produce `failed`.

```mud
stock =
    Grain -> 2_000,
    Bronze -> 500
```

Assigning a key replaces its value; entering a missing key triggers the input if type, domain, capacity and cardinality if permitted; removing a missing key is a no-op.

Reading a missing key results in `empty` in accordance with the declared result form. Absence does not itself produce `failed`; a later context may fail only when its type, domain or cardinality does not accept zero elements. `null` is not used, nor is absence silently replaced by a type default.

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

It has been ruled out that any uniqueness mode be implicit, either for all collections or depending on the member type. Multiplicity is observable and necessary information in collections such as `Num [*]`; removing it by default would alter the meaning of data representing observations, runs or frequencies. A default value depending on the type It would also mean that the same form of collection change from semantics between generic code, aliases and conversions.

The general rule is that absence of a uniqueness mode retains multiplicity. Ordinary `unique` retains one occurrence per whole value; `unique by path` retains one occurrence per projected semantic key.

## Future verification

1. Cardinality omitted and `empty`.
2. Duplicates and keyed collisions, normalisation, warning, first-survivor provenance and idempotence of both uniqueness modes.
3. Intrinsic semantic order, by provenance stable and `ordered by`, including one path stable on associated data and ties by provenance.
4. Missing reading such as `empty`, writing and retrieval of a missing password, and associated-value uniqueness criteria.
5. Equality irrespective of internal representation.
6. Key alias plain and sweetened.
7. Multitudes of union, intersection and difference; rejection of `^` without a whole-value uniqueness guarantee.
8. Conservative, narrow inference of cardinality and domain.
9. Propagation of uniqueness criteria, `ordered` and interior capacity `mut` in the four permitted operations.
10. Canonical order and stable sequence constructed by composing operands, including any possible sequential difference resulting from swapping them.
11. Absence of mutability external in calculated results.

