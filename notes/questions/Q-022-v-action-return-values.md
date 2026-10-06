---
id: Q-022
title: Action return values
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-10-07
decisions:
  - D-118
  - D-127
affects: []
superseded-by: []
---

# Q-022 — Action return values

## Resolution

Actions and subactions return only ActionReply; additional domain results are not admitted. State changes and messages remain effects. The ordinary reply and imagine observation contracts remain unchanged.

## Closure criterion

- C1: The language fixes whether an action may return domain values besides ActionReply and integrates that choice into callable output, expression and grammar contracts.

## Closure evidence

- C1: MUD-TYPE-014 in [[specification/19-expressions]] prohibits extra return types/payloads. [[specification/10-type-system]] fixes action callable output, [[specification/07-concrete-grammar]] preserves ordinary reply capture without added syntax, and [[notes/decisions/ADR-127-actionreply-only-action-results|D-127]] contrasts reply capture with invalid domain-result use.
