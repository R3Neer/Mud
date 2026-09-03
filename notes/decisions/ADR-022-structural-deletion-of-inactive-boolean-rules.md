---
id: D-022
title: "Structural deletion of inactive Boolean rules"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-050"
affects:
  - "future chapters 19, 21 and 26"
---
# ADR-022 — Structural deletion of inactive Boolean rules

- Related open-ended question: [[notes/questions/Q-050-b-pruning-in-remaining-boolean-operators|Q-050]]
- Decision related: [[notes/decisions/ADR-021-cycle-logical-lifespan-and-suspension-by-department|D-021]]
- Documents affected: future Chapters 19, 21 and 26

## Context

One Boolean rule may become inactive due to `destroy` or by the suspension of a branch. Their calls should not always turn into `true` nor cause the whole declaration is invalid. The intention is that the expression should behave as if the clause invoking the rule had been deleted.

The required neutral element depends on the external operator:

$$
p\land\top=p
$$

$$
p\lor\bot=p
$$

Therefore, no value A standard Boolean value represents deletion on its own in all contexts.

## Decision

The assessment introduces a metalinguistic marker:

$$
\mathsf{erased}
$$

which means ‘this syntactic fragment has been deleted’. It is not a value from MUD, cannot be stored and does not belong to `Bool`.

Before erasure, Boolean expressions are reduced to a canonical form:

$$
b ::=
\top
\mid
\bot
\mid
p
\mid
\neg b
\mid
b\land b
\mid
b\lor b
$$

One call to one Boolean rule which is not effective in $W$ It is pruned:

$$
\operatorname{prune}_W(R(\bar e))
=
\mathsf{erased}
\qquad
\text{si }
\neg\operatorname{effective}_W(R)
$$

The receiver and the arguments of a call deleted rules are not evaluated dynamically. They must, however, be correctly resolved and statically typed, as the rule may become effective again in another world.

## Pruning guidelines

Negation preserves the void:

$$
\operatorname{prune}_W(\neg\mathsf{erased})
=
\mathsf{erased}
$$

Conjunction and disjunction eliminate a deleted operand:

$$
\mathsf{erased}\land b=b
\qquad
b\land\mathsf{erased}=b
$$

$$
\mathsf{erased}\lor b=b
\qquad
b\lor\mathsf{erased}=b
$$

If both operands are cleared:

$$
\mathsf{erased}\land\mathsf{erased}
=
\mathsf{erased}
$$

$$
\mathsf{erased}\lor\mathsf{erased}
=
\mathsf{erased}
$$

When the entire external expression is erased, it is recognised as true:

$$
\operatorname{close}(\mathsf{erased})
=
\top
$$

This means that a deleted condition imposes no restrictions.

## Negation

Yes `R` is inactive:

```mud
not R(x)
```

is reduced:

$$
\neg\mathsf{erased}
\longrightarrow
\mathsf{erased}
\longrightarrow
\top
$$

if it is the outward expression.

In:

```mud
P(x) and not R(x)
```

the result residual is `P(x)`.

## Involvement

The plan is drawn up before pruning:

$$
p\Rightarrow q
\quad\rightsquigarrow\quad
\neg p\lor q
$$

If the previous entry is deleted:

$$
\neg\mathsf{erased}\lor q
\longrightarrow
q
$$

If the consequent is deleted:

$$
\neg p\lor\mathsf{erased}
\longrightarrow
\neg p
$$

## Biconditional and Boolean equality

Boolean equality and the biconditional are canonically defined as:

$$
p\Leftrightarrow q
\quad\rightsquigarrow\quad
(p\land q)\lor(\neg p\land\neg q)
$$

If it is deleted $p$:

$$
(\mathsf{erased}\land q)
\lor
(\neg\mathsf{erased}\land\neg q)
$$

can be summarised as:

$$
q\lor\neg q
=
\top
$$

Therefore, a Boolean equality in which one of the operands is omitted evaluates to true regardless of the other operand.

## Dependence on the canonical form

Pruning does not necessarily preserve all equivalences in classical Boolean algebra. Two classically equivalent trees may produce different residues if they are rewritten before a rule is applied.

The conformance requires:

1. Solve and type out the original expression.
2. Derive operators in canonical kernel form.
3. Prune calls to inactive rules.
4. Close a deleted external record using $\top$.
5. Evaluate the residual Boolean expression.

An optimiser cannot apply a classic rewrite that changes the result of this procedure.

## Alternatives

### Inactive rule equals `true`

It is ruled out because `P or R` would always be true and `not R` it would become false, even if the intention is to remove the condition.

### A gender-neutral name chosen directly by the father

It describes intuition well, but it is not sufficient for negation, implication or equality. The mark `erased` It generalises the same idea to a structural path.

### Suspend all declaration which calls for the ruler

It is ruled out because it would prevent a formula from continuing to function under the other conditions that still apply.

## Unresolved issues

- Elaboration exact translation of `!=`, `xor` and other Boolean operators.
- Pruning within quantifiers and Boolean aggregations.
- Interaction with `allowed`, `eventually` and sub-expression errors that disappear.
- Diagnostics or warnings for expressions that are particularly sensitive to their syntactic form.

## Future verification

The suite must cover:

1. A rule that is inactive as an outward expression.
2. Rule inactive under external and nested negation.
3. Left and right positions of `and` y `or`.
4. Two operands deleted.
5. Antecedent and consequent of implication.
6. Both sides of a Boolean equality.
7. Lack of dynamic assessment of receiver y `given` deleted.
8. Reinstatement of the rule and resumption of the standard assessment.
9. Rejection of optimisations that alter the canonical pruning.

