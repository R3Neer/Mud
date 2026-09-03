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

- Amended by: [[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]]
- Related to: [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]]
- Amended by: [[notes/decisions/ADR-058-temporal-triggers-changes-and-reactive-old|D-058]], [[notes/decisions/ADR-059-magnitude-intervals-and-inverted-endpoints|D-059]], [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]]
- Further amended by: [[notes/decisions/ADR-063-signatures-given-and-joint-on-bindings|D-063]] and [[notes/decisions/ADR-066-static-values-and-local-bindings-in-then|D-066]]
- Related questions: Q-002, Q-003, Q-004, Q-022, Q-023, Q-046, Q-059
- Documents concerned: public boundary, effects, request shares, semantics of the root

## Context

One action is the MUD’s writing boundary. Its contract one must distinguish between expected inadmissibility and that of a request the errors that prevent one from obtaining a state valid.

## Decision

```mud
action Recruit for kingdom: Kingdom [mut]
given
    amount: Nat in 1..100
{
    if kingdom.treasury >= amount * kingdom.recruitmentCost
    otherwise "The kingdom cannot afford {amount} recruits"
    then {
        kingdom.treasury -= amount * kingdom.recruitmentCost
        kingdom.soldiers += amount
    }
    after kingdom.soldiers >= old kingdom.soldiers
    otherwise "Recruitment did not increase the army"
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

Within a block `then`, D-066 allows for calculated local links. They are resolved in textual order, reading the delta previous private provision, remain unchanged and do not form part of the state from the world.

### Unified sequence of `then`

There is no semantic distinction between elementary and compound actions. A `then` is an ordered sequence of consequences and may combine local bindings, direct effects, calls to `action` or `subaction`, and `for each` traversals.

Each statement reads the private delta visible at its textual position. An internal call is validated and executed there, observes the preceding private effects, and adds its own effects to the resolution. It is atomic and preserves those effects for subsequent statements; it does not open a separate transaction.

The `after` blocks of all invoked actions and subactions are checked against the final attempted stable state when the complete resolution finishes. Call analysis must prevent executable cycles; Q-023 leaves the proof of acyclicity and impact open when selecting a `callable` descriptor is a dynamic property rather than merely a callability check.

### `after` and `old`

`if` and `after` can be given an `otherwise` reason of type `Text` when false. Omitting it is lawful and implies a suggestion, not a warning, because rejection is a normal response; in that case, the result contains a reason based on the condition and its provenance. The diagnostic is pure and lazy.

`after` is evaluated after all waves against the attempted stable state. If it is false, the result is `rejected`; an error during its evaluation produces `failed`. An error while evaluating `if` or `after` is not captured by `otherwise`, which applies only when the condition has been successfully evaluated as false.

In the context of actions and tests, `old e` reads `e` in the stable state immediately before the action completes and is permitted only within `after`. D-058 adds a different context for `old` within reactive rules, where it compares wave snapshots.

### Results

| Result | Reason |
| --- | --- |
| `accepted` | Request valid, root compatible, stabilisation, invariants and `after` satisfied |
| `rejected` | `given` outside domain, `if` false or `after` false |
| `failed` | Conflict, cycle or oscillation, invalid operation, domain or invalid references, unfulfilled `always`, or propagated semantic failure |

The request returns an object to the external caller whose `state` field contains one of those three results. When it contains `rejected` or `failed`, the object also includes the compulsory `reason: Text` field with a human explanation. Any regulatory case other than `accepted` must provide that reason in accordance with D-061; it may be accompanied by codes and structured reasons.

Every result other than `accepted` restores exactly the previous stable state and publishes no messages or other external effects.

Normalising a linear interval with inverted endpoints to `empty` is valid under D-059 and does not itself produce `failed`. A `given` excluded by its domain, or an `if` or `after` that is false because of that exclusion, produces `rejected`; a domain that leaves a stored value invalid, or an unfulfilled `always` rule, produces `failed` in the tentative state.

## Consequences

- `rejected` is a normal semantic result; `failed` indicates that a valid transition could not be completed.
- Atomicity includes root, waves, `always`, `after` and upcoming events.
- Q-004 is now closed: one `after` 'false' reverses the entire resolution.
- The values of domain returned by a action, if they were to be admitted, they remain open in Q-022.

## Verification

1. Acceptance, rejection of domain from `given`, rejection due to `if` and rejection of `after`.
2. Full rollback of a action rejected in the end.
3. `then` a mixture of effects, local elements and calls in textual order.
4. Spread of the delta private via internal calls and the rejection of a executable cycle calls.
5. `old` note the action outer layer, not an intermediate layer.
6. Linking a receiver-a changeable place and the rejection of a receiver let it just be a value.
7. Normalised inverse interval to `empty` without failure intrinsic.
8. Distinguishing rejection caused by a false condition involving `empty` from failure caused by state outside its domain.
9. Mandatory `reason: Text` for `rejected` and `failed`, and its absence from `accepted`.
10. Explicit and generated `otherwise` diagnostics for `if` and `after`, including lazy evaluation.

## Amendment current by D-096

The distinction between elementary and compound actions is removed from the semantics. Every `then` is an ordered sequence that can combine effects, places, calls and `for each`. An internal call observes the exact delta and contributes to effect resolution. `action` retains the ability to operate at the root; `subaction` can be reused from any `then` but cannot operate at the root. Nested `after` blocks are evaluated against the final stable state of the completed resolution.

