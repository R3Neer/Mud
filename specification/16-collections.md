---
title: Cardinalities and collections
tags:
  - mud/specification
status: current
normative: true
depends-on:
  - "[[11-type-system]]"
  - "[[15-fields-and-mutability]]"
  - "[[21-expressions]]"
questions:
  - Q-032
decisions:
  - D-167
  - D-168
  - D-162
  - D-019
  - D-026
  - D-029
  - D-039
  - D-056
  - D-064
  - D-075
  - D-080
  - D-081
  - D-084
  - D-085
  - D-100
  - D-103
  - D-105
  - D-137
  - D-145
  - D-151
  - D-152
  - D-155
---

# 16. Cardinalities and collections

## Values and shapes

Collections contain finite member occurrences. Cardinality, multiplicity,
uniqueness, logical order and immediate-member authority are independent axes.
An unbounded static upper limit permits arbitrarily large finite values, never
an infinite or lazy source-language sequence.

```mud
scores: Int [*] = [3, 1, 3]
distinct: Int [* unique] = [3, 1, 3]
matrix: Int [*] [*] = [[1, 2], [3, 4]]
```

Every field has an outer collection shape, including singleton `[1]`. An ordered
collection carries its logical sequence throughout its existence; an unordered
collection carries a multiset rather than an observable sequence. Member
occurrences retain stable provenance wherever it can affect future observation.
The physical container, traversal order or hash order is not semantic order.

## Cardinality and nesting

> [!rule] MUD-COLL-001 — Independent finite layers
> `[n]` fixes exactly n outer members; `[l..u]` bounds their finite count.
> Each repeated specification wraps the complete preceding member contract.
> Every layer checks its own bounds, domain, uniqueness, order and capability.
> Values do not flatten implicitly.

Bounds are nonnegative integers with l<=u; `*` denotes the applicable effective
limit, not a guessed runtime population. Omitted ordinary shape means `[1]`.
The stored immutable-field exception infers the exact outer initializer shape;
outwardly mutable stored fields retain `[1]` when omitted. Neither exception
changes dictionary association counting or implicit nested flattening.

`empty` and `[]` contain zero outer members. `[empty]` and `[[]]` contain one
empty collection member and are equal under compatible context, but differ from
empty. At every depth outer count is retained. Thus Int [0] [1] admits one empty
inner collection, while Int [0] [0] admits zero outer members. Int [*] [*]
permits ragged nested collections; it does not prove rectangular matrix shape.
Empty needs a zero-admitting expected context and cannot choose ambiguous
nominal member types or fill a positive lower bound.

## Uniqueness and order

> [!rule] MUD-COLL-002 — Semantic uniqueness and stable keys
> Without a uniqueness modifier, retain multiplicity. `unique` retains one
> occurrence per equal whole value; `unique by path` retains one per equal
> projected stable key. They are alternative modes of one axis. Keyed
> uniqueness additionally guarantees whole-value uniqueness when the member
> type supports whole-value equality.

Whole-value uniqueness, membership and algebra require supported equality;
functional values and compared containers needing their equality fail
MUD-TYPE-040 in [[11-type-system]]. A supported projected key may still serve
keyed normalization without granting whole-value comparison.

The path starts at each member, has singular unambiguous intermediate accesses,
is transitively stable for the collection's lifetime, and supplies a common
equality-compatible final key over every possible union alternative. A thing
identity can be an equality key. `ordered by path` additionally requires a
total semantic order on the final key; a thing identity alone supplies no such
order. Allowed widening cannot erase alias identities or invent a conversion.

Normalize uniqueness in stable provenance order, retaining the first equal
whole value/key. An already present key makes a compatible insertion a no-op;
keyed uniqueness does not turn value removal into removal by key. Literal
collisions proven statically are normalized with a nonblocking warning naming
retained and discarded source occurrences; resulting cardinality still checks.
An already computed value assigned to a stored contract is verified, not
silently rewritten.

`ordered` uses the complete member type's intrinsic total order when it exists,
otherwise stable occurrence provenance. It invents no comparator between union
branches from their spelling, tags or implementation identity. `ordered by`
uses its semantic key and stable provenance for ties. Ordering a literal contrary
to the applicable intrinsic/key order normalizes with the specified warning.
Copying, passing, selecting or serializing an ordered value retains its sequence
unless the operation explicitly removes/replaces order.

## Local and derived transformations

Let C be the temporary collection and let a specification supply domain D,
uniqueness q, order o and bounds [l,u]. Transform in this order, independent of
modifier spelling order: filter by D; normalize q; establish o; truncate to u;
require at least l surviving members. Lower bounds never manufacture values.
The written type remains statically checked and authority cannot be created.

> [!rule] MUD-COLL-003 — Transformation versus stored verification
> Local collection specifications and derived shapes perform their defined
> coercive transformations. Stored value contracts verify produced values.
> Neither operation grants outer mutability, implicit container-alias identity
> or authority absent from the source.

The short local `[n]` retains positional indexing where syntactically ambiguous;
an exact transformation can use `[n..n]`. Constructing a collection counts each
written element expression once, including empty inner collections. An erased
Boolean-rule result used as element data closes to true and remains an element,
under [[21-expressions]]; pruning is not collection deletion.

## Algebra over whole values

Let mu_C(v) be the multiplicity of whole value v in C. Compatible operands use
admitted member types under ordinary compatibility without implicit nominal conversion:

| Operation | Multiplicity/result contract |
| --- | --- |
| A \| B | max(mu_A(v),mu_B(v)); not concatenation or bag addition. |
| A & B | min(mu_A(v),mu_B(v)). |
| A -- B | max(mu_A(v)-mu_B(v),0). |
| A ^ B | Set symmetric difference; both operands must guarantee whole-value uniqueness. |

Union is idempotent even without unique. Difference uses `--`; arithmetic `-`
does not remove collection members. For bounds [a,b] and [c,d], conservative
result bounds are respectively [max(a,c),b+d], [0,min(b,d)],
[max(0,a-d),b] and [max(0,a-d,c-b),b+d]. Domain results are respectively union,
intersection, left domain and union. Stronger guarantees require evidence.

Uniqueness propagates as follows: union yields whole-value uniqueness when both
operands guarantee it; intersection retains a sole/equal keyed criterion,
degrading different keyed criteria to whole-value uniqueness, or retains ordinary
uniqueness when either supplies it; difference retains the left criterion;
symmetric difference yields whole-value uniqueness. Cross-operand keyed criteria
require collision-freedom evidence, never silent keyed normalization of algebra.

Order and inner authority propagate by both/either/left/both for union,
intersection/difference/symmetric difference respectively. Retained order criteria
must be compatible. A provenance-composed union retains left occurrences then
only required additional right occurrences; intersection/difference filter the
appropriate retained sequence. Commutative multiset content does not guarantee
equal observable sequences when operands are exchanged.

## Arithmetic lifting and access

Numeric and alias arithmetic lifts only when at least one static upper bound
is at most one and every possible member pair has an admitted operation.
Result cardinality before normalization is [l_A*l_B,u_A*u_B]. Each occurrence
pair contributes once. Empty absorbs without executing a nonexistent pair;
static signature checks remain mandatory. Both possibly-multiple operands do
not acquire implicit zip, reduction or Cartesian arithmetic. Collision-freedom
is required to preserve uniqueness. Complete-operand alias overloads precede
member lifting under [[21-expressions]].

Positional indexing starts at one and requires observable order. A guaranteed
existing position returns [1], otherwise [0..1]; out-of-range access yields
ordinary absence. A range selects existing positions and preserves surviving
occurrences' order, multiplicity, uniqueness and inner authority. Unordered
positional access is invalid. Dictionary indexing uses keys; Text has its own
positional sequence contract and is not Char [* ordered].

Pure deterministic selection binds a source item/pattern only in its predicate
and returns surviving occurrences, preserving identity and guarantees with
bounds [0,u]. The source is a captured finite enumerable collection; a domain
must be explicitly materialized with `all D`. Dictionary pair selection retains
associations. Pattern mismatch is a static error, not a filter.

`take n from C` requires singleton Nat n and finite enumerable source. It returns
min(n,count(C)) occurrences; constant n gives [min(n,l),min(n,u)]. Observable
order or canonical domain enumeration supplies the prefix; an unordered proper
sample uses reproducible sampling without replacement and does not acquire order.
Zero or provably complete selection needs no random choice. Container-alias
identity is not reconstructed implicitly. Bare domains require explicit all D.

## Examples, diagnostics and evidence

`[1,1,2] | [1,2,2]` has multiplicities two for 1 and two for 2.
`[5] - [3]` is [2], while `[5] -- [3]` is [5]. Symmetric difference over
nonunique collections is invalid. A `[2 unique]` literal `[1,1]` normalizes to
one member, warns for duplication, then fails cardinality. Taking three members
can produce fewer than three; an outer `[3]` contract still requires three.

`items: Int [*] = all` cannot materialize the infinite Int domain. Num is
countably infinite and a bounded rational interval is not thereby finite. Rum
has finitely many representable values but no supplied numeric-domain enumeration;
explicit finite Rum collections remain traversable. Mathematical finiteness and
Mud's finite canonical enumeration evidence are distinct.

The normative finite-analysis procedure is [[types/finite-static-certification]]. Random-point cache/retry protocol
details remain [[../notes/questions/Q-032-a-reproducible-randomness|Q-032]];
they do not permit different cardinality, purity or prefix/sample contracts.
[[types/typing-cases.yaml]], nested syntax tests and type/contract certificates
cover nested empties, shape compatibility, source proof requirements, modifier
propagation and pruning/data boundaries. [[effects/README]] covers stored
update contracts. These witnesses are finite evidence, not an executor.
