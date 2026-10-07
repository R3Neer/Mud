---
id: D-127
title: ActionReply-only action results
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-073
  - Q-022
affects:
  - "[[specification/07-concrete-grammar]]"
  - "[[specification/10-type-system]]"
  - "[[specification/19-expressions]]"
  - Action requests and callable contracts
---

# ADR-127 — ActionReply-only action results

## Context

The author chooses ActionReply as the sole return value of actions. This closes Q-022 without adding a second data result, output tuple or action-specific result type. It clarifies D-118/D-119 and amends the open-return scope of D-042.

- Amended by: [[ADR-140-readable-patches-and-host-only-confirmation-tickets|D-140]].

## Decision

Every action and subaction returns exactly one ActionReply: Success, Refusal or a nonempty Errors value. An action cannot declare an additional domain return type or export a separate domain result. Success carries no additional user-defined domain result. Obtaining the incorporated textual patch is required by D-140, but its access/interface remains Q-073; no Success field is selected. The same result contract applies to imagine.

Actions can still perform authorised state changes and cause messages under their existing contracts. Those effects and outputs are not a second return value. A look can query the relevant state afterwards where its visibility and effect context permit it; no new action return syntax is introduced.

Ordinary explicit reply capture remains possible in an effect-capable context. A bare action effect call continues to propagate non-success, and imagine always discards its tentative changes. This decision does not reopen rollback, recovery or message projection.

## Contrasting cases

- reply: ActionReply = actor.Move() is an ordinary permitted reply capture in an effect block.
- An action call used as a Person or numeric value is statically invalid; it cannot return the object it created as an additional value.
- A state update followed by a permitted look remains separate effect and query operations, not an action return tuple.
- No user-defined success payload or additional domain return is admitted; patch access remains Q-073 and Refusal/Error data retain their existing contracts.

## Integration

MUD-TYPE-014 in [[specification/19-expressions]] and the callable/grammar surfaces state this contract. No grammar, CST, Surface AST or nominal HIR constructor changes are required.
