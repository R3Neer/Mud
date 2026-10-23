---
title: Exact and functional dictionaries
tags:
  - mud/specification
status: current
normative: true
depends-on:
  - "[[10-names-and-anchors]]"
  - "[[11-type-system]]"
  - "[[13-aliases]]"
  - "[[16-collections]]"
  - "[[20-blocks-and-recovery]]"
  - "[[21-expressions]]"
questions: []
decisions:
  - D-183
  - D-184
  - D-185
  - D-182
  - D-181
  - D-180
  - D-176
  - D-178
  - D-174
  - D-173
  - D-172
  - D-169
  - D-167
  - D-168
  - D-033
  - D-039
  - D-080
  - D-081
  - D-085
  - D-086
  - D-090
  - D-098
  - D-105
  - D-117
  - D-122
  - D-137
  - D-155
  - D-157
  - D-162
---

# 17. Exact and functional dictionaries

## Forms and grouping

An exact dictionary stores finite key/value associations. A functional dictionary
is a pure branch policy applied to an input; its selectors and results are
computations, not mutable associations. Value declarations in examples belong
to admitted containing bodies; let/mut are not file-root declarations.

```mud
let labels: Int -> String = 1 -> "one", 2 -> "two"
let describe: Int --> String [ordered] = first {
    value > 0 --> "positive",
        _ --> "other"
}
```

`->` and `-->` admit complete key/input and value/output types. Arrows associate
right: A -> B -> C is A -> (B -> C). An exact arrow's trailing specification constrains associations:
A -> B[2] -> C[3] groups as A -> (B -> C[3])[2]. A functional arrow instead
uses type-adjacent input/output specifications under [[types/functional-families]].
Grouping distinguishes a residual policy from a collection of policies;
A --> (B --> C)[3 ordered] produces three residual values. A dictionary itself is one outer value.

> [!rule] MUD-DICT-001 — Complete arrow forms
> A dictionary arrow must be the complete outer type form. It cannot be hidden
> in a union alternative, including through an alias's effective representation.
> Exact and functional dictionaries are distinct categories and cannot be
> combined by inventing a conversion between arrows.

Nominal aliases may represent dictionaries but retain their alias identity.
TypeKind distinguishes Dictionary and FunctionalDictionary for raw constructors.

## Omitted cardinality and owner contracts

> [!rule] MUD-DICT-006 — Uniform owner-directed cardinality
> A written arrow cardinality is an association/application contract. If it is
> omitted, immutable stored definitions infer it from their initializer/body,
> derived definitions preserve expression-inferred bounds, and mutable stored
> exact dictionaries and type-only positions use [1]. A dictionary's exterior
> remains one value independently of these internal bounds.

| Owner with omitted arrow cardinality | Effective internal cardinality |
| --- | --- |
| Immutable stored exact definition with initializer | Inferred association bounds; proved literal counts are exact. |
| Immutable stored functional definition with body | Inferred application-result bounds over admitted inputs and views. |
| Derived exact/functional definition | The expression's inferred association/application bounds. |
| Mutable stored exact definition | [1], not the initial association count. |
| Type-only position without defining-value inference | [1], including signatures and alias representations. |

Let O be the declaration owner, E its defining expression/body and W an optional
written cardinality. Let Bounds(E) be its conservatively proved static interval
of association counts or normal application-result counts, as appropriate.
The owner judgement resolves an omitted count by the following cases:

- If W is present, retain W and apply its ordinary owner-specific admission or
  derived-transformation rules.
- Otherwise, for immutable stored or derived definitions, use Bounds(E).
- Otherwise, for mutable stored exact or type-only positions, use [1,1].

Missing required type/body evidence is a diagnostic, not another default case.
A dictionary's independent exterior count is resolved at its own layer.

Resolve the member/input/output types and written structure without prematurely
supplying a singleton for an omitted inference slot. Then infer the counted
layer using the owner's initializer/body. A modifier-only specification such
as [ordered] or [unique] still has omitted cardinality. It preserves the written output guarantee without imposing a singleton count;
first/all independently selects branch mode. Existing nested
value contracts and arrow grouping remain independent; a receiving type-only
contract is not inferred anew from every supplied value.

```mud
let names: Int -> String = 1 -> "one", 2 -> "two"  # two associations
let noNames: Int -> String = empty                 # zero associations
mut growing: Int -> String [*] = empty             # explicit variable capacity
let partial: Int --> String [ordered] = first {
    > 0 --> "positive"  # [0..1]
}
let total: Int --> String [1 ordered] = first {
    > 0 --> "positive",
        _ --> "other"
}
```

Without [*], growing defaults to one association and cannot initialize from
empty. Without the last branch, total is rejected for incomplete coverage;
partial instead admits uncovered inputs and returns ordinary empty. In a
signature, Int -> String requires one association and Int --> String requires one
result per application; use explicit bounds to accept other shapes.

Inferred bounds describe every normal result admitted by the static contract,
not a sample invocation or the first state of a live calculation. Use the
supported normative proof procedures and conservative interval operations;
unsupported coverage facts cannot establish a positive inferred minimum.
Uncovered inputs and possibly empty selected results contribute zero; faults
remain faults and do not become zero results. Written positive minima require
coverage and enough results. AllMatches accounts for overlapping selectors,
fallback and any result uniqueness normalization. FirstMatch accounts for the
first admitted result's bounds, including a collection-valued result contract.
A missing inference certificate or type is not repaired by guessing a body,
nominal input, singleton or totality guarantee.

Schema/component defaults with omitted bounds may infer [0] or a fixed count.
Write bounds explicitly when the schema must admit other constructor arguments
or inherited overrides. This requirement is independent of public visibility.

## Exact association construction and query

An association `key -> value` checks one key against the dictionary's key
contract and one complete value against its value contract. The key uses an
ExpressionBlock and the value a ValueBlock, each with independent local scope
and the enclosing permissions. Association insertion can use
`add (key -> value) to dictionary`. Each association is counted once; contained
collection/dictionary value layers do not flatten into more associations.

> [!rule] MUD-DICT-002 — Exact keys and ordinary absence
> Exact keys are intrinsically unique and require supported semantic equality.
> Present-key application returns the admitted associated value; missing-key
> application returns ordinary empty in the applicable output shape. Missing
> lookup alone supplies neither Error nor a type-selected default.

Functional values and compared key structures requiring functional equality
fail MUD-TYPE-040 in [[11-type-system]]. A structural alias can be one composite
key: `board[E, Four]` is sugar for `board[(E, Four)]` under the same expected
alias key contract. It does not create independently indexed multiple keys.
Chained lookup `table[a][b]` requires a dictionary result at the intermediate
step. Member access checks the retrieved value's contract. A later positive
minimum context may fail on absence under ordinary admission/recovery.

Read-only query substitution checks every target key as admitted by the source
key contract and source outputs as included in target outputs, preserving the
association/domain guarantees. Writable roots remain invariant. Query
compatibility grants no insertion/replacement authority.

## Associated-value uniqueness, ordering and mutation

`unique` on an exact dictionary constrains whole associated values across keys;
`unique by path` constrains projected stable value keys. Neither modifies intrinsic
dictionary key uniqueness. The path starts at the associated value and follows
the ordinary stable equality/key rules. Required equality must be supported.
Inserting/replacing an association that violates the effective value criterion
is a whole-proposal no-op, not a partial replacement or Error for that collision.

With authority, direct `dictionary[key] = wholeValue` replaces or inserts the
complete association subject to its contracts. Removing a missing key is a
no-op. Partial alias write-back through an intermediate missing key is separately
a no-op: it cannot insert an alias using defaults. Reconstruction keeps exact
nominality and unchanged stored components under [[13-aliases]].

Dictionary updates retain semantic association/component destinations. Concurrent
consolidation follows [[28-effects]]: deletion priority, compatible partial
changes, whole replacements, joint value-uniqueness checking and final cardinality
validation are distinct stages. Shared roots alone do not imply conflict.
This static chapter does not replace that batch algorithm.

An exact dictionary is enumerable by keys or full associations. Bare `ordered`
preserves the association sequence, independently of key comparability. Literal
association order establishes it. A new sequential key appends; replacing an
existing value preserves that key's position. Deleting and reinserting creates
a new position. Concurrent additions use stable causal-respecting provenance.
Copying and filtering preserve surviving order. Explicit stable-key ordering is
distinct. Hash traversal is not observable order. A single traversal binding
projects the key. A two-position
root pattern projects key and value, with recursive patterns within those
positions. Pattern matching does not alter association identity. Equality of
exact dictionaries compares the same semantic key/value associations, independent
of physical storage ordering, and requires supported compared contents.

## Exact dictionary algebra

Let L and R have compatible key/value contracts and key sets KL, KR. Form these
candidate associations before applying an effective result value-uniqueness
criterion:

| Operator | Candidate key set | Associated value |
| --- | --- | --- |
| L \| R | KL union KR | L's value for a shared key; otherwise the present side. |
| L & R | KL intersection KR | L's value. |
| L -- R | KL minus KR | L's value. |
| L ^ R | Keys present on exactly one side | That side's value. |

Exact union/intersection is not generally commutative as associations because
shared keys retain left values. Exact symmetric difference uses intrinsically
unique keys and does not require value uniqueness merely to select exclusive
keys. Key and value compatibility still checks independently.

Union guarantees whole-value uniqueness when both operands do, but does not
automatically keep keyed uniqueness. Intersection and difference keep the left
value-uniqueness criterion; the right's unique values cannot constrain retained
left values. Symmetric difference guarantees whole-value uniqueness when both
sides do, without automatically keeping a cross-side keyed criterion. Retained
equality guarantees require supported contents. Incorporate surviving left
associations first, then applicable right associations; omit a later collision
when the result carries a value criterion. Thus a uniqueness-constrained result
can have fewer keys than its candidate set. Order/cardinality remain separate
contracts and inferred bounds must account for that omission.

## Functional policy branches

> [!rule] MUD-DICT-003 — Pure selectors and conditional coverage
> Every functional dictionary has pure deterministic interpreted selectors and input coverage when the application minimum is positive. Its results satisfy the complete output contract.

A functional branch has a pure selector and a ValueBlock result. Reserved value denotes the available complete input or
cumulative positional chain product under [[types/functional-families]]. It is
visible in selector/result scopes and cannot be redeclared. Named inputs and
inferred free parameters keep declaration-local symbols and ordinary no-shadowing. Direct selector-preamble locals are visible in that branch's result under the shared-scope contract below. Exact associations
do not inject value: their values are computed at association construction,
not recomputed for each lookup.

### Branch-local scope and derivation reuse

> [!rule] MUD-DICT-005 — Shared selector preamble and demand-preserving reuse
> Direct selector-preamble bindings are visible in the same branch's result.
> A successful demanded derivation must reuse its normal result within that
> application/branch while its inputs and transitive dependencies remain unchanged.
> Sharing is neither eager evaluation nor a stored capture or cross-call cache.

The result's lexical environment extends the completed selector environment.
Direct named locals, pure positional-pattern leaves and successfully exported
immutable foreign bindings retain their original symbols and contracts. Locals
inside nested operand/RHS blocks do not escape. Result locals cannot redeclare
or shadow a visible selector local. Other branches, fallback and the outside
scope receive none of these bindings. Exact key/value scopes and comprehension
filter/result scopes remain independent under their owning contracts.

```mud
# A branch fragment within an admitted functional policy:
{
    let adjusted := adjustedDamage[value]
    adjusted > .shield
} --> adjusted - .shield
```

Names are statically resolved, but the result may use a selector binding only
when every admitted path selecting that result establishes its availability.
A failed selector scope rolls back its locals before recovery. Recovering that
whole selector to true does not resurrect a lost local. A local RHS that itself
recovers normally can establish its binding. Missing definite-availability
proof prevents such a use; handlers retain their ordinary protected-scope rules.

A shared selector-preamble derivation is first evaluated only at an actual demand. Cache its completed
normal outcome, including permitted local recovery, for that binding instance.
On a valid reuse retain the full transitive read/dependency footprint and value
provenance without replaying the RHS or its recovery. An ordinary Error value is
still a value; a later raise creates its own occurrence. Fault supplies no cached
normal value and follows the ordinary error channel.

All policy reads use the stable application snapshot. Explicit permitted private
writes still invalidate any affected captured-local/transitive dependency; an
unproved overlap conservatively invalidates. Unrelated changes do not invalidate
an established independent binding. A valid hit must be reused; invalidated demand
recomputes under the applicable view. Neither reuse nor invalidation permits
stochastic replay, outer writes, lost fault demand or guessed native purity.
Each application, recursive invocation and AllMatches branch has independent
binding instances. A direct derived positional pattern shares its complete RHS
outcome among its named projections; discarded leaves add no demand. No physical cache layout, world-version protocol or cross-call
memoization is selected. A wholly unused local stays undemanded, including when
only the result would first read it. Scope disposal ends its binding/cache lifetime.

Inside a functional branch, `.member` abbreviates `value.member`, including
subsequent access/index/call suffixes and String interpolations. It supplies no
receiver outside that branch and never picks a traversal binding implicitly.

Interpret each selector operand with its established static category before
combining selector `not`, `and` and `or`:

| Written selector | Predicate |
| --- | --- |
| Ordinary singleton Bool expression | The expression itself. |
| Ordinary non-Bool singleton value expression | `value == expression`. |
| Interval/domain expression | `expression has value`, preserving all boundaries. |
| Nominal type reference | `value is Type`. |
| `== expected`, `!= expected`, `< limit`, `<= limit`, `> limit`, `>= limit` | The corresponding comparison with value. |
| `is Type`, `is not Type`, `iis Type`, `iis not Type` | The explicit nominal test. |
| `not selector` | Negation of the interpreted predicate. |
| `_` | Residual fallback. |

Bool operands keep their ordinary predicate meaning: `false` never applies;
`== false` compares the input with false. For a non-Bool expected value,
`not expected` means inequality. For an interval it means exclusion and for a
type it means failed membership. Arbitrary collection expressions acquire no
implicit membership. Explicit equality forces value comparison when supported;
`== (1..10)` compares an interval value, whereas `(1..10)` tests membership in
the open interval. Bare `1..10` retains closed-bound sugar. Type membership does
not erase nominal identity or the distinction between is and iis.

Logical operators combine the expanded predicates with their ordinary demand,
pruning and narrowing rules. `Low or Medium` and `== Low or == Medium` compare
family members, rather than applying Boolean or to member values. A complete
condition such as `value.age >= 18 and value.hasPermit` needs no additional if.
No as input binding, structural selector patterns or new guard form exists.
Supported equality, singleton-Bool admission and purity remain mandatory.

Composite application policy[a,b] retains its written arguments and explicit
product grouping. It can supply one product input or two curried stages when
the resolved static signature admits exactly that interpretation. Multiple
admitted interpretations are an error requiring policy[(a,b)] or policy[a][b].
Named signature parameters and cumulative value may be bound using ordinary
positional patterns; product labels themselves are not injected as locals.
Details, partial specialization and capture lifetimes follow
[[types/functional-families]].

When the application-result minimum is positive, coverage is universal over
the admitted input contract and applicable views, not one runtime sample.
Prove it using declared finite families, nominal alternatives, admitted domain
relations, supported Boolean facts or residual fallback. Unproved positive
coverage is static rejection. A zero-admitting application may be uncovered;
no applicable branch then yields normal empty. An ambiguous inferred output
cannot be made zero-admitting by guessing a contract.

Fallback is unique and last. It applies only when no ordinary selector applies.
A selected result yielding empty has handled that input and does not trigger
fallback. Exhaustive treatment is independent of output presence: `_ --> empty`
is valid when the output admits absence. Selected computing faults propagate;
they do not retry another branch or fallback. The first constructor chooses FirstMatch and the
first applicable selector; all or unmarked branches use AllMatches, evaluating all ordinary selectors
in one snapshot and produces all applicable results. Positive-minimum coverage is required in
both modes; unreachable/redundant cases are diagnosed when provable.

AllMatches aggregates the exterior members of selected branch results. With
contributions [1,2] and [3,4], the result has four occurrences; it is not
[[1,2],[3,4]]. Equal occurrences are retained unless result uniqueness removes
them. Empty contributes no member; a nested collection already contributed as
one member keeps its entire nested shape. Sum contribution bounds before
checking the aggregate cardinality; the aggregate's positive minimum is not a
minimum imposed independently on every branch. Output ordering, uniqueness,
fallback and finite occurrence evidence follow [[types/functional-families]].

Input and output types may be inferred only with unique evidence/context.
`_ --> .name` alone does not establish an input type. An explicit input with
an output hole can, as in `let naming: Person --> _ = first { _ --> .name }`.
Output cardinality follows admitted branch results, not coverage alone; a
covered FirstMatch returning optional values can still produce empty.

Functional dictionaries have no outer mutability or inner `[mut]` capability and cannot enumerate branches or their input population. All reads record transitive dependencies in one stable application snapshot. Branch selector keys remain local normalized reconstruction identities without public anchors; equivalent shorthand normalizes to the same predicate key.

## Pure composition

> [!rule] MUD-DICT-007 — Whole-result composition
> F >> G applies F first and passes its complete normal result as the sole
> input to G. F << G applies G first and passes its complete result to F.
> The selected downstream input contract must admit the whole upstream output
> contract. No per-member distribution, implicit flattening or causal effect is
> introduced.

```mud
let increment: Int --> Int = _ --> value + 1
let double: Int --> Int = _ --> value * 2
let eight := increment >> double[3]
let seven := increment << double[3]
```

Composition constructs a policy value. Construct/evaluate its operand values
once in textual order; it does not invoke their bodies until application.
During an application, execute the semantic upstream first, then the downstream
in the same stable application snapshot. Forward/reverse affects application
order, not textual operand-construction order. A normal empty result is passed
as empty; it does not omit the downstream stage. A Fault stops dependent work;
ordinary error recovery applies. Explicit optional omission keeps its existing
owner boundary and is not silently converted into an empty result.

Cardinality, domains, order, uniqueness and authority check at the complete
intermediate boundary. For an admitted family, retain relational constraints
rather than inventing cross-signature combinations. Incompatible or ambiguous
mandatory specializations are static errors. A downstream scalar policy is not
implicitly mapped over an upstream multi-member result. Use explicit traversal
when per-member application is intended.

## Recursive admission and pointwise algebra

> [!rule] MUD-DICT-004 — Proven recursive descent
> Each recursive call component must carry a well-founded measure strictly
> decreasing along every edge continuing a cycle. Numerical descent,
> cardinality reduction or smaller substructures require valid evidence. Lack
> of proof is static rejection, not permission to try an implementation heuristic.

The version-uniform method is [[types/termination-certification]], with finite
lexicographic tuples, constant declaration phases, actual finite Rum order and
exact affine scalar synthesis. A policy's input domain need not be exhaustively
enumerable to admit individually terminating applications.

For compatible policies F and G and a collection operator op among |, &, --, ^,
define `(F op G)[x] = F[x] op G[x]` in one snapshot. Each side retains its own
selectors and fallback; dependencies combine transitively. No branch merge,
shared fallback or left-preference functional union is introduced. The result
operator retains its supported equality/uniqueness premises and conservative
cardinality. A pair of FirstMatch policies can yield two union/symmetric-difference results.
The computed policy applies each operand's own mode; it does not propagate a
branch mode through a collection-order modifier. Result order/uniqueness/count
follow ordinary result algebra, independently of how the operands selected
branches. Annotation cannot hide an inadmissible result count.

Functional dictionaries have no value ==/!=, including through aliases and
stored structures requiring that comparison. This is distinct from comparing
their Type descriptors' normalized contracts. Extensional algebra supplies no
all-input equivalence oracle or structural policy/capture equality.

## Examples, counterexamples and evidence

With L=(1->"one",2->"two") and R=(2->"other",3->"three"), L|R retains
2->"two", L&R contains that association, L--R retains key 1 and L^R retains
keys 1 and 3. Exchanging L and R changes the shared-key value. A partial write
through an absent key creates nothing; a valid whole association write can insert.

A selector `1 --> "one"` compares value with 1. A Bool selector false is a condition; write `== false` for equality. A policy with unproved coverage and no fallback is invalid.
Assigning policy branches at runtime, using F in `foreach`, comparing F==G,
or using a functional value as an exact key is invalid. Combining -> and -->
operands or putting an effective arrow alias inside a union is invalid.

[[types/typing-cases.yaml]] covers arrow grouping, query/mutability contracts,
generic structural keys, recursive proof boundaries and functional equality.
[[effects/README]] covers association updates, missing write-back, deletion and
joint uniqueness. Grammar/AST retain both arrow forms and local branch provenance;
no new callable category, source trait or nominal HIR branch anchor is introduced.

## Anonymous tuple input projection

> [!definition] Positional alias input projection (MUD-TYPE-047)
> An anonymous exact/functional dictionary input tuple admits a structural alias
> with the same number and sequence of complete stored component contracts,
> ignoring source component names. Its projection uses the target tuple labels.

Compare normalized component types, domains, cardinality, nested shapes,
uniqueness/order and authority. No extra/missing component, hidden private
schema or implicit conversion of nominal component types is admitted. Derived
fields are not stored components and are not exposed by this projection.
This rule is distinct from ===, which continues to compare names and complete
structural contracts, and from general nominal conversion/subtyping.

The projected input is the target tuple, not an alias retaining extra source
members. Inside a functional branch use value, .name or value.name. No bare
component local is injected. Positional patterns remain available for unnamed
inputs. Original caller values are unchanged and retain their nominal identity.
Exact construction, insertion and lookup all project admitted keys identically;
hash/equality use target tuple components and supported semantic equality.
Distinct outer aliases with equal projected contents address the same key.

```mud
alias Journey { let departure: City; let arrival: City }
# Within an admitted owner:
let sameCity: (origin: City, destination: City) --> Bool [ordered] = first {
    _ --> .origin == .destination
    # sameCity[journey] exposes origin/destination, not departure/arrival.
}
```

A zero-admitting application-result contract permits uncovered inputs, producing
normal empty when no branch applies. A positive minimum retains universal
coverage and required-result proofs. FirstMatch never retries after a matching
branch returns empty; AllMatches collects its applicable results. Omission in
a required result is not ordinary empty: [[21-expressions#Optional extraction and omission]]
requires explicit construction to consume it. Computing faults remain faults.
