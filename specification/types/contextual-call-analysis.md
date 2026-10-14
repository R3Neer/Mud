---
title: Contextual static callable analysis
status: proposed
normative: true
depends-on:
  - "[[../10-names-and-anchors]]"
  - "[[../11-type-system]]"
  - "[[../15-fields-and-mutability]]"
questions:
  - Q-029
decisions:
  - D-166
  - D-114
  - D-123
  - D-155
  - D-165
---

# Contextual static callable analysis

## Scope and inputs

This procedure computes conservative destinations and dependency/effect summaries
for a linked, resolved programme. Ordinary lookup, candidate selection, generic
application closure and signature checking retain their canonical contracts.
It does not execute the source, discover host operations or schedule causal work.

```mud
subaction Dispatch for account: Account given op: Account.action() {
    then account.op()
}
subaction A for account: Account { then account.Dispatch(B) }
subaction C for account: Account { then account.Dispatch(A) }
```

B is a compatible leaf operation. The contexts Dispatch(A) and Dispatch(B) are
distinct; C → Dispatch(A) → A → Dispatch(B) → B is acyclic even though merging
all Dispatch invocations creates an apparent declaration cycle.

Let N be the finite catalogue of callable declarations with their admitted exact
static generic applications. A destination is one such identity, not its display
name or a new public anchor. Sort identities by their canonical encodings.
Let S be the finite set of callable-valued signature slots and statically written
component/projection paths relevant to calls. A recursive schema reference is
represented by its existing origin/type node; do not invent successively deeper
paths absent from the source. Unrepresented projections use the conservative
contract fallback below.

> [!rule] MUD-CALL-001 — Finite nominal contexts
> A context key consists of the applied declaration and, for each relevant input
> slot, a canonical subset of N. It records destinations, not arbitrary numeric
> arguments, world states, materialisations or runtime instances. Known distinct
> input destination tuples remain distinct contexts; an uncertain slot contains
> every possible destination established by its conservative analysis.

There are finitely many keys: each slot has at most 2^|N| subsets. Empty is
ordinary absence, not evidence of a callable target. Signature/cardinality
checks independently decide whether that absence is admitted.

## Destination transfer and completion

For a contract c at site s, define U(c,s) as every catalogue destination not
proved impossible by category, complete signature/domain/shape, static generic
arguments and the site's legal provenance/access constraints. An unproved
compatibility cannot remove a destination. Membership of this upper bound does
not establish callable substitution or grant permission: those remain separate
mandatory checks. Diagnostic-only references cannot acquire invocation authority.
Current inactivity, a runtime sample, expected output or import order cannot
exclude a future possible target.

Use the following transfers, preserving the original source's static checks:

| Source form | Destination upper bound |
| --- | --- |
| Resolved concrete callable reference/application | Its singleton catalogue destination. |
| Signature input | The context's subset, or U(c,s) for an unconstrained entry. |
| Immutable local/capture | The bound source's transferred subset. |
| Live derivation | Its definition's transfer under the applicable lexical inputs; no source execution. |
| Stored mutable slot | Union of its initializer and every potentially reaching admitted write; flow locations remain distinct. |
| Known structural/container construction or constant-key projection | Transfer its supplied components/entries; unknown selections join possible members. |
| Normal alternatives, functional query results and recovery results | Union their possible normal destination subsets; Fault has no normal destination. |
| Demonstrated narrowing | Remove only destinations proved impossible by that flow fact. |
| Widening/representation change | Preserve possible provenance, then apply proved target restrictions; never manufacture authority. |
| Other source, opaque projection or unknown legal producer | U(c,s). |

At a selected call, transfer written arguments and explicit effective defaults
into their formal slots, using the selected signature's binding rules. Generate
one context per known call tuple; uncertain subsets remain conservative. Pure
callee result summaries feed callers. Include every potentially reachable body,
handler and default under its original permissions. Only completed static
constant/flow evidence can eliminate an impossible branch. Inactive pruning
never excuses the original static call checks or licenses an activity-based
permanent graph exclusion.

Start internal facts and result summaries at empty, seed every reachable entry
with its declared allowed inputs, and use U for unconstrained inputs. Process
pending sites in canonical source-origin/key order. Add targets, contexts, edges
and summary facts by union; enqueue dependants only when a fact grows. Each fact
ranges over the fixed finite catalogue, slots, source sites and summary vocabulary.
Stop precisely when the worklist is empty and no fact grows. This least fixed
point is reproducible; there is no iteration/depth/collection-size cutoff.
Incomplete tool resources supply no completed verdict.

## Graph obligations

> [!rule] MUD-CALL-002 — Check contextual edges
> For every remaining destination, add the actual call/admissibility edge to its
> context, then compute strongly connected components. An executable component
> involving action/subaction, test or speculative invocation/admissibility must
> satisfy its established acyclicity requirement; a self-edge counts as a cycle.
> Context separation cannot excuse a remaining cycle.

Pure recursive components require their separate normative termination
certificate under Q-029. Computed domains and calculated/local/schema dependency
graphs retain their own acyclicity requirements; a recursive proof cannot waive
a prohibition applying to that owning construct. Declarative when sources are
causal dependencies, not source invocation edges. Causal oscillation or resolution
completion is not proved by this graph.

A direct internal action call creates no additional exterior root. Descriptor
widening preserves normal/sub and privacy/root-capability obligations for all
alternatives. An unknown target set is not automatically rejection: a completed
conservative graph may prove every required obligation. A remaining cycle or
unproved mandatory obligation prevents admission.

## Dependency and effect summaries

> [!rule] MUD-CALL-003 — Substitute and join complete summaries
> At every call edge, substitute the actual receiver/place bindings into the
> callee's read, write, domain, availability, stochastic and isolated-effect
> summaries. Join every remaining alternative, including handlers. A signature
> alone cannot hide body dependencies or grant stronger write authority.

Use the primitive summaries of chapters 15/21/28. Retain concrete roots, known
component/key paths and generations where established. Unknown keys/members use
wildcard regions encompassing their possible destinations, never invented
nonoverlap. Recursive pure reads close over the finite catalogue of root/schema
origins; repeated traversal uses conservative regions rather than infinitely
expanded paths. Real writes, confined local writes and isolated speculative
writes remain separate modes. Action call paths are finite after acyclicity
checking; their place substitutions preserve textual-site authority.

Compute these finite summary unions to the same no-growth fixed point, then run
all mandatory caller checks. Stored-cardinality preservation remains a proof
obligation; residual conflict/overlap retains its existing consolidation policy.
A missing checked/trusted native summary cannot supply a guessed proof. Foreign
protocols remain owned by their separate contracts.

## Evidence and limits

Finite supplied certificates distinguish separate Dispatch contexts, conservative
open inputs, real cycles, narrowing, absent inputs, joined footprints and wildcard
overlap. They are checked by [[test_contextual_call_witnesses.py]] and reviewed
cases in [[typing-cases.yaml]]. They do not parse/typecheck Mud, extract source
summaries or execute an invocation. Nominal HIR retains its existing identities,
roles and references; contexts and permission proofs are later semantic objects.
