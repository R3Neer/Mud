---
id: D-042
title: "Shares, root and results"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-002"
  - "Q-003"
  - "Q-004"
  - "Q-022"
  - "Q-023"
  - "Q-046"
  - "Q-059"
affects:
  - "public boundary, effects, action requests and root semantics"
---
# ADR-042 — Shares, root and results

- Amended by: [[ADR-127-actionreply-only-action-results|D-127]].

- Amended by: [[ADR-119-invocation-owned-completion-and-imagine|D-119]].

- Amended by: [[ADR-118-action-replies-refusals-and-errors|D-118]].

- Amended by: [[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]]
- Related to: [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]]
- Amended by: [[notes/decisions/ADR-058-temporal-triggers-changes-and-reactive-old|D-058]], [[notes/decisions/ADR-059-magnitude-intervals-and-inverted-endpoints|D-059]], [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]]
- Further amended by: [[notes/decisions/ADR-063-signatures-given-and-joint-on-bindings|D-063]] and [[notes/decisions/ADR-066-static-values-and-local-bindings-in-then|D-066]]
- Related questions: Q-002, Q-003, Q-004, Q-022, Q-023, Q-046, Q-059
- Documents concerned: public boundary, effects, request shares, semantics of the root

- Developed by: [[ADR-110-tentative-wave-journal-and-atomic-confirmation|D-110]].

- Amended by: [[ADR-137-live-locals-stored-inference-and-binding-patterns|D-137]].

## Context

One action is the MUD’s writing boundary. Its contract one must distinguish between expected inadmissibility and that of a request the errors that prevent one from obtaining a state valid.

- Amended by: [[ADR-133-provisional-messages-and-scope-aware-tickets|D-133]].

## Decision

```mud
action Recruit for kingdom: Kingdom [mut]
given
    amount: Nat in 1..100
{
    if kingdom.treasury >= amount * kingdom.recruitmentCost
    then {
        kingdom.treasury -= amount * kingdom.recruitmentCost
        kingdom.soldiers += amount
    }
    after kingdom.soldiers >= old kingdom.soldiers
}
```

One action:

- declares participants via `for`;
- can declare values `given` and its domains;
- may state `if` and `after`;
- must state `then`;
- does not state `when` nor does it activate automatically;
- one `action` It can be applied for from abroad and, in that case, the causal resolution root;
- an `action` or `subaction` invoked from a `then` joins the already active causal resolution and does not open an independent root;
- the resolution It is atomic in its entirety, together with all its waves.

Participants are recipients, while `given` values are arguments in accordance with D-036 and D-063. When an action starts, roles are linked by identity, value or place according to their contract; types, cardinalities and capabilities are checked. Omitted `given` values use their static defaults, which are evaluated and validated before `if`. A role with outer `mut` retains its original receiver place as the destination for effects and requires that place to be storable and externally mutable. A `given` value outside its domain or a false `if` has no effect.

Within then, stored locals capture their initial value when the slot is created. Calculated locals register live derivations and read the applicable private sequential view at each use. Both resolve names textually and do not create world fields.

### Unified sequence of `then`

There is no semantic distinction between elementary and compound actions. A `then` is an ordered sequence of consequences and may combine local bindings, direct effects, calls to `action` or `subaction`, and `for each` traversals.

Each statement reads the private delta visible at its textual position. An internal call is validated and executed there, observes the preceding private effects, and adds its own effects to the resolution. It is atomic and preserves those effects for subsequent statements; it does not open a separate transaction.

Each invocation checks after against its own stabilized causal completion projection before the caller resumes. Private and consolidated wave changes remain tentative until stabilisation, all invariants and these postconditions succeed; the complete transition is then confirmed atomically. A non-success outer request discards the entire journal and delivery; a child non-success rolls back its contribution scope before explicit reply observation, or propagates when called as a bare effect. Call analysis must prevent executable cycles; Q-023 leaves the proof of acyclicity and impact open when selecting a `callable` descriptor is a dynamic property rather than merely a callability check.

### Conditions and results

Every invocation yields ActionReply = Success | Refusal | Errors. A false if is IfRefusal, a false after is AfterRefusal and a false always is AlwaysRefusal. Computing failures produce Error occurrences; stored-domain violations and effect conflicts are errors. Each refusal/error carries reason and mandatory Declaration origin; ConditionRefusal retains only the actually evaluated final Boolean expression tree. No false condition is captured by otherwise.

Otherwise handlers belong to expression/value/effect blocks and handle Error values. They use optional on and if, then or raise exclusively. A plain Text diagnostic is invalid. A Refusal never enters an Error handler.

A successful outer request commits atomically. A refused or unhandled erroneous request discards its complete tentative world, suppresses unpublished occurrences and marks published pending tickets Dropped. Nested invocation and speculative execution return the same ordinary reply type without opening independent commits. Actions and subactions return only ActionReply; no additional domain return value is admitted.

In action/test after, old retains its established entry-view contract; reactive old still compares wave snapshots. Computing an invalid operation is distinct from successfully obtaining empty or false.

## Consequences

- Refusal models an unmet condition; Errors model unsuccessful computation.
- Atomicity includes root, waves, `always`, `after` and upcoming events.
- False after rolls back its invocation scope; an unhandled outer Refusal rolls back the complete resolution.
- Actions and subactions have one ActionReply result; state effects and message outputs are not extra return values.

## Verification

1. Acceptance, rejection of domain from `given`, rejection due to `if` and rejection of `after`.
2. Full rollback of a action rejected in the end.
3. `then` a mixture of effects, local elements and calls in textual order.
4. Spread of the delta private via internal calls and the rejection of a executable cycle calls.
5. `old` note the action outer layer, not an intermediate layer.
6. Linking a receiver-a changeable place and the rejection of a receiver let it just be a value.
7. Normalised inverse interval to `empty` without failure intrinsic.
8. Distinguishing rejection caused by a false condition involving `empty` from failure caused by state outside its domain.
9. Mandatory reason/origin on Refusal/Error; no extra Success components.
10. Otherwise captures Error occurrences rather than false conditions.

## Amendment current by D-096

The distinction between elementary and compound actions is removed from the semantics. Every `then` is an ordered sequence that can combine effects, places, calls and `for each`. An internal call observes the exact delta and contributes to effect resolution. `action` retains the ability to operate at the root; `subaction` can be reused from any `then` but cannot operate at the root. Nested after runs at its own invocation completion; the outer resolution is the sole commit boundary.

