---
id: D-055
title: Declarative tests and block error handling
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-059"
affects:
  - "[[notes/questions/README|Active questions]], future chapters 07 to 10, 28, 31, 33, 47, 50 and 53"
---

# ADR-055 — Declarative tests and block error handling

- Amended by: [[ADR-096-modules-callables-look-message-and-activation|D-096]], [[ADR-101-value-blocks-stored-local-variables-and-witness-extrema|D-101]] and [[ADR-118-action-replies-refusals-and-errors|D-118]].

## Decision

A test has a nominal name, its own start with contribution, one then and an after containing one or more Boolean assertions. Test declarations cannot occur inside other declaration bodies and do not form part of the host production API. Metadata remains at the beginning of the test body.

Every run builds a fresh isolated world from the union of the start with contributions of the static transitive closure of reachable tests, not ordinary part start with. It materializes and stabilizes that world before the test root. Called tests reuse this activation closure and never reapply initial activation. Cross-part test calls require uses authorization and a test context; executable call cycles are invalid.

Then shares the ordinary ordered private-effect protocol, local calculation and stored-local rules. After may begin with shared pure preamble statements, followed by Boolean assertions. Old in test after retains the test entry view; reactive old retains its distinct wave-snapshot contract. Each assertion is an ExpressionBlock and may carry Error-only otherwise handlers. Its false result remains an assertion failure, not a captured Error. Otherwise on bindings and optional if select computing errors, then or raise exclusively, without Text-only false-condition diagnostics.

```mud
test CounterIncreases {
    start with Counter
    then Counter.value += 1
    after {
        Counter.value == 1
        old Counter.value == 0
    }
}
```

The executor's passed, failed and error labels describe the test run, not ordinary values in the world. Successful assertions pass; a false assertion fails; unhandled computation errors produce the executor error category. ActionReply values remain ordinary Success | Refusal | Errors values and do not become those executor labels. The complete test observation and aggregation policy remains Q-059.

All test world state and external outputs are discarded. The executor may retain diagnostics and trace. Missing Error handlers generate no warning merely because an assertion can be false. Technical runtime defects/resource interruptions retain their separate implementation boundary under Q-007.

## Verification

Check test grammar and AST, fresh isolation, transitive own-start activation, uses authorization, cycle rejection, private sequencing, entry-view old, false assertion versus computing Error, Error-only handler attachment and unconditional world/output disposal. Q-059 does not leave the value representation of ActionReply open.
