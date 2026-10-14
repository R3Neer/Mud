---
title: Domains and intervals
tags:
  - mud/specification
status: current
normative: true
depends-on:
  - "[[11-type-system]]"
  - "[[15-fields-and-mutability]]"
  - "[[16-collections]]"
  - "[[21-expressions]]"
questions: []
decisions:
  - D-169
  - D-167
  - D-168
  - D-166
  - D-029
  - D-037
  - D-049
  - D-059
  - D-075
  - D-082
  - D-088
  - D-100
  - D-130
  - D-143
  - D-151
  - D-154
  - D-155
---

# 18. Domains and intervals

## Restriction and interval values

A domain restricts values admitted by a complete type contract. An interval is
a domain/value with ordered bounds and explicit endpoint inclusion. A domain
does not become a finite collection merely because it is written with brackets.

```mud
let age: Nat in 0..150 = 18
let eligible in 0..cap := candidateValues
# Interval expressions:
[1..3] | [7..9]
```

The first two are owned declaration fragments; cap and candidateValues have
the required visible contracts. `in` is restriction/binding syntax, not Boolean
membership. Boolean membership is `container has value` or `has not`.

Let D(W) denote a domain's admitted member set in one coherent view W.
Admission first checks type and applicable explicit conversion, then membership
in D(W), then the owning shape obligations. The same view must supply a derived
result and its domain; mixing snapshots cannot produce a valid admission.

## Stable stored bounds and live derived domains

> [!rule] MUD-DOM-001 — Stable stored interval endpoints
> A stored field/local interval restriction must have endpoints transitively
> stable for that binding's lifetime. Direct or hidden reads of mutable state
> cannot supply those bounds. Derived fields/locals may use dynamic intervals
> and domains under their recorded dependencies and coherent read view.

A captured immutable scalar is stable even if its historical source was mutable.
An immutable thing handle does not freeze that thing's mutable fields. A
calculated intermediate name does not hide mutable dependencies. No implicit
endpoint capture rewrites a live expression into a stored bound.

This rule freezes the necessary stored interval endpoints, not all identities
or values that can be members of a domain. Other named-domain contracts retain
their own permitted dependencies. Derived domain restriction filters the result
before cardinality; a lower bound still requires enough survivors. Stored
collections do not self-filter or recompute membership to mimic derived views.

## Acyclic evaluation

> [!rule] MUD-DOM-002 — No recursive computed-domain equations
> Domain computation must be pure, deterministic, non-stochastic and statically
> acyclic, following all transitive calculations needed to evaluate it. A
> potential unproved cycle is not admitted; no least/greatest fixed-point
> evaluation or iterative mutually recursive domain solver is selected.

Let G_D contain an edge from one computation to another when obtaining the
first actually requires evaluation of the second. Admission requires an acyclic
G_D. Reading an already stored candidate value does not recursively evaluate
its domain and adds no validator-to-validator edge merely from that read.
Thus validations a<=b and b<=a can both check stored values and require equality
without creating recursive equations. Initialization that needs an uncomputed
value retains its separate dependency obligations.

Acyclicity does not prove bound stability or finiteness. Recursive productive
type descriptions and cyclic point normalization do not grant recursive domain
evaluation. General dynamically selected callable impact/acyclicity evidence
follows [[types/contextual-call-analysis]].

## Linear interval forms and normalization

The four forms [l..u], (l..u), [l..u) and (l..u] encode closed/open boundaries.
Bare l..u means closed bounds; [l] can mean singleton interval [l..l] only with
an unambiguous expected interval context. The competing singleton collection
form has no arbitrary priority. Ambiguous unannotated construction requires
an explicit type.

Each `*` denotes the effective limit on its own side. A star boundary must be
closed; (*..10] and [1..*) are invalid. Cardinality bounds remain nonnegative
closed integral specifications, distinct from general interval values.

Normalize finite endpoint expressions and quantity units before comparing them.
For l<u preserve inclusion; for l=u retain one member only with both ends
closed; for l>u return the empty interval. Discrete content can be empty even
with l<u, such as two consecutive excluded integer bounds. Endpoint evaluation
faults remain Fault and cannot masquerade as an empty interval. Inversion is
neither descending traversal nor cyclic wraparound.

Magnitude endpoints must have the same admitted magnitude and compatible
representations. `[1 m..5 km]` uses local units. When all finite endpoints are
unitless numeric literals, an outer unit distributes to them: `[1..5] m` and
`1..5 m` are magnitude intervals; `[] m` is typed empty. An outer unit cannot
complete an expression endpoint: `[minimumDistance..5] m` is invalid, while
`[minimumDistance..5 m]` can be valid. `[1..5 m]` mismatches untyped scalar and
quantity; a second outer unit is invalid. Magnitude header domain bounds instead
use bare canonical coordinate numbers under [[19-magnitudes]].

> [!rule] MUD-DOM-003 — Canonical discontinuous content
> Compatible interval |, &, -- and ^ operate on member sets and normalize to
> sorted maximal nonempty convex segments relative to the admitted member
> universe. Merge segments exactly when their union is one interval. Preserve
> excluded holes, member identity, normalized endpoints and inclusion.

Empty has zero segments and a simple nonempty interval one. Equality and exact
keys compare canonical content, not construction order. `[1..3] | [7..9]` and
its reversed spelling have the same key. Overlap `[1..5] | [3..9]` becomes
[1..9]. An excluded rational 3 in [1..3) | (3..5] remains a hole; integral
adjacency differs from dense rational adjacency. No multi-segment literal is
introduced and normalization alone supplies no continuous enumeration.

## Finite enumeration and stepping

> [!rule] MUD-DOM-004 — Finite and enumerable are separate premises
> Materialization all D and finite traversal require a canonical finite
> enumeration certificate, not merely an ordered, bounded or mathematically
> countable domain. A full numeric Rum domain has no supplied enumeration.

Finite explicit domains/containers, Bool, closed families and proved finite
aliases have their canonical enumeration. Nat and Int are infinite; Num is
countably infinite even between ordinary distinct bounded endpoints. Rum's
finite binary64 value space does not supply a numeric domain progression.
Explicit finite Rum collections remain traversable. Any has no exhaustive
enumeration. Actual world populations are finite identity catalogues, not all
possible future thing declarations.

A stepped exact interval requires a static compatible nonzero signed difference,
finite bounds and admitted numeric/quantity representation. Positive steps
anchor at the lower endpoint; negative at the upper. An open initial endpoint
advances once before the first candidate. Nat/Int and Money retain default
increments one and one hundredth where admitted. Num needs an explicit exact
step; Rum numeric stepping is not admitted. The sign can change the member set:
[0..1] by 0.3 and by -0.3 anchor differently. all D uses canonical domain order;
explicit traversal follows its signed progression contract.

Stepping restarts for each normalized discontinuous segment, visiting segments
in descending order for negative steps. A cyclic point source visits at most
one fundamental period. `cycle` is exclusive to point-domain declaration after
a finite contiguous nonempty [a..b), with strictly positive b-a; it does not
modify an ordinary interval expression or add wraparound to cardinality.

The exact version-uniform finite-analysis procedure is [[types/finite-static-certification]]. Proved violation and completed
unproved obligations are distinct static rejection reasons; resource-interrupted
verification yields no completed admission verdict. Optional stronger analysis
can explain but cannot independently expand accepted programs.

## Contextual outcomes and evidence

An out-of-domain required static initializer is a static error. An invalid
action given produces ArgumentRefusal before effects; Boolean-rule given
admission can produce false under its own contract. Invalid stored writes/candidate
states produce Errors and rollback. False owning if/after/always checks produce
their respective Refusal. Inverted interval construction itself remains valid
empty; the subsequent owner decides whether that emptiness violates its contract.

[[types/typing-cases.yaml]] covers stored versus derived endpoints, hidden mutable
reads, capture, acyclic validation versus recursive equations, finite source
requirements and discontinuous content. Finite interval certificates and syntax
coverage validate supplied normal forms, not a general domain solver. These
rules introduce no new domain keyword, nominal anchor or HIR type/effect fields.
