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
labels: Int -> Text = 1 -> "one", 2 -> "two"
describe: Int --> Text [ordered] =
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

> [!rule] MUD-DICT-003 — Explicit pure selectors
> An ordinary `selector --> result` branch has a singleton-Bool ExpressionBlock
> selector and an admitted ValueBlock result. `value` denotes the input in both
> independent scopes. No implicit value equality, type query or membership
> selector is inserted. `_` is fallback, not a binding or readable value.

Selectors/results may read external state, recording all transitive dependencies
and observing one stable application snapshot. They have no world-write/action
authority; result ValueBlocks may use confined private temporaries. Functional
dictionaries admit neither outer mutability nor inner `[mut]`, and cannot supply
a `for each` enumeration of branches or input population.

Ordinary normalized selectors have distinct local branch keys; duplicate keys
are invalid. `_` has one unique fallback key. Changing only a result retains the
selector key; changing a selector changes that local identity. A branch has no
public anchor or metadata-bearing descriptor. Source/model editing of branches
is not runtime policy mutation.

| Mode | Application contract |
| --- | --- |
| FirstMatch (`ordered`) | Test ordinary branches in source order; first match wins. Fallback is last. Without match/fallback result cardinality is [0..1]; fallback supplies the required one result. |
| AllMatches | Evaluate ordinary branches; each match contributes its admitted result. Source order does not select a winner. Fallback contributes one result only with no ordinary match. |

For AllMatches, a proved maximum n of matching branches supplies [0..n] before
result normalization; fallback raises the lower bound to one. Ordinary/keyed
uniqueness normalizes produced result values under its supported equality
criterion. In FirstMatch either criterion is redundant and receives a removal
suggestion. A selected branch's computing fault enters ordinary block recovery;
it is not a reason to retry another signature or treat the branch as no match.
No type provides an implicit fallback.

Composite application `F[a, b]` constructs one contextual input just as
`F[(a, b)]` does. The input must admit that complete positional construction;
there are no independently dispatched multiple keys. Named alias components
may be supplied positionally; anonymous named and positional products remain
distinct. Ordinary input domain/shape checks and once-only argument demand apply.

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

A selector `1 --> "one"` is invalid: write `value == 1 --> "one"`.
Assigning policy branches at runtime, using F in `for each`, comparing F==G,
or using a functional value as an exact key is invalid. Combining -> and -->
operands or putting an effective arrow alias inside a union is invalid.

[[types/typing-cases.yaml]] covers arrow grouping, query/mutability contracts,
generic structural keys, recursive proof boundaries and functional equality.
[[effects/README]] covers association updates, missing write-back, deletion and
joint uniqueness. Grammar/AST retain both arrow forms and local branch provenance;
no new callable category, source trait or nominal HIR branch anchor is introduced.
