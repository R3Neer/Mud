---
title: Blocks and error recovery
tags:
  - mud/specification
status: current
normative: true
depends-on:
  - "[[08-concrete-grammar]]"
  - "[[09-abstract-syntax]]"
  - "[[11-type-system]]"
  - "[[15-fields-and-mutability]]"
  - "[[21-expressions]]"
  - "[[28-effects]]"
questions:
  - Q-007
decisions:
  - D-181
  - D-172
  - D-169
  - D-167
  - D-168
  - D-165
  - D-066
  - D-071
  - D-088
  - D-101
  - D-109
  - D-118
  - D-120
  - D-121
  - D-123
  - D-124
  - D-127
  - D-128
  - D-136
  - D-137
  - D-147
  - D-152
---

# 20. Blocks and error recovery

## Scope and owners

This chapter defines the common block/result/error contracts. Expression typing
is [[21-expressions]]; place permissions are [[15-fields-and-mutability]];
protected effect boundaries and composition are [[28-effects]]. These interfaces
do not define causal occurrence generation, wave discovery or adapter protocols.

```mud
let result: Num = {
    let divisor: Num = 0
    10 / divisor
} otherwise then 0
```

A block owner fixes its normal result contract and mode. ExpressionBlock has
ordered immutable pure preamble derivations and one final expression. ValueBlock
admits ordered private stored/computed locals, permitted private mutations and
iterations, then one final value. EffectBlock has ordered local/effect statements
and its effect completion contract. Short forms normalize to the applicable
category, rather than gaining permissions from omitted braces.

Declaration, schema and metadata braces are not evaluated normal-result owners.
LocalStatementBlock groups statements within the owning value computation and
shares its error channel; it does not acquire an independent handler list.
A following `otherwise` attaches to the nearest complete eligible block.
Explicit braces must delimit a nested handler when an outer chain is intended.

## Static modes and checking judgement

Let C=(Gamma,Sigma,Phi,delta) be the type environment, resolved catalogue,
established facts and owner mode from [[15-fields-and-mutability]]. Let tau be
the owner's well-formed expected normal contract, epsilon its symbolic effect
summary and O the required obligations. Write
`C |- b <= tau |> (epsilon,O)` for successful checking of a block b. This
judgement includes handlers and every written continuation, even when execution
may stop before reaching that continuation.

| Mode | Permitted block computation |
| --- | --- |
| Expression | Externally pure calculation; no storage writes or real action execution. |
| Value(L) | Calculation and mutations confined to the owner's private region L. |
| Effect | Authorised local/world effects and real calls under the enclosing contract. |
| Static requirement | Additional closed, deterministic, statically evaluable requirement on an Expression/Value computation. |

> [!rule] MUD-BLOCK-001 — Inherited owner restrictions
> Every subordinate initializer, block, call, handler and foreign region must
> obey the enclosing owner's permissions and static requirements. Recovery and
> explicit error production cannot grant mutation, temporal, random or root
> authority absent from that context.

Error production is possible in all modes. An effectful operation hidden in a
local initializer remains effectful. A confined value computation may update
an enclosing private local in the same region, but cannot update captured
external storage. Real action execution in an Effect initializer may capture
ActionReply; a pure live derivation cannot replay those world effects.

Body and handler completion follow [[types/termination-certification]]. Normal, Fault and applicable Refusal completion are distinct from guaranteed success; every recovery call must satisfy the same ranking obligations.

Functional selector/result sharing follows [[17-dictionaries]]. It extends only
normal direct-preamble bindings. Whole-selector recovery does not restore locals
from its rolled-back scope; result access still requires definite availability.
A normally recovered local RHS may supply a reusable normal value. Per-application
reuse preserves dependency/fault demand and never caches a Fault as Normal.

## Normal and Fault outcomes

Let v be a finite ordinary value admitted by tau, and let E be a finite nonempty
sequence of Error occurrences. An occurrence comprises an Error value and its
distinct semantic occurrence identity/provenance; the representation is not a
new source type or required physical record. The outcome alternatives are:

`Normal(v)` or `Fault(E)`.

For an effect block, Normal denotes its successful effect completion rather than
an invented source Unit return value. The equivalent channel representation
uses Error [*]: empty accompanies a normal result, nonempty makes that result
unavailable. No partial normal value is available on Fault.

> [!rule] MUD-BLOCK-002 — Separate values and fault production
> Producing Error, Errors, false, empty or Refusal as an ordinary value does not
> itself raise a fault. A computing failure or admitted explicit `raise` produces
> Error occurrences and no normal result. Refusal is not Error and cannot be
> selected by `otherwise`.

Dependent sequential evaluation stops at its first failed dependency. Independent
concurrent computations can contribute distinct occurrences. Equal Error values
are not deduplicated; occurrence selection and causal diagnostics preserve their
defined stable provenance. No ordering modifier is added to the source Errors
alias merely because traversal has a canonical order.

ActionReply is the nominal alias over Success, Refusal and nonempty Errors.
An action's explicit result capture is an observation boundary: its Errors
alternative can be an ordinary captured value. Bare effect calls retain their
non-success propagation contract. A false successfully evaluated owning if,
after or always condition yields its specified Refusal; an error while computing
the condition has no Bool result and uses the error channel. Static diagnostics
are not runtime Error values.

Diagnostic origin/argument descriptors crossing a public boundary retain only the component-scoped provenance exception MUD-TYPE-042 in [[11-type-system]]. Private helper failures need not lose their origin; diagnostic receipt grants no private-schema or operation authority.

## Explicit raise

Define ErrorPayload as the existing checking contract admitting one Error or
a nonempty Errors-compatible collection; this is metalanguage, not a new source
type. To check `raise b` against any well-formed tau, check b against ErrorPayload
in C and retain its effect summary/obligations. No inhabitant of tau is created.

> [!rule] MUD-BLOCK-003 — Raise without a normal value
> A successful raise payload supplies Fault with its distinct Error occurrences.
> String, Refusal and empty cannot be successful payloads. Without a determining
> normal-result context, raise alone cannot infer a nominal result type. There
> is no storable bottom/never value or implicit return, break, continue or finally.

Payload computation uses its own nearest protected block first. If that
computation faults, ordinary recovery determines whether a payload ever becomes
available. A successful payload is flattened as Error occurrences, preserving
multiplicity. The producing block then handles the explicit fault; unhandled
occurrences propagate through the existing block/call/invocation boundaries.
Source continuations remain statically checked. A required static owner must
complete normally after applicable recovery; an unhandled raise makes it
inadmissible.

## Handler signatures and scopes

An `otherwise` clause has optional `on` bindings, optional `if` and exactly one
`then` or `raise` branch. Each role is an immutable clause-local value typed by
an alias specialising Error. All roles must bind jointly before evaluating the
filter. Multiple roles do not impose implicit distinctness: one occurrence can
satisfy overlapping role types. No `on` means catch-all once per pending
occurrence, not one invocation receiving the entire Errors aggregate.

The optional filter is an externally pure singleton-Bool ExpressionBlock under the owner's restrictions. False leaves
the selected occurrences pending. A filter fault propagates outward and does
not reenter this chain. Handler bindings and valid enclosing locals are in scope;
failed protected-body locals, partially bound patterns and partial foreign
exports are unavailable after rollback.

> [!rule] MUD-BLOCK-004 — Category-preserving recovery
> A `then` recovery checks against the protected normal-result contract and
> owner mode. A `raise` recovery checks ErrorPayload under that mode. Both
> branches in one clause, String-only diagnostics and Refusal `on` bindings are
> static errors. Handler locals create no public declaration anchors.

Expression recovery remains pure and supplies the expected result. Value
recovery may use only its permitted private region and supplies the expected
value. Effect recovery can make only authorised effects. An `otherwise raise`
short form is catch-all sugar; nested payload value blocks retain their own
handlers and are not flattened into the surrounding chain.

## Occurrence selection and result composition

Let Pending initially contain the protected block's distinct Error occurrences.
Visit clauses in textual order. For each clause, enumerate jointly compatible
role-binding tuples in stable causal occurrence order; select only currently
pending occurrences. An accepted tuple executes one branch and consumes the
set of occurrences selected by that tuple once. A shared occurrence bound to
two roles is consumed once. Already consumed occurrences cannot be selected
again. False filters leave their tuple's occurrences pending for later matches.
Catch-all follows the same per-occurrence rule.

Successful recovery proposals share one tentative recovery scope. For expression
and value owners they propose one normal result slot: equal compatible values
agree; incompatible proposals yield a composition error. There is no arbitrary
first/last result preference. Effect proposals use ordinary common-view
composition, including semantic destinations and their conflict rules.

> [!rule] MUD-BLOCK-005 — Protected rollback and outward propagation
> Roll back the failed protected work before running handlers. Earlier successful
> enclosing work remains tentative. If any original occurrence remains unhandled
> or any handler/filter produces new errors, discard the recovery scope and
> propagate pending original plus new occurrences outward. New handler errors
> cannot be caught by that same chain.

If all original occurrences are handled and proposals compose without new
errors, resume with the recovered normal result/effect completion. Successfully
handled original occurrences do not reappear merely because another pending
occurrence propagates. Successful recovery cannot publish earlier failed writes.
It remains tentative and is discarded if its containing scope subsequently fails.
The details of causal occurrence discovery and invocation completion remain
outside this shared block contract.

## Examples and counterexamples

The following are fragments with stated contracts. `failure` is one existing
concrete Error value, `refusal` one Refusal value, and `issue` a handler binding:

```mud
let result: Num = { raise failure } otherwise then 0
let errors: Error = failure       # ordinary value; no implicit fault
let flag: Bool = false            # ordinary value; no intrinsic refusal
```

The first fragment checks as Num and recovers zero; raise does not construct
a Num. To wrap an Error, an explicit concrete Error subtype can store `issue`
in its inherited optional cause component and be raised. Cause storage does not
automatically reproduce the original occurrence in the pending set.

```mud
let result: Num = { raise "explanation" } # invalid: String is not ErrorPayload
let result: Num = { raise empty }         # invalid: payload cannot be empty
let result: Num = { raise refusal }       # invalid: Refusal is not Error
```

Boundary example: two equal-valued Error occurrences each match a catch-all;
they require two recoveries. Two accepted fallbacks proposing 1 and 2 for one
protected Num result conflict. A false filter consumes neither occurrence.
An overlapping two-role binding can consume one original occurrence once.
A handler-raised error goes outward even if a later clause could match its type.

## Error catalogue boundary and evidence

The exhaustive semantic error subtype/code catalogue and resource/engine-defect
boundary remain [[../notes/questions/Q-007-f-technical-failures|Q-007]].
They do not alter Error-only matching, occurrence multiplicity or this block
typing contract. Foreign protocols and cancellation are not defined here.

[[types/typing-cases.yaml]] covers Normal/Fault typing, Error versus Refusal,
raise context/payload restrictions, handler branch alternatives and pure modes.
[[syntax/test_raise_contract.py]] and [[syntax/test_local_contract.py]] check
the declared AST/grammar preservation of raise, nested handlers and local
owners. [[effects/README]] supplies rollback/composition traces; their checker
validates supplied certificates rather than executing a causal runtime.
