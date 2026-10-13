---
title: Quantifiers and finite iteration
tags:
  - mud/specification
status: proposed
normative: true
depends-on:
  - "[[11-type-system]]"
  - "[[15-fields-and-mutability]]"
  - "[[16-collections]]"
  - "[[17-dictionaries]]"
  - "[[18-domains-and-intervals]]"
  - "[[20-blocks-and-recovery]]"
  - "[[21-expressions]]"
questions:
  - Q-028
  - Q-029
  - Q-032
decisions:
  - D-164
  - D-033
  - D-047
  - D-048
  - D-075
  - D-081
  - D-088
  - D-095
  - D-101
  - D-137
  - D-150
  - D-151
  - D-152
  - D-155
---

# 22. Quantifiers and finite iteration

## Forms and result categories

Quantifiers consume a finite enumerable source and a Boolean predicate.
Executable `for each` consumes such a source to produce effects or confined
private computation; it does not construct a collection of body results.

```mud
anyPositive := exists item in values : item > 0
positiveCount := count item in values : item > 0
action Accumulate for values: Int [* ordered], mut total: Int {
    then for each item in values : total += item
}
```

The first two are pure owned fragments with a finite Int collection values.
The mandatory `:` separates each header/body even when the body has braces or
starts on the next line. `by` precedes optional `if`. It is progression, not
a stride over an arbitrary collection.

## Admission and bindings

Let C be the owner environment/mode and S its checked source. Write Enum(S,W,E)
when E is a finite canonical enumeration of S captured in view W. Source
production, enumeration and each body require their own purity/termination
contracts; finite individual values or countability alone do not prove Enum.
The complete certification procedures remain
[[../notes/questions/Q-028-f-finiteness|Q-028]] and
[[../notes/questions/Q-029-t-termination|Q-029]].

> [!rule] MUD-ITER-001 — Captured finite source and lexical binding
> Check source and optional step in the outer environment before introducing
> the iteration pattern. Capture source membership once at traversal entry.
> Validate the complete pattern and introduce all named leaves jointly only
> in its predicate/body scopes. Discards introduce no symbol or readable value.

Patterns use the exact positional contract of [[11-type-system]], preserving
nominal source identity. Exact dictionaries project keys for one name/discard
and key/value associations for a two-position root pattern; nested key patterns
go inside the first position. Selection retains full associations and extrema
retain original key witnesses. Pattern mismatch is a static error, not a
mechanism to discard source items. Filter locals disappear before an executable
iteration body and bindings do not escape the construct.

Quantifiers and for each can consume an admitted finite domain directly.
Collection-producing selection/take instead require `all D`. Functional
dictionaries have no branch/input enumeration; explicit finite inputs can
be traversed and individually applied to a policy.

## Boolean quantifiers, count and witnesses

> [!rule] MUD-ITER-002 — Pure Boolean bodies
> exists, forall, count, min and max require pure deterministic singleton-Bool
> ExpressionBlock predicates. min/max predicates select witnesses and do not
> compute a numeric aggregation result or an ordering key.

For successfully evaluated source occurrences E and predicate p, ordinary
results are:

| Form | Normal result |
| --- | --- |
| exists | True exactly when some occurrence satisfies p; empty source yields false. |
| forall | True exactly when every occurrence satisfies p; empty source yields true. |
| count | Nat number of accepted occurrences, retaining source multiplicity; empty yields zero. |
| min | First accepted source witness in its usable semantic order, or empty. |
| max | Last accepted source witness in that order, or empty. |

exists/forall yield Bool [1]; count yields Nat [1] bounded by source size.
min/max yield the source member contract with [0..1], narrowable to [1] only
with accepted-witness evidence. No accepted witness is ordinary absence,
not an aggregation error. A later `[1]` context still checks that absence.
An unordered source without usable semantic order cannot supply extrema.
Progression generation direction does not redefine the source's semantic order.

Predicate computing faults enter the producing block's error channel and do
not become false, zero or absence. Static validation of source, body, step,
bindings and required proofs remains mandatory even for an empty source.

## Predicate demand

> [!rule] MUD-ITER-004 — Semantic-order predicate demand
> Ordered exists tests from the first semantic position until true; ordered forall until false. Unordered exists/forall evaluate every predicate in the same view, preserving independent faults. Count examines all. Min searches from the first semantic end and max from the last in reverse, stopping at their first accepted witness. Source production, capture/validation and step computation remain required before this search.

Skipped predicate instances contribute no reads or faults. A demanded fault stops dependent ordered evaluation and propagates; unordered independent computations combine their error occurrences without using technical enumeration order to skip work. Ordinary source/result admission and static checking of every predicate remain mandatory. Source errors cannot be skipped by a witness, and establishing source order can still require examining/sorting the complete input. These extrema filter an already ordered source; they do not compute arbitrary minima of an unsorted collection without that work.

## Inactive-rule pruning in predicates

Canonical Boolean pruning and ordered operand demand follow [[21-expressions]].
A wholly erased predicate closes to true for each actual source witness: it
no longer filters that witness. Thus on a nonempty source wholly erased exists
and forall predicates yield true; count accepts all occurrences and extrema
retain their normal first/last witnesses. An empty source still yields exists
false, forall true, count zero and empty extrema. Pruning cannot manufacture
a witness, erase a demanded prefix fault or waive source/body proof obligations.

Stored Bool captures are ordinary values; transparent derived predicates retain
their registered pruning context. Domain/collection value boundaries close
erasure before transformation rather than deleting source occurrences.

## Executable and local traversal

> [!rule] MUD-ITER-003 — Order determines iteration observation
> An ordered traversal evaluates each pure non-stochastic if immediately before
> that iteration, observing preceding sequential effects in the private delta.
> An unordered traversal's filters observe one initial snapshot; accepted
> iterations produce simultaneous contributions under ordinary composition.

Consequently for each with if is not universally equivalent to first materializing
a pure selection. Source membership remains captured even when effects alter
the underlying collection; current access/activity and generation obligations
still govern effects on captured identities. Conflicting unordered contributions
use the enclosing protected rollback contract, not an arbitrary iteration order.

EffectBlock traversal has the enclosing authority and no additional permissions.
LocalForEach inside ValueBlock instead has LocalStatementBlock grouping and may
mutate only permitted private storage. Neither iteration nor filter bindings
become world fields, public participants or persistent memory. Every body must
meet its owner's obligations; grouping does not add a separate error channel.

## Signed progression

At runtime evaluate a compatible signed step once before traversal and keep it
fixed. A point step is a difference of its underlying linear magnitude; a Nat
interval can use an Int difference. A demonstrably zero step is a static error;
an admitted runtime step evaluating to zero faults with progression-step-zero
before traversal. A stepped domain instead requires a static nonzero difference.

Positive progression anchors at the lower bound, negative at the upper; an open
initial endpoint advances once. Emit only admitted in-bound candidates, ending
before the first outside one. `[1..8] by 2` visits 1,3,5,7 and by -3 visits
8,5,2. Reaching the far endpoint exactly is not required. Inverted bounds are
empty, never descending syntax.

Only Nat/Int and Money progression have the fixed default increments 1 and
0.01. Num needs an explicit exact step; Rum numeric progression is invalid,
while explicit finite Rum collections are enumerable without by. Discontinuous
segments restart the step and reverse segment visit order for a negative step.
A cyclic point source visits one fundamental period and cannot wrap forever.

## Diagnostics and evidence

Reject missing colon, pattern mismatch, non-Bool/stochastic predicate, infinite
or nonenumerable source, unproved mandatory obligations, incompatible/zero step,
missing successor, Rum progression and by on a source without progression.
No warning is required solely because valid Boolean pruning can affect a predicate.
Random-point cache/retry details remain
[[../notes/questions/Q-032-a-reproducible-randomness|Q-032]] and do not permit
random filters or change the admitted observation contract.

[[types/typing-cases.yaml]] and finite demand/pruning/interval certificates cover source
admission, empty results, pattern projections and erasure boundaries. Source
AST/grammar coverage retains ExpressionBlock predicates, mandatory separators
and LocalForEach/ForEachEffect. [[effects/README]] covers private/sequential
and simultaneous composition; it does not execute general source traversal.
