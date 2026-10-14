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
computations, not mutable associations.

```mud
let labels: Int -> Text = 1 -> "one", 2 -> "two"
let describe: Int --> Text [ordered] =
    value > 0 --> "positive",
    _ --> "other"
```

`->` and `-->` admit complete key/input and value/output types. Arrows associate
right: A -> B -> C is A -> (B -> C). A bracketed specification after an arrow
constrains that dictionary's associations or application results, not the count
of independent dictionary values. A -> B [2] -> C [3] groups as
A -> (B -> C [3]) [2]. Parentheses delimit a dictionary used as key or shaped as
an outer collection. A dictionary itself is one outer value.

> [!rule] MUD-DICT-001 — Complete arrow forms
> A dictionary arrow must be the complete outer type form. It cannot be hidden
> in a union alternative, including through an alias's effective representation.
> Exact and functional dictionaries are distinct categories and cannot be
> combined by inventing a conversion between arrows.

Nominal aliases may represent dictionaries but retain their alias identity.
TypeKind distinguishes Dictionary and FunctionalDictionary for raw constructors.

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

An exact dictionary is enumerable by keys or full associations. `ordered` uses
the applicable canonical key order/provenance contract; hash traversal is not
observable order. A single traversal binding projects the key. A two-position
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

> [!rule] MUD-DICT-003 — Pure exhaustive selectors
> Every functional dictionary has pure deterministic interpreted selectors and proven input coverage. Its results satisfy the complete output contract.

A functional branch has a pure selector and a ValueBlock result. Its input
is the implicit immutable ordinary variable `value`, visible in both sibling
scopes. It is not a reserved or contextually classified word. Normal lookup,
duplicate-name and no-shadowing rules apply; neither result nor selector may
redeclare it. Selector locals do not escape to the result. Exact associations
do not inject value: their values are computed at association construction,
not recomputed for each lookup.

Inside a functional branch, `.member` abbreviates `value.member`, including
subsequent access/index/call suffixes and Text interpolations. It supplies no
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

Composite application `policy[a, b]` supplies one complete contextual input,
equivalent to `policy[(a, b)]`. The implicit value is that complete tuple or
nominal product, not one independently dispatched argument. No argument names
are injected as locals. Named components are accessible through value/.member;
anonymous positional products use admitted positional binding.

```mud
let total: (Int, Int) --> Int [ordered] =
    _ --> {
        let (left, right) = value
        left + right
    }
```

total[2,3] applies this one tuple-input policy and produces 5 under its contract.
A nominal named product cannot be opened with that positional binding; access
its named components instead. Structural input identity and once-only input
evaluation retain the ordinary contextual-construction rules.

Coverage is universal over the admitted input contract and applicable views,
not a check of one current world or runtime sample. State-dependent guards
require fallback unless the version's finite static certificate procedure
proves coverage independently of that sample. Finite family enumeration,
nominal inclusion/exclusion, static domain coverage and propositional Boolean
certificates use the existing static proof rules. No general theorem solver
or type-based nominal guessing is introduced.

Each dictionary must cover every input admitted by its complete input contract.
Coverage must be proved from declared family members, nominal alternatives,
admitted interval/domain relations, ordinary supported Boolean facts or a
residual `_`. Unproved coverage is static rejection, including for a dictionary
with an empty-admitting output. Arbitrary predicates need a fallback when the
supported proof procedure cannot establish coverage. Closed-family members
can be enumerated; union coverage respects overlapping ancestry and exact iis
tests rather than treating every nominal type as a disjoint variant.

Fallback is unique and last. It applies only when no ordinary selector applies.
A selected result yielding empty has handled that input and does not trigger
fallback. Exhaustive treatment is independent of output presence: `_ --> empty`
is valid when the output admits absence. Selected computing faults propagate;
they do not retry another branch or fallback. Ordered FirstMatch chooses the
first applicable selector; unordered AllMatches evaluates all ordinary selectors
in one snapshot and produces all applicable results. Coverage is required in
both modes; unreachable/redundant cases are diagnosed when provable.

Input and output types may be inferred only with unique evidence/context.
`_ --> .name` alone does not establish an input type. An explicit input with
an output hole can, as in `let naming: Person --> _ [ordered] = _ --> .name`.
Output cardinality follows admitted branch results, not coverage alone; a
covered FirstMatch returning optional values can still produce empty.

Functional dictionaries have no outer mutability or inner `[mut]` capability and cannot enumerate branches or their input population. All reads record transitive dependencies in one stable application snapshot. Branch selector keys remain local normalized reconstruction identities without public anchors; equivalent shorthand normalizes to the same predicate key.

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
cardinality. A pair of FirstMatch policies can yield two union/symmetric-difference
results, generally losing ordered FirstMatch mode; intersection/difference can
retain it when at most one result is proved. Annotation cannot hide the loss.

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
