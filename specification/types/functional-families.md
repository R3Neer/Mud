---
title: Functional families, currification and static application
status: current
normative: true
depends-on:
  - "[[../10-names-and-anchors]]"
  - "[[../11-type-system]]"
  - "[[../17-dictionaries]]"
  - "[[finite-static-certification]]"
  - "[[termination-certification]]"
questions: []
decisions:
  - D-183
  - D-182
  - D-180
---

# Functional families, currification and static application

A functional value is a pure policy or a statically constrained family of
policies. Currification returns a residual functional value with earlier
arguments captured. It creates values, not new nominal types or host endpoints.

```mud
let add: (a: Int) --> (b: Int) --> Int = a + b
let inferred: a --> b --> _ = a + b
let generic = a + b
let other = generic
let addTwo = generic[2]
let five := addTwo[3]
```

> [!rule] MUD-FUNC-001 — Correlated family schemes
> A family has a statically represented scheme forall Q. C => S, where Q is
> its ordered type/shape variables, C its retained relational obligations and
> S its complete curried signature. Specialization substitutes a solution for
> Q and must discharge C. Never replace this scheme by independent unions of
> operand and result types or by an inventory of current runtime inhabitants.

## 1. Formation, generalization and copied values

The judgement Gamma |- e => (Q,C,S) synthesizes a scheme from already resolved
captures, written signature structure and body obligations. Written concrete
contracts constrain inference; an omitted input/output type becomes a fresh
static variable only in this functional-definition context. A lowerCamel name
in a parameter position is a binder, not a nominal generic type. A grouped
(name: Type) input records both binder and complete input contract. Names do
not enter signature identity. Type-only unbound lowerCamel parameters without
a defining/inherited scheme are invalid rather than dynamically typed.

A definition generalizes variables not fixed by captured contracts or explicit
annotations. Copying a family preserves that scheme and its captures; every
static use can specialize its quantified variables independently. Passing or
storing a family retains its complete scheme. A required monomorphic contract
must be met by an unambiguous admitted specialization. A polymorphic required
contract must be satisfied for all its permitted instantiations, not one sample.
An inferred stored component can retain a closed-static family default; its
reflected ~type exposes the checked normalized scheme for an explicit type
reference elsewhere. No new function declaration category is introduced.

Constraints include admitted ordered operator signatures and their result
relation, literal admissibility, domains/cardinalities, trait requirements,
authority, purity, visibility and termination. Solve under the existing finite
normative proof procedures and preserve unresolved quantified constraints.
When a use requires a concrete solution and several inequivalent candidates
remain, reject that use. Never choose by imports, runtime type or Any fallback.
Parametric body correctness and a finite generic/application closure are required;
unsupported polymorphic recursion is rejected, not unrolled to a cutoff.

### Implicit parameters

In an immutable definition with an expected functional signature, or without a
nonfunctional expected contract, unresolved free lowerCamel variable references
in its pure body can introduce implicit parameters. Scan source occurrence order,
bind the first occurrence once and reuse repeated occurrences. Resolve ordinary
outer symbols first: those are captures. Property labels, named-argument labels,
nominal names, local declarations, bound patterns and foreign source text are
not free variable references. Missing members/callees are not invented inputs.
An ordinary context requiring a nonfunctional value does not silently change
its result category. Effect statements, guards and declaration headers do not
acquire this implicit-parameter rule.

If a definition has no functional expected shape, no free parameters and no
explicit branch/policy constructor, it remains an ordinary value. Thus let n=2
stores a number, not a zero-argument function. An unknown name in an eligible
unannotated body may be an intended parameter or a typo; show the inferred
signature/captures without requiring warnings on every such definition.

Access through value or .member alone does not invent a chain arity or an
arbitrary nominal input type when that information is absent. Retain a supplied
constraint scheme or require enough defining signature evidence.

value is a reserved input reference, never an inferred free parameter or ordinary
local. A user member named value is permitted only by the explicit member-name
exceptions; qualified .value does not introduce or shadow a local parameter.

## 2. Currification, captures and cumulative input

For an unconditional body with n declared/inferred inputs, application of the
first k<n inputs returns a residual with those complete evaluated inputs. The
final body is demanded only when the needed inputs are supplied. Explicit outer
branch selectors/results are evaluated when their own stage is applied; errors
at that stage are not deferred merely because its result is another policy.
Each explicit nested policy definition starts a new parameter chain/scope.

Within a chain's final body, value denotes the complete supplied argument when
there is one input, or an ordered positional product of chain inputs when there
are several. An earlier stage can access only its available inputs. Nested
products remain components: a tuple input plus scalar yields ((a,b),c), not
(a,b,c). Indexing is base one. Parenthesized (a) is grouping; [a] is a collection.
Existing positional patterns may bind value in a ValueBlock. Reserved value
cannot be redeclared; named arguments and pattern locals obey no-shadowing.

```mud
let add: Int --> Int --> Int = {
    let (a, b) = value
    a + b
}
let subtract: Int --> Int --> Int = value[1] - value[2]
```

.member considers accessible fields on the currently available complete argument
positions. Exactly one statically admissible receiver resolves it; multiple
receivers are an ambiguity, even if a runtime sample would disambiguate. An
unknown/inaccessible field does not become an implicit parameter. Name the
argument or use value's positional component to qualify it explicitly.

Stored = evaluates the policy/residual value once. Derived := can reconstruct
it from changed dependencies. Captured argument values keep their evaluated
values; a captured thing identity does not freeze its mutable fields. Later
internal reads use the application's stable view and transitive footprints.
Residuals may outlive a local binding because its captured value is retained,
but no dead writable place, foreign resource lifetime or authority is invented.
A composed application shares its application view across stages; a separately
stored residual applied later uses that later application view for live reads.

## 3. Partial specialization and contextual literals

A partial application substitutes argument constraints without requiring every
quantified variable to become concrete. A literal such as 2 retains every
admitted contextual numeric interpretation compatible with the remaining
scheme. Store its literal evidence/value, not a guessed nominal type or a
runtime choice of overload. A previously typed variable keeps that type; partial
application cannot reinterpret it as an unrelated numeric/magnitude type.
Copying or transmitting the residual preserves the pending constraints.

let addTwo = generic[2] may therefore support several later static applications.
A concrete destination/argument context can select an interpretation; if that
mandatory choice remains ambiguous, reject it. Literal-domain, precision and
numeric-conversion rules still apply to every selected specialization.

## 4. Product versus compact curried application

IndexExpr retains its complete written list and explicit product grouping.
Elaboration forms the complete product-input interpretation and the sequential
curried interpretation permitted by the resolved static signature. It never
evaluates operands while exploring candidates. If exactly one interpretation
survives, use it; if several inequivalent interpretations survive, diagnose
ambiguity and show the explicit alternatives. If none survives, diagnose the
contract mismatch. Do not attempt a runtime fallback after a failure.

f[a][b][c] explicitly sequences applications. f[a,b,c] abbreviates those stages
when that is the unique admitted interpretation. f[(a,b),c] explicitly groups
the product argument; it does not flatten it into two chain positions. A sole
product input can still use f[a,b]. With an Any input and a residual result,
both product and curried interpretations may fit; require f[(a,b)] or f[a][b].
Each written argument is evaluated once in textual order, and later argument
work is not demanded after a failed/omitted required prefix. Validate the whole
source statically even when a path will not execute.

No application distributes over a collection of residual policies. The next
stage must receive exactly one policy value, or an explicit extraction/traversal
must establish it. Composition likewise passes the complete intermediate result.

An operator reference may retain unary and binary signatures of the same
symbol. Application cannot silently choose between a complete result and a
residual policy when both shapes fit. Supply a functional signature/context
that fixes arity: Int --> Int for unary (-), or Int --> Int --> Int for binary
(-). Without that evidence, (-)[2] is ambiguous when both alternatives remain
admitted. No union of a scalar result and a callable is invented to hide it.

## 5. Arrows, count ownership and branch selection

Both arrows associate right. For -->, each adjacent type's specifications belong
to that input/output value. Thus A[N] --> B[M] --> C[P] takes N As, then M Bs,
and finally produces P Cs. It returns one intermediate residual policy unless
a collection suffix explicitly wraps that result. A --> (B --> C)[3 ordered]
returns three residual policies in sequence. Repeated specifications are distinct
nested collection layers. Parenthesized result dictionaries preserve their own
constructor category and counts.

For ->, the first trailing specification still counts associations of that exact
arrow. Mixed chains elaborate from the right, preserving explicit grouping and
the class of each arrow. A --> (B -> C[P]) returns one exact dictionary with P
associations; A --> (B -> C)[P] returns P exact dictionaries. Explicit grouping
is required to alter ownership, not a type-driven greedy reassignment of counts.
In --> annotations, ordered describes the output collection only and never
selects a branch mode.

first { selector --> result, ... } constructs FirstMatch. all { ... } constructs
AllMatches. Unmarked explicit branches use AllMatches. In a functional expected
context a plain ValueBlock/expression is one unconditional case and may omit
_ -->. The selection mode belongs to the policy value/body, not the function
signature's collection-order field. Bodies/returned values retain ordinary
termination and error rules. A mode is redundant only when changing it preserves
result, faults, demand, dependencies and termination; cardinality alone is not
such a proof. AllMatches output ordering follows its actual declared collection
construction/explicit criterion and never an internal hash enumeration.

For AllMatches, each selected branch contributes its exterior result members,
not a new wrapper containing its complete result. If selected contributions are
C1,...,Ck, the exterior population before uniqueness is their disjoint occurrence
sum: |R| = sum_i |Ci|. Empty contributes zero. Repeated equal members remain
distinct occurrences unless an explicit uniqueness guarantee normalizes them.
An already nested member is preserved as one member; aggregation removes no
additional collection layer. Branch-result bounds are summed conservatively,
including overlap and fallback reachability, then result guarantees and the
final cardinality contract are checked. A final positive minimum does not
require every individual contribution to meet that minimum.

```mud
let contributions: Int --> Int [*] = all {
    > 0 --> [1, 2],
    >= 0 --> [3, 4]
}
# contributions[1] contains four exterior occurrences, not two collections.
let nested: Int --> Int [*] [*] = all {
    > 0 --> [[1, 2]],
    >= 0 --> [[3, 4]]
}
# nested[1] contains two collection members; neither member is flattened.
```

An ordered output without a comparator assembles selected contributions in
branch source order and preserves each contribution's own observable sequence.
Without that ordered contract, branch source order supplies stable occurrence
provenance only, not permission to use sequence operations. An explicit ordered
by criterion orders the aggregate under the ordinary collection rules. All
ordinary selectors are demanded in the same application view; an earlier
nonempty contribution does not suppress another selected branch's error.

Omitted cardinality follows the ordinary owner matrix for the input/output
value layer, independently of residual-policy population. Explicit counts are
contracts or ordinary derived transforms. Coverage is required for a positive
result minimum; otherwise uncovered inputs contribute normal empty. A selected
empty result never triggers fallback. Inference covers all admitted inputs and
state views, not just the first application.

## 6. Equality, reflection and effect boundary

Family schemes normalize variable names/parameter names by ordered binding
position; comparison preserves constraints and correlated occurrences. Existing
Type === compares normalized contracts, not arbitrary logical equivalence of
predicates. Unknown constraint equivalence is not a fabricated equality proof.
Functional values/families/residuals still lack value ==/!= and ordinary whole-
value uniqueness. TypeKind remains FunctionalDictionary for their public type.
Descriptor identity and actual policy captures are separate from a scheme.

Policies may use pure looks/Boolean rules and private ValueBlock storage under
existing contracts. They cannot execute real actions, publish messages, mutate
world state or manufacture authority. Application partiality, inference and
composition do not create reactive activators. Actions, messages, reactive and
always rules retain their independent causal contracts; the operational causal
algorithm is outside this pure functional type contract.
