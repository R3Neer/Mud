---
title: Effect conformance witnesses
status: proposed
normative: true
questions: []
decisions:
  - D-146
  - D-133
  - D-128
---

# Effect conformance witnesses

[[../28-effects]] specifies the effects and batch boundary. [[effect-cases.json]] maps the eight Surface AST effect constructors and nine assignment operators to chapter sections and contrasting cases. It includes bounded executable exact-arithmetic, lifecycle and dictionary witnesses, plus reviewed declarative traces for compound/adapter/invocation boundaries.

Run `python specification/effects/validate_effect_spec.py` and `python -m unittest discover -s specification/effects -p test_*.py`.

The checker executes only its finite certificate language. Numeric operands are supplied exact integers; it does not evaluate MUD RHS expressions or infer Money/Rum overloads. Lifecycle generation counters are illustrative distinct tokens, not required runtime encoding. Dictionary proposals supply a fixed valid priority order, not an implementation of seeded provenance construction. Expected declarative traces remain human-review obligations. This is not a parser, typechecker, full runtime, general proof of causality/termination or adapter implementation.

[[message-delivery-cases.json]] records reviewed message lifetime traces: frozen payload, disappeared/recreated participants, validated barriers, root/child/block rollback, joint ownership, recovery, isolation, equal-valued occurrences and race-free subscription. The effect checker validates trace coverage and ticket-state contracts; these traces are not scheduler/transport execution tests.

Alias-authored compound updates are reviewed replacement traces, not numeric-stage witnesses. No overload selection or algebraic proof engine is implemented.
