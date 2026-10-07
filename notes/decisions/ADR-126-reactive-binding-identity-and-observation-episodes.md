---
id: D-126
title: Reactive binding identity and observation episodes
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-005
affects:
  - "[[specification/04-mathematical-model]]"
  - "[[specification/08-concrete-grammar]]"
  - "[[specification/10-names-and-anchors]]"
  - "[[specification/15-fields-and-mutability]]"
  - "[[specification/21-expressions]]"
  - Reactive waves and runtime lifecycle operational formalisation
---

# ADR-126 — Reactive binding identity and observation episodes

## Context

The author selects identity by rule and role-associated participant identities, discards observation history when a binding disappears, restarts observation after suspension, and treats rematerialisation as a new observation episode. The author retains the existing semantics of changes. This completes Q-005 and amends D-041, D-045, D-058 and D-099.

## Decision

A persistent reactive binding is identified by its canonical rule identity and the assignment of participant identities to named roles. Role association matters: exchanging two participants between distinct roles gives a different binding. Changing a participant's fields or enumeration position does not change that identity. Existing causal matches additionally retain their witnesses and occurrence identities; equal payloads never merge distinct causal occurrences. This decision does not replace occurrence identity with a participant tuple.

Temporal memory belongs to an observation episode of that binding. It is valid only across consecutive wave snapshots where the binding is observable under the same rule activation and the same concrete participant materialisations. Absence or dependency suspension in a wave snapshot ends the episode. Reappearance starts a new baseline without firing merely because observation resumes. Suspension still preserves independently owned world storage; clearing observation memory does not destroy that storage.

Explicit destruction/recreation of the rule or a concrete participant starts a new episode. Generation changes are detected even if both lifecycle instructions occur between two observed snapshots. Generations distinguish observation continuity, not public thing identity or nominal anchors. Redundant create/destroy no-ops do not reset memory.

A false if suppresses consequences, not observation or binding membership. The temporal history continues to update for a binding that remains observable. Binding sets remain fixed at the start of a wave; changes enter the next wave rather than changing current-wave matches retroactively. Memory changes remain tentative and follow resolution rollback and imagine isolation.

Initial start-with bindings retain the existing special baseline: Rise may fire from virtual false, but changes does not fire and old reads the initial snapshot itself. Any later or resumed episode takes its first observable wave as baseline without a memory-based temporal pulse; comparison begins in the following wave. Direct message/firing occurrence sources retain their existing causal-match semantics; temporal baselines do not suppress or deduplicate those occurrences. An observed expression changing from empty to a value is a genuine change. An expression with no previous observation instead needs a baseline.

Trigger remains an internal temporal qualification, not a first-class storable MUD type. Changes remains restricted to when in reactive rules/messages; this decision adds no new temporal syntax or general-purpose changes operator.

## Contrasting cases

| Observations | Required behaviour |
| --- | --- |
| Same binding; health 10 then 7 in consecutive waves | changes pulses; old health is 10 |
| Binding absent, returns with health 4, then health 3 | Baseline at 4 without pulse; next wave pulses for 4 to 3 |
| Rule suspended while condition becomes true, then resumes | New baseline; no accumulated transition on resumption |
| Alice destroyed and recreated with health 10 between snapshots | New episode despite same public identity; no comparison to destroyed payload |
| Alice already active; create Alice | Existing observation episode continues |
| Trigger pulses but if is false | No consequences; current observations remain the next baseline |
| Existing binding observes members from empty to Alice | changes pulses on the collection; a newly formed Alice binding separately takes its baseline |
| Initial start-with binding with true Boolean condition | Rise may pulse; changes alone does not |

## Integration

MUD-TIME-001/MUD-TIME-002 in [[specification/04-mathematical-model]], temporal/effect contracts in [[specification/08-concrete-grammar]] and the temporal typing boundary in [[specification/21-expressions]] preserve these distinctions. No runtime memory nodes are added to nominal HIR. Operational trace formalisation remains future work, not an unanswered choice in Q-005.
