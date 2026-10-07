---
id: D-125
title: Instruction-local lifecycle no-ops
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-046
affects:
  - "[[specification/04-mathematical-model]]"
  - "[[specification/08-concrete-grammar]]"
  - Effects and runtime lifecycle operational formalisation
---

# ADR-125 — Instruction-local lifecycle no-ops

## Context

The author chooses instruction-by-instruction lifecycle evaluation. A redundant activation or destruction does not suppress its enclosing rule, block or action. This amends D-023, D-054, D-099 and D-117 and resolves Q-046.

## Decision

`create d` when d is explicitly active and `destroy d` when d is explicitly inactive are successful no-ops. Availability is tested against the executing branch's current private view, including preceding effects and internal calls. Suspension of an explicitly active declaration does not make it inactive for this test.

No-op instructions change neither activation, materialisation generation, initialised payload nor reactive temporal memory. They do not independently yield Refusal or Errors and do not skip subsequent instructions. An otherwise successful action returns Success, even if its lifecycle instructions were all no-ops; other guards, errors, invariants and after checks retain their contracts.

Rules and actions with several creations or destructions do not require all targets to be jointly absent or present. Each instruction has the same policy, including instructions executed by internal calls. Effective creation/destruction remains tentative and subject to existing validation and atomic rollback. Concurrent creation of one absent identity remains idempotent; concurrent destroy precedence and generation-bound writes remain unchanged. Instruction-local no-ops do not impose an ordering between parallel branches.

## Contrasting cases

| Entry state and sequence | Required behaviour |
| --- | --- |
| Alice active, Bob inactive; create Alice; create Bob | Alice unchanged; Bob created; enclosing rule is not skipped |
| Alice inactive; destroy Alice; create Alice | First instruction no-op; second creates its initialised materialisation |
| Alice inactive; create Alice; create Alice | One materialisation; second instruction does not rerun initialisers |
| Alice active; destroy Alice; destroy Alice | First ends the materialisation; second does not destroy again |
| Alice active; destroy Alice; create Alice | Fresh generation and initial payload; identity unchanged |
| Alice active but suspended; create Alice | No-op; no reinitialisation or forced recovery of dependencies |

All resulting transitions still obey domain/cardinality and checkpoint validation. These are semantic conformance obligations, not claims of an implemented runtime test suite.

## Integration

MUD-LIFE-001 in [[specification/04-mathematical-model]] and the effect contract in [[specification/08-concrete-grammar]] express the accepted rule. Q-046 is archived with explicit closure evidence. No grammar, AST or nominal-HIR constructor is added.
