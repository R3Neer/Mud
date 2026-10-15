---
title: Boolean rules
tags:
  - mud/specification
status: current
normative: true
depends-on:
  - "[[10-names-and-anchors]]"
  - "[[11-type-system]]"
  - "[[15-fields-and-mutability]]"
  - "[[20-blocks-and-recovery]]"
  - "[[21-expressions]]"
  - "[[22-quantifiers-and-iteration]]"
questions:
  - Q-030
decisions:
  - D-176
  - D-167
  - D-168
  - D-166
  - D-006
  - D-021
  - D-022
  - D-036
  - D-041
  - D-044
  - D-048
  - D-063
  - D-071
  - D-087
  - D-096
  - D-114
  - D-134
  - D-136
  - D-137
  - D-142
  - D-150
  - D-152
  - D-155
---

# 23. Boolean rules

## Pure query declarations

A Boolean rule has explicit caller-supplied `for` roles, optional read-only
`given` values and one pure Bool result. It is distinct from reactive and always
rules, whose participants are automatically bound with on.

```mud
rule CanSpend for account: Account given amount: Money {
    account.balance >= amount
}
```

Account is a visible thing type with a Money balance field accessible to the
rule's declaring part. The rule may read a mutable stored field without gaining
write authority. False is an ordinary result, not a refusal or computing error.

> [!rule] MUD-RULE-001 — Pure Boolean signature
> A Boolean rule must have a pure singleton-Bool body, explicit names for every
> for/given slot, and no outer mutable receiver or given capability. It must
> not declare on/when/then clauses or execute real world effects. Its permitted
> queries and dependencies must satisfy their own static contracts.

## Receivers, arguments and selection

For roles can have any admitted declared value type with domain and collection
shape. Ordinary thing roles retain strict membership; collection roles are not
implicitly projected into unqualified member names. Inner capabilities retain
their ordinary contract meanings but cannot authorize writes from a pure body.
Given values have neither outer nor inner mutability. Defaults are explicit
closed pure deterministic static values, independent of participants, other
given values, locals and mutable world state.

Bind ordered positional receivers or the exact exhaustive named receiver form
without mixing modes. Positional given arguments may precede named arguments;
after a named argument no positional one follows. Named arguments may omit
intermediate explicit defaults, while positional omission requires a complete
defaulted suffix. Unknown/repeated names and missing required slots are errors.
Every supplied value checks the full type/domain/cardinality/permission contract.
For an otherwise statically admitted call, an out-of-domain runtime
Boolean-rule given produces its established false admission
result; a computing fault obtaining that argument is not false.

Select one declaration from the first nonempty nominal lookup level using the
supplied receivers and actually written given arguments. Candidate-local literal
contexts and generic constraints remain separate. Missing required arguments
exclude a candidate; unknown compatibility/inference cannot manufacture its
exclusion. Expected results, defaults' values, bodies and runtime subtypes do
not break ambiguity. Unlike alias operator specificity, homonymous call selection
introduces no most-specific fallback.

## Body checking and dependency summary

Let C be the declaring environment with bound signature inputs, Gamma its local
contracts, epsilon a dependency/effect summary and O the proof obligations.
Using the shared judgement, require `C |- body <= Bool [1] |> (epsilon,O)` with
Expression permissions and all applicable obligations discharged. A required
static owner additionally imposes static eligibility; a runtime pure query is
not automatically a closed constant calculation.

ExpressionBlock locals are immutable sequential derivations: each becomes
available after its declaration, without forward reference, cycles, shadowing
or assignment. Live derived reads use their registered definition in the call's
coherent view; captured stored values retain their capture semantics where
their owning form permits them. Subordinate blocks, calls and handlers cannot
escape pure permissions.

The body may use admitted look/sublook queries, Boolean rules, quantifiers,
imagine and eventually. Speculative queries retain their isolation/admission
contracts and are not real action execution. Direct stochastic calculations
or reads of stochastic derived fields are invalid in this condition context;
ordinary captured stored values do not replay their historical random production.
Unknown foreign effects cannot establish purity. Dependencies include actual
derived reads, transitive queries, domains and availability conditions; a compiler
must not conceal them behind locals or cached results.

Contextual dynamic-call impact follows [[types/contextual-call-analysis]].
Finite source/application and recursive body certification follow
[[types/finite-static-certification]] and [[types/termination-certification]].
Deeper eventually state-profile design remains Q-030. Required evidence is not waived;
this chapter supplies neither a causal search algorithm nor an implementation-
specific admission heuristic.

## Normal Bool, Fault and inactive pruning

A successfully evaluated active rule returns one ordinary Bool. False does not
itself create Refusal. A computing error yields Fault with Error occurrences,
handled under [[20-blocks-and-recovery]]; a then recovery must supply the Bool
contract and remain pure. Raise is permitted with a valid Error payload and
does not infer a normal type without the surrounding result context.

> [!rule] MUD-RULE-002 — Inactive calls erase syntax, not truth
> A non-effective Boolean-rule call is structurally erased in the canonical
> Boolean context. Its receiver and arguments are not dynamically evaluated,
> while the original source remains resolved and statically checked. Erasure
> is not a storable third Bool or an ordinary constant return value.

Negation preserves erasure; and/or retain surviving operands under their original
left-to-right demand. A decisive ordinary left operand short-circuits; an erased
operand cannot decide one. Original equality/inequality/xor operands retain
their prescribed once-only demand. Wholly erased Boolean data closes to true.
An active rule's result is an ordinary value boundary, not transparency through
arbitrary called bodies.

A `:=` Boolean derivation can transmit erased context on actual read, including
its demanded prefix calculations/faults. `=` captures ordinary Bool. Identical
shape confirmation remains transparent; domains and value-consuming transforms
close erasure before operating. Quantifier predicates use the source-witness
contract in [[22-quantifiers-and-iteration]]: erased filters never manufacture
witnesses or excuse static obligations. No pruning-sensitivity warning is required.

Pure recursive bodies retain their ordinary static result contract. [[types/termination-certification]] supplies their ranking search and evidence; it does not infer an ambiguous result, introduce nominal types or bypass independent owner-specific acyclicity.

## Generic and callable contracts

Boolean rules may declare static type parameters with the ordinary bounds,
finite application closure and generic inference rules. Their bodies are checked
using only established bounds; calls specialize before input/body checking.
Generic application does not introduce another rule anchor or lifecycle identity.

A rule descriptor may have BooleanRuleCallable contract. Storing it does not
prebind receivers/given. Inputs are contravariant under admitted read-only
substitution, purity/determinism guarantees remain required, and named invocation
needs one unequivocal static slot-name contract across every possible alternative.
Runtime inspection of descriptors cannot recover names or select new targets.
A Boolean rule is not a production host action/look/message endpoint.

## Activity, reflection and caching limits

The canonical rule has explicit declaration activity and whole-declaration hard
dependency suspension. Create/destroy refers to that existing definition, not
an individual call or participant instance. Declaration category and anchor
`rule::<qualified-name>` survive reactivation. Metadata is read-only, separate
from result values and not runtime condition storage.

Memoization is permitted only when it preserves the same view, inputs, domains,
availability, dependency observations, errors and demand. It cannot merge
distinct source occurrences or turn a skipped argument into work. No general
cache layout, invalidation protocol or causal scheduler is defined here.

## Counterexamples and evidence

`rule Bad for mut total: Num { total += 1 }` violates pure receiver/body rules.
`on` cannot replace `for` in a query signature. Text-only recovery and returning
empty instead of singleton Bool are invalid. An inactive call containing an
invalid argument remains statically invalid even though it skips argument
evaluation at runtime. Two accepted homonymous signatures cannot be selected
using an expected Bool or body behavior.

[[types/typing-cases.yaml]], finite call/generic/pruning certificates and the
syntax model cover signature selection, named binding, contextual input checks,
pure bodies and value/erasure boundaries. These are scoped evidence, not a full
recursive admission solver or Boolean evaluator. Nominal HIR retains original
rule/participant identities and scopes without effect summaries or cached values.

Explicit optional extraction can contribute erasure under
[[21-expressions#Optional extraction and omission]]. Its source is evaluated to
establish absence, unlike an inactive Boolean-rule call whose arguments are
not demanded. Once erasure reaches the Boolean core, the same demand, negation,
closure and derived/stored boundaries apply. A wholly erased guard closes true
and does not establish that an optional receiver exists.
